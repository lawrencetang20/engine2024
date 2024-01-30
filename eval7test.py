import eval7, pprint
from pprint import pprint
# import numpy as np

deck = eval7.Deck()
deck.shuffle()
hand = deck.deal(5)
#pprint.pprint(hand)
  
hand1 = [eval7.Card('9c'), eval7.Card('Tc'), eval7.Card('Jc'), eval7.Card('Qc'), eval7.Card('Ac')]
x = eval7.evaluate(hand1)
print(x)

# print(eval7.handtype(x))

hr = eval7.HandRange("89+")
# print(hr.hands)

# print(len(all_hands))

# print(np.random.normal(1,.5))

board = [eval7.Card(x) for x in []]
my_hole = [eval7.Card(a) for a in ['Ah', 'Kd']]
opp_hole = [eval7.Card(a) for a in ['Ts', 'Tc']]
comb = board + my_hole
num_more_board = 5 - len(board)


# ya = False

# if len(my_hole) == 2 and ya:
#     opp_num = 3
# else:
#     opp_num = 2


opp_num = 2
auction_num = 1

# deck = eval7.Deck()
# for card in comb:
#     deck.cards.remove(card)

        # see amount of hands that you are better than opponent with auction vs. without auction; determine what type of bet you should make then

# num_need_auction = 0
# num_win_without_auction = 0
# num_win_with_auction = 0
# trials = 0

# while trials < 500:
#     deck.shuffle()
#     # either you get the auction card, or the opponent gets the auction card

#     cards = deck.peek(num_more_board+opp_num+auction_num)
#     opp_hole = cards[:opp_num]
#     board_rest = cards[opp_num:len(cards)-1]
#     auction_card = [cards[-1]]

#     # me with auction
#     my_auc_val = eval7.evaluate(my_hole+board+board_rest+auction_card)
#     opp_no_auc_val = eval7.evaluate(opp_hole+board+board_rest)

#     # oppo with auction
#     my_no_auc_val = eval7.evaluate(my_hole+board+board_rest)
#     opp_auc_val = eval7.evaluate(opp_hole+board+board_rest+auction_card)

#     if my_auc_val > opp_no_auc_val and my_no_auc_val < opp_auc_val:
#         num_need_auction += 1
    
#     if my_no_auc_val > opp_auc_val:
#         num_win_without_auction += 1
    
#     if my_auc_val > opp_no_auc_val:
#         num_win_with_auction += 1

#     trials += 1

# need_auction = num_need_auction/trials
# win_without = num_win_without_auction/trials
# win_with = num_win_with_auction/trials

# print(need_auction, win_without, win_with)

board = [eval7.Card(board_card) for board_card in ['Qd', '6d', '3d']]
my_hole = [eval7.Card(my_card) for my_card in ['Td', 'Ac']]
comb = board + my_hole
num_more_board = 5 - len(board)

ya = True

if len(my_hole) == 2 and ya:
    opp_num = 3
else:
    opp_num = 2


deck = eval7.Deck()
for card in comb:
    deck.cards.remove(card)

num_better = 0
trials = 0
draw_hit = 0

while trials < 500:
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
    if my_val >= 67305472 and my_val <= 84715911:
        draw_hit += 1

percent_better_than = num_better/(2*trials)
draw_hit_pct = draw_hit/trials
print(percent_better_than)
print(draw_hit_pct)
