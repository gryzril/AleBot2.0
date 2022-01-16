import string
from Games.bingo import generate_board, print_board
from Games import bingo as bg


#board = bg.generate_board()
#bg.print_board(board)
#bg.save_object(board)

def start(bet):
    board = bg.generate_board()
    print_board(board)
    
    return board
    