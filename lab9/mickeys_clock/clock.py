import pygame
import datetime
import os

class MickeyClock:
    def __init__(self, screen, center):
        self.screen = screen
        self.center = center

        #руки микки
        img_path = os.path.join(os.path.dirname(__file__), "images", "mickey_hand.png")
        self.hand_img = pygame.image.load(img_path).convert_alpha()

        #две версии рук
        self.minute_hand = pygame.transform.smoothscale(self.hand_img, (30, 180))  # длинная
        self.second_hand = pygame.transform.smoothscale(self.hand_img, (25, 150))  # короче

        #создаем центр
        self.minute_offset = self.minute_hand.get_rect(center=(0, self.minute_hand.get_height()//2))
        self.second_offset = self.second_hand.get_rect(center=(0, self.second_hand.get_height()//2))

    def draw_hand(self, hand_img, angle):
        #рука вращается
        rotated = pygame.transform.rotate(hand_img, -angle)
        rect = rotated.get_rect(center=self.center)
        self.screen.blit(rotated, rect.topleft)

    def update(self):
        now = datetime.datetime.now()
        seconds = now.second
        minutes = now.minute

        #угол для каждой руки
        seconds_angle = (seconds / 60) * 360
        minutes_angle = (minutes / 60) * 360

        #руки рисуем
        self.draw_hand(self.second_hand, seconds_angle)
        self.draw_hand(self.minute_hand, minutes_angle)