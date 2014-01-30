import sys
import math

class State:
    def __init__(self, player_1_cards=(1,2), player_2_cards=(5,6)):
        self.player = 1
        self.pot = 1
        self.player_1_cards = player_1_cards 
        self.player_2_cards = player_2_cards
        self.player_1_commited = 0
        self.player_2_commited = 0
        self.stage = "betting_stage_1" 
        self.previous_action = []
        self.flop = 0 

    def __str__(self):
        return (" player :" + str(self.player) + 
        "\n pot = " + str(self.pot) + 
        "\n p1 commit = " + str(self.player_1_commited) + 
        "\n p2 commit = " + str(self.player_2_commited) + 
        "\n p1 cards = " + str(self.player_1_cards) + 
        "\n p2 cards = " + str(self.player_2_cards) + 
        "\n stage = " + str(self.stage) + 
        "\n previous_action = " + str(self.previous_action) + 
        "\n flop = " + str(self.flop) + 
        "\n #################################\n")

    def deepcopy(self):
        newstate = State()
        newstate.player = self.player
        newstate.pot = self.pot
        newstate.player_1_commited = self.player_1_commited
        newstate.player_2_commited = self.player_2_commited
        newstate.player_1_cards = self.player_1_cards
        newstate.player_2_cards = self.player_2_cards
        newstate.flop = self.flop
        newstate.stage = self.stage[:]
        newstate.previous_action = self.previous_action[:]
        return newstate


def get_actions(state):
    def betting_stage_outcomes(action_at_stage):
            if action_at_stage == []:
                # first turn, p1 can check or bet
                return ["check","bet"]
            elif action_at_stage == ["check"]:
                # if p1 checked
                return ["check"]
            elif action_at_stage == ["bet"]:
                return ["fold","bet"]
            # elif action_at_stage == ["check","bet"]:
            #     # p1 checked, p2 bet, p1 can bet(call) or fold
            #     return ["fold","bet"]
    if state.stage == "betting_stage_1":
        return betting_stage_outcomes(state.previous_action)
    elif state.stage == "betting_stage_2":
        return betting_stage_outcomes(state.previous_action[3:])


def result(state,action):

    newstate = state.deepcopy()
    newstate.previous_action.append(action)
    if action == "fold":
        newstate.stage = "finished"
        return newstate

    if action == "bet":
        newstate.pot += 1
        if state.stage == "betting_stage_1" and state.player == 1:
            newstate.player = 2
            newstate.player_1_commited = 1
        elif state.stage == "betting_stage_1" and state.player == 2:
            newstate.stage="flop"
            newstate.player_2_commited = 1
            newstate.player = 1
        elif state.stage == "betting_stage_2" and state.player == 1:
            newstate.player = 2
            newstate.player_1_commited = state.player_1_commited + 1
        elif state.stage =="betting_stage_2" and state.player ==2:
            newstate.stage = "finished"
            newstate.player_2_commited = state.player_2_commited + 1 
        return newstate

    if action == "check":
        if state.stage == "betting_stage_1" and state.player == 1:
            newstate.player = 2
        elif state.stage == "betting_stage_1" and state.player ==2:
            newstate.player = 1
            newstate.stage = "flop"
        elif state.stage == "betting_stage_2" and state.player ==1:
            newstate.player = 2
        elif state.stage =="betting_stage_2" and state.player ==2:
            newstate.stage = "finished"
        return newstate

    # if action in [1,2,3,4,5,6]:
    #     newstate.flop = action
    #     newstate.player = 1
    #     newstate.stage = "betting_stage_2"
    #     return newstate



def terminal_test(state):
    if state.stage == "finished":
        return True
    else:
        return False

def utility(state):
    if state.previous_action[-1:] == ["fold"]:
        if state.player == 1:
            return 0-state.pot
        else:
            #player 2 folded
            return state.pot - state.player_1_commited
    if state.stage == "finished":
        player_1_score = sum(state.player_1_cards)
        player_2_score = sum(state.player_2_cards)
        if state.flop in state.player_1_cards:
            player_1_score -= state.flop
        if state.flop in state.player_2_cards:
            player_2_score -= state.flop

        if player_1_score > player_2_score:
            return state.pot - state.player_1_commited
        elif player_1_score < player_2_score:
            return 0-state.pot + state.player_2_commited
        else:
            #draw
            return state.pot/2.0



def exp_min_max(state):
    max = -4
    for a in get_actions(state):
        state_copy = state.deepcopy()
        resulting_state = result(state_copy, a)
        v = min_value_search(resulting_state)
        if v >= max:
            max = v
            act = a
    return (act,v)




def max_value_search(state):
    if terminal_test(state):
        return utility(state)
    if(state.stage == "flop"):
        ev = expected_value(state) 
        return ev
    v = -4 
    for action in get_actions(state):
        state_copy = state.deepcopy()
        resulting_state = result(state_copy,action)
        v = max(v, min_value_search(resulting_state))
    return v

def expected_value(state):
        total = 0
        for card in [1,2,3,4,5,6]:
            copy = state.deepcopy()
            copy.player = 1
            copy.stage = "betting_stage_2"
            copy.flop = card
            copy.previous_action.append(card)
            values = list()
            for a in get_actions(copy):
                values.append(min_value_search(result(copy,a)))
            max_v = max(values)
            total += (1.0/6.0) * max_v
        return total


def min_value_search(state):
    if terminal_test(state):
        # print(str(state.previous_action) + str(utility(state)))
        return utility(state)
    v = 4 
    for action in get_actions(state):
        state_copy = state.deepcopy()
        resulting_state = result(state_copy, action)
        v = min(v, max_value_search(resulting_state))
    return v

def main():
    if len(sys.argv) != 5:
        for i in range(1,7):
            for j in range(1,7):
                for a in range(1,7):
                    for b in range(1,7):
                        if len(set([i,j,a,b])) == 4:
                            print(str((i,j)) +" vs " + str((a,b)) + " = ")
                            state = State(player_1_cards=(i,j), player_2_cards=(a,b))
                            print(exp_min_max(state))
    else:
        i = int(sys.argv[1])
        j = int(sys.argv[2])
        a = int(sys.argv[3])
        b = int(sys.argv[4])
        print(str((i,j)) +" vs " + str((a,b)) + " = ")
        state = State(player_1_cards=(i,j), player_2_cards=(a,b))
        print(exp_min_max(state))



if __name__ == '__main__':
    main()