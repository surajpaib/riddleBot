import random
import sys
import numpy as np

class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    @staticmethod
    def distance_metric(vector1, vector2):
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

    def get_closest_snippet(self, snippet, position):
        distances = []
        for coord in snippet:
            distance = self.distance_metric(coord, position)
            distances.append(distance)

        min_index = np.argmin(distances)
        min_value = distances[int(min_index)]
        nearest_snippet = snippet[int(min_index)]
        return min_value, nearest_snippet

    def compare_best_choice(self, legal, new_distance, position, nearest_snippet):
        for (pos_addition, choice) in legal:
            pos = np.array(position) + np.array(pos_addition)
            possible_distance = self.distance_metric(nearest_snippet, pos)
            if new_distance <= possible_distance:
                return True

    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        #self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            snippet, position, opponent = self.get_grid()
            if snippet == []:
                (_, choice) = random.choice(legal)
                return choice
            min_value, nearest_snippet = self.get_closest_snippet(snippet, position)

            while 1:
                (pos_addition, choice) = random.choice(legal)
                pos = np.array(position) + np.array(pos_addition)
                new_distance = self.distance_metric(nearest_snippet, pos)
                if new_distance < min_value:
                    break
                else:
                    if self.compare_best_choice(legal, new_distance, position, nearest_snippet):
                        break

            return choice
