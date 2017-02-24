import random
import sys
import numpy as np

class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def distance_metric(self, vector1 , vector2):
        vector1mag = np.sqrt(vector1[0] ** 2 + vector1[1] ** 2)
        vector2mag = np.sqrt(vector2[0] ** 2 + vector2[1] ** 2)
        distance = np.abs(vector1mag - vector2mag)
        return distance

    def get_grid(self):
        global opponent_loc
        global my_loc
        field = np.array(self.game.field.cell)
        [field_height, field_width] = self.game.field_height, self.game.field_width
        field = np.reshape(field, (field_height, field_width))
        print field
        snippet_loc = []
        for idx in range(field_height):
            for idy in range(field_width):
                if field[idx][idy] == 6 :
                    snippet_loc.append([idx, idy])
                if field[idx][idy] == int(self.game.my_botid) :
                    my_loc = [idx, idy]
                if field[idx][idy] == int(self.game.other_botid) :
                    opponent_loc = [idx, idy]

        return snippet_loc, my_loc, opponent_loc



    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        #self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            snippet, position, opponent = self.get_grid()
            print snippet
            print position
            for coord in snippet:
                similarity = self.distance_metric(coord, position)



