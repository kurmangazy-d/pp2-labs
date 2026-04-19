#импорты
import pygame
import sys
import random
import time
import os
from pygame.locals import *


pygame.init()


FPS = 60
FramePerSec = pygame.time.Clock()

#цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)

#окно
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#параметры
SPEED = 5
ENEMY_SPEED = 5
SCORE = 0
COINS = 0
PICKED = 0
N = 5                 

#шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

#пути
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

IMAGES = os.path.join(BASE_DIR, "assets", "images")
SOUNDS = os.path.join(BASE_DIR, "assets", "sounds")

#грузим фото
background = pygame.image.load(
    os.path.join(IMAGES, "AnimatedStreet.png")
)

player_img = pygame.image.load(
    os.path.join(IMAGES, "Player.png")
)

enemy_img = pygame.image.load(
    os.path.join(IMAGES, "Enemy.png")
)

gold_coin = pygame.image.load(
    os.path.join(IMAGES, "coin.png")
)

bronze_coin = pygame.image.load(
    os.path.join(IMAGES, "bronze.png")
)

silver_coin = pygame.image.load(
    os.path.join(IMAGES, "silver.png")
)

#размеры для монет
gold_coin = pygame.transform.scale(gold_coin, (40, 40))
silver_coin = pygame.transform.scale(silver_coin, (35, 35))
bronze_coin = pygame.transform.scale(bronze_coin, (30, 30))

#грузим звук
crash_sound = pygame.mixer.Sound(
    os.path.join(SOUNDS, "crash.wav")
)

background_sound = pygame.mixer.Sound(
    os.path.join(SOUNDS, "background.wav")
)

background_sound.play(-1)

#окно
DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Racer")

#классы
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

        self.rect.move_ip(0, ENEMY_SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1

            self.rect.top = 0
            self.rect.center = (
                random.randint(40, SCREEN_WIDTH - 40),
                0
            )


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


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        #рандом
        self.weight = random.choice([1, 2, 3])

        
        if self.weight == 1:
            self.image = bronze_coin

        elif self.weight == 2:
            self.image = silver_coin

        else:
            self.image = gold_coin

        self.rect = self.image.get_rect()

        self.rect.center = (
            random.randint(40, SCREEN_WIDTH - 40),
            random.randint(-150, -40)
        )

    def move(self):
        self.rect.move_ip(0, SPEED)

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

#создаем объекты
P1 = Player()
E1 = Enemy()

#группы
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

#события
INC_SPEED = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2

pygame.time.set_timer(INC_SPEED, 1000)
pygame.time.set_timer(SPAWN_COIN, 2000)

#главный цикл
while True:

    for event in pygame.event.get():

        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        #скорость дороги
        if event.type == INC_SPEED:
            SPEED += 0.2

        #спамним рандомный коин
        if event.type == SPAWN_COIN:
            new_coin = Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)

    #фон
    DISPLAYSURF.blit(background, (0, 0))

    #наш счкт
    score_text = font_small.render(
        "Score: " + str(SCORE),
        True,
        BLACK
    )
    DISPLAYSURF.blit(score_text, (10, 10))

    #текст для коина
    coin_text = font_small.render(
        "Coins: " + str(COINS),
        True,
        BLACK
    )
    coin_rect = coin_text.get_rect(
        topright=(SCREEN_WIDTH - 10, 10)
    )
    DISPLAYSURF.blit(coin_text, coin_rect)

    
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    #collision
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

    #коллекшн коина
    collected = pygame.sprite.spritecollide(
        P1,
        coins,
        True
    )

    if collected:

        for coin in collected:
            COINS += coin.weight
            PICKED += 1

            #повышается скорость
            if PICKED % N == 0:
                ENEMY_SPEED += 1

    pygame.display.update()
    FramePerSec.tick(FPS)