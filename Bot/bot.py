import random
import sys


class Bot:

    def __init__(self):
        self.game = None
        self.previous = None

    def setup(self, game):
        self.game = game

    def repeat_previous_move(self, legal):
        if self.previous is None:
            (_, choice) = random.choice(legal)
            self.previous.append(choice)
            return choice

        else:
            last_move = self.previous
            for ((row, col), move) in legal:
                if last_move == move:
                    return last_move

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


