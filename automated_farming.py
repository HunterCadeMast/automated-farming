import time
import random
from automated_states import idle, drive, harvest, plant, obstacleDetection, edgeDetection, safety
from field import Field

class FarmingVehicle(object):
    # Initializes variables.
    def __init__(self):
        self.state = idle()
        self.field = Field()
        self.move_count = 0
        self.x = 0
        self.y = 0
        self.orientation = 'N'

    # Sends command to the state machine.
    def on_event(self, event):
        self.state = self.state.on_event(event)

    # Checks on status of tanks if they exceed our desired harvest or plant goal.
    def crop_status(self):
        threshold = 0.95
        return (self.field.harvested_count / self.field.total_tiles >= threshold or self.field.planted_count / self.field.total_tiles >= threshold)

    # Moves vehicle throughout field. Also, will count moves so if vehicle does not infinitely loop.
    def move(self):
        next_x, next_y = self.calculate_next_position()
        if not isinstance(self.state, drive):
            if self.field.full_state == 'Grown':
                self.field.change_to_harvested(self.x, self.y)
            elif self.field.full_state == 'Empty':
                self.field.change_to_planted(self.x, self.y)
        else:
            self.move_count += 1
            if self.field.full_state == 'Grown':
                self.field.set_tile_state(self.x, self.y, 'Harvested')
            elif self.field.full_state == 'Empty':
                self.field.set_tile_state(self.x, self.y, 'Planted')
        self.field.set_vehicle_position(next_x, next_y)
        self.x, self.y = next_x, next_y
        self.field.print_field()

    # Automatically runs through different commands depending on the current state. Will also start from idle() and set vehicle into the field.
    def automatic_movement(self):
        self.state = self.state.on_event('start')
        self.field.set_vehicle_position(self.x, self.y)
        while True:
            decision = self.make_decision()
            self.on_event(decision)
            time.sleep(0.1)

    # Changes the state depending on current state of the field.
    def make_decision(self):
        next_x, next_y = self.calculate_next_position()
        current_x = self.x
        current_y = self.y
        if isinstance(self.state, drive):
            # Makes sure vehicle does not run infinitely.
            if self.move_count > 30:
                return 'stop'
            # Checks all tiles around for grown when edge or object appears.
            elif self.field.get_tile_state(next_x, next_y) == 'Grown':
                return 'harvest'
            elif self.field.get_tile_state(next_x, next_y) == 'Empty':
                return 'plant'
            elif self.field.get_tile_state(current_x + 1, current_y) == 'Grown' and not self.is_approaching_edge(current_x + 1, current_y):
                self.orientation = 'E'
                return 'harvest'
            elif self.field.get_tile_state(current_x - 1, current_y) == 'Grown' and not self.is_approaching_edge(current_x - 1, current_y):
                self.orientation = 'W'
                return 'harvest'
            elif self.field.get_tile_state(current_x, current_y + 1) == 'Grown' and not self.is_approaching_edge(current_x, current_y + 1):
                self.orientation = 'N'
                return 'harvest'
            elif self.field.get_tile_state(current_x, current_y - 1) == 'Grown' and not self.is_approaching_edge(current_x, current_y - 1):
                self.orientation = 'S'
                return 'harvest'
            elif self.field.get_tile_state(current_x + 1, current_y) == 'Empty' and not self.is_approaching_edge(current_x + 1, current_y):
                self.orientation = 'E'
                return 'plant'
            elif self.field.get_tile_state(current_x - 1, current_y) == 'Empty' and not self.is_approaching_edge(current_x - 1, current_y):
                self.orientation = 'W'
                return 'plant'
            elif self.field.get_tile_state(current_x, current_y + 1) == 'Empty' and not self.is_approaching_edge(current_x, current_y + 1):
                self.orientation = 'N'
                return 'plant'
            elif self.field.get_tile_state(current_x, current_y - 1) == 'Empty' and not self.is_approaching_edge(current_x, current_y - 1):
                self.orientation = 'S'
                return 'plant'
            # Should move through harvested or planted tiles adjacent if no grown or empty tiles are adjacent.
            elif self.field.get_tile_state(next_x, next_y) == 'Harvested':
                self.move()
                return 'continue'
            elif self.field.get_tile_state(next_x, next_y) == 'Planted':
                self.move()
                return 'continue'
            elif self.field.get_tile_state(current_x + 1, current_y) == 'Harvested' and not self.is_approaching_edge(current_x + 1, current_y):
                self.orientation = 'E'
                self.move()
                return 'continue'
            elif self.field.get_tile_state(current_x - 1, current_y) == 'Harvested' and not self.is_approaching_edge(current_x - 1, current_y):
                self.orientation = 'W'
                self.move()
                return 'continue'
            elif self.field.get_tile_state(current_x, current_y + 1) == 'Harvested' and not self.is_approaching_edge(current_x, current_y + 1):
                self.orientation = 'N'
                self.move()
                return 'continue'
            elif self.field.get_tile_state(current_x, current_y - 1) == 'Harvested' and not self.is_approaching_edge(current_x, current_y - 1):
                self.orientation = 'S'
                self.move()
                return 'continue'
            elif self.field.get_tile_state(current_x + 1, current_y) == 'Planted' and not self.is_approaching_edge(current_x + 1, current_y):
                self.orientation = 'E'
                self.move()
                return 'continue'
            elif self.field.get_tile_state(current_x - 1, current_y) == 'Planted' and not self.is_approaching_edge(current_x - 1, current_y):
                self.orientation = 'W'
                self.move()
                return 'continue'
            elif self.field.get_tile_state(current_x, current_y + 1) == 'Planted' and not self.is_approaching_edge(current_x, current_y + 1):
                self.orientation = 'N'
                self.move()
                return 'continue'
            elif self.field.get_tile_state(current_x, current_y - 1) == 'Planted' and not self.is_approaching_edge(current_x, current_y - 1):
                self.orientation = 'S'
                self.move()
                return 'continue'
            # Checks if obstacle is blocking path.
            elif self.field.is_obstacle_at(next_x, next_y):
                return 'obstacle'
            # Checks if edge is blocking path.
            elif self.is_approaching_edge(next_x, next_y):
                return 'edge'
            # Checks if crop status exceeds the threshold.
            elif self.crop_status():
                return 'stop'
            else:
                return 'safety'
        # Moves around similar to the drive state, but for harvesting.
        if isinstance(self.state, harvest):
            if self.field.get_tile_state(next_x, next_y) == 'Planted' or self.field.get_tile_state(next_x, next_y) == 'Harvested':
                return 'drive'
            elif self.field.is_obstacle_at(next_x, next_y):
                return 'obstacle'
            elif self.is_approaching_edge(next_x, next_y):
                return 'edge'
            elif self.crop_status():
                return 'stop'
            self.move()
            return 'continue'
        # Moves around similar to the drive state, but for planting.
        if isinstance(self.state, plant):
            if self.field.get_tile_state(next_x, next_y) == 'Planted' or self.field.get_tile_state(next_x, next_y) == 'Harvested':
                return 'drive'
            if self.field.is_obstacle_at(next_x, next_y):
                return 'obstacle'
            if self.is_approaching_edge(next_x, next_y):
                return 'edge'
            if self.crop_status():
                return 'stop'
            self.move()
            return 'continue'
        # Chooses action to move from obstacle depending on surrounding tiles.
        if isinstance(self.state, obstacleDetection):
            next_x, next_y = self.calculate_next_position()
            if self.try_turn_left():
                self.turn_left()
            elif self.try_turn_right():
                self.turn_right()
            if self.field.get_tile_state(next_x, next_y) == 'Empty':
                return 'plant'
            elif self.field.get_tile_state(next_x, next_y) == 'Grown':
                return 'harvest'
            elif self.field.get_tile_state(next_x, next_y) == 'Planted' or self.field.get_tile_state(next_x, next_y) == 'Harvested':
                return 'drive'
            else:
                return 'stop'
        # Chooses action to move from edge depending on surrounding tiles.
        if isinstance(self.state, edgeDetection):
            next_x, next_y = self.calculate_next_position()
            if self.try_turn_left():
                self.turn_left()
            elif self.try_turn_right():
                self.turn_right()
            if self.field.get_tile_state(next_x, next_y) == 'Empty':
                return 'plant'
            elif self.field.get_tile_state(next_x, next_y) == 'Grown':
                return 'harvest'
            elif self.field.get_tile_state(next_x, next_y) == 'Planted' or self.field.get_tile_state(next_x, next_y) == 'Harvested':
                return 'drive'
            else:
                return 'stop'

    # Calculates the next position ahead depending on the orientation of vehicle.
    def calculate_next_position(self):
        next_x = self.x
        next_y = self.y
        if self.orientation == 'N':
            next_y += 1
        elif self.orientation == 'S':
            next_y -= 1
        elif self.orientation == 'W':
            next_x -= 1
        elif self.orientation == 'E':
            next_x += 1
        return next_x, next_y

    # Changes orientation to the left.
    def turn_left(self):
        if self.orientation == 'N':
            self.orientation = 'W'
        elif self.orientation == 'S':
            self.orientation = 'E'
        elif self.orientation == 'E':
            self.orientation = 'N'
        elif self.orientation == 'W':
            self.orientation = 'S'

    # Checks if a left turn is available.
    def try_turn_left(self):
        given_x = self.x
        given_y = self.y
        if self.orientation == 'N':
            given_x -= 1
        elif self.orientation == 'S':
            given_x += 1
        elif self.orientation == 'W':
            given_y -= 1
        elif self.orientation == 'E':
            given_y += 1
        valid_move = self.field.is_within_bounds(given_x, given_y) and not self.field.is_obstacle_at(given_x, given_y)
        return valid_move

    # Changes orientation to the right.
    def turn_right(self):
        if self.orientation == 'N':
            self.orientation = 'E'
        elif self.orientation == 'S':
            self.orientation = 'W'
        elif self.orientation == 'E':
            self.orientation = 'S'
        elif self.orientation == 'W':
            self.orientation = 'N'

    # Checks if a right turn is available.
    def try_turn_right(self):
        given_x = self.x
        given_y = self.y
        if self.orientation == 'N':
            given_x += 1
        elif self.orientation == 'S':
            given_x -= 1
        elif self.orientation == 'W':
            given_y += 1
        elif self.orientation == 'E':
            given_y -= 1
        valid_move = self.field.is_within_bounds(given_x, given_y) and not self.field.is_obstacle_at(given_x, given_y)
        return valid_move

    # Checks if specific tile is within the bounds.
    def is_approaching_edge(self, next_x, next_y):
        return (next_x >= self.field.width or next_y >= self.field.height)

# Runs program.
if __name__ == "__main__":
    farming_vehicle = FarmingVehicle()
    farming_vehicle.automatic_movement()