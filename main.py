import pygame
from pygame.locals import QUIT

pygame.init()

clock = pygame.time.Clock()  # Create a clock object

HEIGHT = 800
WIDTH = 1200
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

player_size = (20, 20)
player = pygame.Surface(player_size)
player.fill(COLOR_WHITE)
player_rect = player.get_rect()

# Center the player initially in the window
player_rect.center = (WIDTH // 2, HEIGHT // 2)
player_speed = [1, 1]

playing = True
while playing:
    clock.tick(120)  # Control the frame rate
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
    main_display.fill(COLOR_BLACK)

    
    if player_rect.bottom >= HEIGHT or player_rect.top <= 0:
        player_speed[1] = -player_speed[1]  
    if player_rect.right >= WIDTH or player_rect.left <= 0:
        player_speed[0] = -player_speed[0]  
    
    main_display.blit(player, player_rect)
    player_rect = player_rect.move(player_speed)

    pygame.display.flip()
