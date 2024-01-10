'''
Simple example pokerbot, written in Python.
'''
from skeleton.actions import FoldAction, CallAction, CheckAction, RaiseAction, BidAction
from skeleton.states import GameState, TerminalState, RoundState
from skeleton.states import NUM_ROUNDS, STARTING_STACK, BIG_BLIND, SMALL_BLIND
from skeleton.bot import Bot
from skeleton.runner import parse_args, run_bot
import random
import eval7
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
        counter = 1
        self.possible_opp_hands = {}
        card1_list = []
        card2_list = []
        for suit in 'hdsc':
            for rank in 'AKQJT98765432':
                card1_list.append(rank+suit)
                card2_list.append(rank+suit)
        for card1 in card1_list:
            for card2 in card2_list:
                if card1 != card2:
                    self.possible_opp_hands[card1,card2] = counter
                    counter+=1
        print(self.possible_opp_hands)
            

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
        # my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind

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
        
    def get_preflop_action(self, game_state, round_state, active):
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
                return CallAction()
        else: 
            return CheckAction()

    def refine_opp_hands(self, cards, board):
        #remove impossible hands for your opponent to have
        total_cards = cards+board


    def get_hand_analysis(self,cards,board):
        total_cards = cards+board
        for hand in self.possible_opp_hands.values():
            print(4)




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
        min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise        
        
        #PREFLOP
        if street == 0:
            return(self.get_preflop_action(game_state,round_state,active))
        
        #AUCTION
        if BidAction in legal_actions:
            print(my_stack)
            return(BidAction(round(my_stack*(2/5))))
        

        if CheckAction in legal_actions:
            return CheckAction()
        elif BidAction in legal_actions:
            return BidAction(int(random.random()*my_stack)) # random bid between 0 and our stack
        return CallAction()
    
if __name__ == '__main__':
    run_bot(Player(), parse_args())
