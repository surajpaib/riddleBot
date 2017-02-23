import random
import sys


class Bot:

    def __init__(self):
        self.game = None
        self.previous = None
        self.opp = {
            "left" : "right",
            "right" : "left",
            "up" : "down",
            "down" : "up"
        }
        self.repeat_count = 0

    def setup(self, game):
        self.game = game

    def repeat_previous_move(self, legal):
        if self.previous is None:
            (_, choice) = random.choice(legal)
            return choice

        elif self.repeat_count <= 3:
            last_move = self.previous
            for ((row, col), move) in legal:
                if last_move == move:
                    self.repeat_count += 1
                    return last_move
        self.repeat_count = 0

        (_, choice) = random.choice(legal)
        return choice

    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        #self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            choice = self.repeat_previous_move(legal)
            self.previous = choice
            self.game.issue_order(choice)


