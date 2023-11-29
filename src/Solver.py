from src.Node import Node
import math


class Solver():
    """Solver - Implements various algorithms for solving the Tic-Tac-Toe game.

    This class provides methods for evaluating game states, generating children nodes, and implementing minimax algorithms.

    Attributes:
        algorithm (str): The algorithm to be used for solving the game.

    Methods:
        __init__(algorithm="minimax"): Initializes the Solver object with the specified algorithm (default is "minimax").

        geometry(node: Node) -> int: Evaluates the game state and returns a score based on certain conditions.

        generate_children(node: Node, next_player: int): Generates child nodes for the given node based on available moves.

        minimax_algorithms(node: Node, depth: int, eval_max: bool): Invokes the specified minimax algorithm.

        minimax(node: Node, depth: int, eval_max: bool) -> int: Implements the minimax algorithm for game state evaluation.

        minimax_alpha_beta(node: Node, depth: int, alpha: float, beta: float, eval_max: bool) -> int:
            Implements the minimax algorithm with alpha-beta pruning for game state evaluation.
    """

    def __init__(self, algorithm="minimax"):
        """
        Initializes the Solver object with the specified algorithm (default is "minimax").

        Parameters:
            algorithm (str): The algorithm to be used for solving the game.

        Returns:
            None
        """
        self.algorithm = algorithm

    def geometry(self, node: Node) -> int:
        """
        Evaluates the game state and returns a score based on certain conditions.

        The winner earns 10 points, the player with the middle cell earns 5 points,
        and the player with a corner cell earns 3 points.

        Parameters:
            node (Node): The node representing the game state.

        Returns:
            int: The score based on the game state evaluation.
        """
        # the winner earn 10 points
        res = node.game.win() * 10

        # the player who has the middle earn 5 points
        res += node.game.board[1, 1] * 5

        # the player who has one corner earn 3 points
        res += node.game.board[0, 0] * 3
        res += node.game.board[0, 2] * 3
        res += node.game.board[2, 0] * 3
        res += node.game.board[2, 2] * 3

        return res

    def generate_children(self, node: Node, next_player: int):
        """
        Generates child nodes for the given node based on available moves.

        Parameters:
            node (Node): The node for which children nodes are to be generated.
            next_player (int): The player (1 or -1) making the next move.

        Returns:
            None
        """
        for i in range(3):
            for j in range(3):
                if node.game.board[i, j] == 0:
                    tmp = node.game.copy()
                    tmp.play((i, j), next_player)
                    node.children.append(Node(tmp, node, (i, j)))

    def minimax_algorithms(self, node: Node, depth: int, eval_max: bool) -> int:
        """
        Invokes the specified minimax algorithm.

        Parameters:
            node (Node): The node representing the current game state.
            depth (int): The depth of the search in the game tree.
            eval_max (bool): True if maximizing player's turn, False otherwise.

        Returns:
            None
        """
        if self.algorithm == "minimax":
            self.minimax(node, depth, eval_max)
        if self.algorithm == "minimax_alpha_beta":
            self.minimax_alpha_beta(node, depth, -math.inf, math.inf, eval_max)

    def minimax(self, node: Node, depth: int, evalMax: bool) -> int:
        """
        Implements the minimax algorithm for game state evaluation.

        Parameters:
            node (Node): The node representing the current game state.
            depth (int): The depth of the search in the game tree.
            eval_max (bool): True if maximizing player's turn, False otherwise.

        Returns:
            int: The evaluated score for the current game state.
        """
        if depth == 0 or node.game.win() or node.game.draw():
            return self.geometry(node)

        else:
            if evalMax:
                value = -math.inf
                for child in node.children:
                    value = max(value, self.minimax(child, depth-1, False))
            else:
                value = math.inf
                for child in node.children:
                    value = min(value, self.minimax(child, depth-1, True))

        return value

    def minimax_alpha_beta(self, node: Node, depth: int, alpha: float, beta: float, eval_max: bool) -> int:
        """
        Implements the minimax algorithm with alpha-beta pruning for game state evaluation.

        Parameters:
            node (Node): The node representing the current game state.
            depth (int): The depth of the search in the game tree.
            alpha (float): The alpha value for alpha-beta pruning.
            beta (float): The beta value for alpha-beta pruning.
            eval_max (bool): True if maximizing player's turn, False otherwise.

        Returns:
            int: The evaluated score for the current game state.
        """
        if depth == 0 or node.game.win() or node.game.draw():
            return self.geometry(node)

        if eval_max:
            value = -math.inf
            for child in node.children:
                value = max(value, self.minimax_alpha_beta(
                    child, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = math.inf
            for child in node.children:
                value = min(value, self.minimax_alpha_beta(
                    child, depth-1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value
