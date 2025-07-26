from circleshape import CircleShape
import pygame
from constants import ASTEROID_MIN_RADIUS
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.original_image = pygame.image.load("assets/asteroid.png").convert_alpha()
        size = int(self.radius * 2)
        self.original_image = pygame.transform.scale(self.original_image, (size, size))
        
        self.image = self.original_image
        self.rotation = random.uniform(0, 360)

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.original_image, self.rotation)
        rect = rotated_image.get_rect(center=self.position)
        screen.blit(rotated_image, rect)

    def update(self, dt, keys=None):
        self.position += self.velocity * dt
        self.rotation += 20 * dt
        self.wrap_pos()
    def split(self, group):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        angle = random.uniform(20, 50)
        split1 = self.velocity.rotate(angle) * 1.2
        split2 = self.velocity.rotate(-angle) * 1.2
        split_rad = self.radius - ASTEROID_MIN_RADIUS
        offset = pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))
        asteroid1 = Asteroid(self.position.x + offset.x, self.position.y + offset.y, split_rad)
        asteroid2 = Asteroid(self.position.x - offset.x, self.position.y - offset.y, split_rad)
        asteroid1.velocity = split1
        asteroid2.velocity = split2
        group.add(asteroid1)
        group.add(asteroid2)
