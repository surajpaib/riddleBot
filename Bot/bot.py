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




    @staticmethod
    def set_distances(field2, field_height, field_width):

        distance = field2
        for idx in range(field_height):
            for idy in range(field_width):
                distance[idx][idy] = -1

        return distance

    @staticmethod
    def set_grid(field, field_height, field_width, my_pos):
        """
    
        :param field_height: 
        :param field_width: 
        :return: Prepare Grid and Distance objects for BFS 
        """
        grid = field
        for idx in range(field_height):
            for idy in range(field_width):
                if grid[idx][idy] == int(my_pos):
                    grid[idx][idy] = 2
                elif grid[idx][idy] == 3:
                    grid[idx][idy] = 0
                else:
                    grid[idx][idy] = 1
        return grid

    def get_grid(self):
        """
        
        :return: Current playing field value sent from Engine
        """
        field = self.game.field.cell
        [field_height, field_width] = self.game.field_height, self.game.field_width
        grid = self.set_grid(self.reshape(field, field_height, field_width), field_height, field_width, self.game.my_botid)
        distance = self.set_distances(self.reshape(field, field_height, field_width), field_height, field_width)
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

