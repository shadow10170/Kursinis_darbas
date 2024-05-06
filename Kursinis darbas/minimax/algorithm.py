from copy import deepcopy
import pygame

RED = (255,0,0)
WHITE =(255,255,255)

def minimax(position, depth,max_player, game):
    if depth == 0 or game.winner() != None:
        return position.evaluate(), position
    if max_player:
        maxE = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxE= max(maxE, evaluation)
            if maxE == evaluation:
                best_move = move
        return maxE, best_move
    else:
        minE = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minE= min(minE, evaluation)
            if minE == evaluation:
                best_move = move
        return minE, best_move
    
def simulate_move(piece, move, board, game, skip):
    board.move(piece,move[0],move[1])
    if skip:
        board.remove(skip)
    return board

def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)
    
    return moves
