"""Contains different Player classes."""

from __future__ import annotations

import doctest
from python_ta.contracts import check_contracts
import python_ta

import random
import connect_four
from typing import Optional
from game_tree import GameTree
import pickle
import graphplot


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
        - game_instancee is a beginning game state
        """
        self.player_number = player_number
        self.game = game_instance

    def make_move(self) -> None:
        """Make a move in the current game.

        Preconditions:
        - (game.is_player_1_turn() and self.player_number == 1) or self.player_number == 2
        - the game is not finished
        """
        raise NotImplementedError

    def reset(self, game_instance: connect_four.ConnectFour) -> None:
        """Reset this player instance to play another game"""
        self.game = game_instance


# @check_contracts
class HumanPlayer(Player):
    """A class representing a human player as self.player_number"""
    def make_move(self, y: int = 0, x: int = 0) -> None:
        """Make a move in the current game.

        Preconditions:
        - 0 <= y < game.board_size[0] and 0 <= x < game.board_size[1]
        - (game.is_player_1_turn() and self.player_number == 1) or self.player_number == 2
        - the game is not finished
        """
        self.game.record_move(y, x)


# @check_contracts
class AIPlayer(Player):
    """A class representing the AI agent with q-learning player as self.player_number.

    Instance Attributes:
    - complete_tree: Saves the complete GameTree associated to this AIPlayer instance
    - curr_tree: current subtree/position in complete_tree
    - initial_q_val: the initial q-value of a state-action pair when the state (depicted by a GameTree instance) has just been initialized
    - reward: the value of the reward when AIAgent wins a game

    Representation Invariants:
    - self.reward > 0
    - self.curr_tree == self.complete_tree or self.curr_tree is a descendant of self.complete_tree
    """
    complete_tree: GameTree
    curr_tree: Optional[GameTree]

    initial_q_val: float = 0.0
    reward: float = 10

    def __init__(self, game_instance: connect_four.ConnectFour, player_number: int,
                 tree_file: Optional[str] = None) -> None:
        """Initialize the AI and possibly retrieve an existing GameTree from tree_file

        Preconditions:
        - tree_file is a binary file which can be retrieved by pickle.load()
        - game_instance is a beginning game state
        - player_number in {1, 2}
        """
        Player.__init__(self, game_instance, player_number)
        if tree_file is not None:
            tree_file_handler = open(f'AI Models/{tree_file}', 'rb')
            self.complete_tree = pickle.load(tree_file_handler)
            tree_file_handler.close()
        else:
            self.complete_tree = GameTree(game_instance, self.initial_q_val, self.reward)
        self.curr_tree = self.complete_tree

    def make_move(self, training: bool = False, explore_rate: float = 0.0) -> None:
        """Make a move.

        Preconditions:
        - (game.is_player_1_turn() and self.player_number == 1) or self.player_number == 2
        - the game is not finished
        """

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
        if self.curr_tree is None or self.curr_tree.get_subtrees() == {} or (training and explore_num < explore_rate):
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

    def play_against(self, num_games: int, opponent: Player, train: bool = False, tree_file_name: Optional[str] = None,
                     learning_rate: float = 0.2, discount: float = 0.9, max_explore_rate: float = 1.0,
                     min_explore_rate: float = 0.0) -> None:
        """Train self to play as self.player_number by playing num_games times with opponent.
        If AI is under training, exploration rate decreases linearly from max_explore_rate to min_explore_rate.
        Learning_rate and discount are parameters in q-learning.

        Preconditions:
        - opponent.player_number != self.player_number
        - opponent able to choose a move itself/automatically
        - num_games > 0
        - not train or tree_file_name is not None
        """
        explore_rate = max_explore_rate
        exploration_prob_decay = (max_explore_rate - min_explore_rate) / num_games
        results = []
        stats = {0: 0, 1: 0, 2: 0}
        for _ in range(num_games):
            if self.player_number == 1:
                while self.game.get_winner() is None:
                    self.make_move(train, explore_rate)
                    if self.game.get_winner() is not None:
                        break
                    opponent.make_move()
                winner = self.game.get_winner()
                if train:
                    self.complete_tree.update_q_tables(self.game.move_sequence, 1, winner, learning_rate, discount)
            else:
                while self.game.get_winner() is None:
                    opponent.make_move()
                    if self.game.get_winner() is not None:
                        break
                    self.make_move(train, explore_rate)
                winner = self.game.get_winner()
                if train:
                    self.complete_tree.get_subtrees()[self.game.move_sequence[0]].\
                        update_q_tables(self.game.move_sequence, 2, winner, learning_rate, discount, 1)
            results.append(winner)
            stats[winner] += 1
            explore_rate -= exploration_prob_decay
            new_game = connect_four.ConnectFour(self.game.board_size[0], self.game.board_size[1])
            self.reset(new_game)
            opponent.reset(new_game)
        print(f'draw: {stats[0]} ({stats[0] / num_games * 100}), P1 wins: {stats[1]} ({stats[1] / num_games * 100}),'
              f' P2 wins: {stats[2]} ({stats[2] / num_games * 100})')
        graph = graphplot.GraphPlot(results, self.player_number)
        graph.plot_game_stats()
        if train:
            tree_file = open(f'AI Models/{tree_file_name}', 'wb')
            pickle.dump(self.complete_tree, tree_file)
            tree_file.close()

    def reset(self, game_instance: connect_four.ConnectFour) -> None:
        """Reset this player instance to play another game."""
        Player.reset(self, game_instance)
        self.curr_tree = self.complete_tree


# @check_contracts
class RandomAgent(Player):
    """A class representing an agent in Connect 4 who is entirely random."""
    def make_move(self) -> None:
        """Make a move in the current game.

        Preconditions:
        - (game.is_player_1_turn() and self.player_number == 1) or self.player_number == 2
        - the game is not finished
        """
        random_move = random.choice(self.game.possible_moves)
        self.game.record_move(random_move[0], random_move[1])


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['random', 'connect_four', 'game_tree', 'graphplot', 'pickle'],
        'disable': ['too-many-nested-blocks', 'too-many-locals', 'too-many-arguments', 'wrong-import-order',
                    'forbidden-IO-function', 'consider-using-with'],
        'max-line-length': 150
    })
