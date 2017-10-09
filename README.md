# Automata
Conversion of NDFA to DFA in python.

# How to run
It is very simple just open the python3 and provide the .py

The application will search for a Atomata.txt which describes the input and automata's properties.

At the end of execution the automata's properties are printed, as well wheter the input is accepted/rejected.

# Automata.txt
The file must be in this formate:

Line1: The input string to be recognized

Line2: The states separed by space.

Line3: The alphabet of the language separed by space.

Line4: The initial state.

Line5: The set of final states separed by space.

Line6+: The remaining lines of file represents each transition separed by space: "actual_state" letter "next_state"

Obs:
There is an example of an automata description and input in Automata.txt.

The epsolon transition is represented by special reserved caracter: &

All non-defined transitions are considered as transitions which leads the computation to error state, therefore they do not need to be described in file.
