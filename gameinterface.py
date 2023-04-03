"""
Game Interface class
"""
from __future__ import annotations
from typing import Optional, Any

import sys
import math
import pygame
import numpy as np
import connect_four
import graphplot


class GameInterface:
    """
    A GameInterface class where the current game is displayed using the information from the Game class
    (such as the players’ moves and checking for winners) and use pygame to provide a GUI (Graphical User Interface)
    for the human player to interact with the AI model.

    Instance Attributes:
        - col: The number of columns of the game board.
        - row: The number of rows of the game board.
        - screen: The pygame screen

    Representation Invariants:
        - self.col >= 5
        - self.row >= 5
    """
    col: int
    row: int
    screen: pygame.Surface

    def __init__(self, row: Optional[int] = 6, col: Optional[int] = 7) -> None:
        """Initialize a new GameInterface instance.
        """
        self.row = row
        self.col = col
        size = (500, 600)
        pygame.display.init()
        self.screen = pygame.display.set_mode(size)
        self.screen.fill((0, 0, 0))
        pygame.display.update()

    def drop_piece(self, board: np.ndarray, row: int, col: int, player: int) -> None:
        """Drop the token into a column.

        Preconditions:
            - 0 <= row < self.row
            - 0 <= col < self.col
        """
        board[row][col] = player

    def get_next_open_row(self, board: np.ndarray, col: int) -> Optional[int]:
        """
        Returns the next open row number.

        Preconditions:
            - 0 <= col < self.col
        """
        for row_num in range(0, self.row):
            if board[row_num][col] == 0:
                return row_num
        return None

    def draw_board(self, board: np.ndarray) -> None:
        """
        Draw a game board in pygame.
        """
        for col in range(0, self.col):
            for row in range(0, self.row + 1):
                pygame.draw.rect(self.screen, (0, 0, 255), (col * 100, row * 100 + 100, 100, 100))
                pygame.draw.circle(self.screen, (0, 0, 0), (int(col * 100 + 50), int(row * 100 + 50)), 45)

        for col in range(0, self.col):
            for row in range(0, self.row):
                if board[row][col] == 1:
                    # player 1, red circle
                    # pygame.draw.circle(screen, (255, 0, 0), (int(col * 100 + 50), int((row + 1) * 100 + 50)), 45)
                    pygame.draw.circle(self.screen, (255, 0, 0), (int(col * 100 + 50), 600 - int(row * 100 + 50)), 45)

                elif board[row][col] == 2:
                    # player 2, yellow circle
                    # pygame.draw.circle(screen, (255, 255, 0), (int(col * 100 + 50), int((row + 1) * 100 + 50)), 45)
                    pygame.draw.circle(self.screen, (255, 255, 0), (int(col * 100 + 50), 600-int(row * 100 + 50)), 45)
        pygame.display.update()


# def run_game() -> connect_four.ConnectFour:
#     """
#     Run one Connect4 game between player 1 and player 2.
#     Return the ConnectFour instance after the game is complete.
#     """
#     size = (500, 500)
#     gboard = GameInterface(5, 5)
#     screen = pygame.display.set_mode(size)
#     pygame.display.update()
#     game = connect_four.ConnectFour(5, 5)
#     gboard.draw_board(game.board, screen)
#
#     while game.get_winner() is None:
#         for event in pygame.event.get():
#             # if event.type is pygame.QUIT
#             if event.type == 256:
#                 sys.exit()
#             # if event.type is pygame.MOUSEBUTTONDOWN
#             elif event.type == 1025:
#                 if game.is_player_1_turn():
#                     x = event.pos[0]
#                     handle_move(x, gboard, game, 1)
#                 else:
#                     x = event.pos[0]
#                     handle_move(x, gboard, game, 2)
#
#                 gboard.draw_board(game.board, screen)
#
#     assert game.get_winner() is not None
#
#     return game
#

def handle_move(x: Any, board: GameInterface, game: connect_four.ConnectFour, player: int) -> None:
    """
    Helper function to handle a move by either player 1 or player 2.
    """
    col_num = int(math.floor(x / 100))
    row_num = board.get_next_open_row(game.board, col_num)
    board.drop_piece(game.board, row_num, col_num, player)
    game.record_move(col_num, row_num)


# def run_games(num_games: int, ai: int, print_game: bool = True, show_stats: bool = False) -> dict[str, int]:
#     """
#     Run num_games Connect4 game between player 1 and player 2.
#
#     Optional arguments:
#         - print_game: print a record of each game (default: True)
#         - show_stats: use GraphPlot to display statistics for the game runs (default: False)
#
#     Preconditions:
#         - num_games >= 1
#     """
#     stats = {'1': 0, '2': 0}
#     results = []
#     for i in range(0, num_games):
#         game = run_game()
#         winner = game.get_winner()
#         stats[winner] += 1
#         results.append(winner)
#
#         if print_game:
#             print(f'Game {i} winner: {winner}.')
#
#     for outcome in stats:
#         print(f'{outcome}: {stats[outcome]}/{num_games} ({100.0 * stats[outcome] / num_games:.2f}%)')
#
#     if show_stats:
#         resultsg = graphplot.GraphPlot(results, ai)
#         resultsg.plot_game_stats()
#
#     return stats


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    # import python_ta

    # python_ta.check_all(config={
    #     'extra-imports': ['pygame', 'numpy', 'sys', 'math', 'connect_four', 'graphplot'],
    #     'allowed-io': ['run_games'],  # the names (strs) of functions that call print/open/input
    #     'disable': ['too-many-nested-blocks'],
    #     'max-line-length': 120
    # })
