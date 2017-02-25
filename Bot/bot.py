import random
import math

class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    @staticmethod
    def distance_metric(vector1, vector2):
        vertical_d = abs(vector1[0] - vector2[0])
        horizontal_d = abs(vector1[1] - vector2[1])
        distance = abs(vertical_d + horizontal_d)
        return distance

    @staticmethod
    def argmin(array):
        global index
        new_array = sorted(array)
        min_value = new_array[0]

        for i in range(len(array)):
            if min_value == array[i]:
                index = i
        return index

    @staticmethod
    def reshape(list1, height, width):
        array = []
        for h in range(height):
            array_inner = []
            for w in range(width):
                array_inner.append(list1[h][w][0])
            array.append(array_inner)

        return array

    def get_grid(self):
        global opponent_loc
        global my_loc
        field = self.game.field.cell
        [field_height, field_width] = self.game.field_height, self.game.field_width
        field = self.reshape(field, field_height, field_width)
        snippet_loc = []
        for idx in range(field_height):
            for idy in range(field_width):
                if field[idx][idy] == 6:
                    snippet_loc.append([idx, idy])
                if field[idx][idy] == int(self.game.my_botid):
                    my_loc = [idx, idy]
                if field[idx][idy] == int(self.game.other_botid):
                    opponent_loc = [idx, idy]

        return snippet_loc, my_loc, opponent_loc

    @staticmethod
    def add(list1, list2):
        idx = list1[0] + list2[0]
        idy = list1[1] + list2[1]

        return [idx, idy]

    def get_closest_snippet(self, snippet, position):
        distances = []
        for coord in snippet:
            distance = self.distance_metric(coord, position)
            distances.append(distance)

        min_index = self.argmin(distances)
        min_value = distances[int(min_index)]
        nearest_snippet = snippet[int(min_index)]
        return min_value, nearest_snippet

    def compare_best_choice(self, legal, new_distance, position, nearest_snippet):
        for (pos_addition, choice) in legal:
            pos = self.add(list(position), list(pos_addition))
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
                self.game.issue_order(choice)
                return
            min_value, nearest_snippet = self.get_closest_snippet(snippet, position)

            while 1:
                (pos_addition, choice) = random.choice(legal)
                pos = self.add(list(position), list(pos_addition))
                new_distance = self.distance_metric(nearest_snippet, pos)
                if new_distance <= min_value:
                    break
                else:
                    if self.compare_best_choice(legal, new_distance, position, nearest_snippet):
                        break

            self.game.issue_order(choice)
