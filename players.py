from __future__ import annotations

import random

from python_ta.contracts import check_contracts
import connect_four
from typing import Optional
import csv
from game_tree import GameTree
import pickle


# @check_contracts
class Player:
    """An abstracted class representing a player in Connect 4.

    This class can be subclassed to implement different strategies for a player.

    Instance Attributes:
    - player_number: Indicate whether this Player instance is player 1 or 2
    - game: the game instance this Player instance is playing on

    Representation Invariants:
    - self.player_number in {1, 2}
    - self.game must be a beginning game instance, ie nobody has placed their move yet
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


class AIPlayer(Player):
    """A class representing the AI agent with q-learning player as self.player_number.

    Instance Attributes:
    - max_explore_prob: max exploration probability
                        shd be set the same as min_explore_prob when constant explore_prob is desired
    """
    complete_tree: GameTree
    curr_tree: Optional[GameTree]

    initial_q_val: float = 0.0
    reward: float
    learning_rate: float
    discount: float

    exploration_prob: float
    max_explore_prob: float
    min_explore_prob: float

    def __init__(self, game_instance: connect_four.ConnectFour, player_number: int, ai_config_file: str,
                 tree_file: Optional[str] = None) -> None:
        """Initialize the AI with ai_config_file and possibly retrieve an existing GameTree from tree_file

        Preconditions:
        - ai_config_file has only one line and is in the format of  reward, learning_rate, discount,
                                                                    max_explore_prob and min_explore_prob
        - game_instance is a beginning game state
        """
        Player.__init__(self, game_instance, player_number)
        with open(f'AI Models/{ai_config_file}') as csv_file:
            reader = list(csv.reader(csv_file))
            self.reward, self.learning_rate, self.discount, self.max_explore_prob, self.min_explore_prob = \
                float(reader[0][0]), float(reader[0][1]), float(reader[0][2]), float(reader[0][3]), float(reader[0][4])
            self.exploration_prob = self.max_explore_prob
        if tree_file is not None:
            tree_file_handler = open(f'AI Models/{tree_file}', 'rb')
            self.complete_tree = pickle.load(tree_file_handler)
            tree_file_handler.close()
        else:
            self.complete_tree = GameTree(game_instance, self.initial_q_val, self.reward, self.learning_rate, self.discount)
        self.curr_tree = self.complete_tree

    def make_move(self, training: bool = False) -> None:
        """Make a move."""

        # 1) Move self.curr_tree to current valid state for self by (adding and) moving down self.complete_tree
        #    according to the opponent's move
        if self.curr_tree is not None and (self.player_number != 1 or self.curr_tree != self.complete_tree):
            latest_move = self.game.move_sequence[-1]
            if latest_move in self.curr_tree.get_subtrees():
                self.curr_tree = self.curr_tree.get_subtrees()[latest_move]
            elif not training:
                self.curr_tree = None
            else:
                self.curr_tree.add_subtree(self.game, latest_move)
                self.curr_tree = self.curr_tree.get_subtrees()[latest_move]

        # 2) Choose a random action and (add and) move along the GameTree if necessary
        explore_num = random.uniform(0.0, 1.0)
        if self.curr_tree is None or self.curr_tree.get_subtrees() == {} or (training and explore_num < self.exploration_prob):
            chosen_action = random.choice(self.game.possible_moves)
            self.game.record_move(chosen_action[0], chosen_action[1])
            if training:
                assert self.curr_tree is not None
                if chosen_action not in self.curr_tree.get_subtrees():
                    self.curr_tree.add_subtree(self.game, chosen_action)
                self.curr_tree = self.curr_tree.get_subtrees()[chosen_action]
            else:
                self.curr_tree = None

        # 2) Choose among actions with highest q_value randomly if there are actions recorded in self.curr_tree
        #    and AI decides to exploit instead of exploring
        else:
            optimal_actions = []
            for recorded_move in self.curr_tree.get_subtrees():
                if optimal_actions == [] or self.curr_tree.q_values[recorded_move] == self.curr_tree.q_values[optimal_actions[0]]:
                    optimal_actions.append(recorded_move)
                elif self.curr_tree.q_values[recorded_move] > self.curr_tree.q_values[optimal_actions[0]]:
                    optimal_actions = [recorded_move]
            chosen_action = random.choice(optimal_actions)
            self.game.record_move(chosen_action[0], chosen_action[1])
            self.curr_tree = self.curr_tree.get_subtrees()[chosen_action]

    def train(self, num_games: int, opponent: Player, tree_file_name: str) -> None:
        """Train self to play as self.player_number by playing num_games times with opponent.

        Preconditions:
        - opponent.player_number != self.player_number
        - opponent able to choose a move itself/automatically
        - num_games > 0
        """
        exploration_prob_decay = (self.max_explore_prob - self.min_explore_prob) / num_games
        results = []
        stats = {0: 0, 1: 0, 2: 0}
        for _ in range(num_games):
            if self.player_number == 1:
                while self.game.get_winner() is None:
                    self.make_move(True)
                    if self.game.get_winner() is not None:
                        break
                    opponent.make_move()
                winner = self.game.get_winner()
                self.complete_tree.update_q_tables(self.game.move_sequence, 1, winner)
            else:
                while self.game.get_winner() is None:
                    opponent.make_move()
                    if self.game.get_winner() is not None:
                        break
                    self.make_move(True)
                winner = self.game.get_winner()
                self.complete_tree.get_subtrees()[self.game.move_sequence[0]].\
                    update_q_tables(self.game.move_sequence, 2, winner, 1)
            results.append(winner)
            stats[winner] += 1
            self.exploration_prob -= exploration_prob_decay
            new_game = connect_four.ConnectFour(self.game.board_size[0], self.game.board_size[1])
            self.reset(new_game)
            opponent.reset(new_game)
        print(f'draw: {stats[0]} ({stats[0] / num_games * 100}), P1 wins: {stats[1]} ({stats[1] / num_games * 100}),'
              f' P2 wins: {stats[2]} ({stats[2] / num_games * 100})')
        tree_file = open(f'AI Models/{tree_file_name}', 'wb')
        pickle.dump(self.complete_tree, tree_file)
        tree_file.close()

    def reset(self, game_instance: connect_four.ConnectFour) -> None:
        """Reset this player instance to play another game."""
        Player.reset(self, game_instance)
        self.curr_tree = self.complete_tree


class TrainingAgent(Player):
    """A class representing the training agent in Connect 4. This agent is able to read ahead one move."""
    def make_move(self) -> None:
        """Make a move in the current game.

        Preconditions:
        - 0 <= y < game.board_size[0] and 0 <= x < game.board_size[1]
        - (game.is_player_1_turn() and self.player_number == 1) or self.player_number == 2
        - the game is not finished
        """
        # First iteration, find immediate win
        # Second iteration, block immeidate win by opponent
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

        # Choose random action if no immediate win can be done or blocked
        random_move = random.choice(self.game.possible_moves)
        self.game.record_move(random_move[0], random_move[1])
