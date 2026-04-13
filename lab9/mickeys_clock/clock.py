import pygame
import datetime
import os


class MickeyClock:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        base_dir = os.path.dirname(__file__)
        image_dir = os.path.join(base_dir, "images")

        self.background = pygame.image.load(
            os.path.join(image_dir, "clock.png")
        ).convert_alpha()

        self.left_hand = pygame.image.load(
            os.path.join(image_dir, "left_hand.png")
        ).convert_alpha()

        self.right_hand = pygame.image.load(
            os.path.join(image_dir, "right_hand.png")
        ).convert_alpha()

        self.background = pygame.transform.scale(
            self.background, (width, height)
        )

        self.left_hand = pygame.transform.scale(
            self.left_hand, (width, height)
        )

        self.right_hand = pygame.transform.scale(
            self.right_hand, (width, height)
        )

        self.center = (width // 2, height // 2)

        self.left_angle = 0
        self.right_angle = 0

    def update(self):
        now = datetime.datetime.now()

        minutes = now.minute
        seconds = now.second

        self.right_angle = -(minutes + seconds / 60) * 6
        self.left_angle = -seconds * 6

    def draw(self, screen):
        screen.blit(self.background, (0, 0))

        rotated_right = pygame.transform.rotate(
            self.right_hand, self.right_angle
        )

        rotated_left = pygame.transform.rotate(
            self.left_hand, self.left_angle
        )

        right_rect = rotated_right.get_rect(center=self.center)
        left_rect = rotated_left.get_rect(center=self.center)

        screen.blit(rotated_right, right_rect)
        screen.blit(rotated_left, left_rect)