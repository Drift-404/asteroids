import pygame
import random
from constants import SCREEN_HEIGHT, SCREEN_WIDTH

class ShieldPickup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/shield_{i}.png").convert_alpha(),
                (48, 48)
            )
            for i in range(10) 
        ]
        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(random.randint(50, SCREEN_WIDTH - 50),
                                       random.randint(50, SCREEN_HEIGHT - 50))
        self.rect.center = self.position

        self.timer = 0
        self.frame_speed = 0.08 

    def update(self, dt, keys=None):
        self.timer += dt
        if self.timer >= self.frame_speed:
            self.timer = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.rect = self.image.get_rect(center=self.position)