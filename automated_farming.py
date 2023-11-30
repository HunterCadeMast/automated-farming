import threading
import time
import random
from states import idle
from states import turn
from states import speedControl
from states import obstacleDetection
from states import obstacleHit
from states import fieldData
from states import cropStatus
from states import cropFull
from states import cropEmpty
from states import drive
from states import harvest
from states import plant
from field import Field

class FarmingVehicle(object):
    """ 
    A simple state machine that mimics the functionality of a device from a 
    high level.
    """

    def __init__(self, field_width = 10, field_height = 10, obstacles=[(2, 3), (5, 5)]):
        """ Initialize the components. """

        # Start with a default state.
        self.state = idle()
        self.speed = 0
        self.orientation = 'N'
        self.field = Field(field_width, field_height, obstacles)
        self.automatic_movement_thread = threading.Thread(target=self.automatic_movement, daemon=True)
        self.automatic_movement_thread.start()

    def set_speed(self, speed):
        self.speed = speed

    def move(self, direction):
        x, y = self.state_position()
        if direction == 'forward':
            if direction == 'up':
                y -= self.speed
            elif direction == 'down':
                y += self.speed
            elif direction == 'left':
                x -= self.speed
            elif direction == 'right':
                x += self.speed
        elif direction == 'left':
            self.turn_left()
        elif direction == 'right':
            self.turn_right()
        if self.field.is_within_bounds(x, y) and not self.field.is_obstacle_at(x, y):
            self.state.set_position(x, y)
    
    def turn_left(self):
        if self.orientation == 'N':
            self.orientation == 'W'
        elif self.orientation == 'S':
            self.orientation == 'E'
        elif self.orientation == 'E':
            self.orientation == 'N'
        elif self.orientation == 'W':
            self.orientation == 'S'

    def turn_right(self):
        if self.orientation == 'N':
            self.orientation == 'E'
        elif self.orientation == 'S':
            self.orientation == 'S'
        elif self.orientation == 'E':
            self.orientation == 'W'
        elif self.orientation == 'W':
            self.orientation == 'N'

    def on_event(self, event):
        """
        This is the bread and butter of the state machine. Incoming events are
        delegated to the given states which then handle the event. The result is
        then assigned as the new state.
        """

        # The next state will be the result of the on_event function.
        self.state = self.state.on_event(event)

    def automatic_movement(self):
        while True:
            decision = self.make_decision()
            self.on_event(decision)
            time.sleep(2)

    def make_decision(self):
        if isinstance(self.state, idle):
            return 'start'
        elif isinstance(self.state, drive):
            # WHAT TO DO IF DRIVING
            decisions = ['turn_left', 'turn_right']
            return decisions[0]

    def state_position(self):
        if isinstance(self.state, drive):
            return self.state.get_position()
        return (0, 0)
        