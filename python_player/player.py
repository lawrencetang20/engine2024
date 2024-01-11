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
        self.preflop_dict = {'AAo':1,'KKo':2,'QQo':3,'JJo':4,'TTo':5,'99o':6,'88o':7,'AKs':8,'77o':9,'AQs':10,'AJs':11,'AKo':12,'ATs':13,
                             'AQo':14,'AJo':15,'KQs':16,'KJs':17,'A9s':18,'ATo':19,'66o':20,'A8s':21,'KTs':22,'KQo':23,'A7s':24,'A9o':25,'KJo':26,
                             '55o':27,'QJs':28,'K9s':29,'A5s':30,'A6s':31,'A8o':32,'KTo':33,'QTs':34,'A4s':35,'A7o':36,'K8s':37,'A3s':38,'QJo':39,
                             'K9o':40,'A5o':41,'A6o':42,'Q9s':43,'K7s':44,'JTs':45,'A2s':46,'QTo':47,'44o':48,'A4o':49,'K6s':50,'K8o':51,'Q8s':52,
                             'A3o':53,'K5s':54,'J9s':55,'Q9o':56,'JTo':57,'K7o':58,'A2o':59,'K4s':60,'Q7s':61,'K6o':62,'K3s':63,'T9s':64,'J8s':65,
                             '33o':66,'Q6s':67,'Q8o':68,'K5o':69,'J9o':70,'K2s':71,'Q5s':72,'T8s':73,'K4o':74,'J7s':75,'Q4s':76,'Q7o':77,'T9o':78,
                             'J8o':79,'K3o':80,'Q6o':81,'Q3s':82,'98s':83,'T7s':84,'J6s':85,'K2o':86,'22o':87,'Q2s':88,'Q5o':89,'J5s':90,'T8o':91,
                             'J7o':92,'Q4o':93,'97s':94,'J4s':95,'T6s':96,'J3s':97,'Q3o':98,'98o':99,'87s':100,'T7o':101,'J6o':102,'96s':103,'J2s':104,
                             'Q2o':105,'T5s':106,'J5o':107,'T4s':108,'97o':109,'86s':110,'J4o':111,'T6o':112,'95s':113,'T3s':114,'76s':115,'J3o':116,'87o':117,
                             'T2s':118,'85s':119,'96o':120,'J2o':121,'T5o':122,'94s':123,'75s':124,'T4o':125,'93s':126,'86o':127,'65s':128,'84s':129,'95o':130,
                             '53s':131,'92s':132,'76o':133,'74s':134,'65o':135,'54s':136,'85o':137,'64s':138,'83s':139,'43s':140,'75o':141,'82s':142,'73s':143,
                             '93o':144,'T2o':145,'T3o':146,'63s':147,'84o':148,'92o':149,'94o':150,'74o':151,'72s':152,'54o':153,'64o':154,'52s':155,'62s':156,
                             '83o':157,'42s':158,'82o':159,'73o':160,'53o':161,'63o':162,'32s':163,'43o':164,'72o':165,'52o':166,'62o':167,'42o':168,'32o':169,
                             }
        
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
        # round_num = game_state.round_num  # the round number from 1 to NUM_ROUNDS
        # print(round_num)
        # my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind
        self.times_bet_preflop = 0

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
        
    def categorize_cards(self,cards):
        print(cards)
        rank1 = cards[0][0]
        rank2 = cards[1][0]
        suit1 = cards[0][1]
        suit2 = cards[1][1]
        hpair = ''
        onsuit = ''
        ranking = 'AKQJT98765432'
        if ranking.index(rank1)<ranking.index(rank2):
            hpair = rank1+rank2
        else:
            hpair = rank2+rank1
        
        if suit1 == suit2:
            onsuit = 's'
        else:
            onsuit = 'o'
        
        return (hpair+onsuit)

    def no_illegal_raises(self,bet,round_state):
        min_raise, max_raise = round_state.raise_bounds()  # the smallest and largest numbers of chips for a legal bet/raise        
        if bet >= max_raise:
            return max_raise
        else:
            return bet
        
    def get_preflop_action(self,cards,round_state,active):
        legal_actions = round_state.legal_actions()  # the actions you are allowed to take
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot
        pot = my_contribution+opp_contribution
        big_blind = bool(active)  # True if you are the big blind
        new_cards = self.categorize_cards(cards)
        #3BET
        if big_blind == False and self.times_bet_preflop == 0:
            if self.preflop_dict[new_cards] in range(1,20):
                self.times_bet_preflop +=1
                my_bet = 3*pot
                return RaiseAction(self.no_illegal_raises(my_bet,round_state))
            elif self.preflop_dict[new_cards] in range(20,144):
                self.times_bet_preflop +=1
                my_bet = 2*pot
                return RaiseAction(self.no_illegal_raises(my_bet,round_state))
            else:
                print (self.preflop_dict[new_cards])
                return FoldAction()
        #4BET 
        if big_blind == True and self.times_bet_preflop ==0:
            if self.preflop_dict[new_cards] in range(1,20) and RaiseAction in legal_actions:
                self.times_bet_preflop +=1
                my_bet = 2*pot
                return RaiseAction(self.no_illegal_raises(my_bet,round_state))
            elif self.preflop_dict[new_cards] in range(20,144):
                if CallAction in legal_actions:
                    return CallAction()
                else:
                    return CheckAction()
            else:
                return FoldAction()
            
        #5BET
        if big_blind == False and self.times_bet_preflop == 1:
            if self.preflop_dict[new_cards] in range(1,5) and RaiseAction in legal_actions:
                self.times_bet_preflop +=1
                my_bet = 2*pot
                return RaiseAction(self.no_illegal_raises(my_bet,round_state))
            elif self.preflop_dict[new_cards] in range(5,71):
                return CallAction()
            else:
                return FoldAction()
        #6BET
        if big_blind == True and self.times_bet_preflop == 1:
            if self.preflop_dict[new_cards] in range(1,3) and RaiseAction in legal_actions:
                self.times_bet_preflop +=1
                my_bet = 2*pot
                return RaiseAction(self.no_illegal_raises(my_bet,round_state))
            elif self.preflop_dict[new_cards] in range(3,11):
                return CallAction()
            else:
                return FoldAction()
        #7BET
        if big_blind == False and self.times_bet_preflop == 2:
            if self.preflop_dict[new_cards] in range(1,3):
                return CallAction()
            else:
                return FoldAction()
        #8BET
        if big_blind == True and self.times_bet_preflop == 2:
            if self.preflop_dict[new_cards] in range(1,3):
                return CallAction()
            else:
                return FoldAction()

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
            # print(my_cards)
            if self.categorize_cards(my_cards)[1] ==1:
                print(self.times_bet_preflop)
            return(self.get_preflop_action(my_cards,round_state,active))
        
        #AUCTION
        if BidAction in legal_actions:
            # print(my_stack)
            return(BidAction(round(my_stack*(2/5))))
        

        if CheckAction in legal_actions:
            return CheckAction()
        elif BidAction in legal_actions:
            return BidAction(int(random.random()*my_stack)) # random bid between 0 and our stack
        return CallAction()
    
if __name__ == '__main__':
    run_bot(Player(), parse_args())


#CODE WASTELAND
