from python_ta.contracts import check_contracts

GAME_START_MOVE = '*'


class GameTree:
    """A decision tree for Connect Four moves. Each node in the tree represents a move.

    Instance Attributes:
        - move: the current move (an x, y coordinate represented as a tuple), or '*' if this tree represents the start
                of a game
        - x: the width of the game board associated with this GameTree
        - y: the height of the game board associated with this GameTree

    Representation Invariants:
        - self.move == GAME_START_MOVE or self.move is a valid Connect Four move
        - all(key == self._subtrees[key].move for key in self._subtrees)
        - GAME_START_MOVE not in self._subtrees  # since it can only appear at the very top of a game tree
        - self.move[0] < x
        - self.move[1] < y
        - all(self.x == self._subtrees[key].x for key in self._subtrees)
        - all(self.y == self._subtrees[key].y for key in self._subtrees)
    """
    x: int
    y: int
    move: tuple[int, int]

    # Private Instance Attributes:
    #  - _subtrees:
    #      the subtrees of this tree, which represent the game trees after a possible
    #      move by the current player. It is a mapping where the keys
    #      are the move coordinates and the values are GameTrees.
    _subtrees: dict[str | tuple[str, ...], GameTree]

    def __init__(self, x: int, y: int, move: tuple[int, int] = GAME_START_MOVE) -> None:
        """Initialize a new game tree.

        >>> game = GameTree()
        >>> game.move == GAME_START_MOVE
        True
        """
        self.x = x
        self.y = y
        self.move = move
        self._subtrees = {}

    def get_subtrees(self) -> list[GameTree]:
        """Return the subtrees of this game tree."""
        return list(self._subtrees.values())

    def add_subtree(self, subtree: GameTree) -> None:
        """Add a subtree to this game tree."""
        self._subtrees[subtree.move] = subtree

    def find_subtree_by_move(self, move: str | tuple[str, ...]) -> Optional[GameTree]:
        """Return the subtree corresponding to the given move.

        Return None if no subtree corresponds to that move.
        """
        if move in self._subtrees:
            return self._subtrees[move]
        else:
            return None
