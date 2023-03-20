"""
Game Interface class
"""
from __future__ import annotations
from typing import Optional, Any

import sys
import math
import pygame
import numpy as np
import connect_4
import graphplot

COL = 7
ROW = 6


class GameInterface:
    """
    A GameInterface class where the current game is displayed using the information from the Game class
    (such as the players’ moves and checking for winners) and use pygame to provide a GUI (Graphical User Interface)
    for the human player to interact with the AI model.
    """
    board: np.ndarray

    def __init__(self) -> None:
        self.board = np.zeros((ROW, COL))

    def drop_piece(self, row: int, col: int, player: int) -> None:
        """
        Drop the token into a column.

        Preconditions:
            - 0 <= row <= ROW
            - 0 <= col <= COL
        """
        self.board[row][col] = player

    def get_next_open_row(self, col: int) -> Optional[int]:
        """
        Returns the next open row number.

        Preconditions:
            - 0 <= col <= COL
        """
        for row_num in range(0, ROW):
            if self.board[row_num][col] == 0:
                return row_num
        return None

    def draw_board(self, screen: pygame.Surface) -> None:
        """
        Draw a game board in pygame
        """
        for col in range(0, COL):
            for row in range(0, ROW):
                pygame.draw.rect(screen, (0, 0, 255), (col * 100, row * 100 + 100, 100, 100))
                pygame.draw.circle(screen, (0, 0, 0), (int(col * 100 + 50), int(row * 100 + 50)), 45)

        for col in range(0, COL):
            for row in range(0, ROW):
                if self.board[row][col] == 1:
                    # player 1, red circle
                    pygame.draw.circle(screen, (255, 0, 0), (int(col * 100 + 50), 700 - int(row * 100 + 50)), 45)

                elif self.board[row][col] == 2:
                    # player 2, yellow circle
                    pygame.draw.circle(screen, (255, 255, 0), (int(col * 100 + 50), 700 - int(row * 100 + 50)), 45)
        pygame.display.update()


def run_game() -> connect_4.ConnectFour:
    """
    Run one game.
    """
    size = (700, 600)
    board = GameInterface()
    screen = pygame.display.set_mode(size)
    board.draw_board(screen)
    pygame.display.update()
    game = connect_4.ConnectFour()

    while game.get_winner() is None:
        for event in pygame.event.get():
            # if event.type == pygame.QUIT:
            if event.type == 256:
                sys.exit()
            # elif event.type == pygame.MOUSEBUTTONDOWN:
            elif event.type == 1025:
                if game.is_player_1_turn():
                    x = event.pos[0]
                    handle_move(x, board, game, 1)
                else:
                    x = event.pos[0]
                    handle_move(x, board, game, 2)

                board.draw_board(screen)

    assert game.get_winner() is not None

    return game


def handle_move(x: Any, board: GameInterface, game: connect_4.ConnectFour, player: int) -> None:
    """
    Helper function to handle a move by either player 1 or player 2.
    """
    col_num = int(math.floor(x / 100))
    row_num = board.get_next_open_row(col_num)
    board.drop_piece(row_num, col_num, player)
    game.record_move(col_num, row_num)


def run_games(num_games: int, print_game: bool = True, show_stats: bool = False) -> dict[str, int]:
    """
    Run num_games games.
    """
    stats = {'1': 0, '2': 0}
    results = []
    for i in range(0, num_games):
        game = run_game()
        winner = game.get_winner()
        stats[winner] += 1
        results.append(winner)

        if print_game:
            print(f'Game {i} winner: {winner}.')

    for outcome in stats:
        print(f'{outcome}: {stats[outcome]}/{num_games} ({100.0 * stats[outcome] / num_games:.2f}%)')

    if show_stats:
        resultsg = graphplot.GraphPlot(results)
        resultsg.plot_game_stats()

    return stats


if __name__ == '__main__':
    import doctest

    doctest.testmod(verbose=True)
    import python_ta

    python_ta.check_all(config={
        'extra-imports': ['pygame', 'numpy', 'sys', 'math', 'connect_4', 'graphplot'],
        'allowed-io': ['run_games'],  # the names (strs) of functions that call print/open/input
        'disable': ['too-many-nested-blocks'],
        'max-line-length': 120
    })
