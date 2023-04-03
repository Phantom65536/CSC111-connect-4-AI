"""
Game Interface class
"""
from __future__ import annotations
from typing import Optional, Any

import math
import pygame
import numpy as np
import connect_four


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
                    pygame.draw.circle(self.screen, (255, 255, 0), (int(col * 100 + 50), 600 - int(row * 100 + 50)), 45)
        pygame.display.update()


def handle_move(x: Any, board: GameInterface, game: connect_four.ConnectFour, player: int) -> None:
    """
    Helper function to handle a move by either player 1 or player 2.
    """
    col_num = int(math.floor(x / 100))
    row_num = board.get_next_open_row(game.board, col_num)
    board.drop_piece(game.board, row_num, col_num, player)
    game.record_move(col_num, row_num)


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
