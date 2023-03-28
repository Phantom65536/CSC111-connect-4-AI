from __future__ import annotations
from python_ta.contracts import check_contracts
import numpy as np
from numpy import ndarray
from typing import Optional
from itertools import groupby


# @check_contracts
class ConnectFour:
    """Represents the state of a Connect Four game.
    Instance Attributes:
    - board_size: the dimension of the board in (rows, columns), ie (y, x) in coordinates
    - board: a numpy ndarray storing the current board state. Each position stores 0 if the space is unoccupied,
             1 if occupied by player 1 and 2 if occupied by player 2.
    - move_sequence: a list of tuples storing the coordinates of player moves in the format (player_move_y, player_move_x).
    - possible_moves: a list of tuples storing the coordinates of all moves that can be taken in current game state.
    Representation Invariants:
    - self.board_size[0] >= 5 and self.board_size[1] >= 5
    - all values in board are either 0, 1 or 2
    - all(0 <= move[0] < self.board_size[0] and 0 <= move[1] < self.board_size[1] for move in self.move_sequence)
    - all(0 <= move[0] < self.board_size[0] and 0 <= move[1] < self.board_size[1] for move in self.possible_moves)
    - all tuples in self.moves are unique
    """
    board_size: tuple[int, int]
    board: ndarray
    move_sequence: list[tuple[int, int]]
    possible_moves: list[tuple[int, int]]

    def __init__(self, y: int = 6, x: int = 7) -> None:
        """Initialize all positions in board to 0, indicating all positions are empty"""
        self.board = np.zeros((y, x), dtype=int)
        self.move_sequence = []
        self.board_size = (y, x)
        self.possible_moves = [(0, each_x) for each_x in range(x)]

    def copy(self) -> ConnectFour:
        """Return a copy of this game state."""
        new_game = ConnectFour(self.board_size[0], self.board_size[1])
        new_game.board_size = self.board_size
        new_game.board = np.copy(self.board)
        new_game.move_sequence = self.move_sequence.copy()
        new_game.possible_moves = self.possible_moves.copy()
        return new_game

    def is_player_1_turn(self) -> bool:
        """Returns whether it is player 1's turn."""
        return len(self.move_sequence) % 2 == 0

    def record_move(self, y: int, x: int, forced_move_player: Optional[int] = None) -> None:
        """Records the player move at the specified coordinate, setting the value corresponding to the player number.
        If forced_move_player is not None, a move is placed for this player disregarding whether it is their turn.
        Preconditions:
        - 0 <= x < self.board_size[1]
        - 0 <= y < self.board_size[0]
        - self.board[y, x] == 0
        - (y, x) in self.available_moves()
        - forced_move_player in {1, 2, None}
        """
        if forced_move_player is not None:
            self.board[y, x] = forced_move_player
        elif self.is_player_1_turn():
            self.board[y, x] = 1
        else:
            self.board[y, x] = 2

        self.move_sequence.append((y, x))
        self.possible_moves.remove((y, x))
        if y != self.board_size[0] - 1:
            self.possible_moves.append((y + 1, x))

    def get_winner(self) -> Optional[int]:
        """Returns the number corresponding to the winning player, 0 if draw. Returns None if game is not finished."""
        # check diagonals
        board = self.board
        for _ in range(2):
            board = np.flip(board, 1)
            for i in range(4 - self.board_size[0], self.board_size[1] - 3):
                diagonal = board.diagonal(i).tolist()
                if winner := consecutive_in_list(diagonal):
                    return winner

        # check rows
        for i in range(self.board_size[0]):
            row = self.board[i].tolist()
            if winner := consecutive_in_list(row, True):
                return winner

        # check columns
        for i in range(self.board_size[1]):
            column = self.board[:, i].tolist()
            if winner := consecutive_in_list(column):
                return winner

        # check draw
        if self.possible_moves == []:
            return 0


# @check_contracts
def consecutive_in_list(lst: list, wrap: bool = False) -> Optional[int]:
    """A helper function checking for four consecutive values of 1 or 2 in a list, and returns that value."""
    grouped_diagonal = [[k, len(list(g))] for k, g in groupby(lst)]
    if wrap and grouped_diagonal[-1][0] == grouped_diagonal[0][0]:
        grouped_diagonal[-1][1] += grouped_diagonal[0][1]
    if any([i == 1 and n >= 4 for i, n in grouped_diagonal]):
        return 1
    if any([i == 2 and n >= 4 for i, n in grouped_diagonal]):
        return 2
