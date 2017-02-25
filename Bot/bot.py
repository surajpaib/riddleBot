import random
import math

class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    @staticmethod
    def distance_metric(vector1, vector2):
        vect1_mag = math.sqrt(vector1[0]**2 + vector1[1]**2)
        vect2_mag = math.sqrt(vector2[0]**2 + vector2[1]**2)
        distance = abs(vect1_mag + vect2_mag)
        return distance

    @staticmethod
    def argmin(array):
        global index
        new_array = sorted(array)
        min_value = new_array[0]

        for i in range(len(array)):
            if min_value == array[i]:
                index = i
        return index, min_value

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

        min_index, min_value = self.argmin(distances)
        nearest_snippet = snippet[min_index]
        return min_value, nearest_snippet

    def compare_best_choice(self, legal, new_distance, position, nearest_snippet):
        for (pos_addition, choice) in legal:
            pos = self.add(list(position), list(pos_addition))
            possible_distance = self.distance_metric(nearest_snippet, pos)
            if new_distance <= possible_distance:
                return True

    def pick_best_move(self,legal, my_position, nearest_snippet_location):
        distances_from_snippet = []
        for (direction_coord, direction) in legal:
            new_coordinates = self.add(my_position, direction_coord)
            distances_from_snippet.append(self.distance_metric(new_coordinates, nearest_snippet_location))

        index, distance_min = self.argmin(distances_from_snippet)
        (_, choice) = legal[index]
        return choice

    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        #self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            snippet, my_position, opponent = self.get_grid()
            if snippet is None:
                (_, choice) = random.choice(legal)
                self.game.issue_order(choice)
                return
            min_value, nearest_snippet = self.get_closest_snippet(snippet, my_position)
            choice = self.pick_best_move(legal, my_position, nearest_snippet)
            self.game.issue_order(choice)
