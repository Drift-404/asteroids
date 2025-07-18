from circleshape import CircleShape
import pygame
from constants import PLAYER_RADIUS,PLAYER_TURN_SPEED,PLAYER_SPEED,SHOT_RADIUS,PLAYER_SHOOT_SPEED,PLAYER_SHOOT_COOLDOWN
PLAYER_SHOOT_COOLDOWN = 0.2

class Player(CircleShape):
    def __init__(self, x, y,shots_group):
        super().__init__(x, y,PLAYER_RADIUS)
        self.shots_group = shots_group
        self.rotation = 0
        self.shoot_timer = 0
        
        
        
    
# in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self,screen):
    
        pygame.draw.polygon(screen,(255,255,255),self.triangle(),2)
        
    def rotate(self,dt):
        self.rotation += PLAYER_TURN_SPEED*dt
    
    def update(self, dt):
        keys = pygame.key.get_pressed()

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
            if self.shoot_timer < 0:
                self.shoot_timer = 0
                
            
    def move(self,dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        
    def shoot(self):
        if self.shoot_timer > 0:
            return
        new_shot = Shot(self.position,SHOT_RADIUS)
        initial_vector = pygame.math.Vector2(0,1)
        rotated_vector = initial_vector.rotate(self.rotation)
        final_velocity = rotated_vector * PLAYER_SHOOT_SPEED
        new_shot.velocity = final_velocity
        self.shots_group.add(new_shot)
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN
        
        

class Shot(CircleShape):
    def __init__(self, pos, radius,velocity = pygame.math.Vector2(0,0)):
        super().__init__(pos, radius,1)
        
    def draw(self, screen):
        pygame.draw.circle(screen,(255,255,255), (int(self.position.x), int(self.position.y)),self.radius)
        
    def update(self,dt):
        keys = pygame.key.get_pressed()
        self.position += self.velocity*dt