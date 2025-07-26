from circleshape import CircleShape
import pygame
from constants import *
import math
from utils import load_shield_frames

class Player(CircleShape):
    def __init__(self, x, y, shots_group):
        super().__init__(x, y, PLAYER_RADIUS)
        self.shots_group = shots_group
        self.rotation = 0
        self.shoot_timer = 0
        self.velocity = pygame.Vector2(0, 0)

        self.invulnerable = False
        self.invul_timer = 0.0
        self.from_shield = False
        
        self.image_idle = pygame.image.load("assets/ship_idle.png").convert_alpha()
        self.image_thrust = pygame.image.load("assets/ship_thrust.png").convert_alpha()
        self.image_idle = pygame.transform.scale(self.image_idle, (40, 40))
        self.image_thrust = pygame.transform.scale(self.image_thrust, (40, 40))

        self.original_image = self.image_idle
        self.image = self.original_image
        self.rect = self.image.get_rect(center=self.position)

        self.is_thrusting = False  
        
        self.shield_active = False
        self.shield_timer = 0
        
        self.shield_sprite = load_shield_frames(64) 
        self.shield_active = False
        self.shield_index = 0
        self.shield_timer = 0
        self.shield_timer_accum = 0
        self.shield_hits = 0
        
        self.default_cooldown = PLAYER_SHOOT_COOLDOWN
        self.current_cooldown = self.default_cooldown
        self.rapid_fire_active = False
        self.rapid_fire_timer = 0
        

    def draw(self, screen):
        self.original_image = self.image_thrust if self.is_thrusting else self.image_idle

        
        self.image = pygame.transform.rotate(self.original_image, -self.rotation + 180)
        self.rect = self.image.get_rect(center=self.position)
        
        if self.rapid_fire_active:
            t = pygame.time.get_ticks() / 100  
            pulse = 100 + math.sin(t) * 80     
            glow_size = 60 + math.sin(t) * 10 

            glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
            pygame.draw.circle(
                glow_surface,
                (255, 90, 0, int(pulse)),       
                (glow_size // 2, glow_size // 2),
                glow_size // 2
            )
            screen.blit(glow_surface, self.position - pygame.Vector2(glow_size // 2))
            
        if self.invulnerable and not self.from_shield:
            current_time = pygame.time.get_ticks()
            if (current_time // 100) % 2 == 0:
                return  
        else:
            self.image.set_alpha(255)
        
        if self.shield_active:
            shield_img = self.shield_sprite[self.shield_index]
            shield_rect = shield_img.get_rect(center=self.position)
            screen.blit(shield_img, shield_rect)
           

        screen.blit(self.image, self.rect)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt, direction=1):
        forward = pygame.Vector2(0, -1).rotate(self.rotation)  
        acceleration = forward * PLAYER_ACCELERATION * direction
        self.velocity += acceleration * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        new_shot = Shot(self.position, SHOT_RADIUS,self.rotation)
        self.shots_group.add(new_shot)
        Player.containers[1].add(new_shot)
        Player.containers[0].add(new_shot)
        self.shoot_timer = self.current_cooldown

    def update(self, dt, keys=None):
        self.is_thrusting = False

        if keys:
            if keys[pygame.K_a]:
                self.rotate(-dt)
            if keys[pygame.K_d]:
                self.rotate(dt)
            if keys[pygame.K_w]:
                self.move(dt, direction=1)
                self.is_thrusting = True
            if keys[pygame.K_s]:
                self.move(dt, direction=-1)
            if keys[pygame.K_SPACE]:
                self.shoot()

        if self.shoot_timer > 0:
            self.shoot_timer -= dt
            self.shoot_timer = max(0, self.shoot_timer)
        
        if self.invulnerable and not self.from_shield:
            self.invul_timer -= dt
            if self.invul_timer <= 0:
                self.invulnerable = False

        
        if self.shield_active:
            self.shield_timer -= dt
            self.shield_timer_accum += dt
            if self.shield_timer_accum >= 0.08:
                self.shield_timer_accum = 0
                self.shield_index = (self.shield_index + 1) % len(self.shield_sprite)
            if self.shield_timer <= 0:
                self.shield_active = False
                self.invulnerable = False
                
        if self.rapid_fire_active:
            self.rapid_fire_timer -= dt
            if self.rapid_fire_timer <= 0:
                self.rapid_fire_active = False
                self.current_cooldown = self.default_cooldown

        self.position += self.velocity * dt
        self.velocity *= 0.9854 
        self.wrap_pos()


class Shot(CircleShape):
    def __init__(self, pos, radius, rotation):
        super().__init__(pos.x, pos.y, radius)

        
        base_image = pygame.image.load("assets/laser_bolt.png").convert_alpha()
        base_image = pygame.transform.scale(base_image, (24, 12))  

       
        direction = pygame.Vector2(0, -1).rotate(rotation)
        self.velocity = direction * PLAYER_SHOOT_SPEED


        angle = -rotation  
        self.image = pygame.transform.rotate(base_image, angle)
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, keys=None):
        self.position += self.velocity * dt
        self.rect.center = self.position
        if not (0 <= self.position.x <= SCREEN_WIDTH and 0 <= self.position.y <= SCREEN_HEIGHT):
            self.kill()
        self.wrap_pos()

    def draw(self, screen):
        screen.blit(self.image, self.rect)

