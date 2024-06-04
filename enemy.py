from bullet import Bullet
from position import Position
import random
import pygame
import settings
from unit import Unit

class Enemy(Unit):
    # Sprite Inheritance
    def __init__(self):
        super(Enemy, self).__init__()

        # Sprite handling
        sprite_path = "./Assets/Enemy.png"
        self.surf = pygame.image.load(sprite_path).convert_alpha()
        self.rect = self.surf.get_rect()

        # Enemy stats
        self.radius = settings.ENEMY_RADIUS
        self.speed = settings.ENEMY_SPEED
        self.SHOOT_COOLDOWN_MAX = settings.ENEMY_COOLDOWN
        self.shoot_cooldown = self.SHOOT_COOLDOWN_MAX

        # Random position on spawn
        enemy_x = settings.WINDOW_WIDTH * random.random()
        enemy_y = settings.ENEMY_RADIUS * 2
        self.position = Position(enemy_x, enemy_y)

    def fire(self):
        """
        Initializes and returns a bullet object
        Parameters:
            none
        Returns:
            Bullet object
        """
        bullet_spawn_position = Position(self.get_position().get_x(), self.get_position().get_y() + self.get_radius() + settings.BULLET_RADIUS)
        return Bullet(bullet_spawn_position, settings.BULLET_SPEED, player_bullet=False)

    def update(self):
        """
        Autonomous firing
        """
        # Firing logic (LAST, includes a return statement)
        bullets = []
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        else:
            bullets.append(self.fire())
            self.shoot_cooldown = self.SHOOT_COOLDOWN_MAX
        return bullets