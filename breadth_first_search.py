import random
from collections import deque
from field import Field

class Breadth(Field):
    def __init__(self, width = 10, height = 10, num_chunks = 2):
        super().__init__(width, height, num_chunks)
        self.current_position = (0, 0)

    # Gets all current states from the field.
    def get_states(self):
        states = []
        for y in range(self.height):
            for x in range(self.width):
                if 'obstacle' not in self.field[y][x]:
                    states.append((x, y))
        return states

    # Recognizes all current actions.
    def get_actions(self, state):
        x, y = state
        actions = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        return [action for action in actions if self.is_within_bounds(*action) and not self.is_obstacle_at(*action)]

    # Plans path from current state.
    def bfs_path_planning(self, start, goal):
        queue = deque([(start, [])])
        visited = set()
        while queue:
            current, path = queue.popleft()
            if current == goal:
                return path
            if current not in visited:
                visited.add(current)
                for action in self.get_actions(current):
                    next_state = action
                    if next_state not in visited and not self.is_obstacle_at(*next_state):
                        queue.append((next_state, path + [next_state]))
        return None

    # Gets policy informaiton.
    def get_policy(self, state):
        unvisited_states = [s for s in self.get_states() if s not in self.visited_states]
        if not unvisited_states:
            return state
        nearest_state = min(unvisited_states, key=lambda s: abs(state[0] - s[0]) + abs(state[1] - s[1]))
        path_to_nearest = self.bfs_path_planning(state, nearest_state)
        if path_to_nearest:
            return path_to_nearest[0]
        else:
            return state

    # Computes optimal path.
    def compute_optimal_path(self):
        current_state = self.current_position
        optimal_path = [current_state]
        while current_state != (self.width - 1, self.height - 1):
            action = self.get_policy(current_state)
            next_state = action
            optimal_path.append(next_state)
            current_state = next_state
            self.visited_states.add(next_state)
        return optimal_path

    # Performs actions to move vehicle through field.
    def perform_action(self, action):
        next_x, next_y = action
        if self.previous_state == 'Harvested':
            self.set_tile_state(self.x, self.y, 'Harvested')
        elif self.previous_state == 'Planted':
            self.set_tile_state(self.x, self.y, 'Planted')
        elif self.full_state == 'Grown':
            self.change_to_harvested(self.x, self.y)
        elif self.full_state == 'Empty':
            self.change_to_planted(self.x, self.y)
        self.previous_state = self.get_tile_state(next_x, next_y)
        self.set_vehicle_position(next_x, next_y)
        self.x, self.y = next_x, next_y
        self.visited_states.add((next_x, next_y))
        self.print_field()
        print('\n')

    # Moves through the path.
    def follow_optimal_path(self, optimal_path):
        for state in optimal_path:
            action = self.get_policy(state)
            self.perform_action(action)
            self.visited_states.add(state)

# Starts search.
field = Breadth(width=10, height=10, num_chunks=2)
optimal_path = field.compute_optimal_path()
print("Optimal Path:", optimal_path)
field.follow_optimal_path(optimal_path)
print("Optimal Path Followed!")