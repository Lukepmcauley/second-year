# Implementing a depth-first graph search
# Inf2D Lecture 6
# pseudocode p76 Russel Norvig 

class Problem:

    #sucessor function state -> (action, result)
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

class Frontier:

    def __init__(self):
        self.states = set()
        self.nodes = list()

# Depth-First Graph Search 
# Complete on finite state spaces
# Time and Space complexity bounded by state space
def graph_search(problem):

    frontier = Frontier()
    explored = set()

    #initialize the frontier
    for (action, result) in problem.successor_function(problem.initial_state):
        frontier.nodes.append(Node(result, [action]))
        frontier.states.add(result)


    while(frontier.nodes):
        node = frontier.nodes.pop()
        explored.add(node.state)

        #if goal is reached
        if problem.goal_test(node.state):
            return node.action_sequence

        # if goal is not reached
        for (action, result) in problem.successor_function(node.state):
            if (not result in frontier.states) and (result not in explored):
                sequence = node.action_sequence[:]
                sequence.append(action)
                frontier.nodes.append(Node(result,sequence))
                frontier.states.add(result)

    #No Solution found
    return None

def main():
    states = [1,2,3,4,5,6,7]
    initial_state = 1
    graph = {
        1 : [2,3],
        2 : [5],
        3 : [1],
        4 : [],
        5 : [6, 7],
        6 : [5],
        7 : [],
    }
    def goal_test(state):
        return state==7

    def successor_funct(state):
        results = list()
        for new_state in graph[state]:
            results.append(("go to" + str(new_state), new_state))
        return results

    result = graph_search(Problem(states, initial_state, successor_funct, goal_test))

    print("solution = "+ str(result))



if __name__ == '__main__':
    main()
