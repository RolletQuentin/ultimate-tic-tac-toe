class Node():
    """Node - Represents a node in the game tree for the Tic-Tac-Toe AI.

    Each node contains information about the game state, its parent node, and the last move made to reach this state.

    Attributes:
        game (TicTacToe): The TicTacToe object representing the game state.
        children (list): List of child nodes in the game tree.
        parent (Node): The parent node in the game tree.
        last_move (tuple): The last move made to reach this game state, represented as (row, column).

    Methods:
        None
    """

    def __init__(self, game, parent, last_move):
        """
        Initializes a Node object in the game tree.

        Parameters:
            game (TicTacToe): The TicTacToe object representing the game state.
            parent (Node): The parent node in the game tree.
            last_move (tuple): The last move made to reach this game state, represented as (row, column).

        Returns:
            None
        """
        self.game = game
        self.children = []
        self.parent = parent
        self.last_move = last_move
