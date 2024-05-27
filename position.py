import math

class Position():
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_distance(self, target_position):
        """
        Parameter:
            target_position - position to determine distance between
        Return: 
            distance (float)
        """
        distance_x = abs(target_position.get_x() - self.get_x())
        distance_y = abs(target_position.get_y() - self.get_y())
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        return distance
    
    def set_position(self, target_position):
        self.set_x(target_position.get_x())
        self.set_y(target_position.get_y())

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y