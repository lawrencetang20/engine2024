import eval7, pprint
from pprint import pprint

board = [eval7.Card(x) for x in ['9s', '6s', 'Kh']]
my_hole = [eval7.Card(a) for a in ['6c', '5d']]
comb = board + my_hole
num_more_board = 5 - len(board)
opp_num = 2
auction_num = 1

# print(my_hole)
# print(board)

deck = eval7.Deck()
for card in comb:
    deck.cards.remove(card)

# see amount of hands that you are better than opponent with auction vs. without auction; determine what type of bet you should make then

num_need_auction = 0
num_win_without_auction = 0
num_win_with_auction = 0
trials = 0

while trials < 250:
    deck.shuffle()
    # either you get the auction card, or the opponent gets the auction card

    cards = deck.peek(num_more_board+opp_num+auction_num)
    opp_hole = cards[:opp_num]
    board_rest = cards[opp_num:len(cards)-1]
    auction_card = [cards[-1]]

    # print("\n NEW TRIAL")

    # print("opp", opp_hole) 
    # print("my", my_hole)
    # print("board", board + board_rest)
    # print("auction", auction_card)

    # me with auction
    my_auc_val = eval7.evaluate(my_hole+board+board_rest+auction_card)
    # print("me with auc", my_hole+board+board_rest+auction_card, my_auc_val)
    opp_no_auc_val = eval7.evaluate(opp_hole+board+board_rest)
    # print("opp no auc", opp_hole+board+board_rest, opp_no_auc_val)

    # oppo with auction
    my_no_auc_val = eval7.evaluate(my_hole+board+board_rest)
    # print("me no auc", my_hole+board+board_rest, my_no_auc_val)
    opp_auc_val = eval7.evaluate(opp_hole+board+board_rest+auction_card)
    # print("opp with auc", opp_hole+board+board_rest+auction_card, opp_auc_val)

    if my_auc_val > opp_no_auc_val and my_no_auc_val < opp_auc_val:
        num_need_auction += 1
        # print("need auction\n")
    
    if my_no_auc_val > opp_auc_val:
        num_win_without_auction += 1
    
    if my_auc_val > opp_no_auc_val:
        num_win_with_auction += 1


    trials += 1


print("need auction", num_need_auction/trials)
print("win without auc", num_win_without_auction/trials)
print("win with auc", num_win_with_auction/trials)

# if win without auc < 0.2 --> then Bid 1 (dont need auction, going to fold)

# if win without auc > 0.5 --> then Bid need_auction * stack (somewhat want auction, going to win anyways)

# if win without auc > 0.2 and < 0.5 AND need/win without > 0.5 --> Bid need_auction * stack (want auction card, increases win chance by a lot)
