"""
Bot actions 
"""
import random

UP, DOWN, LEFT, RIGHT = [[-1, 0], [1, 0], [0, -1], [0, 1]]
directions ={
    "[-1, 0]" : "up",
    "[1, 0]" : "down",
    "[0, -1]" : "left",
    "[0, 1]" : "right"
}


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
        self.mypos = None
        self.snippetpos = []
        self.bugs = []


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

    def get_positions(self, field, field_height, field_width):
        for idx in range(field_height):
            for idy in range(field_width):
                if field[idx][idy] == int(self.game.my_botid):
                    self.mypos = [idx, idy]
                elif (field[idx][idy] == 6) or (field[idx][idy] == 5):
                    self.snippetpos.append([idx, idy])
                elif field[idx][idy] == 4:
                    self.bugs.append([idx, idy])

    @staticmethod
    def set_distances(field, field_height, field_width):

        distance = field
        for idx in range(field_height):
            for idy in range(field_width):
                distance[idx][idy] = -1

        return distance

    @staticmethod
    def add(array1, array2):
        array_idx = array1[0] + array2[0]
        array_idy = array1[1] + array2[1]

        return [array_idx, array_idy]

    @staticmethod
    def set_grid(field, field_height, field_width, my_pos):
        """
    
        :param field_height: 
        :param field_width: 
        :return: Prepare Grid object for BFS 
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
        field = self.reshape(field, field_height, field_width)
        return field, grid, distance

    def breadth_first_search(self, mypos, grid, distance):
        iterator = Iterator()
        iterator.enqueue(mypos)
        distance[mypos[0]][mypos[1]] = 0
        grid[mypos[0]][mypos[1]] = 2

        while not iterator.isEmpty():
            position = iterator.dequeue()

            for i in [-1, 0, 1]:
                for j in [-1, 0 , 1]:
                    if abs(i) == abs(j):
                        continue
                    new_pos = self.add(position, [i, j])
                    if new_pos[0] < 0:
                        new_pos[0] = 0
                    elif new_pos[0] > int(self.game.field_height - 1):
                        new_pos[0] = int(self.game.field_height - 1)
                    if new_pos[1] < 0:
                        new_pos[1] = 0
                    elif new_pos[1] > int(self.game.field_width - 1):
                        new_pos[1] = int(self.game.field_width - 1)

                    if new_pos == position:
                        continue

                    if (distance[int(new_pos[0])][int(new_pos[1])]) == -1:
                        if grid[new_pos[0]][new_pos[1]] != 0:
                            distance[new_pos[0]][new_pos[1]] = distance[position[0]][position[1]] + 1
                            iterator.enqueue(new_pos)
        return distance

    def get_closest_event(self, distance, event):
        event_distances = []
        for snipp in event:
            event_distances.append(distance[snipp[0]][snipp[1]])

        closest_distance = min(event_distances)
        for i, dist in enumerate(event_distances):
            if closest_distance == dist:
                closest_event = event[i]
                break
        return closest_event, closest_distance

    def execute_next_move(self, distance, grid):
            closest_snippet, closest_distance = self.get_closest_event(distance, self.snippetpos)
            possible_moves = self.game.field.legal_moves(self.game.my_botid, self.game.players)

            for move in UP, DOWN, LEFT, RIGHT:
                # Check if the move is legal before running next move algorithm
                legal = 0
                for legal_move in possible_moves:
                    if move == list(legal_move[0]):

                        legal = 1
                if legal != 1:
                    continue
                new_position = self.add(self.mypos, move)
                # Get field, grid and distance f``rom start
                field, grid, distance = self.get_grid()
                # Set new position as my current position
                distance[self.mypos[0]][self.mypos[1]] = -1
                grid[self.mypos[0]][self.mypos[1]] = 0
                # Run BFS on the new position
                distance = self.breadth_first_search(new_position, grid, distance)
                (_, new_closest_distance) = self.get_closest_event(distance, self.snippetpos)
                if new_closest_distance < closest_distance:
                    return move

    def evade_bugs(self, distance, grid):
        closest_bug, closest_distance = self.get_closest_event(distance, self.bugs)
        possible_moves = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        if closest_distance > 2:
            return

        for move in UP, DOWN, LEFT, RIGHT:

            # Check if the move is legal before running next move algorithm
            legal = 0
            for legal_move in possible_moves:
                if move == list(legal_move[0]):
                    legal = 1
            if legal != 1:
                continue
            new_position = self.add(self.mypos, move)
            # Get field, grid and distance f``rom start
            field, grid, distance = self.get_grid()
            # Set new position as my current position
            distance[self.mypos[0]][self.mypos[1]] = -1
            grid[self.mypos[0]][self.mypos[1]] = 0
            # Run BFS on the new position
            distance = self.breadth_first_search(new_position, grid, distance)
            (_, new_closest_distance) = self.get_closest_event(distance, self.bugs)
            if new_closest_distance >= closest_distance:
                return move

    def do_turn(self):
        """
        
        :return: Play a turn of the game
        """
        self.snippetpos = []
        self.bugs = []
        self.mypos = None
        legal = self.game.field.legal_moves(self.game.my_botid, self.game.players)
        #self.game.field.output()
        if len(legal) == 0:
            self.game.issue_order_pass()
        else:
            field, grid, distance = self.get_grid()
            self.get_positions(field, self.game.field_height, self.game.field_width)

            # No snippet fallback
            if self.snippetpos == []:
                (_, choice) = random.choice(legal)
                self.game.issue_order(choice)
                return

            distance = self.breadth_first_search(self.mypos, grid, distance)

            if self.bugs != []:
                choice = self.evade_bugs(distance, grid)
                if choice is not None:
                    self.game.issue_order(directions[str(choice)])
                    return

            choice = self.execute_next_move(distance, grid)
            if choice is not None:
                self.game.issue_order(directions[str(choice)])
            else:
                self.game.issue_order_pass()
