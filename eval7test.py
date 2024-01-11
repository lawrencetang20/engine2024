import eval7, pprint
from pprint import pprint
import numpy as np

deck = eval7.Deck()
deck.shuffle()
hand = deck.deal(5)
#pprint.pprint(hand)
  
hand1 = [eval7.Card('2h'), eval7.Card('2h')]
x = eval7.evaluate(hand1)
# print(x)
# print(eval7.handtype(x))

hr = eval7.HandRange("89+")
# print(hr.hands)

# print(len(all_hands))

# print(np.random.normal(1,.5))

board = [eval7.Card(x) for x in ['Js', 'Jc', '2s', '8d']]
my_hole = [eval7.Card(a) for a in ['As', '6s']]
comb = board + my_hole
num_more_board = 5 - len(board)


ya = False

if len(my_hole) == 2 and ya:
    opp_num = 3
else:
    opp_num = 2

deck = eval7.Deck()
for card in comb:
    deck.cards.remove(card)

num_better = 0
trials = 0

while trials < 500:
    deck.shuffle()
    cards = deck.peek(opp_num + num_more_board)
    opp_hole = cards[:opp_num]
    board_rest = cards[opp_num:]
    print(opp_hole, board_rest)
    my_val = eval7.evaluate(my_hole+board+board_rest)
    opp_value = eval7.evaluate(opp_hole+board+board_rest)
    if my_val >= opp_value:
        num_better += 1
    trials += 1

percent_better_than = num_better/trials
print(percent_better_than)
