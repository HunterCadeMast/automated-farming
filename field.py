import random
import time

class Field(object):
    def __init__(self, width, height, num_chunks):
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
        for _ in range(num_obstacles):
            x = random.randint(1, self.width - 2)
            y = random.randint(1, self.height - 2)
            if 'obstacle' not in self.field[y][x]:
                self.field[y][x]['obstacle'] = True

    def initialize_states(self):
        if random.random() < 0.5:
            self.full_state = 'Empty'
            all(all(cell['state'] == 'Empty' for cell in row) for row in self.field)
            for _ in range(self.num_chunks):
                chunk_state = 'Planted'
                self.initialize_chunk(chunk_state)
        else:
            self.full_state = 'Grown'
            all(all(cell['state'] == 'Grown' for cell in row) for row in self.field)
            for _ in range(self.num_chunks):
                chunk_state = 'Harvested'
                self.initialize_chunk(chunk_state)

    def initialize_chunk(self, chunk_state):
        chunk_x = random.randint(1, self.width - 2)
        chunk_y = random.randint(1, self.height - 2)
        chunk_size = random.randint(2, 4)

        for y in range(chunk_y, min(chunk_y + chunk_size, self.height - 1)):
            for x in range(chunk_x, min(chunk_x + chunk_size, self.width - 1)):
                if self.field[y][x]['state'] is None:
                    self.field[y][x]['state'] = chunk_state
        if chunk_state == 'Harvested':
            harvested_count = self.count_state('Harvested')
        elif chunk_state == 'Planted':
            planted_count = self.count_state('Planted')

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
        return self.field[y][x]['obstacle']

    def get_tile_state(self, x, y):
        return self.field[y][x]['state']

    def set_tile_state(self, x, y, new_state):
        self.field[y][x]['state'] = new_state

    def set_vehicle_position(self, x, y):
        self.field[y][x]['state'] = 'Vehicle'

    def change_to_planted(self, x, y):
        self.planted_count += 1
        print("Planted: {:.2%}".format(self.planted_tiles / self.total_tiles))
        self.set_tile_state(x, y, 'Planted')

    def change_to_harvested(self, x, y):
        self.harvested_count += 1
        print("Harvested: {:.2%}".format(self.harvested_tiles / self.total_tiles))
        self.set_tile_state(x, y, 'Harvested')

    def print_field(self):
        for y in range(self.height):
            for x in range(self.width):
                if 'obstacle' in self.field[y][x]:
                    print('O', end=' ')
                elif 'Vehicle' in self.field[y][x]:
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

# Example Usage:
# Set field dimentions and number of chunks
field_width = 10
field_height = 10
num_chunks = 2
field = Field(field_width, field_height, num_chunks)

for _ in range(10):
    field.print_field()
    time.sleep(10)