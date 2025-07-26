import pygame
from constants import SCREEN_HEIGHT,SCREEN_WIDTH
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        pass

    def update(self, dt, keys=None):
        pass

    def check_collision(self, other):
        return pygame.math.Vector2.distance_to(self.position, other.position) <= self.radius + other.radius

    def wrap_pos(self):
        self.position.x %= SCREEN_WIDTH
        self.position.y %= SCREEN_HEIGHT