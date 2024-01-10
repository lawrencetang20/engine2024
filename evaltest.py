import eval7

hand1 = ['7h','6h']
board1 = ['Th','9h','8h']
def flush_in_play(board):
    hearts = 0
    diamonds = 0
    spades = 0
    clubs = 0
    for card in board:
        if card[1] == 'h':
            hearts+=1 
        if card[1] == 'd':
            diamonds+=1 
        if card[1] == 's':
            spades+=1 
        if card[1] == 'c':
            clubs+=1 
    if hearts <= 3: 
        return 'hearts'
    if diamonds <=3:
        return 'diamonds'
    if spades <=3:
        return 'spades'
    if clubs <=3: 
        return 'clubs'
            
total_cards1 = hand1 + board1
print(total_cards1)
evalhand = [eval7.Card(s) for s in total_cards1]
a = eval7.evaluate(evalhand)
print(a)
print(eval7.handtype(a))

print(flush_in_play(board1))

