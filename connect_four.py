import numpy as np
from numpy import ndarray
from typing import Optional
from itertools import groupby


class ConnectFour:
    board: ndarray
    moves: list[tuple]

    def __init__(self, x: int = 7, y: int = 6) -> None:
        self.board = np.zeros((y, x))
        self.moves = []

    def is_player_1_turn(self) -> bool:
        return len(self.moves) % 2 == 0

    def record_move(self, x: int, y: int) -> None:
        """Records the player move at the specified coordinate, setting the value corresponding to the player number.

        Preconditions:
        - 0 <= x < self.board.shape[1]
        - 0 <= y < self.board.shape[0]
        - self.board[y, x] == 0
        - the move is a valid move
        """
        if self.is_player_1_turn():
            self.board[y, x] = 1
        else:
            self.board[y, x] = 2

        self.moves.append((x, y))

    def get_winner(self) -> Optional[int]:
        """Returns the number corresponding to the winning player. Returns None if there is no winner."""
        y, x = self.board.shape

        #check diagonals
        if y >= 4 and x >= 4:
            board = self.board
            for _ in range(2):
                board = np.flip(board, 1)
                for i in range(4 - y, x - 3):
                    diagonal = board.diagonal(i).tolist()
                    if winner := consecutive_in_list(diagonal):
                        return winner

        #check rows
        for i in range(y):
            row = self.board[i].tolist()
            if winner := consecutive_in_list(row, True):
                return winner

        #check columns
        for i in range(x):
            column = self.board[:, i].tolist()
            if winner := consecutive_in_list(column):
                return winner


def consecutive_in_list(lst: list, wrap: bool = False) -> Optional[int]:
    grouped_diagonal = [[k, len(list(g))] for k, g in groupby(lst)]
    if wrap:
        grouped_diagonal[-1][1] += grouped_diagonal[0][1]
    if any([i == 1 and n >= 4 for i, n in grouped_diagonal]):
        return 1
    if any([i == 2 and n >= 4 for i, n in grouped_diagonal]):
        return 2
