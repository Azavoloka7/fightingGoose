import random
import pygame
from pygame.locals import QUIT

pygame.init()

clock = pygame.time.Clock()

# Screen dimensions
HEIGHT = 600
WIDTH = 800

# Colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)

# Set up the display
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Enemies!")

# Load music
pygame.mixer.music.load('C:/Users/zavol/Downloads/zav_music.mp3')  # Replace 'background_music.mp3' with the path to your music file
game_over_music = 'C:/Users/zavol/Downloads/game_over.wav'  # Path to game over music
pygame.mixer.music.play(-1)  # Play the music indefinitely

# Load sound effects
bonus_sound = pygame.mixer.Sound('C:/Users/zavol/Downloads/bonus.mp3')  

# Player settings
player_size = 20
player_color = COLOR_WHITE
player_rect = pygame.Rect(WIDTH // 2 - player_size // 2, HEIGHT // 2 - player_size // 2, player_size, player_size)
player_speed = 5
player_speed_increase = 1

# Enemy settings
enemy_size = 30
enemy_color = COLOR_RED
enemy_speed = 3
enemies = []

# Bonus settings
bonus_size = 20
bonus_color = COLOR_GREEN
bonus_speed = 5
bonuses = []

# Game variables
game_over = False
score = 0

# Function to create a new enemy
def create_enemy():
    x = WIDTH
    y = random.randint(0, HEIGHT - enemy_size)
    enemy_rect = pygame.Rect(x, y, enemy_size, enemy_size)
    return enemy_rect

# Function to create a new bonus
def create_bonus():
    x = random.randint(0, WIDTH - bonus_size)
    y = -bonus_size
    bonus_rect = pygame.Rect(x, y, bonus_size, bonus_size)
    return bonus_rect

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True

    # Move the player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        player_rect.y += player_speed
    if keys[pygame.K_UP]:
        player_rect.y -= player_speed
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed

    # Keep player within the screen bounds
    player_rect.x = max(0, min(player_rect.x, WIDTH - player_size))
    player_rect.y = max(0, min(player_rect.y, HEIGHT - player_size))

    # Create a new enemy every 1 second
    if random.random() < 0.01:
        enemies.append(create_enemy())

    # Create a new bonus every 2 seconds
    if random.random() < 0.005:
        bonuses.append(create_bonus())

    # Move enemies from right to left and check for collisions with player
    for enemy in enemies:
        enemy.x -= enemy_speed
        if enemy.colliderect(player_rect):
            game_over = True
        if enemy.right < 0:
            enemies.remove(enemy)

    # Move bonuses falling from the sky and check for collisions with player
    for bonus in bonuses:
        bonus.y += bonus_speed
        if bonus.colliderect(player_rect):
            score += 1
            player_speed += player_speed_increase
            bonuses.remove(bonus)
            bonus_sound.play()  # Play the bonus sound effect
        if bonus.top > HEIGHT:
            bonuses.remove(bonus)

    # Fill the display with background color
    main_display.fill(COLOR_BLACK)

    # Draw the player
    pygame.draw.rect(main_display, player_color, player_rect)

    # Draw the enemies
    for enemy in enemies:
        pygame.draw.rect(main_display, enemy_color, enemy)

    # Draw the bonuses
    for bonus in bonuses:
        pygame.draw.rect(main_display, bonus_color, bonus)

    # Update the display with score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, COLOR_WHITE)
    score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
    main_display.blit(score_text, score_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

try:
    # Play game over music
    pygame.mixer.music.stop()  # Stop the background music
    pygame.mixer.music.load(game_over_music)
    pygame.mixer.music.play()

    # Wait for a moment before showing the game over screen
    pygame.time.wait(1000)

    # Game over screen
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over!", True, COLOR_WHITE)
    game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    main_display.blit(game_over_text, game_over_rect)
    pygame.display.flip()

    # Wait for a moment before closing the window
    pygame.time.wait(2000)

except pygame.error as e:
    print("Error:", e)  # Print the error message for debugging purposes

finally:
    # Quit Pygame
    pygame.quit()
