from position import Position
import pygame
import settings
from unit import Unit



class Bullet(Unit):
    def __init__(self, spawn_position : Position, speed):
        super(Bullet, self).__init__()

        self.position = Position(spawn_position.get_x(), spawn_position.get_y())
        self.speed = speed
        self.radius = settings.BULLET_RADIUS
        # Sprite image path
        sprite_path = "./Assets/Player_Bullet.png"
        # Load image
        self.surf = pygame.image.load(sprite_path).convert_alpha()
        # Save player rect into accessible variable
        self.rect = self.surf.get_rect()
    
    def update(self):
        target = Position(self.get_position().get_x(), self.get_position().get_y() + self.get_speed())
        self.move(target)
        if self.get_position().get_y() > settings.WINDOW_HEIGHT or self.get_position().get_y() < 0:
            self.die()