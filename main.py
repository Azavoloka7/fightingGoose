import random
import pygame
from pygame.locals import QUIT

# Initialize Pygame
pygame.init()

# Screen dimensions
HEIGHT = 600
WIDTH = 800

# Set up the display
main_display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Enemies!")

# Load images for player animation
player_images = [pygame.image.load(f"C:/Users/zavol/Documents/zavGame/images/player{i}.png").convert_alpha() for i in range(1, 6)]
current_player_image_index = 0  # Start with the first image
player_image = player_images[current_player_image_index]
player_animation_frame_count = 0
player_animation_speed = 10  # Switch image every 10 frames

# Load other images
background_image = pygame.image.load("C:/Users/zavol/Documents/zavGame/images/background.png").convert()
enemy_image = pygame.image.load("C:/Users/zavol/Documents/zavGame/images/enemy.png").convert_alpha()
bonus_image = pygame.image.load("C:/Users/zavol/Documents/zavGame/images/bonus.png").convert_alpha()

# Load music
pygame.mixer.music.load('C:/Users/zavol/Documents/zavGame/sounds/zav_music.mp3')
game_over_music = 'C:/Users/zavol/Documents/zavGame/sounds/game_over.mp3'
pygame.mixer.music.play(-1)

# Load sound effects
bonus_sound = pygame.mixer.Sound('C:/Users/zavol/Documents/zavGame/sounds/bonus.mp3')

# Player settings
player_scale = 0.5  # Scale down the player size
player_image = pygame.transform.scale(player_image, (int(player_image.get_width() * player_scale), int(player_image.get_height() * player_scale)))
player_rect = player_image.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Enemy settings
enemy_scale = 0.5  # Scale down the enemy size
enemy_image = pygame.transform.scale(enemy_image, (int(enemy_image.get_width() * enemy_scale), int(enemy_image.get_height() * enemy_scale)))

# Game variables
game_over = False
score = 0
player_speed = 5
enemy_speed = 3
bonus_speed = 5
player_speed_increase = 1

# Create lists for enemies and bonuses
enemies = []
bonuses = []

# Function to create a new enemy
def create_enemy():
    x = WIDTH
    y = random.randint(0, HEIGHT - enemy_image.get_height())
    enemy_rect = enemy_image.get_rect(topleft=(x, y))
    return enemy_rect

# Function to create a new bonus
def create_bonus():
    x = random.randint(0, WIDTH - bonus_image.get_width())
    y = -bonus_image.get_height()
    bonus_rect = bonus_image.get_rect(topleft=(x, y))
    return bonus_rect

# Main game loop
clock = pygame.time.Clock()
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
    player_rect.x = max(0, min(player_rect.x, WIDTH - player_rect.width))
    player_rect.y = max(0, min(player_rect.y, HEIGHT - player_rect.height))

    # Update player image for animation
    player_animation_frame_count += 1
    if player_animation_frame_count >= player_animation_speed:
        current_player_image_index = (current_player_image_index + 1) % len(player_images)
        player_image = player_images[current_player_image_index]
        player_image = pygame.transform.scale(player_image, (int(player_image.get_width() * player_scale), int(player_image.get_height() * player_scale)))
        player_animation_frame_count = 0

    # Create a new enemy randomly
    if random.random() < 0.01:
        enemies.append(create_enemy())

    # Create a new bonus randomly
    if random.random() < 0.005:
        bonuses.append(create_bonus())

    # Move enemies and check for collisions with player
    for enemy in enemies:
        enemy.x -= enemy_speed
        if enemy.colliderect(player_rect):
            game_over = True
        if enemy.right < 0:
            enemies.remove(enemy)

    # Move bonuses and check for collisions with player
    for bonus in bonuses:
        bonus.y += bonus_speed
        if bonus.colliderect(player_rect):
            score += 1
            player_speed += player_speed_increase
            bonuses.remove(bonus)
            bonus_sound.play()
        if bonus.top > HEIGHT:
            bonuses.remove(bonus)

    # Draw the background
    main_display.blit(background_image, (0, 0))

    # Draw the player
    main_display.blit(player_image, player_rect)

    # Draw the enemies
    for enemy in enemies:
        main_display.blit(enemy_image, enemy)

    # Draw the bonuses
    for bonus in bonuses:
        main_display.blit(bonus_image, bonus)

    # Display score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(topright=(WIDTH - 10, 10))
    main_display.blit(score_text, score_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Game over
pygame.mixer.music.stop()
pygame.mixer.music.load(game_over_music)
pygame.mixer.music.play()

font = pygame.font.Font(None, 36)
game_over_text = font.render("Game Over!", True, (255, 255, 255))
game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
main_display.blit(game_over_text, game_over_rect)
pygame.display.flip()

pygame.time.wait(2000)

pygame.quit()
