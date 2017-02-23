import random
import sys
import numpy as np


class Bot:


    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    def mimic_opponent(self):
        [height, width] = self.game.field_height, self.game.field_width
        field = self.game.field
        field = np.reshape(field, (height, width))
	
    def do_turn(self):


        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        #self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            (_, choice) = random.choice(legal)
            self.game.issue_order(choice)

