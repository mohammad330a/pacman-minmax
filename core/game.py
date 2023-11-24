import random
import time

INF = 1000000000

class Game:
    def __init__(self, pacman_location:tuple, ghost1_location:tuple, ghost2_location:tuple):
        self.depth = 7
        self.map = [
            ['.','.','.','.','#','.','.','.','.','.','.','.','.','#','.','.','.','.'],
            ['.','#','#','.','#','.','#','#','#','#','#','#','.','#','.','#','#','.'],
            ['.','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#','.'],
            ['.','#','.','#','#','.','#','#','#','#','#','#','.','#','#','.','#','.'],
            ['.','.','.','.','.','.','#','.','.','.','.','#','.','.','.','.','.','.'],
            ['.','#','.','#','#','.','#','#','.','.','#','#','.','#','#','.','#','.'],
            ['.','#','.','.','.','.','.','.','.','.','.','.','.','.','.','.','#','.'],
            ['.','#','#','.','#','.','#','#','#','#','#','#','.','#','.','#','#','.'],
            ['.','.','.','.','#','.','.','.','.','.','.','.','.','#','.','.','.','.'],
        ]

        self.pacman_location = pacman_location
        self.ghost1_location = ghost1_location
        self.ghost2_location = ghost2_location

        self.pacman_score = 0

        self.dist = dict()
        self.calc_distances()

    def calc_distances(self):
        for i1, row1 in enumerate(self.map):
            self.dist[str(i1)] = dict()
            for j1, cell1 in enumerate(row1):
                self.dist[str(i1)][str(j1)] = dict()
                for i2, row2 in enumerate(self.map):
                    self.dist[str(i1)][str(j1)][str(i2)] = dict()
                    for j2, cell2 in enumerate(row2):
                        self.dist[str(i1)][str(j1)][str(i2)][str(j2)] = 0

        for i1, row1 in enumerate(self.map):
            for j1, cell1 in enumerate(row1):
                node = (j1, i1)
                visited = []
                queue = []

                visited.append(node)
                queue.append(node)
                while queue:
                    s = queue.pop(0)

                    for move in (0, 1, 2, 3):
                        neighbour = self.get_move_location(s, move)
                        if neighbour not in visited:
                            self.dist[str(i1)][str(j1)][str(neighbour[1])][str(neighbour[0])] = self.dist[str(i1)][str(j1)][str(s[1])][str(s[0])] + 1
                            # print(node, neighbour, self.dist[str(i1)][str(j1)][str(neighbour[1])][str(neighbour[0])])
                            visited.append(neighbour)
                            queue.append(neighbour)

    def get_distance(self, node1, node2):
        return self.dist[str(node1[1])][str(node1[0])][str(node2[1])][str(node2[0])]

    def print_map(self):
        for i, row in enumerate(reversed(self.map)):
            for j, cell in enumerate(row):
                if (j, 8-i) == self.pacman_location:
                    print('P', end=' ')
                elif (j, 8-i) == self.ghost1_location or (j, 8-i) == self.ghost2_location:
                    print('G', end=' ')
                else:
                    print(cell, end=' ')
            print()

    def run(self):
        turn = 0
        while self.pacman_location != self.ghost1_location and self.pacman_location != self.ghost2_location and self.get_remaining_dots():
            print(f"Round: {turn}, pacman score: {self.pacman_score}")
            self.print_map()
            if turn%3 == 0:
                print("Pacman turn ...")
                minmax_score, move = self.calculate_minimax(0, self.depth, self.pacman_location, self.ghost1_location, self.ghost2_location, 0)
                print(f"pacman move: {move}")
                # print("aloooooooooooo", minmax_score)
                dist_location = self.get_move_location(self.pacman_location, move)
                upd_score = 10 * (self.map[dist_location[1]][dist_location[0]] == '.') - 1
                self.map[dist_location[1]][dist_location[0]] = '*'
                self.pacman_location = dist_location
                self.pacman_score += upd_score
            elif turn%3 == 1:
                print("Ghost1 turn ...")
                move = random.randint(0, 3)
                print(f"Ghost1 move: {move}")
                self.ghost1_location = self.get_move_location(self.ghost1_location, move)
            elif turn%3 == 2:
                print("Ghost2 turn ...")
                move = random.randint(0, 3)
                print(f"Ghost2 move: {move}")
                self.ghost2_location = self.get_move_location(self.ghost2_location, move)
            turn += 1
            print('\n')
            # time.sleep(0.2)
        if self.pacman_location == self.ghost1_location:
            print("You lost. ghost #1 cached pacman!")
        if self.pacman_location == self.ghost2_location:
            print("You lost. ghost #2 cached pacman!")
        if self.get_remaining_dots() == 0:
            print("You won :)) pacman ate all of the dots !")
        print(f"SCORE: {self.pacman_score}")
        self.print_map()

    def get_remaining_dots(self):
        rem = 0
        for row in self.map:
            for cell in row:
               rem += (cell == '.')
        return rem

    def calculate_minimax(self, cur_depth, target_depth, pacman_location, ghost1_location, ghost2_location, turn_number):
        if pacman_location == ghost1_location or pacman_location == ghost2_location:
            return -INF, -1
        if cur_depth == target_depth:
            return self.e_utility(pacman_location, ghost1_location, ghost2_location), -1
        if cur_depth%3 == 0:
            score = -INF
            moves = [0]
            for move_number in (0, 1, 2, 3):
                dist_location = self.get_move_location(pacman_location, move_number)
                upd_score = 10 * (self.map[dist_location[1]][dist_location[0]] == '.') - 1
                tmp = self.map[dist_location[1]][dist_location[0]]
                self.map[dist_location[1]][dist_location[0]] = '*'
                next_score = \
                    self.calculate_minimax(cur_depth + 1, target_depth, dist_location, ghost1_location, ghost2_location, turn_number + 1)[0] \
                    + upd_score
                self.map[dist_location[1]][dist_location[0]] = tmp
                if next_score > score:
                    moves = list()
                    moves.append(move_number)
                    score = next_score
                elif next_score == score:
                    moves.append(move_number)
                # if cur_depth == 0:
                #     print(move_number, dist_location, upd_score, tmp, next_score, pacman_location, ghost1_location, ghost2_location, self.calculate_minimax(cur_depth + 1, target_depth, dist_location, ghost1_location, ghost2_location, turn_number + 1))
            return score, random.choice(moves)
        elif cur_depth%3 == 1:
            score = INF
            moves = [0]
            for move_number in (0, 1, 2, 3):
                next_score = self.calculate_minimax(cur_depth + 1, target_depth, pacman_location, self.get_move_location(ghost1_location, move_number), ghost2_location, turn_number + 1)[0]
                if next_score < score:
                    moves = list()
                    moves.append(move_number)
                    score = next_score
                elif next_score == score:
                    moves.append(move_number)
            return score, random.choice(moves)
        elif cur_depth%3 == 2:
            score = INF
            moves = [0]
            for move_number in (0, 1, 2, 3):
                next_score = self.calculate_minimax(cur_depth + 1, target_depth, pacman_location, ghost1_location, self.get_move_location(ghost2_location, move_number), turn_number + 1)[0]
                if next_score < score:
                    score = next_score
                    moves = list()
                    moves.append(move_number)
                elif next_score == score:
                    moves.append(move_number)
            return score, random.choice(moves)

    def get_move_location(self, initial_location, move_number):
        """
        0: left
        1: up
        2: right
        3: down
        """
        i, j = initial_location[0], initial_location[1]
        if move_number == 0:
            i -= self.get_cell(initial_location[0] - 1, initial_location[1]) != '#'
        elif move_number == 1:
            j += self.get_cell(initial_location[0], initial_location[1] + 1) != '#'
        elif move_number == 2:
            i += self.get_cell(initial_location[0] + 1, initial_location[1]) != '#'
        elif move_number == 3:
            j -= self.get_cell(initial_location[0], initial_location[1] - 1) != '#'
        return i, j

    def get_cell(self, i, j):
        if i == -1 or  i == 18 or j == -1 or j == 9:
            return '#'
        else:
            return self.map[j][i]

    def e_utility(self, pacman_location, ghost1_location, ghost2_location):
        ghost_distance = min(self.get_distance(pacman_location, ghost1_location), self.get_distance(pacman_location, ghost2_location))

        nearest_dot = INF
        dot_counts = 0
        for i, row in enumerate(self.map):
            for j, cell in enumerate(row):
                if cell == '.':
                    dot_counts += 1
                    nearest_dot = min(nearest_dot, self.dist[str(pacman_location[1])][str(pacman_location[0])][str(i)][str(j)])

        if nearest_dot == INF:
            nearest_dot = 0

        # return min(ghost_distance, 10) - 100 * nearest_dot*nearest_dot + (min(ghost_distance , 2) - 2) * 1000 - 100*dot_counts*dot_counts

        # return min(ghost_distance, 10) - 10 * nearest_dot*nearest_dot + (min(ghost_distance , 2) - 2) * 10 - 10*dot_counts*dot_counts

        return min(ghost_distance, 10) - 10 * nearest_dot + (min(ghost_distance, 2) - 2) * 100 - 100 * dot_counts
