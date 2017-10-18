import sys, getopt

# Function to open the file that contains the description of 
# the Automata
def openfile(argv):
	fileToUse = 'Automata.txt'
	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile="])
		# print("opts; ", opts)
	except getopt.GetoptError:
		# print ("Error: unknow input file")
		return fileToUse
		# sys.exit()
	for opt, arg in opts:
		if opt == '-h':
			print ("-h:\n\tShow this help message\n\n-i <inputfile>:\n\tUse the <inputfile> to execute the algorithm. <inputfile> must conteins the description of one NDFA.")
			sys.exit()
		elif opt in ("-i", "--ifile"):
			fileToUse = arg
	return fileToUse

descriptionFile=openfile(sys.argv[1:])
file = open('%s' % descriptionFile, 'r')
word = file.readline().strip()
states = set(state for state in file.readline().split())
alphabet = set(letter for letter in file.readline().split())
initial_state = file.readline().split()[0]
final_states = set(state for state in file.readline().split())
transitions = dict()
for transition in [line.split() for line in file]:
    if (transition[0], transition[1]) in transitions:
        transitions[(transition[0], transition[1])].update(transition[2])
    else:
        transitions[(transition[0], transition[1])] = set(transition[2])

# given a set of states it returns a set of reachable states by epsolon
def epsolon_closure(closure):
    previous_size = 0
    while len(closure) != previous_size:
        previous_size = len(closure)
        for episolon_state in [st for st in closure if (st, '&') in transitions]:
            closure.update(transitions[(episolon_state, '&')])
    return closure

# given a set of states it returns a set of reachable states by a letter
def letter_closure(closure, letter):
    closure_letter = set()
    for i in[transitions[(state, letter)] for state in closure if (state, letter) in transitions]:
        closure_letter.update(i)
    return closure_letter

# given a state and a letter it returns a set of reachable states by &*.letter.&* transitions
def closure(state, letter):
    epsolon = epsolon_closure(set(state))
    closure_letter = letter_closure(epsolon, letter)
    epsolon = epsolon_closure(closure_letter)
    return epsolon

#return a new transition function without & transitions
def remove_epsolon_transitions(transitions):
    new_transitions = dict()
    for state in states:
        for letter in alphabet:
            if len(closure(state, letter)) != 0:
                new_transitions[(state, letter)] = closure(state, letter)
    return new_transitions

# Convert the NFA(without & transitions) to a DFA
# Return new transition function, new set of final states, and new set of states
def determinize():
    new_transitions = dict()
    pending_states = [(initial_state, set(initial_state))]
    visited_states = []
    states_final = set()
    while len(pending_states) != 0:
        actual_state = pending_states.pop()
        visited_states.append(actual_state[0])
        for state in actual_state[1]:
            if state in final_states:
                states_final.add(actual_state[0])
        for letter in alphabet:
            closure_letter = letter_closure(actual_state[1], letter)
            if len(closure_letter) != 0:
                new_transitions[(actual_state[0], letter)] = ''.join(sorted(closure_letter))
                if ''.join(sorted(closure_letter)) not in visited_states:
                    pending_states.append((''.join(sorted(closure_letter)), closure_letter))
    return new_transitions, states_final, {state[0] for state in new_transitions}

def compute(word):
    if len(word) == 0:#check if the language is void
        if initial_state in final_states:
            return 1
        return 0
    actual_state = initial_state
    for c in word:
        if (actual_state, c) not in transitions:
            return 0
        actual_state = transitions[(actual_state, c)]
    if actual_state not in final_states:
        return 0
    return 1

#check for & transitions
epsolon_transitions = 0
for transition in transitions:
    if transition[1] == '&':
        epsolon_transitions = 1
if epsolon_transitions == 1:
    transitions = remove_epsolon_transitions(transitions)

transitions, final_states, states = determinize()

print("States: ", states)
print("Alphabet: ", alphabet)
print("Initial State: ", initial_state)
print("Final States: ", final_states)
print("Transitions:", transitions)
print("Input: ",word)
if compute(word) == 1:
    print("word accepted.")
else:
    print("word rejected.")
