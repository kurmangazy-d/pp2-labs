# ==========================================
# RACER GAME - improved version
# Added:
# 1) Levels
# 2) Scoreboard (saved to file)
# 3) Better difficulty scaling
# 4) Restart / game over screen
# ==========================================

import pygame
import sys
import random
import os
import json
from pygame.locals import *

pygame.init()
pygame.mixer.init()

# ------------------------------------------
# SETTINGS
# ------------------------------------------
FPS = 60
clock = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (210, 50, 50)
GREEN = (30, 160, 70)
YELLOW = (255, 215, 0)
DARK = (40, 40, 40)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES = os.path.join(BASE_DIR, "assets", "images")
SOUNDS = os.path.join(BASE_DIR, "assets", "sounds")
SCORE_FILE = os.path.join(BASE_DIR, "scoreboard.json")

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# ------------------------------------------
# FONTS
# ------------------------------------------
big_font = pygame.font.SysFont("Verdana", 42)
mid_font = pygame.font.SysFont("Verdana", 24)
small_font = pygame.font.SysFont("Verdana", 18)

# ------------------------------------------
# LOAD IMAGES
# ------------------------------------------
background = pygame.image.load(
    os.path.join(IMAGES, "AnimatedStreet.png")
).convert()

player_img = pygame.image.load(
    os.path.join(IMAGES, "Player.png")
).convert_alpha()

enemy_img = pygame.image.load(
    os.path.join(IMAGES, "Enemy.png")
).convert_alpha()

gold_coin = pygame.image.load(
    os.path.join(IMAGES, "coin.png")
).convert_alpha()

bronze_coin = pygame.image.load(
    os.path.join(IMAGES, "bronze.png")
).convert_alpha()

silver_coin = pygame.image.load(
    os.path.join(IMAGES, "silver.png")
).convert_alpha()

gold_coin = pygame.transform.scale(gold_coin, (40, 40))
silver_coin = pygame.transform.scale(silver_coin, (35, 35))
bronze_coin = pygame.transform.scale(bronze_coin, (30, 30))

# ------------------------------------------
# LOAD SOUNDS
# ------------------------------------------
crash_sound = pygame.mixer.Sound(
    os.path.join(SOUNDS, "crash.wav")
)

background_sound = pygame.mixer.Sound(
    os.path.join(SOUNDS, "background.wav")
)

# ------------------------------------------
# SCOREBOARD FUNCTIONS
# ------------------------------------------
def load_scoreboard():
    if not os.path.exists(SCORE_FILE):
        return []
    try:
        with open(SCORE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_scoreboard(data):
    with open(SCORE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def add_score(score, coins, level):
    board = load_scoreboard()
    board.append({
        "score": score,
        "coins": coins,
        "level": level
    })
    board.sort(key=lambda x: (x["score"], x["coins"]), reverse=True)
    board = board[:5]   # top 5 best results
    save_scoreboard(board)

# ------------------------------------------
# DRAW HELPERS
# ------------------------------------------
def draw_text(text, font, color, x, y, center=False):
    img = font.render(text, True, color)
    rect = img.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    DISPLAYSURF.blit(img, rect)

def draw_panel(score, coins, level, enemy_speed):
    pygame.draw.rect(DISPLAYSURF, WHITE, (0, 0, SCREEN_WIDTH, 70))
    pygame.draw.line(DISPLAYSURF, DARK, (0, 70), (SCREEN_WIDTH, 70), 2)

    draw_text(f"Score: {score}", small_font, BLACK, 10, 10)
    draw_text(f"Coins: {coins}", small_font, BLACK, 10, 35)
    draw_text(f"Level: {level}", small_font, BLACK, 150, 10)
    draw_text(f"Enemy speed: {enemy_speed}", small_font, BLACK, 150, 35)

def draw_scoreboard():
    board = load_scoreboard()

    panel_width = 300
    panel_height = 180
    panel_x = (SCREEN_WIDTH - panel_width) // 2
    panel_y = 180

    pygame.draw.rect(DISPLAYSURF, WHITE, (panel_x, panel_y, panel_width, panel_height), border_radius=12)
    pygame.draw.rect(DISPLAYSURF, DARK, (panel_x, panel_y, panel_width, panel_height), 2, border_radius=12)

    draw_text("TOP 5 SCORES", mid_font, BLACK, SCREEN_WIDTH // 2, panel_y + 25, center=True)

    if not board:
        draw_text("No scores yet", small_font, DARK, SCREEN_WIDTH // 2, panel_y + 80, center=True)
    else:
        y = panel_y + 60
        for i, item in enumerate(board, start=1):
            line = f"{i}. Score {item['score']} | Coins {item['coins']} | Lvl {item['level']}"
            draw_text(line, small_font, BLACK, panel_x + 15, y)
            y += 24

# ------------------------------------------
# CLASSES
# ------------------------------------------
class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.speed = speed
        self.reset_position()

    def reset_position(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def update(self):
        self.rect.move_ip(0, self.speed)

    def respawn(self):
        self.reset_position()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, 520)
        self.speed = 6

    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT] or pressed_keys[K_a]:
            self.rect.move_ip(-self.speed, 0)

        if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
            self.rect.move_ip(self.speed, 0)

        # keep inside screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Coin(pygame.sprite.Sprite):
    def __init__(self, fall_speed):
        super().__init__()

        # weight and image
        self.weight = random.choice([1, 2, 3])

        if self.weight == 1:
            self.image = bronze_coin
        elif self.weight == 2:
            self.image = silver_coin
        else:
            self.image = gold_coin

        self.rect = self.image.get_rect()
        self.fall_speed = fall_speed
        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-150, -40)
        )

    def update(self):
        self.rect.move_ip(0, self.fall_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# ------------------------------------------
# GAME FUNCTIONS
# ------------------------------------------
def create_game():
    game_data = {
        "score": 0,
        "coins": 0,
        "level": 1,
        "enemy_speed": 5,
        "coin_speed": 4,
        "level_step": 5,   # every 5 score -> next level
        "running": True
    }

    player = Player()
    enemy = Enemy(game_data["enemy_speed"])

    enemies = pygame.sprite.Group()
    enemies.add(enemy)

    coins = pygame.sprite.Group()

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    all_sprites.add(enemy)

    return game_data, player, enemy, enemies, coins, all_sprites

def check_level_up(data):
    new_level = data["score"] // data["level_step"] + 1
    if new_level > data["level"]:
        data["level"] = new_level
        data["enemy_speed"] += 1
        data["coin_speed"] += 0.5

def game_over_screen(score, coins, level):
    add_score(score, coins, level)

    while True:
        DISPLAYSURF.blit(background, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        DISPLAYSURF.blit(overlay, (0, 0))

        draw_text("GAME OVER", big_font, RED, SCREEN_WIDTH // 2, 90, center=True)
        draw_text(f"Score: {score}", mid_font, WHITE, SCREEN_WIDTH // 2, 140, center=True)
        draw_text(f"Coins: {coins}", mid_font, WHITE, SCREEN_WIDTH // 2, 170, center=True)
        draw_text(f"Level reached: {level}", mid_font, WHITE, SCREEN_WIDTH // 2, 200, center=True)

        draw_scoreboard()

        draw_text("Press R to restart", small_font, WHITE, SCREEN_WIDTH // 2, 500, center=True)
        draw_text("Press ESC to quit", small_font, WHITE, SCREEN_WIDTH // 2, 530, center=True)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN:
                if event.key == K_r:
                    return
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# ------------------------------------------
# EVENTS
# ------------------------------------------
SPAWN_COIN = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_COIN, 1500)

# ------------------------------------------
# MAIN LOOP
# ------------------------------------------
while True:
    game_data, P1, E1, enemies, coins, all_sprites = create_game()

    background_sound.play(-1)

    while game_data["running"]:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SPAWN_COIN:
                new_coin = Coin(game_data["coin_speed"])
                coins.add(new_coin)
                all_sprites.add(new_coin)

        # update enemy speed according to level
        E1.speed = game_data["enemy_speed"]

        # draw background
        DISPLAYSURF.blit(background, (0, 0))

        # update and draw sprites
        for entity in all_sprites:
            entity.update()
            DISPLAYSURF.blit(entity.image, entity.rect)

        # if enemy passed screen -> score +1
        if E1.rect.top > SCREEN_HEIGHT:
            game_data["score"] += 1
            E1.respawn()
            check_level_up(game_data)

        # collect coins
        collected = pygame.sprite.spritecollide(P1, coins, True)
        if collected:
            for coin in collected:
                game_data["coins"] += coin.weight

        # collision with enemy
        if pygame.sprite.spritecollideany(P1, enemies):
            background_sound.stop()
            crash_sound.play()
            pygame.time.delay(500)
            game_data["running"] = False

        # panel
        draw_panel(
            game_data["score"],
            game_data["coins"],
            game_data["level"],
            game_data["enemy_speed"]
        )

        pygame.display.update()
        clock.tick(FPS)

    game_over_screen(
        game_data["score"],
        game_data["coins"],
        game_data["level"]
    )