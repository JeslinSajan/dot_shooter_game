import pygame
import sys
import random
from pygame.locals import *
from math import hypot

# Initializing Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Creating the game window
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
can_shoot = True

# Opponent variables
opponent_radius = 25
opponent_speed = 5
opponents = []

# Game variables
score = 0
high_score = 0
time_limit = 30
current_time = 0

# Level variables
level = 1
level_time = 0
level_duration = 30  # seconds per level
speed_factor = 1.0

# Fonts
font = pygame.font.Font(None, 36)

# Drawing functions
def draw_player(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, player_width, player_height])

def draw_bullet(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, bullet_width, bullet_height])

def draw_opponent(x, y):
    pygame.draw.circle(screen, RED, (x, y), opponent_radius)

def display_score(score):
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

def display_high_score(high_score):
    high_score_text = font.render("High Score: " + str(high_score), True, WHITE)
    screen.blit(high_score_text, (10, 50))

def display_time(time_left):
    time_text = font.render("Time: " + str(time_left), True, WHITE)
    screen.blit(time_text, (SCREEN_WIDTH - 120, 10))

def display_level(level):
    level_text = font.render("Level: " + str(level), True, WHITE)
    screen.blit(level_text, (SCREEN_WIDTH - 120, 50))

def display_pause():
    pause_text = font.render("Paused", True, GREEN)
    screen.blit(pause_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 - 20))

def display_settings(speed_factor):
    settings_text = font.render("Settings - Speed Factor: " + str(round(speed_factor, 2)), True, GREEN)
    screen.blit(settings_text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))

def initialize_opponents():
    opponents.clear()
    for _ in range(5):
        opponents.append([random.randint(0, SCREEN_WIDTH - 2 * opponent_radius), -opponent_radius])

# Initialize opponents
initialize_opponents()

# Game loop
running = True
paused = False
settings_mode = False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                if not settings_mode:
                    paused = not paused
            elif event.key == K_s and not paused:
                settings_mode = not settings_mode

    if not paused and not settings_mode:
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed
        if keys[K_SPACE] and can_shoot:
            bullets.append([player_x + player_width // 2 - bullet_width // 2, player_y - bullet_height])
            can_shoot = False
        if not keys[K_SPACE]:
            can_shoot = True

        # Move bullets
        for bullet in bullets:
            bullet[1] -= bullet_speed

        # Move opponents safely
        new_opponents = []
        for opponent in opponents:
            opponent[1] += int(opponent_speed * speed_factor)
            if opponent[1] <= SCREEN_HEIGHT:
                new_opponents.append(opponent)
            else:
                # Respawn off-screen
                new_opponents.append([random.randint(0, SCREEN_WIDTH - 2 * opponent_radius), -opponent_radius])
        opponents = new_opponents

        # Check collisions
        for bullet in bullets[:]:
            for opponent in opponents[:]:
                distance = hypot(bullet[0] - opponent[0], bullet[1] - opponent[1])
                if distance < opponent_radius:
                    bullets.remove(bullet)
                    opponents.remove(opponent)
                    opponents.append([random.randint(0, SCREEN_WIDTH - 2 * opponent_radius), -opponent_radius])
                    score += 1
                    break

        # Remove bullets off-screen
        bullets = [bullet for bullet in bullets if bullet[1] > 0]

        # Update timers
        current_time += 1 / FPS
        level_time += 1 / FPS

        # Level up
        if level_time >= level_duration:
            level += 1
            level_time = 0
            opponent_speed += 1
            speed_factor += 0.1
            opponents.append([random.randint(0, SCREEN_WIDTH - 2 * opponent_radius), -opponent_radius])

        # Draw everything
        screen.fill((0, 0, 0))
        draw_player(player_x, player_y)
        display_score(score)
        display_high_score(high_score)
        display_time(max(0, int(time_limit - current_time)))
        display_level(level)

        for bullet in bullets:
            draw_bullet(bullet[0], bullet[1])
        for opponent in opponents:
            draw_opponent(opponent[0], opponent[1])

    # Pause and settings
    if paused:
        display_pause()
    elif settings_mode:
        display_settings(speed_factor)

    pygame.display.flip()
    clock.tick(FPS)

    # Game over check
    if current_time > time_limit:
        if score > high_score:
            high_score = score
        # Reset game
        current_time = 0
        level_time = 0
        score = 0
        level = 1
        opponent_speed = 5
        speed_factor = 1.0
        initialize_opponents()
        bullets = []

# Quit
pygame.quit()
sys.exit()