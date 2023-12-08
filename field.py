import random
import time

class Field(object):
    def __init__(self, width = 10, height = 10, num_chunks = 2):
        self.width = width
        self.height = height
        self.num_chunks = num_chunks
        self.total_tiles = width * height
        self.harvested_count = 0
        self.planted_count = 0
        self.field = [[{'state': None} for _ in range(width)] for _ in range(height)]
        self.full_state = 'NULL'
        self.initialize_obstacles()
        self.initialize_states()

    def initialize_obstacles(self):
        num_obstacles = random.randint(1, 5)
        for obstacles in range(num_obstacles):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if 'obstacle' not in self.field[y][x]:
                self.field[y][x]['obstacle'] = True
        self.total_tiles -= num_obstacles

    def initialize_states(self):
        if random.random() < 0.5:
            self.full_state = 'Empty'
            for column in range(self.height):
                for row in range(self.width):
                    self.field[column][row]['state'] = 'Empty'
            for chunk in range(self.num_chunks):
                chunk_state = 'Planted'
                self.initialize_chunk(chunk_state)
        else:
            self.full_state = 'Grown'
            for column in range(self.height):
                for row in range(self.width):
                    self.field[column][row]['state'] = 'Grown'
            for chunk in range(self.num_chunks):
                chunk_state = 'Harvested'
                self.initialize_chunk(chunk_state)

    def initialize_chunk(self, chunk_state):
        chunk_x = random.randint(1, self.width - 2)
        chunk_y = random.randint(1, self.height - 2)
        chunk_size = random.randint(2, 4)
        for y in range(chunk_y, min(chunk_y + chunk_size, self.height - 1)):
            for x in range(chunk_x, min(chunk_x + chunk_size, self.width - 1)):
                self.field[y][x]['state'] = chunk_state
        if chunk_state == 'Harvested':
            self.harvested_count = self.count_state('Harvested')
        elif chunk_state == 'Planted':
            self.planted_count = self.count_state('Planted')

    def count_state(self, target_state):
        count = 0
        for y in range(self.height):
            for x in range(self.width):
                if self.field[y][x]['state'] == target_state:
                    count += 1
        return count

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_obstacle_at(self, x, y):
        if not self.is_within_bounds(x, y):
            return True
        return 'obstacle' in self.field[y][x]

    def get_tile_state(self, x, y):
        if self.is_within_bounds(x, y):
            return self.field[y][x]['state']
        else:
            return None

    def set_tile_state(self, x, y, state):
        self.field[y][x]['state'] = state

    def set_vehicle_position(self, x, y):
        self.field[y][x]['state'] = 'Vehicle'

    def change_to_planted(self, x, y):
        self.planted_count += 1
        print("Planted: {:.2%}".format(self.planted_count / self.total_tiles))
        self.field[y][x]['state'] = 'Planted'

    def change_to_harvested(self, x, y):
        self.harvested_count += 1
        print("Harvested: {:.2%}".format(self.harvested_count / self.total_tiles))
        self.field[y][x]['state'] = 'Harvested'

    def print_field(self):
        for y in range(self.height):
            for x in range(self.width):
                if 'obstacle' in self.field[y][x]:
                    print('O', end=' ')
                elif 'Vehicle' == self.field[y][x]['state']:
                    print('V', end=' ')
                elif self.full_state == 'Grown':
                    state = self.field[y][x]['state']
                    if state == 'Harvested':
                        print('H', end=' ')
                    elif state == 'Grown':
                        print('#', end=' ')
                    elif state is None:
                        print('#', end=' ')
                elif self.full_state == 'Empty':
                    state = self.field[y][x]['state']
                    if state == 'Planted':
                        print('P', end=' ')
                    elif state == 'Empty':
                        print('.', end=' ')
                    elif state is None:
                        print('.', end=' ')
            print()