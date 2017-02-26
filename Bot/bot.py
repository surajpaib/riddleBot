import random
import math

UP, DOWN, LEFT, RIGHT = [(-1, 0), (1, 0), (0, -1), (0, 1)]
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
                # if field[idx][idy] == 5:
                #     weapon_loc = [idx, idy]
                # if field[idx][idy] == 4:
                #     bug_loc = [idx, idy]

        return field, snippet_loc, my_loc, opponent_loc

    @staticmethod
    def add(list1, list2):
        idx = list1[0] + list2[0]
        idy = list1[1] + list2[1]

        return [idx, idy]

    @staticmethod
    def sub(list1, list2):
        idx = list1[0] - list2[0]
        idy = list1[1] - list2[1]

        return [idx, idy]

    # def get_closest_snippet(self, snippet, position):
    #     distances = []
    #     for coord in snippet:
    #         distance = self.distance_metric(coord, position)
    #         distances.append(distance)
    #
    #     min_index, min_value = self.argmin(distances)
    #     nearest_snippet = snippet[min_index]
    #     return min_value, nearest_snippet
    #
    # def compare_best_choice(self, legal, new_distance, position, nearest_snippet):
    #     for (pos_addition, choice) in legal:
    #         pos = self.add(list(position), list(pos_addition))
    #         possible_distance = self.distance_metric(nearest_snippet, pos)
    #         if new_distance <= possible_distance:
    #             return True

    def fallback_move(self, legal):
        if (self.snippet is None) & (self.weapon is None) & (self.bug is None):
            (_, choice) = random.choice(legal)
            self.game.issue_order(choice)
            return True

    def next_move(self, my_pos, hop):
        moves = []
        field = self.field
        up = self.add(my_pos, UP)
        if field[up[0]][up[1]] != 3:
            moves.append(up)
        down = self.add(my_pos, DOWN)
        if field[down[0]][down[1]] != 3:
            moves.append(down)
        left = self.add(my_pos, LEFT)
        if field[left[0]][left[1]] != 3:
            moves.append(left)
        right = self.add(my_pos, RIGHT)
        if field[right[0]][right[1]] != 3:
            moves.append(right)

        hop += 1
        return moves, hop

    def possible_paths(self, moves, hop, path) :
        for move in moves:
            path.append(move)
            if self.field[move[0]][move[1]] == 6 or self.field[move[0]][move[1]] == 5:
                if self.snippet_path is not None:
                    for snippet in self.snippet_path:
                        if snippet == path:
                            path = []
                            hop = 0
                            continue
                self.snippet_path.append(path)
                self.snippet_hop.append(hop)
                path = []
                hop = 0
            if len(path) >= 3:
                if (path[-1] == path[-3]):
                    path.remove(path[-1])
                    hop -= 1
                    continue
            moves, hop = self.next_move(move, hop)
            if len(moves) != 0:
                for move in moves:
            else:
                path.remove(object=path[-1])
                hop -= 1

    def shortest_path_algorithm(self, my_pos, snippet, weapon, bug):
        field = self.field
        hop = 0
        path = []
        moves, hop = self.next_move(my_pos, hop) # State 0 - Moves around my position
        self.possible_paths(moves, hop, path)
        index, min_hop = self.argmin(self.snippet_hop)
        shortest_path = self.snippet_path[index]
        choice = self.sub(shortest_path[0], my_pos)
        return choice


    def do_turn(self):
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        #self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
            return
        self.field, self.snippet, self.my_pos, self.opponent = self.get_grid()
        if self.fallback_move(legal) is True:
            return
        choice = self.shortest_path_algorithm(self.my_pos, self.snippet, self.weapon, self.bug)
        self.game.issue_order(choice)
