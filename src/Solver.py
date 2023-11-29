from src.Node import Node
import math


class Solver():

    def __init__(self, algorithm="minimax"):
        self.algorithm = algorithm

    def geometry(self, node: Node) -> int:
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
        for i in range(3):
            for j in range(3):
                if node.game.board[i, j] == 0:
                    tmp = node.game.copy()
                    tmp.play((i, j), next_player)
                    node.children.append(Node(tmp, node, (i, j)))

    def minimax_algorithms(self, node: Node, depth: int, eval_max: bool) -> int:
        if self.algorithm == "minimax":
            self.minimax(node, depth, eval_max)
        if self.algorithm == "minimax_alpha_beta":
            self.minimax_alpha_beta(node, depth, -math.inf, math.inf, eval_max)

    def minimax(self, node: Node, depth: int, evalMax: bool) -> int:
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
