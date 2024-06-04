from bullet import Bullet
from enemy import Enemy
from player import Player
from position import Position
import pygame
import settings

def main():
    # Window Variables (Pixels)
    settings.init()
    WIDTH = settings.WINDOW_WIDTH
    HEIGHT = settings.WINDOW_HEIGHT

    # Initialize Pygame engine
    pygame.init()

    # Initialize window
    screen = pygame.display.set_mode(size=[WIDTH, HEIGHT])

    # Initialize music and sounds
    music_filename = "Assets\Ludum Dare 30 - 09.ogg"
    pygame.mixer.music.load(music_filename)
    pygame.mixer.music.set_volume(settings.WINDOW_VOLUME)
    pygame.mixer.music.play(fade_ms=500)

    fire_sound_filename = "Assets\gun-2.wav"
    fire_sound = pygame.mixer.Sound(fire_sound_filename)
    fire_sound.set_volume(settings.WINDOW_VOLUME)

    # Clock for frame rate
    clock = pygame.time.Clock()

    # Initialize player
    player = Player()
    player.update(Position(WIDTH / 2, HEIGHT - 40))

    unit_list = []
    score = 0

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            # End game if player closes windows
            if event.type == pygame.QUIT:
                running = False

        # Spawn new enemies if necessary
        enemy_count = 0
        for unit in unit_list:
            if isinstance(unit, Enemy):
                enemy_count += 1
        if enemy_count < settings.ENEMY_MAX_COUNT:
            # Initialize an enemy and add it to unit_list
            enemy = Enemy()
            unit_list.append(enemy)

        # Inputs handled here
        added_bullets = handle_input(player)
        for bullet in added_bullets:
            unit_list.append(bullet)
            fire_sound.play()

        unit_list = handle_units(unit_list)

        render_screen(screen, player, unit_list)

        # max frames per second: 60
        clock.tick(settings.WINDOW_FPS)

def handle_input(player : Player):
    """
    Input handling:
    A, Left Arrow
        player_delta_x = -player_speed
    D, Right Arrow
        player_delta_x = player_speed
        Need to check if speed is negative (other button held down), set to zero if true instead of positive

    Parameters:
        player: player to be controlled
    Returns:
        list of bullets to be added to bullet array
        
    """
    # Player movement deltas
    player_delta_x = 0
    player_delta_y = 0
    HEIGHT = settings.WINDOW_HEIGHT
    WIDTH = settings.WINDOW_WIDTH

    keys = pygame.key.get_pressed()

    fire = False

    # X movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player_delta_x = -player.get_speed()

    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        # If holding both, hold still
        if player_delta_x != 0:
            player_delta_x = 0
        else:
            player_delta_x = player.get_speed()
    
    if keys[pygame.K_SPACE]:
        fire = True



    # Update player position using player_delta_vector
    player_position = player.get_position()
    new_player_x = player_position.get_x() + player_delta_x
    new_player_y = player_position.get_y() + player_delta_y
    # Window boundary checking
    if new_player_x > WIDTH - player.get_radius():
        new_player_x = WIDTH - player.get_radius()
    if new_player_x < player.get_radius():
        new_player_x = player.get_radius()
    if new_player_y > HEIGHT:
        new_player_y = HEIGHT
    if new_player_y < 0:
        new_player_y = 0

    added_bullets = player.update(Position(new_player_x, new_player_y),
                                   fire_pressed=fire)
    return added_bullets

def handle_units(unit_list):
    # Setup explode sound (Would be more efficient to set up as a global)
    explode_sound_filename = "Assets\explode-3.wav"
    explode_sound = pygame.mixer.Sound(explode_sound_filename)
    explode_sound.set_volume(settings.WINDOW_VOLUME)

    new_unit_list = []
    if len(unit_list) > 0:
        for unit in unit_list:
            """
            Collisions:
                if this is a player or enemy
                create a temporary list of only bullets
                if colliding with a bullet
                kill bullet and player/enemy
            """
            if isinstance(unit, Enemy) or isinstance(unit, Player):
                tmp_bullet_list = filter(lambda a : isinstance(a, Bullet), unit_list)
                for bullet in tmp_bullet_list:
                    if unit.check_collision(bullet):
                        unit.die()
                        bullet.die()
                        explode_sound.play()
                        # Update score
                        if isinstance(unit, Enemy):
                            # increment score
                            pass
                        elif isinstance(unit, Player):
                            # you lose screen
                            pass
                        
            if unit.get_alive():
                bullet_list = unit.update()
                new_unit_list.append(unit)
                # Handle spawned bullets next frame
                for bullet in bullet_list:
                    new_unit_list.append(bullet)
    return new_unit_list

def render_screen(screen, player, unit_list):
    # Render to screen
    # Background
    screen.fill((255, 255, 255))
    # Player
    screen.blit(player.surf, (player.get_position().get_x() - 40,
                               player.get_position().get_y() - 40))
    # Units
    for unit in unit_list:
        screen.blit(unit.surf, (unit.get_position().get_x() - unit.get_radius(),
                                 unit.get_position().get_y() - unit.get_radius()))

    # Reveal
    pygame.display.flip()

if __name__ == "__main__":
    main()