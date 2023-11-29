class Node():

    def __init__(self, game, parent, last_move):
        self.game = game
        self.children = []
        self.parent = parent
        self.last_move = last_move
