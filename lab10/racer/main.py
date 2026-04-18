# Imports
import pygame
import sys
import random
import time
import os
from pygame.locals import *

# -------------------------
# Initialize pygame
# -------------------------
pygame.init()

# -------------------------
# FPS
# -------------------------
FPS = 60
FramePerSec = pygame.time.Clock()

# -------------------------
# Colors
# -------------------------
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# -------------------------
# Screen settings
# -------------------------
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# -------------------------
# Game variables
# -------------------------
SPEED = 5
SCORE = 0
COINS = 0

# -------------------------
# Fonts
# -------------------------
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# -------------------------
# Paths
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGES = os.path.join(BASE_DIR, "assets", "images")
SOUNDS = os.path.join(BASE_DIR, "assets", "sounds")

# -------------------------
# Load images
# -------------------------
background = pygame.image.load(
    os.path.join(IMAGES, "AnimatedStreet.png")
)

player_img = pygame.image.load(
    os.path.join(IMAGES, "Player.png")
)

enemy_img = pygame.image.load(
    os.path.join(IMAGES, "Enemy.png")
)

coin_img = pygame.image.load(
    os.path.join(IMAGES, "Coin.png")
)

coin_img = pygame.transform.scale(coin_img, (35, 35))

# -------------------------
# Load sounds
# -------------------------
crash_sound = pygame.mixer.Sound(
    os.path.join(SOUNDS, "crash.wav")
)

background_sound = pygame.mixer.Sound(
    os.path.join(SOUNDS, "background.wav")
)

background_sound.play(-1)   # infinite loop

# -------------------------
# Create screen
# -------------------------
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# -------------------------
# Enemy class
# -------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = enemy_img
        self.rect = self.image.get_rect()

        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            0
        )

    def move(self):
        global SCORE

        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1

            self.rect.top = 0
            self.rect.center = (
                random.randint(40, SCREEN_WIDTH - 40),
                0
            )

# -------------------------
# Player class
# -------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# -------------------------
# Coin class
# -------------------------
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = coin_img
        self.rect = self.image.get_rect()

        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-150, -40)
        )

    def move(self):
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# -------------------------
# Create objects
# -------------------------
P1 = Player()
E1 = Enemy()

# Groups
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# -------------------------
# Events
# -------------------------
INC_SPEED = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2

pygame.time.set_timer(INC_SPEED, 1000)
pygame.time.set_timer(SPAWN_COIN, 2200)

# -------------------------
# Main loop
# -------------------------
while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == INC_SPEED:
            SPEED += 0.2

        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    # Draw background
    DISPLAYSURF.blit(background, (0, 0))

    # Show score
    score_text = font_small.render(
        "Score: " + str(SCORE),
        True,
        BLACK
    )

    DISPLAYSURF.blit(score_text, (10, 10))

    # Show coins top right
    coin_text = font_small.render(
        "Coins: " + str(COINS),
        True,
        BLACK
    )

    coin_rect = coin_text.get_rect(
        topright=(SCREEN_WIDTH - 10, 10)
    )

    DISPLAYSURF.blit(coin_text, coin_rect)

    # Move / draw sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Collision with enemy
    if pygame.sprite.spritecollideany(P1, enemies):

        background_sound.stop()
        crash_sound.play()

        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        time.sleep(2)

        pygame.quit()
        sys.exit()

    # Collect coins
    collected = pygame.sprite.spritecollide(
        P1,
        coins,
        True
    )

    if collected:
        COINS += len(collected)

    pygame.display.update()
    FramePerSec.tick(FPS)