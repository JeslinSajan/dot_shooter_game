import pygame
import sys
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dot Shooter Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Player variables
player_width = 50
player_height = 50
player_x = (SCREEN_WIDTH - player_width) // 2
player_y = SCREEN_HEIGHT - player_height - 10
player_speed = 10

# Bullet variables
bullet_width = 5
bullet_height = 10
bullet_speed = 15
bullets = []

# Opponent (New)
opponent_radius = 25
opponent_speed = 5
opponents = []

# Game variables
score = 0
high_score = 0  # New
time_limit = 30
current_time = 0

# Fonts
font = pygame.font.Font(None, 36)

def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, player_width, player_height])

def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, bullet_width, bullet_height])

def draw_opponent(x, y):
    pygame.draw.circle(screen, RED, (x, y), opponent_radius)

def display_score(score):
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

def display_high_score(high_score):  # New
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    screen.blit(high_score_text, (10, 50))

def display_time(time_left):
    time_text = font.render("Time: " + str(time_left), True, WHITE)
    screen.blit(time_text, (SCREEN_WIDTH - 120, 10))

# New functions for pause and settings
def display_pause():
    pause_text = font.render("Paused", True, GREEN)
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 20))

def display_settings(speed_factor):
    settings_text = font.render("Settings - Speed Factor: " + str(speed_factor), True, GREEN)
    screen.blit(settings_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))

# New function to initialize opponents
def initialize_opponents():
    for _ in range(5):  # Adjust the number of opponents as needed
        opponents.append([random.randint(0, SCREEN_WIDTH - 2 * opponent_radius), -opponent_radius])

# Initialize opponents at the beginning
initialize_opponents()

# Game loop
running = True
paused = False  # New
settings_mode = False  # New
speed_factor = 1.0  # New

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if not settings_mode:  # Toggle pause if not in settings mode
                    paused = not paused
            elif event.key == K_s and not paused:  # Enter settings mode
                settings_mode = not settings_mode

    if not paused and not settings_mode:
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        if keys[K_SPACE]:
            bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y - bullet_height])

        # Move bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed

        # Move opponents (New)
        for opponent in opponents:
            opponent[1] += int(opponent_speed * speed_factor)
            if opponent[1] > SCREEN_HEIGHT:
                opponents.remove(opponent)
                opponents.append([random.randint(0, SCREEN_WIDTH - 2 * opponent_radius), -opponent_radius])

        # Check for collisions with opponents (New)
        for bullet in bullets:
            for opponent in opponents:
                if (
                    opponent[0] - opponent_radius < bullet[0] < opponent[0] + opponent_radius
                    and opponent[1] - opponent_radius < bullet[1] < opponent[1] + opponent_radius
                ):
                    bullets.remove(bullet)
                    opponents.remove(opponent)
                    opponents.append([random.randint(0, SCREEN_WIDTH - 2 * opponent_radius), -opponent_radius])
                    score += 1

        # Remove bullets that go off the screen
        bullets = [bullet for bullet in bullets if bullet[1] > 0]

        # Update time
        current_time += 1 / FPS

        # Draw everything
        screen.fill((0, 0, 0))
        draw_player(player_x, player_y)
        display_score(score)
        display_high_score(high_score)  # New
        display_time(max(0, int(time_limit - current_time)))

        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])

        for opponent in opponents:
            draw_opponent(opponent[0], opponent[1])

    # Additional features for pause and settings mode
    if paused:
        display_pause()
    elif settings_mode:
        display_settings(speed_factor)

    pygame.display.flip()
    clock.tick(FPS)

    # Check for game over
    if current_time > time_limit:
        if score > high_score:
            high_score = score  # Update high score if necessary
        # Reset game variables for a new game
        current_time = 0
        score = 0
        # Reset opponents and bullets
        initialize_opponents()
        bullets = []

# After the game loop
pygame.quit()
sys.exit()

