import random
import math

UP, DOWN, LEFT, RIGHT = [[-1, 0], [1, 0], [0, -1], [0, 1]]
class Bot:

    def __init__(self):
        self.game = None

    def setup(self, game):
        self.game = game

    @staticmethod
    def distance_metric(vector1, vector2):


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
                if field[idx][idy] == 5:
                    weapon_loc = [idx, idy]
                if field[idx][idy] == 4:
                    bug_loc = [idx, idy]

        return field, snippet_loc, my_loc, opponent_loc, weapon_loc, bug_loc

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

    def fallback_move(self, legal, snippet, weapon, bug):
        if snippet is None & weapon is None & bug is None:
            (_, choice) = random.choice(legal)
            self.game.issue_order(choice)
            return True

    def next_move(self, my_pos, field, hop):
        moves = []
        with self.add(my_pos, UP) as up:
            if field[up] != 3:
                moves.append(up)

        with self.add(my_pos, DOWN) as down:
            if field[down] != 3:
                moves.append(down)
        with self.add(my_pos, LEFT) as left:
            if field[left] != 3:
                moves.append(left)
        with self.add(my_pos, RIGHT) as right:
            if field[right] != 3:
                moves.append(right)
        hop += 1
        return moves

    def shortest_path_alogrithm(self, field, my_pos, snippet, weapon, bug):
        hop = 0
        moves = self.next_move(my_pos, field, hop)
        for move in moves:
            


    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        #self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
            return
        field, snippet, my_pos, opponent, weapon, bug = self.get_grid()
        if self.fallback_move(legal, snippet, weapon, bug) is True:
            return

        self.shortest_path_algoirthm(field, my_pos, snippet, weapon, bug)

        min_value, nearest_snippet = self.get_closest_snippet(snippet, my_position)
        choice = self.pick_best_move(legal, my_position, nearest_snippet)
        self.game.issue_order(choice)
