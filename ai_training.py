import connect_four
from players import AIPlayer, RandomAgent


def train_p1_against_rand_p2(generate: bool = False) -> None:
    """Train a P1 AI against a P2 RandomAgent and compare their performance."""
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


def train_p2_against_rand_p1(generate: bool = False) -> None:
    """Train a P2 AI against a P1 RandomAgent and compare their performance."""
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


def compare_p1_p2_ai() -> None:
    """Compare performance between trained P1 and trained P2."""
    g = connect_four.ConnectFour(5, 5)
    ai1 = AIPlayer(g, 1, '5x5_tree_randagent_P1')
    ai2 = AIPlayer(g, 2, '5x5_tree_randagent_P2')
    ai1.play_against(1000, ai2)


def train_p2_ai_against_p1_ai(generate: bool = False) -> None:
    """Train a P2 AI against a P1 AI and compare their performance."""
    # Train P2 AI against P1 AI
    g = connect_four.ConnectFour(5, 5)
    ai1 = AIPlayer(g, 1, '5x5_tree_randagent_P1')
    if generate:
        ai2 = AIPlayer(g, 2, '5x5_tree_randagent_P2')
        ai2.play_against(5000, ai1, True, '5x5_tree_rand+ai_P2')
    else:
        ai2 = AIPlayer(g, 2, '5x5_tree_rand+ai_P2')

    # Compare their performance
    ai2.play_against(1000, ai1)


def short_demo() -> None:
    """A short demo to train a P1 AI against a P2 RandomAgent."""
    g = connect_four.ConnectFour(5, 5)
    ai = AIPlayer(g, 1)
    b = RandomAgent(g, 2)
    ai.play_against(10000, b, True, '5x5_tree_randagent_P1_demo')


if __name__ == '__main__':
    # Perform short demo
    short_demo()

    # See performance between different Players
    # to train the AI models, change the parameters to True
    # WARNING: it takes ~30s for EACH of the AI models to be loaded
    train_p1_against_rand_p2(False)
    train_p2_against_rand_p1(False)
    compare_p1_p2_ai()
    train_p2_ai_against_p1_ai(False)
