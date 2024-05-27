import pygame
from position import Position

DEFAULT_SPEED = 5
DEFAULT_RADIUS = 5

class Unit(pygame.sprite.Sprite):
    # Inherites Sprite
    def __init__(self):
        super(Unit, self).__init__()

        self.alive = True
        self.position = Position(0, 0)
        self.radius = DEFAULT_RADIUS
        self.speed = DEFAULT_SPEED

    def check_collision(self, other_unit):
        """
        Parameters:
            other_position: position to check if this unit is colliding with that one
        Returns:
            boolean to determine if their radius overlap
        """
        distance = self.get_position().get_distance(other_unit.get_position())
        if distance < self.get_radius() + other_unit.get_radius():
            return True
        else:
            return False
        
    def die(self):
        self.alive = False

    def fire(self):
        pass
        
    def get_alive(self):
        return self.alive

    def get_position(self):
        return self.position
    
    def get_radius(self):
        return self.radius
    
    def get_speed(self):
        return self.speed
    
    def move(self, target_position : Position):
        # Let main class handle oob
        self.position.set_position(target_position)
            

    
    