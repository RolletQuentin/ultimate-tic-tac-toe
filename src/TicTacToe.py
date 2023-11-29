import numpy as np
import math
from src.Solver import Solver
from src.Node import Node


class TicTacToe():
    """TicTacToe - Simple implementation of a Tic-Tac-Toe game in Python using NumPy.

    This class represents a Tic-Tac-Toe game board with a 3x3 grid. Each cell on the board can be in one of three states: 
    - Empty, represented by 0.
    - Player 1, represented by -1.
    - Player 2, represented by 1.

    The game provides methods for making a move, checking for a winner, checking for a draw, and displaying the current state of the board.

    Attributes:
        board (numpy.ndarray): A 3x3 NumPy array representing the Tic-Tac-Toe board.

    Methods:
        __init__(): Initializes the TicTacToe object with an empty 3x3 board.

        __str__(): Returns a string representation of the current state of the Tic-Tac-Toe board.

        play(position, player): Makes a move on the board at the specified position for the given player.

        win(): Checks for a winner on the current board. Returns the player number (0 or 1) if there is a winner, otherwise returns -1.

        draw(): Checks if the game is a draw. Returns True if the board is full and there is no winner, otherwise returns False.
    """

    def __init__(self, board=None):
        """
        Initializes the TicTacToe object with an empty 3x3 board.

        The board is represented as a NumPy array, where each cell is initialized to -1.

        Parameters:
            None

        Returns:
            None
        """
        if board is None:
            self.board = np.zeros((3, 3))
        else:
            self.board = board

    def __str__(self) -> str:
        """
        Returns a string representation of the current state of the Tic-Tac-Toe board.

        The board is displayed as a 3x3 grid with each cell represented by 'O' (Player 0), 'X' (Player 1),
        or a space (' ') for an empty cell. Rows and columns are separated by vertical and horizontal lines.

        Parameters:
            None

        Returns:
            str: String representation of the current state of the Tic-Tac-Toe board.
        """

        horizontal_line = "-----------\n"
        result = ""

        for i in range(3):
            # Replace 0 with space
            row_str = " " + " | ".join(" " if x == 0 else ("O" if x == 1 else "X")
                                       for x in self.board[i]) + "\n"
            result += row_str

            if i != 2:
                result += horizontal_line

        return result

    def copy(self):
        return TicTacToe(self.board.copy())

    def play(self, position, player) -> int:
        """
        Makes a move on the board at the specified position for the given player.

        If the specified position is empty, the player's symbol is placed in that position,
        and the player number (-1 or 1) is returned. If the position is already occupied,
        0 is returned, indicating an invalid move.

        Parameters:
            position (tuple): A tuple representing the (row, column) position on the board.
            player (int): The player making the move (-1 or 1).

        Returns:
            int: Player number (0 or 1) if the move is valid, -1 if the move is invalid.
        """

        i, j = position

        match self.board[i, j]:
            case 0:
                self.board[i, j] = player
                return player
            case _:
                return 0

    def win(self) -> int:
        """
        Checks for a winner on the current board.

        Checks for a winner in the rows, columns, and diagonals. Returns the player number (-1 or 1)
        if there is a winner, otherwise returns 0.

        Parameters:
            None

        Returns:
            int: Player number (-1 or 1) if there is a winner, 0 if there is no winner.
        """

        # check rows
        for j in range(3):
            player = self.board[0, j]
            if player != 0:
                win = True
                for i in range(1, 3):
                    if self.board[i, j] != player:
                        win = False
                if win:
                    return player

        # check columns
        for i in range(3):
            player = self.board[i, 0]
            if player != 0:
                win = True
                for j in range(1, 3):
                    if self.board[i, j] != player:
                        win = False
                if win:
                    return player

        # check diag
        if self.board[0, 0] != 0 and self.board[0, 0] == self.board[1, 1] == self.board[2, 2]:
            return self.board[0, 0]

        # check anti-diag
        if self.board[0, 2] != 0 and self.board[0, 2] == self.board[1, 1] == self.board[2, 0]:
            return self.board[0, 2]

        return 0

    def draw(self) -> bool:
        """
        Checks if the game is a draw.

        Returns True if the board is full and there is no winner, indicating a draw.
        Returns False if there are still empty cells or if there is a winner.

        Parameters:
            None

        Returns:
            bool: True if the game is a draw, False otherwise.
        """

        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    return False

        return True

    def play_with_ai(self):

        print("Welcome to Tic-Tac-Toe against the AI!")

        while not self.draw() and self.win() == 0:
            print(self)
            player_move = self.get_player_move()
            self.play(player_move, -1)  # Assume player is alaways -1
            print(f"\nPlayer move:\n{self}")

            if not self.draw() and self.win() == 0:
                print("AI is making a move...")
                ai_move = self.get_ai_move()
                self.play(ai_move, 1)
                print(f"\nAI move:\n{self}")

        winner = self.win()
        if winner == 0:
            print("It's a draw!")
        elif winner == -1:
            print("The Player wins!")
        else:
            print("The AI wins!")

    def get_player_move(self):

        try:
            row = int(input("Enter the row (0, 1, or 2): "))
            col = int(input("Enter the column (0, 1, or 2): "))
            if 0 <= row <= 2 and 0 <= col <= 2 and self.board[row, col] == 0:
                return row, col
            else:
                print("Invalid move. Try again.")
                return self.get_player_move()
        except ValueError:
            print("Invalid input. Please enter a number.")
            return self.get_player_move()

    def get_ai_move(self):
        ai = Solver("minimax_alpha_beta")
        root = Node(self, None, None)

        # generate the game tree
        ai.generate_children(root, 1)
        for node in root.children:
            ai.generate_children(node, -1)
            for child_node in node.children:
                ai.generate_children(child_node, 1)

        best_value = -math.inf
        best_move = None

        for child in root.children:
            value = ai.minimax(child, 2, False)
            if value > best_value:
                best_value = value
                best_move = child.last_move

        return best_move


if __name__ == "__main__":
    tictactoe = TicTacToe()
    tictactoe.play((0, 0), -1)
    tictactoe.play((0, 1), 1)
    tictactoe.play((1, 1), -1)
    tictactoe.play((0, 2), 1)
    print(tictactoe.win())
    tictactoe.play((2, 2), -1)
    print(tictactoe.draw())
    print(tictactoe)
