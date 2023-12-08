import time
import random
from automated_states import idle, drive, harvest, plant, obstacleDetection, edgeDetection, safety
from field import Field

class FarmingVehicle(object):
    def __init__(self):
        self.state = idle()
        self.field = Field()
        self.move_count = 0
        self.x = 0
        self.y = 0
        self.orientation = 'N'

    def on_event(self, event):
        self.state = self.state.on_event(event)

    def crop_status(self):
        threshold = 0.95
        return (self.field.harvested_count / self.field.total_tiles >= threshold or self.field.planted_count / self.field.total_tiles >= threshold)

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

    def automatic_movement(self):
        self.state = self.state.on_event('start')
        self.field.set_vehicle_position(self.x, self.y)
        while True:
            decision = self.make_decision()
            self.on_event(decision)
            time.sleep(0.1)

    def make_decision(self):
        next_x, next_y = self.calculate_next_position()
        current_x = self.x
        current_y = self.y
        if isinstance(self.state, drive):
            if self.move_count > 30:
                return 'stop'
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
            # Should move through harvested or planted tiles if no grown or empty tiles adjacent
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
            elif self.field.is_obstacle_at(next_x, next_y):
                return 'obstacle'
            elif self.is_approaching_edge(next_x, next_y):
                return 'edge'
            elif self.crop_status():
                return 'stop'
            else:
                return 'stop'
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

    def turn_left(self):
        if self.orientation == 'N':
            self.orientation = 'W'
        elif self.orientation == 'S':
            self.orientation = 'E'
        elif self.orientation == 'E':
            self.orientation = 'N'
        elif self.orientation == 'W':
            self.orientation = 'S'

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

    def turn_right(self):
        if self.orientation == 'N':
            self.orientation = 'E'
        elif self.orientation == 'S':
            self.orientation = 'W'
        elif self.orientation == 'E':
            self.orientation = 'S'
        elif self.orientation == 'W':
            self.orientation = 'N'

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

    def is_approaching_edge(self, next_x, next_y):
        return (next_x >= self.field.width or next_y >= self.field.height)

if __name__ == "__main__":
    farming_vehicle = FarmingVehicle()
    farming_vehicle.automatic_movement()