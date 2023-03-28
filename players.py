from __future__ import annotations

import random

from python_ta.contracts import check_contracts
import connect_four
from typing import Optional


# @check_contracts
class Player:
    """An abstracted class representing a player in Connect 4.

    This class can be subclassed to implement different strategies for a player.

    Instance Attributes:
    - player_number: Indicate whether this Player instance is player 1 or 2
    - game: the game instance this Player instance is playing on

    Representation Invariants:
    - self.player_number in {1, 2}
    """
    player_number: int
    game: connect_four.ConnectFour

    def __init__(self, game_instance: connect_four.ConnectFour, player_number: int) -> None:
        """Initialize a Player instance.

        Preconditions:
        - player_number in {1, 2}
        """
        self.player_number = player_number
        self.game = game_instance

    def make_move(self, y: int, x: int) -> None:
        """Make a move in the current game.

        Preconditions:
        - 0 <= y < game.board_size[0] and 0 <= x < game.board_size[1]
        - (game.is_player_1_turn() and self.player_number == 1) or self.player_number == 2
        - the game is not finished
        """
        self.game.record_move(y, x)

    def reset(self, game_instance: connect_four.ConnectFour) -> None:
        """Reset this player instance to play another game"""
        self.game = game_instance


class TrainingAgent(Player):
    """A class representing the training agent in Connect 4. This agent is able to read ahead one move."""
    def make_move(self) -> None:
        """Make a move in the current game.

        Preconditions:
        - 0 <= y < game.board_size[0] and 0 <= x < game.board_size[1]
        - (game.is_player_1_turn() and self.player_number == 1) or self.player_number == 2
        - the game is not finished
        """
        opponent_number = 2 if self.player_number == 1 else 1
        predict_move_order = (self.player_number, opponent_number)
        for i in range(0, 2):
            for coordinate in self.game.possible_moves:
                game_further_move = self.game.copy()
                game_further_move.record_move(coordinate[0], coordinate[1], predict_move_order[i])
                future_winner = game_further_move.get_winner()
                if future_winner == predict_move_order[i]:
                    self.game.record_move(coordinate[0], coordinate[1])
                    return
        random_move = random.choice(self.game.possible_moves)
        self.game.record_move(random_move[0], random_move[1])
