<<<<<<< HEAD
'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, BidAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import random

# merged, test changes, added another test

class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        pass

    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        #my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        #game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        #round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        #my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind
        print("new round")
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        #my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        #previous_state = terminal_state.previous_state  # RoundState before payoffs
        #street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        pass

    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        # May be useful, but you may choose to not use.
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        my_bid = round_state.bids[active]  # How much you bid previously (available only after auction)
        opp_bid = round_state.bids[1-active]  # How much opponent bid previously (available only after auction)
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot


        if RaiseAction in legal_actions:
           min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
           min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
           max_cost = max_raise - my_pip  # the cost of a maximum bet/raise
        
        if RaiseAction in legal_actions and random.random() < 0.3:
            return RaiseAction(random.randint(min_raise, max_raise))
        if CheckAction in legal_actions:
            return CheckAction()
        elif BidAction in legal_actions:
            return BidAction(my_stack) # random bid between 0 and our stack
        return CallAction()


if __name__ == '__main__':
    run_bot(Player(), parse_args())
=======
'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, BidAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import random
import eval7, pprint

class Player(Bot):
    '''
    A pokerbot.
    '''

    def __init__(self):
        '''
        Called when a new game starts. Called exactly once.

        Arguments:
        Nothing.

        Returns:
        Nothing.
        '''
        faces = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suit11 = ['h', 's', 'd', 'c']
        all_cards = []
        for face in faces:
            for suit in suit11:
                all_cards.append(face+suit)

        self.all_2hands = []
        self.all_3hands = []
        for ix, card1 in enumerate(all_cards):
            for ix2, card2 in enumerate(all_cards[ix+1:]):
                self.all_2hands.append([eval7.Card(card1), eval7.Card(card2)])
                for card3 in all_cards[ix2+1:]:
                    self.all_3hands.append([eval7.Card(card1), eval7.Card(card2), eval7.Card(card3)])


    def handle_new_round(self, game_state, round_state, active):
        '''
        Called when a new round starts. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your cards
        big_blind = bool(active)  # True if you are the big blind
        pass

    def handle_round_over(self, game_state, terminal_state, active):
        '''
        Called when a round ends. Called NUM_ROUNDS times.

        Arguments:
        game_state: the GameState object.
        terminal_state: the TerminalState object.
        active: your player's index.

        Returns:
        Nothing.
        '''
        my_delta = terminal_state.deltas[active]  # your bankroll change from this round
        previous_state = terminal_state.previous_state  # RoundState before payoffs
        street = previous_state.street  # 0, 3, 4, or 5 representing when this round ended
        my_cards = previous_state.hands[active]  # your cards
        opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed
        pass

    def decide_action_postflop(self, opp_pip, my_pip, hand_strength, my_contribution, opp_contribution):
        rand = random.random()
        if opp_pip == 0: #Check, raise
            if rand < hand_strength and hand_strength > .6:
                return RaiseAction, (1+random.random()) #value bet, random conf number, planned for bet sizing
            if rand < hand_strength / 3 and hand_strength <= .6:
                return RaiseAction, 0 #bluff
            return CheckAction, None
        elif opp_pip > 0: #Fold, Call, Raise
            pot_equity = (opp_pip-my_pip) / (my_contribution + opp_contribution)
            if pot_equity > .9 and pot_equity < 1.5:
                pot_equity = .9
            elif pot_equity >= 1.5 and pot_equity < 2.5:
                pot_equity = .95
            elif pot_equity >= 2.5:
                pot_equity = .975
            if hand_strength < pot_equity: #bad pot equity
                if rand > hand_strength / 10:
                    return FoldAction, None
                return RaiseAction, 0 #bluff
            else: #good pot equity
                if hand_strength > .9 or hand_strength - pot_equity > .25:
                    return RaiseAction, (1+(2*random.random())) #random confidence number, planned for bet sizing
                return CallAction, None


    def decide_action_preflop(self, legal_actions, opp_pip, my_pip, hand_strength, my_contribution, opp_contribution):
        #will become solver based right now just randomized so code will run
        rand = random.random()
        if CheckAction in legal_actions: #Check, raise
            if rand < hand_strength and hand_strength > .7:
                return RaiseAction, (1+random.random()) #value bet
            if rand < hand_strength / 3 and hand_strength <= .7:
                return RaiseAction, 1 #bluff
            return CheckAction, None
        else: #Fold, Call, Raise
            pot_equity = (opp_pip-my_pip) / (my_contribution + opp_contribution)
            if pot_equity > .9 and pot_equity < 1.25:
                pot_equity = .9
            elif pot_equity >= 1.25 and pot_equity < 2.5:
                pot_equity = .95
            elif pot_equity >= 2.5:
                pot_equity = .975
            pot_equity -= .075
            if hand_strength < pot_equity: #bad pot equity
                if rand > hand_strength / 10:
                    return FoldAction, None
                return RaiseAction, 0 #bluff
            else: #good pot equity
                if hand_strength > .9 or hand_strength - pot_equity > .25:
                    return RaiseAction, (1+(2*random.random()))
                return CallAction, None


    def decide_action_auction(self, hand_strength, my_contribution, opp_contribution):
        if hand_strength > .5:
            return BidAction(int(1.5*(my_contribution+opp_contribution)))
        return BidAction(1)

    def hand_strength(self, round_state, street, active):
        board = [eval7.Card(x) for x in round_state.deck[:street]]
        my_hole = [eval7.Card(a) for a in round_state.hands[active]]
        comb = board + my_hole
        my_val = eval7.evaluate(board+my_hole)
        num_better = 0
        if len(my_hole) == 2 and street > 0:
            possible = self.all_3hands
        else:
            possible = self.all_2hands
        trials = 0
        while trials < 500:
            opp_hole = random.choice(possible)
            if opp_hole[0] in comb or opp_hole[1] in comb:
                continue
            opp_value = eval7.evaluate(opp_hole+board)
            if opp_value > my_val:
                num_better += 1
            trials += 1
        percent_better_than = 1 - (num_better/trials)
        return percent_better_than


    def get_action(self, game_state, round_state, active):
        '''
        Where the magic happens - your code should implement this function.
        Called any time the engine needs an action from your bot.

        Arguments:
        game_state: the GameState object.
        round_state: the RoundState object.
        active: your player's index.

        Returns:
        Your action.
        '''
        # May be useful, but you may choose to not use.
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        street = round_state.street  # 0, 3, 4, or 5 representing pre-flop, flop, turn, or river respectively
        my_cards = round_state.hands[active]  # your cards
        board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        my_bid = round_state.bids[active]  # How much you bid previously (available only after auction)
        opp_bid = round_state.bids[1-active]  # How much opponent bid previously (available only after auction)
        continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot
        if RaiseAction in legal_actions:
           min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise
           min_cost = min_raise - my_pip  # the cost of a minimum bet/raise
           max_cost = max_raise - my_pip  # the cost of a maximum bet/raise
           print(min_raise, max_raise, my_stack, opp_stack, my_pip, opp_pip)

        min_raise, max_raise = round_state.raise_bounds()
        hand_strength = self.hand_strength(round_state, street, active)
        
        print(hand_strength)

        if BidAction in legal_actions:
            return self.decide_action_auction(hand_strength, my_contribution, opp_contribution)
        elif street == 0:       
            decision, conf = self.decide_action_preflop(legal_actions, opp_pip, my_pip, hand_strength, my_contribution, opp_contribution)
            if decision == RaiseAction:
                amount = random.randint(min_raise, min_raise + 4)
                return RaiseAction(amount)
        else:
            decision, conf = self.decide_action_postflop(opp_pip, my_pip, hand_strength, my_contribution, opp_contribution)

        if decision == RaiseAction and street != 0:
            amount = random.randint(min_raise, max_raise)
            return RaiseAction(amount)
        return decision()


if __name__ == '__main__':
    run_bot(Player(), parse_args())

>>>>>>> 9d80c3adb480bb76ade34479a9493611c446a5bd
