# Implementing a  depth limited search
# Info: Russel Norvig page 89
# inf2b Lecture 6
# Luke McAuley
# 28/1/14

from problem import *
CUTOFF = "CUTOFF"
FAILURE = "FAILURE"
# complete when d < l 
# time = O(b^l)
# space = O(bl)
# can terminate with sucess, cutoff or failure

def depth_limited_search(problem, limit):
    return recursive_dls(Node(problem.initial_state, []), problem, limit)

def recursive_dls(node, problem, limit):
    if(problem.goal_test(node.state)):
        return node.action_sequence
    elif limit == 0:
        return CUTOFF 
    else:
        cutoff_reached = False
        for action, result in problem.successor_function(node.state):
            action_sequence = node.action_sequence[:]
            action_sequence.append(action)
            child = Node(result, action_sequence)
            search_result = recursive_dls(child, problem, limit-1)
            if search_result == CUTOFF:
                cutoff_reached = True
            elif not search_result == FAILURE :
                return search_result 
        if cutoff_reached:
            return CUTOFF
        else:
            return FAILURE 

def main():
    states  = range(1,18)
    initial_state = 1
    graph = {
        1 : [2,3],
        2 : [4,5],
        3 : [6,7],
        4 : [8,9],
        5 : [10,11],
        6 : [12,13],
        7 : [14,15],
        8 : [11,16],
        9 : [2],
        10 : [1],
        11 : [],
        12 : [3],
        13 : [],
        14 : [],
        15 : [17],
        16 : [],
        17 : [],
    }
    def goal_test(state):
        return state==17

    def successor_funct(state):
        results = list()
        for new_state in graph[state]:
            results.append(("go to " + str(new_state), new_state))
        return results

    result1 = depth_limited_search(Problem(states, initial_state, successor_funct, goal_test), 2)
    result2 = depth_limited_search(Problem(states, initial_state, successor_funct, goal_test), 4)
    result3 = depth_limited_search(Problem(states, initial_state, successor_funct, goal_test), 11)

    print("Cutoff = 2, solution = "+ str(result1))
    print("Cutoff = 4, solution = "+ str(result2))
    print("Cutoff = 11, solution = "+ str(result3))


if __name__ == '__main__':
    main()
