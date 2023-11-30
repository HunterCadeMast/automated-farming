class Field(object):
    def __init__(self, width, height, obstacles=[]):
        self.width = width
        self.height = height
        self.obstacles = obstacles

    def is_obstacle_at(self, x, y):
        return (x, y) in self.obstacles

    def is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height