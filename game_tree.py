from __future__ import annotations
from python_ta.contracts import check_contracts
import connect_four
from typing import Optional


# @check_contracts
class GameTree:
    """A decision tree for Connect Four moves. Each node in the tree represents a move.
    Instance Attributes:
        - board_size: the dimension of the board in (rows, columns), ie (y, x) in coordinates
        - state: current game state storing q-values if position is unoccupied and None if position is occupied
        - initial_q_val: the initial q value of each unoccupied position when a GameTree instance is initialised
        - learning_rate: the learning rate (alpha) of an AI agent in q-learning
        - discount: the discount (gamma) of an AI agent in q-learning
    Representation Invariants:
        - board_size[0] >= 5 and board_size[1] >= 5
        - self.reward > 0 and 0 <= self.learning_rate <= 1 and 0 <= self.discount <= 1
        - all None values in self.state corresponds to the occupied positions in game.board
        - self.state has the same dimension as game.board
    """
    board_size: tuple[int, int]
    q_values: dict[tuple[int, int], float]

    initial_q_val: float
    reward: float
    learning_rate: float
    discount: float

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      action by the current player. It is a mapping where the keys
    #      are the move coordinates (y, x) and the values are GameTrees.
    _subtrees: dict[tuple[int, int], GameTree]

    def __init__(self, game_instance: connect_four.ConnectFour, initial_q: float, reward: float, alpha: float, gamma: float) -> None:
        """Initialize a new game tree."""
        self.board_size = game_instance.board_size
        self.q_values = {}
        for coordinate in game_instance.possible_moves:
            self.q_values[coordinate] = float(initial_q)
        self._subtrees = {}
        self.initial_q_val, self.reward = initial_q, reward
        self.learning_rate, self.discount = alpha, gamma

    def get_subtrees(self) -> dict[tuple[int, int], GameTree]:
        """Return the subtrees of this game tree."""
        return self._subtrees

    def add_subtree(self, game_instance: connect_four.ConnectFour, move: tuple[int, int]) -> None:
        """Add a subtree with the action move applied to this game tree self.
        Preconditions:
        - move is in the format (y, x)
        - move not in self._subtrees
        - position of move on game board is unoccupied
        """
        subtree = GameTree(game_instance, self.initial_q_val, self.reward, self.learning_rate, self.discount)
        self._subtrees[move] = subtree

    def find_subtree_by_move(self, move: tuple[int, int]) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.
        Return None if no subtree corresponds to that move.
        Preconditions:
        - move is in the format (y, x)
        """
        if move in self._subtrees:
            return self._subtrees[move]
        else:
            return None

    def update_q_tables(self, move_sequence: list[tuple[int, int]], player: int, winner: int, curr_move_index: int = 0) -> None:
        """Update all q values corresponding to the move in move_sequence in the descendants of self
        Preconditions:
        - move_sequence depicts all moves from start to end of a game
        - every tuple in move_sequence is in the format (y, x)
        - move_sequence has no duplicates
        - len(move_sequence) > 0
        - move_sequence[curr_move_index] in self._subtrees
        - winner in {0, 1, 2}
        - if winner is 0 it means the game ends in a tie
        - player in {1, 2}
        - player indicates whether AI agent is player 1 or 2
        - self is a state for player
        - move_sequence[curr_move_index] in self.q_values
        """
        original_q_value = self.q_values[move_sequence[curr_move_index]]
        if curr_move_index + 2 < len(move_sequence):
            next_state_tree = self._subtrees[move_sequence[curr_move_index]]._subtrees[move_sequence[curr_move_index + 1]]
            next_state_tree.update_q_tables(move_sequence, player, winner, curr_move_index + 2)
            self.q_values[move_sequence[curr_move_index]] = (1 - self.learning_rate) * original_q_value + \
                self.learning_rate * (self.discount * max(next_state_tree.q_values[action] for action in next_state_tree.q_values))
        elif winner == player:
            self.q_values[move_sequence[curr_move_index]] = (1 - self.learning_rate) * original_q_value + self.learning_rate * self.reward
        elif winner + player == 3:
            self.q_values[move_sequence[curr_move_index]] = (1 - self.learning_rate) * original_q_value + self.learning_rate * -self.reward
        else:
            self.q_values[move_sequence[curr_move_index]] = (1 - self.learning_rate) * original_q_value