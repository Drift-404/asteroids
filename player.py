from circleshape import CircleShape
import pygame
from constants import *

class Player(CircleShape):
    def __init__(self, x, y, shots_group):
        super().__init__(x, y, PLAYER_RADIUS)
        self.shots_group = shots_group
        self.rotation = 0
        self.shoot_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        new_shot = Shot(self.position, SHOT_RADIUS)
        new_shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
        self.shots_group.add(new_shot)
        Player.containers[1].add(new_shot)
        Player.containers[0].add(new_shot)
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN

    def update(self, dt, keys=None):
        if keys:
            if keys[pygame.K_a]:
                self.rotate(-dt)
            if keys[pygame.K_d]:
                self.rotate(dt)
            if keys[pygame.K_w]:
                self.move(dt)
            if keys[pygame.K_s]:
                self.move(-dt)
            if keys[pygame.K_SPACE]:
                self.shoot()
        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            self.shoot_timer = max(0, self.shoot_timer)

class Shot(CircleShape):
    def __init__(self, pos, radius):
        super().__init__(pos.x, pos.y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.position.x), int(self.position.y)), self.radius)

    def update(self, dt, keys=None):
        self.position += self.velocity * dt
        if not (0 <= self.position.x <= SCREEN_WIDTH and 0 <= self.position.y <= SCREEN_HEIGHT):
            self.kill()
