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

    # Clock for frame rate
    clock = pygame.time.Clock()

    # Initialize player
    player = Player()
    player.update(Position(WIDTH / 2, HEIGHT - 40))

    # Initialize score
    score = 0
    unit_list = []

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            # End game if player closes windows
            if event.type == pygame.QUIT:
                running = False

        # Inputs handled here
        added_bullets = handle_input(player)
        for bullet in added_bullets:
            unit_list.append(bullet)

        unit_list = handle_units(unit_list)

        render_screen(screen, player, unit_list, score)

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

    added_bullets = player.update(Position(new_player_x, new_player_y), fire_pressed=fire)
    return added_bullets

def handle_units(unit_list):
    new_unit_list = []
    if len(unit_list) > 0:
        for unit in unit_list:
            if unit.get_alive():
                unit.update()
                new_unit_list.append(unit)
    return new_unit_list

def render_screen(screen, player, unit_list, score):
    # Render to screen
    # Background
    screen.fill((255, 255, 255))
    # Player
    screen.blit(player.surf, (player.get_position().get_x() - 40, player.get_position().get_y() - 40))
    # Units
    for unit in unit_list:
        screen.blit(unit.surf, (unit.get_position().get_x() - unit.get_radius(), unit.get_position().get_y() - unit.get_radius()))
    # Score
    score_font = pygame.font.SysFont("any_font", 30)
    score_block = score_font.render(f"Score: {score}", False, (0, 0, 0))
    screen.blit(score_block, (25,25))

    # Reveal
    pygame.display.flip()

if __name__ == "__main__":
    main()