class Problem:

    #sucessor function state -> [(action, result)]
    def __init__(self, states, initial_state, successor_function, goal_test_function):
       self.states = states
       self.initial_state = initial_state
       self.successor_function = successor_function
       self.goal_test = goal_test_function

class Node:

    def __init__(self, state, action_sequence):
        self.state = state
        self.action_sequence = action_sequence

    def __str__(self):
        return self.state