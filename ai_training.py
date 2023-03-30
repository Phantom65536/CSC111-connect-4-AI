"""Module for training AIPlayer instances and comparing performances."""
import doctest
from python_ta.contracts import check_contracts
import python_ta
import connect_four
from players import AIPlayer, RandomAgent


# @check_contracts
def train_p1_against_rand_p2(generate: bool = False) -> AIPlayer:
    """Train a P1 AI against a P2 RandomAgent and compare their performance.
    Return the trained/loaded P1 AI
    """
    # Train P1 AI against P2 RandomAgent
    g = connect_four.ConnectFour(5, 5)
    b = RandomAgent(g, 2)
    if generate:
        ai = AIPlayer(g, 1)
        ai.play_against(100000, b, True, '5x5_tree_randagent_P1')
    else:
        ai = AIPlayer(g, 1, '5x5_tree_randagent_P1')

    # Compare their performance
    ai.play_against(1000, b)

    return ai


# @check_contracts
def train_p2_against_rand_p1(generate: bool = False) -> AIPlayer:
    """Train a P2 AI against a P1 RandomAgent and compare their performance.
    Return trained/loaded P2 AI.
    """
    # Train P2 AI against P1 RandomAgent
    g = connect_four.ConnectFour(5, 5)
    b = RandomAgent(g, 1)
    if generate:
        ai = AIPlayer(g, 2)
        ai.play_against(200000, b, True, '5x5_tree_randagent_P2')
    else:
        ai = AIPlayer(g, 2, '5x5_tree_randagent_P2')

    # Compare their performance
    ai.play_against(1000, b)

    return ai


# @check_contracts
def compare_p1_p2_ai(p1_ai: AIPlayer, p2_ai: AIPlayer) -> None:
    """Compare performance between trained P1 and trained P2.

    Preconditions:
    - P1_ai.player_number == 1 and P2_ai.player_number == 2"""
    g = connect_four.ConnectFour(5, 5)
    p1_ai.reset(g)
    p2_ai.reset(g)
    p1_ai.play_against(1000, p2_ai)


# @check_contracts
def train_p2_ai_against_p1_ai(p1_ai: AIPlayer, generate: bool = False) -> AIPlayer:
    """Train a P2 AI against a trained & given P1 AI and compare their performance.
    Return retrained P2 AI.

    Preconditions:
    - P1_ai.player_number == 1 and P2_ai.player_number == 2
    - not generate or p2_ai is not None
    """
    # Train P2 AI against P1 AI
    g = connect_four.ConnectFour(5, 5)
    p1_ai.reset(g)
    if generate:
        p2_ai = AIPlayer(g, 2, '5x5_tree_randagent_P2')
        p2_ai.play_against(5000, p1_ai, True, '5x5_tree_rand+ai_P2')
    else:
        p2_ai = AIPlayer(g, 2, '5x5_tree_rand+ai_P2')

    # Compare their performance
    p2_ai.play_against(1000, p1_ai)

    return p2_ai


# @check_contracts
def short_demo() -> None:
    """A short demo to train a P1 AI against a P2 RandomAgent."""
    g = connect_four.ConnectFour(5, 5)
    ai = AIPlayer(g, 1)
    b = RandomAgent(g, 2)
    ai.play_against(10000, b, True, '5x5_tree_randagent_P1_demo')


# @check_contracts
def run_games() -> None:
    """Run training demo + see performance between different players"""

    # Perform short demo
    short_demo()

    # See performance between different Players
    # to train the AI models, change the parameters to True (for the last one just comment out the last statement)
    # WARNING: it takes ~30s for EACH of the AI models to be loaded
    ai1 = train_p1_against_rand_p2(False)
    ai2 = train_p2_against_rand_p1(False)
    compare_p1_p2_ai(ai1, ai2)
    train_p2_ai_against_p1_ai(ai1, False)


if __name__ == '__main__':
    doctest.testmod()
    python_ta.check_all(config={
        'extra-imports': ['players', 'connect_four'],
        'allowed-io': ['run_games'],  # the names (strs) of functions that call print/open/input
        'disable': ['too-many-nested-blocks'],
        'max-line-length': 120
    })
