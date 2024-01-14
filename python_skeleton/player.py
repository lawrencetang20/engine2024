'''
Simple example pokerbot, written in Python.

UP BY CLOSE TO 1.5* rounds left, play nittier?


add fozz ranges

board paired -- makes nit more 

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
        
        self.trials = 125
        self.rounds_won = 0
        self.total_rounds = 0
        self.already_won = False
        self.nit = 0

        self.switched_to_100 = False
        self.switched_to_50 = False

        self.num_auctions_seen=0
        self.my_total_bid=0
        self.opp_total_bid=0
        self.auction_factor=1


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
        #my_cards = round_state.hands[active]  # your cards
        #big_blind = bool(active)  # True if you are the big blind

        self.times_bet_preflop = 0

        if my_bankroll > 1.5*(NUM_ROUNDS-self.total_rounds)+2:
            self.already_won = True

        if game_clock < 20 and round_num <= 333 and not self.switched_to_100:
            self.trials = 100
            self.switched_to_100 = True
            self.nit = .03
            print('switch to 100')

        
        elif game_clock < 10 and round_num <= 666 and not self.switched_to_50:
            self.trials = 50
            self.switched_to_50 = True
            self.nit = .06
            print('switch to 50')
        
        print(self.auction_factor)

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
        #my_cards = previous_state.hands[active]  # your cards
        #opp_cards = previous_state.hands[1-active]  # opponent's cards or [] if not revealed

        self.total_rounds += 1

        if game_state.round_num == NUM_ROUNDS:
            print(game_state.game_clock)

        if my_delta > 0:
            self.rounds_won += 1
        
        if street>=3:
            self.num_auctions_seen+=1
            my_bid=terminal_state.bids[active]
            opp_bid=terminal_state.bids[1-active]
            self.my_total_bid+=my_bid
            self.opp_total_bid+=opp_bid
            if self.num_auctions_seen>=50 and self.opp_total_bid>self.my_total_bid: #they're bidding more than us on avg
                self.auction_factor=.8*self.opp_total_bid/self.my_total_bid #bid just under what they would be bidding so they pay more
            elif self.num_auctions_seen>=50 and self.opp_total_bid<=self.my_total_bid: #we are bidding more than them on avg
                self.auction_factor=1.2*self.opp_total_bid/self.my_total_bid #bid just over what they would be bidding to win cheaper auction


    def categorize_cards(self,cards):
        rank1 = cards[0][0]
        rank2 = cards[1][0]
        suit1 = cards[0][1]
        suit2 = cards[1][1]
        hpair = ''
        onsuit = ''
        ranking = {'A': 0, 'K': 1, 'Q': 2, 'J': 3, 'T': 4, '9': 5, '8': 6, '7': 7, '6': 8, '5': 9, '4': 10, '3': 11, '2': 12}

        if ranking[rank1]<ranking[rank2]:
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
        opp_pip = round_state.pips[1-active]
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
                return FoldAction()
        #4BET -- you are big blind, and small blind raises or calls
        elif big_blind == True and self.times_bet_preflop ==0:
            if self.preflop_dict[new_cards] in range(1,8):
                self.times_bet_preflop +=1
                my_bet = 2*pot
                if RaiseAction in legal_actions:
                    return RaiseAction(self.no_illegal_raises(my_bet,round_state))
                elif CallAction in legal_actions:
                    return CallAction()
                else:
                    print("this shouldn't ever happen")
                    # 144 is the worst hand we could call a limp with 
                    # 8 we call 200, 144 we call 2
                    # 144-8 = 136, 144 - sqrt((pip-2)/198) * 136
            elif self.preflop_dict[new_cards] in range(8,int(144-((opp_pip-2)/198)**(1/3)*136)) and opp_pip <= 200:
                if CallAction in legal_actions:
                    return CallAction()
                else:
                    return CheckAction()
            else:
                if CheckAction in legal_actions:
                    return CheckAction()
                return FoldAction()
        # 100 is the end range
        else:
            if self.preflop_dict[new_cards] in range(1,6):
                self.times_bet_preflop +=1
                my_bet = 2*pot
                if RaiseAction in legal_actions:
                    return RaiseAction(self.no_illegal_raises(my_bet,round_state))
                elif CallAction in legal_actions:
                    return CallAction()
                else:
                    print("this shouldn't ever happen")
            elif self.preflop_dict[new_cards] in range(6, int(101-((opp_pip-2)/398)**(1/3)*95)):
                if CallAction in legal_actions:
                    return CallAction()
                else:
                    return CheckAction()
            else:
                if CheckAction in legal_actions:
                    return CheckAction()
                return FoldAction()

    def decide_action_postflop(self, opp_pip, my_pip, hand_strength, pot, legal_actions, street):
        rand = random.random()
        if CheckAction in legal_actions: #Check, raise
            if rand < hand_strength and hand_strength > .8:
                return RaiseAction, 1 #value bet
            elif street == 5 and hand_strength > .875:
                return RaiseAction, 1  #no checks on river with super strong hands
            elif rand < hand_strength / 7 and hand_strength <= .4:
                return RaiseAction, 0 #bluff
            return CheckAction, None
        else: #Fold, Call, Raise
            pot_equity = (opp_pip-my_pip) / (pot - (opp_pip - my_pip))
            if pot_equity > .725 and pot_equity < .875:
                pot_equity = .725
            elif pot_equity >= .875 and pot_equity < 1.1:
                pot_equity = .875
            elif pot_equity >= 1.1:
                pot_equity = .9
            elif pot_equity <= .75:
                pot_equity = min(pot_equity+0.0725,0.725)
            if hand_strength < pot_equity: #bad pot equity
                return FoldAction, None
            elif hand_strength < .35:
                return FoldAction, None
            else: #good pot equity
                if hand_strength > .925 or (hand_strength - pot_equity > .25 and hand_strength > .85):
                    return RaiseAction, 1 #value raise
                return CallAction, None

    def auction_strength(self, round_state, street, active):
        board = [eval7.Card(board_card) for board_card in round_state.deck[:street]]
        my_hole = [eval7.Card(my_card) for my_card in round_state.hands[active]]
        comb = board + my_hole
        num_more_board = 5 - len(board)
        opp_num = 2
        auction_num = 1

        deck = eval7.Deck()
        for card in comb:
            deck.cards.remove(card)

        # see amount of hands that you are better than opponent with auction vs. without auction; determine what type of bet you should make then

        num_need_auction = 0
        num_win_without_auction = 0
        num_win_with_auction = 0
        trials = 0

        while trials < self.trials:
            deck.shuffle()
            # either you get the auction card, or the opponent gets the auction card

            cards = deck.peek(num_more_board+opp_num+auction_num)
            opp_hole = cards[:opp_num]
            board_rest = cards[opp_num:len(cards)-1]
            auction_card = [cards[-1]]

            # me with auction
            my_auc_val = eval7.evaluate(my_hole+board+board_rest+auction_card)
            opp_no_auc_val = eval7.evaluate(opp_hole+board+board_rest)

            # oppo with auction
            my_no_auc_val = eval7.evaluate(my_hole+board+board_rest)
            opp_auc_val = eval7.evaluate(opp_hole+board+board_rest+auction_card)

            if my_auc_val > opp_no_auc_val and my_no_auc_val < opp_auc_val:
                num_need_auction += 1
            
            if my_no_auc_val > opp_auc_val:
                num_win_without_auction += 1
            
            if my_auc_val > opp_no_auc_val:
                num_win_with_auction += 1


            trials += 1

        need_auction = num_need_auction/trials
        win_without = num_win_without_auction/trials
        win_with = num_win_with_auction/trials

        return need_auction, win_without, win_with

    def decide_action_auction(self, auction_strength, my_stack):

        # figure our auction size based on auction_strength
        # if win without auc < 0.2 --> then Bid 1 (dont need auction, going to fold)
        # if win without auc > 0.5 --> then Bid need_auction * stack (somewhat want auction, going to win anyways)
        # if win without auc > 0.2 and < 0.5 AND need/win without > 0.5 --> Bid need_auction * stack (want auction card, increases win chance by a lot)
        # else Bid need_auction * stack/2
        
        need_auction, win_without, win_with = auction_strength

        if win_without < 0.2 or win_with < .6:
            return BidAction(min(my_stack, int(self.opp_total_bid/self.num_auctions_seen * 1/2)))
        elif win_without > 0.5:
            return BidAction(int(self.auction_factor*need_auction*my_stack*1/3))
        elif win_without <= 0.5 and win_without >= 0.2:
            return BidAction(int(self.auction_factor*need_auction*my_stack*1/4))
        else:
            return BidAction(int(self.auction_factor*need_auction*my_stack/3))
        
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
        trials = 0

        while trials < self.trials:
            deck.shuffle()
            cards = deck.peek(opp_num + num_more_board)
            opp_hole = cards[:opp_num]
            board_rest = cards[opp_num:]
            my_val = eval7.evaluate(my_hole+board+board_rest)
            opp_value = eval7.evaluate(opp_hole+board+board_rest)
            if my_val > opp_value:
                num_better += 2
            if my_val == opp_value:
                num_better += 1
            trials += 1

        percent_better_than = num_better/(2*trials)
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
        #board_cards = round_state.deck[:street]  # the board cards
        my_pip = round_state.pips[active]  # the number of chips you have contributed to the pot this round of betting
        opp_pip = round_state.pips[1-active]  # the number of chips your opponent has contributed to the pot this round of betting
        my_stack = round_state.stacks[active]  # the number of chips you have remaining
        opp_stack = round_state.stacks[1-active]  # the number of chips your opponent has remaining
        #my_bid = round_state.bids[active]  # How much you bid previously (available only after auction)
        #opp_bid = round_state.bids[1-active]  # How much opponent bid previously (available only after auction)
        #continue_cost = opp_pip - my_pip  # the number of chips needed to stay in the pot
        my_contribution = STARTING_STACK - my_stack  # the number of chips you have contributed to the pot
        opp_contribution = STARTING_STACK - opp_stack  # the number of chips your opponent has contributed to the pot


        if self.already_won:
            if BidAction in legal_actions:
                return BidAction(0)
            elif CheckAction in legal_actions:
                return CheckAction()
            else:
                return FoldAction()
            
        pot = my_contribution + opp_contribution
        min_raise, max_raise = round_state.raise_bounds()
        hand_strength = self.hand_strength(round_state, street, active) - self.nit
        auction_strength = self.auction_strength(round_state, street, active)

        if my_contribution > 100 and hand_strength < 0.85:
            hand_strength -= 0.03

        if BidAction in legal_actions:
            return self.decide_action_auction(auction_strength, my_stack)
        elif street == 0:       
            return self.get_preflop_action(my_cards,round_state,active)
        else:
            decision, conf = self.decide_action_postflop(opp_pip, my_pip, hand_strength, pot, legal_actions, street)

        rand = random.random()
        if decision == RaiseAction and RaiseAction in legal_actions:
            minimum = max(min_raise, pot / 4)
            if conf != 0:
                bet_max = int((1+(2*(hand_strength**2)*rand)) * pot/2 )
                maximum = min(max_raise, bet_max)
            else:
                maximum = min(max_raise, pot)
            if maximum <= minimum:
                amount = int(min_raise)
            else:
                amount = int(rand * (maximum - minimum) + minimum)
            return RaiseAction(amount)
        if decision == RaiseAction and RaiseAction not in legal_actions:
            if CallAction in legal_actions:
                return CallAction()
            return CheckAction()
        return decision()


if __name__ == '__main__':
    run_bot(Player(), parse_args())

