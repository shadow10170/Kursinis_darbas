import pygame
from minimax.algorithm import minimax
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH /COLS

RED = (255,0,0)
WHITE =(255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREY = (128,128,128)
FPS = 20
CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'),(44,25))
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('Checkers')

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings= self.white_kings = 0
        self.create_board()

    def draw_squares(self,win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, ROWS,2):
                pygame.draw.rect(win,RED,(row*SQUARE_SIZE,col*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row + 1) % 2):
                    if row < 3:
                        self.board[row].append((Piece(row, col,WHITE)))
                    elif row>4:
                        self.board[row].append((Piece(row, col,RED)))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
    def draw(self,win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces
    
    def move(self,piece,row,col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row,col)

        if row == ROWS-1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings+=1
            else:
                self.red_kings+=1
    def get_piece(self,row,col):
        return self.board[row][col]
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves
    
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves
    
    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, -1)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
    
    def remove(self,pieces):
        for piece in pieces:
            self.board[piece.row][piece.col]=0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -=1
                else:
                    self.white_left-=1
                    
    
class Piece:
    Pading = 10
    Outline = 2
   
    def __init__(self,row,col,color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        if self.color == RED:
            self.direction = -1
        else:
            self.direction = 1
        self.x = 0
        self.y = 0
        self.calc_pos()
   
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE / 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE / 2
    
    def make_king(self):
        self.king = True

    def draw(self,win):
        radius = SQUARE_SIZE/2 - self.Pading
        pygame.draw.circle(win,GREY,(self.x,self.y),radius + self.Outline)
        pygame.draw.circle(win,self.color,(self.x,self.y),radius)
        if self.king:
            win.blit(CROWN,(self.x-CROWN.get_width()/2, self.y - CROWN.get_height()/2))
   
    def move(self,row,col):
        self.row = row
        self.col = col
        self. calc_pos()
    
class Game:
    def __init__(self,win):
        self._init()
        self.win = win
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
   
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def reset(self):
        self._init()

    def select(self,row,col):
        if self.selected:
            result = self._move(row,col)
            if not result:
                self.selected = None
                self.select(row,col)
        piece = self.board.get_piece(row,col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        return False
        
    def _move(self, row, col):
        piece = self.board.get_piece(row,col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row,col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False
        return True
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else :
            self.turn = RED
    
    def winner(self):
        if self.board.red_left <= 0:
            return WHITE
        elif self.board.white_left <= 0:
            return RED
        
        return None 
    
    def draw_valid_moves(self,moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win,BLUE,(col*SQUARE_SIZE+SQUARE_SIZE//2,row*SQUARE_SIZE +SQUARE_SIZE//2),15)
    
    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        self.change_turn()

def get_row_col_from_mouse(pos):
        x, y = pos
        row = int(y /SQUARE_SIZE)
        col = int(x / SQUARE_SIZE)
        return row, col

def main():
    run = True
    game = Game(WIN)
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, WHITE, game)
            game.ai_move(new_board)
       
        if game.winner() != None:
            print(game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row,col)
        game.update()
main()