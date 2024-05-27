from bullet import Bullet
import pygame
from position import Position
import settings
from unit import Unit

RADIUS = 25
SPEED = 5

class Player(Unit):
    # Inherites Sprite
    def __init__(self):
        super(Player, self).__init__()

        # Sprite image path
        player_sprite_path = "./Assets/Ship.png"
        # Load image
        self.surf = pygame.image.load(player_sprite_path).convert_alpha()
        # Save player rect into accessible variable
        self.rect = self.surf.get_rect()
        
        self.radius = RADIUS
        self.speed = SPEED
        self.position = Position(0, 0)

    def fire(self):
        # Always fire up
        bullet_spawn_position = Position(self.get_position().get_x(), self.get_position().get_y() - self.get_radius() - settings.BULLET_RADIUS)
        return Bullet(bullet_spawn_position, -settings.BULLET_SPEED)

    def update(self, target_position, fire_pressed=False):
        """
        Handles movement and firing.
        Parameters:
            target_position: movement target
            fire_pressed: if true, try to fire a bullet
        """
        self.move(target_position)

        bullets = []
        if fire_pressed:
            bullets.append(self.fire())
        return bullets



    