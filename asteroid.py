from circleshape import CircleShape
import pygame
from constants import ASTEROID_MIN_RADIUS
import random
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        
    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255),self.position,self.radius,2)
        
    def update(self, dt):
        self.position += self.velocity*dt
        
    def split(self,asteroids):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        angle = random.uniform(20,50)
        split1 = self.velocity.rotate(angle)*1.2
        split2 = self.velocity.rotate(-angle)*1.2 
        split_rad = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x,self.position.y,split_rad)
        asteroid2 = Asteroid(self.position.x,self.position.y,split_rad)
        asteroid1.velocity = split1
        asteroid2.velocity = split2
        asteroids.add(asteroid1)
        asteroids.add(asteroid2)