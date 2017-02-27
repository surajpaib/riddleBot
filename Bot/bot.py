import random
import math

UP, DOWN, LEFT, RIGHT = [(-1, 0), (1, 0), (0, -1), (0, 1)]

class Iterator:
    def __init__(self):
        self.fields = []

    def isEmpty(self):
        return self.fields == []

    def enqueue(self, item):
        self.fields.insert(0, item)

    def dequeue(self):
        return self.fields.pop()

    def size(self):
        return len(self.fields)

class Bot:

    def __init__(self):
        self.game = None
        self.field = None
        self.snippet = None
        self.weapon = None
        self.bug = None
        self.my_pos = None
        self.opponent = None
        self.snippet_path = []
        self.snippet_hop = []

    def setup(self, game):
        self.game = game

    @staticmethod
    def reshape(list1, height, width):
        array = []
        for h in range(height):
            array_inner = []
            for w in range(width):
                array_inner.append(list1[h][w][0])
            array.append(array_inner)

        return array

    def set_grid_and_distances(self, field_height, field_width):
        grid = self.field
        distance = self.field
        for idx in range(field_height):
            for idy in range(field_width):
                # Set initial distance to -1
                distance[idx][idy] = -1

                if self.field[idx][idy] == int(self.game.my_botid):
                    grid[idx][idy] = 2
                if self.field[idx][idy] == 3:
                    grid[idx][idy] = 0
                else:
                    grid[idx][idy] = 1

        return grid, distance

    def get_grid(self):
        """
        
        :return: Current playing field value sent from Engine
        """
        global opponent_loc
        global my_loc
        field = self.game.field.cell
        [field_height, field_width] = self.game.field_height, self.game.field_width
        self.field = self.reshape(field, field_height, field_width)
        [grid, distance] = self.set_grid_and_distances(field_height, field_width)
        print(grid, distance)

    def do_turn(self):
        """
        
        :return: Play a turn of the game
        """
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        #self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            self.get_grid()

