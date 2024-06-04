from bullet import Bullet
import pygame
from position import Position
import settings
from unit import Unit

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
        
        self.radius = settings.PLAYER_RADIUS
        self.speed = settings.PLAYER_SPEED
        self.position = Position(0, 0)

        self.shoot_cooldown = 0
        self.SHOOT_COOLDOWN_MAX = settings.PLAYER_COOLDOWN # frames between shots

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
        
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
            # While I could eliminate one check by letting shoot cooldown tick infinitely, shoot_cooldown doesn't need to keep going below 0

        if fire_pressed and self.shoot_cooldown <= 0:
            bullets.append(self.fire())
            self.shoot_cooldown = self.SHOOT_COOLDOWN_MAX # Reset cooldown
        return bullets



    