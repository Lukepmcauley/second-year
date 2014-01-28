# Implementing a iterative deepening search
# pseudocode Russel Norvig page 92
# Inf2b Lecture 6
# Luke McAuley
# 28/1/14
from depth_limited_search import *


# In theory could be infinite
ABSOLUTE_LIMIT = 100

# Complete =  when d is finite
# Optimal = Yes when each step has the same cost
# Memory = O(bd)
# Time = O(b^d)
# NB Even thought the top of the tree
#    is generated mulitple times this has little effect 
#    on the time and has the same big-O as BFS 
# Used for problems with large search space, with solutions
# at an unknown depth

def iterative_deepening_search(problem):
    for depth in range(0, ABSOLUTE_LIMIT):
        result = depth_limited_search(problem, depth)
        if not result == CUTOFF:
            return result


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

    result = iterative_deepening_search(Problem(states, initial_state, successor_funct, goal_test))

    print("Solution = "+ str(result))


if __name__ == '__main__':
    main()


