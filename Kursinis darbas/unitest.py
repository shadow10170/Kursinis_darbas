import unittest
import pygame
from Augustas_Tamasiunas_checkers import Board, Piece, Game, SQUARE_SIZE, ROWS, COLS

class TestCheckers(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.win = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Checkers')

    def tearDown(self):
        pygame.quit()

    def test_board_initialization(self):
        board = Board()
        # Test that the board initializes correctly
        self.assertEqual(len(board.board), ROWS)
        self.assertEqual(len(board.board[0]), COLS)

    def test_piece_initialization(self):
        piece = Piece(0, 0, (255, 255, 255))  # Create a white piece at row 0, column 0
        # Test that the piece initializes correctly
        self.assertEqual(piece.row, 0)
        self.assertEqual(piece.col, 0)
        self.assertEqual(piece.color, (255, 255, 255))

    def test_game_initialization(self):
        game = Game(self.win)
        # Test that the game initializes correctly
        self.assertEqual(game.turn, (255, 0, 0))  # RED starts
        self.assertIsNone(game.selected)
        self.assertEqual(game.valid_moves, {})

    # Add more test cases for other functionalities such as piece movement, selecting pieces, etc.

if __name__ == '__main__':
    unittest.main()