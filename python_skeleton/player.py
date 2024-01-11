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
        my_bankroll = game_state.bankroll  # the total number of chips you've gained or lost from the beginning of the game to the start of this round
        game_clock = game_state.game_clock  # the total number of seconds your bot has left to play this game
        round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        my_cards = round_state.hands[active]  # your cards
        big_blind = bool(active)  # True if you are the big blind
        if round_num == 1:
            print(game_clock)
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
        if game_state.round_num == NUM_ROUNDS:
            print(game_state.game_clock)
        pass

    def get_preflop_range(self,size,round_state,active):
        my_cards = round_state.hands[active]  # your cards
        big_blind = bool(active)  # True if you are the big blind
        rank1 = my_cards[0][0]
        rank2 = my_cards[1][0]
        suit1 = my_cards[0][1]
        suit2 = my_cards[1][1]
        # Writing out preflop ranges
        
        if size == 'small' and big_blind == False:
            if rank1 in '9876543' and rank2 == '2' and suit1 != suit2:
                return 0
            elif rank2 in '9876543' and rank1 == '2' and suit1 != suit2:
                return 0
            elif rank2 in '87' and rank1 == '3' and suit1 != suit2:
                return 0
            elif rank1 in '87' and rank2 == '3' and suit1 != suit2:
                return 0
            elif rank1 == '4' and rank2 == '3' and suit1 != suit2:
                return 0
            elif rank2 == '4' and rank1 == '3'and suit1 != suit2:
                return 0
            else:
                return 5
        
        if size == 'medium' and big_blind == False:
            if rank1 in 'T987654' and rank2 in '32' and suit1 != suit2:
                return 0
            elif rank2 in 'T987654' and rank1 in '32' and suit1 != suit2:
                return 0
            elif rank2 in '9876' and rank1 == '4' and suit1 != suit2:
                return 0
            elif rank1 in '9876' and rank2 == '4' and suit1 != suit2:
                return 0
            elif rank2 in '32' and rank1 in '32' and rank1 != rank2:
                return 0
            else:
                return 7
        
        if size == 'large' and big_blind == False:
            if rank1 in '9876543' and rank2 =='2':
                return 0
            elif rank2 in '9876543' and rank1 =='2':
                return 0
            elif rank2 in '87' and rank1 == '3':
                return 0
            elif rank1 in '87' and rank2 == '3':
                return 0
            elif rank1 in 'QJT' and rank2 == '2' and suit1 != suit2:
                return 0
            elif rank2 in 'QJT' and rank1 == '2' and suit1 != suit2:
                return 0
            elif rank2 in 'JT98765' and rank1 in '34' and suit1 != suit2:
                return 0
            elif rank1 in 'JT98765' and rank2 in '34' and suit1 != suit2:
                return 0
            elif rank2 in 'T9876' and rank1 == '5' and suit1 != suit2:
                return 0
            elif rank1 in 'T9876' and rank2 == '5' and suit1 != suit2:
                return 0
            elif rank1 == '4' and rank2 =='3' and suit1 != suit2:
                return 0
            elif rank2 == '4' and rank1 =='3' and suit1 != suit2:
                return 0
            else:
                return 9
        
        if size in 'small,medium,large' and big_blind == True:
            return 1
        
    def decide_action_preflop(self, game_state, round_state, active):
        big_blind = bool(active)  # True if you are the big blind
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot
        if not(big_blind):
            if RaiseAction in legal_actions and opp_contribution == 2:
                if self.get_preflop_range('medium',round_state,active) ==0:
                    return FoldAction()
                else:
                    return RaiseAction(self.get_preflop_range('medium',round_state,active))
            else:
                if CallAction in round_state.legal_actions():
                    return CallAction()
                return CheckAction()
        else: 
            if CheckAction in round_state.legal_actions():
                return CheckAction()
            return CallAction()


    def decide_action_postflop(self, opp_pip, my_pip, hand_strength, pot, legal_actions, street):
        rand = random.random()
        if CheckAction in legal_actions: #Check, raise
            if rand < hand_strength and hand_strength > .7:
                return RaiseAction, 1 #value bet
            elif street == 5 and hand_strength > .85:
                return RaiseAction, 1  #no checks on river with super strong hands
            elif rand < hand_strength / 7 and hand_strength <= .4:
                return RaiseAction, 0 #bluff
            return CheckAction, None
        else: #Fold, Call, Raise
            pot_equity = (opp_pip-my_pip) / (pot - (opp_pip - my_pip))
            if pot_equity > .70 and pot_equity < 1:
                pot_equity = .7
            elif pot_equity >= 1 and pot_equity < 2:
                pot_equity = .8
            elif pot_equity >= 2:
                pot_equity = .875
            if hand_strength < pot_equity: #bad pot equity
                return FoldAction, None
            elif hand_strength < .25:
                return FoldAction, None
            else: #good pot equity
                if hand_strength > .85 or (hand_strength - pot_equity > .25 and hand_strength > .7):
                    return RaiseAction, 1 #value raise
                return CallAction, None

    def decide_action_auction(self, hand_strength, active, my_stack):
        return BidAction(random.randint(1,2))

    def hand_strength(self, round_state, street, active):
        board = [eval7.Card(x) for x in round_state.deck[:street]]
        my_hole = [eval7.Card(a) for a in round_state.hands[active]]
        comb = board + my_hole
        num_more_board = 5 - len(board)

        if len(my_hole) == 2 and street > 0 and BidAction not in round_state.legal_actions():
            opp_num = 3
        elif len(my_hole) == 3 and street > 0 and (round_state.bids[active] == round_state.bids[1-active]):
            opp_num = 3
        else:
            opp_num = 2

        deck = eval7.Deck()
        for card in comb:
            deck.cards.remove(card)

        num_better = 0

        for _ in range(250):
            deck.shuffle()
            cards = deck.peek(opp_num + num_more_board)
            opp_hole = cards[:opp_num]
            board_rest = cards[opp_num:]
            my_val = eval7.evaluate(my_hole+board+board_rest)
            opp_value = eval7.evaluate(opp_hole+board+board_rest)
            if my_val >= opp_value:
                num_better += 1

        percent_better_than = num_better/250
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
        legal_actions = round_state.legal_actions() # the actions you are allowed to take
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

        pot = my_contribution + opp_contribution
        min_raise, max_raise = round_state.raise_bounds()
        hand_strength = self.hand_strength(round_state, street, active)

        if BidAction in legal_actions:
            return self.decide_action_auction(hand_strength, my_contribution, max_raise)
        elif street == 0:       
            return self.decide_action_preflop(game_state, round_state, active)
        else:
            decision, conf = self.decide_action_postflop(opp_pip, my_pip, hand_strength, pot, legal_actions, street)

        if decision == RaiseAction and RaiseAction in legal_actions:
            minimum = max(min_raise, pot / 4)
            if conf != 0:
                bet_max = int((1+(2*(hand_strength**2)*random.random())) * pot/2 )
                maximum = min(max_raise, bet_max)
            else:
                maximum = min(max_raise, pot)
            if maximum <= minimum:
                amount = int(min_raise)
            else:
                amount = int(random.random() * (maximum - minimum) + minimum)
            return RaiseAction(amount)
        if decision == RaiseAction and RaiseAction not in legal_actions:
            if CallAction in legal_actions:
                return CallAction()
            return CheckAction()
        return decision()


if __name__ == '__main__':
    run_bot(Player(), parse_args())

