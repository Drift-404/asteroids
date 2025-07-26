import pygame
import sys
import random
from constants import *
from player import Player, Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
from explosion_vfx import Explosion
from shield import ShieldPickup

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
    background = pygame.image.load("assets/space_bg1.png").convert()
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    nebula_overlay = pygame.image.load("assets/Nebula3.jpg").convert_alpha()
    nebula_overlay = pygame.transform.scale(nebula_overlay, (SCREEN_WIDTH, SCREEN_HEIGHT ))
    nebula_overlay.set_alpha(80)
    import random

    import math

    stars = []
    for _ in range(150):
        x = random.uniform(0, SCREEN_WIDTH)
        y = random.uniform(0, SCREEN_HEIGHT)
        radius = random.choice([1, 1, 2])  
        depth = random.uniform(0.2, 1.0) 
        base_brightness = random.randint(180, 225)
        twinkle_speed = random.uniform(1.0, 2.5)
        offset = random.uniform(0, math.pi * 2)
        stars.append({
            'pos': pygame.Vector2(x, y),
            'r': radius,
            'depth': depth,
            'base': base_brightness,
            'speed': twinkle_speed,
            'offset': offset
        })


    pygame.display.set_caption("Asteroids")
    font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 35)
    clock = pygame.time.Clock()
    heart_image = pygame.image.load("assets/heart.png").convert_alpha() 
    heart_image = pygame.transform.scale(heart_image, (32, 32))
    dimmed_heart = heart_image.copy()
    dimmed_heart.fill((100, 100, 100, 255), special_flags=pygame.BLEND_RGBA_MULT)
    nebula_offset = pygame.Vector2(0,0)
    score = 0
    last_score = -1
    lives = 3
    player_dead = False
    respawn_timer = 0
    powerup_spawn_score = 750
    next_powerup_at = powerup_spawn_score
    rapid_spawn_score = 1000
    next_rapid_at = rapid_spawn_score
    
    score_x, score_y = 30,30
    score_text = font.render(f"SCORE: {score}", True, (255, 255, 255))

    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    explosions = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    effects = pygame.sprite.Group()
    rapid_powerups = pygame.sprite.Group()
    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroidfield = AsteroidField()
    asteroidfield.asteroid_group = asteroids

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots)
    last_player_pos = player.position.copy()
    
    

    while True:
        dt = clock.tick(60)/1000
        keys = pygame.key.get_pressed()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
        for powerup in powerups:
            if player.rect.colliderect(powerup.rect):
                powerup.kill()
                player.shield_active = True
                player.shield_timer = 8.0
                player.from_shield = True
                player.invulnerable = True
                player.shield_index = 0
                player.shield_timer_accum = 0
                player.shield_hits = 4
                
        for p in rapid_powerups:
            if not p.activated and player.rect.colliderect(p.rect):
                p.activate()
                player.rapid_fire_active = True
                player.rapid_fire_timer = 5.0
                player.current_cooldown = 0.05

        screen.blit(background, (0, 0))
        now = pygame.time.get_ticks() / 1000
        movement = player.position - last_player_pos
        for star in stars:
    
            star['pos'] -= movement * star['depth'] * 0.2  

    
            if star['pos'].x < 0: star['pos'].x += SCREEN_WIDTH
            if star['pos'].x > SCREEN_WIDTH: star['pos'].x -= SCREEN_WIDTH
            if star['pos'].y < 0: star['pos'].y += SCREEN_HEIGHT
            if star['pos'].y > SCREEN_HEIGHT: star['pos'].y -= SCREEN_HEIGHT

    
            brightness = star['base'] + math.sin(now * star['speed'] + star['offset']) * 100
            brightness = max(0, min(255, int(brightness)))
            color = (brightness, brightness, brightness)

            # Glow effect: draw a faint, larger circle behind
            glow_color = (color[0], color[1], color[2], 40)  # Low alpha glow
            glow_surface = pygame.Surface((10, 10), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (5, 5), 5)
            screen.blit(glow_surface, (int(star['pos'].x) - 5, int(star['pos'].y) - 5))

        
            pygame.draw.circle(screen, color, (int(star['pos'].x), int(star['pos'].y)), star['r'])
        nebula_offset += pygame.Vector2(7,3)*dt
        screen.blit(nebula_overlay, (-200 + int(nebula_offset.x), -100 + int(nebula_offset.y)))
        
        dim_overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        dim_overlay.set_alpha(30) 
        dim_overlay.fill((0, 0, 0))
        screen.blit(dim_overlay, (0, 0))
        for effect in effects:
            effect.draw(screen)
        explosions.update(dt)
        last_player_pos = player.position.copy()
        updatable.update(dt,keys if not player_dead else None)
        effects.update(dt)
        
        powerups.update(dt)
        for powerup in powerups:
            screen.blit(powerup.image, powerup.rect)
            
        rapid_powerups.update(dt)
        for p in rapid_powerups:
            screen.blit(p.image, p.rect)
        
        
        if player_dead:
            respawn_timer -= dt
            if respawn_timer <= 0:
                player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots)
                player.invulnerable = True
                player.from_shield = False
                player.invul_timer = 2.0 
                player_dead = False

                
        
                
        for sprite in drawable:
            sprite.draw(screen)
        for explosion in explosions:
            explosion.draw(screen)
        if not player_dead:
            for asteroid in asteroids:
                if asteroid.check_collision(player):
                    if player.invulnerable:
                       
                        explosion = Explosion(asteroid.position, asteroid.radius)
                        explosions.add(explosion)
                        asteroid.split(asteroids)
                        asteroid.kill()
                        player.shield_hits -= 1
                        if player.shield_hits <= 0:
                            effects.add(ShieldBreakBurst(player.position))
                            player.shield_active = False
                            player.invulnerable = False
                        
                    else:
                      
                        explosion = Explosion(asteroid.position, asteroid.radius)
                        explosions.add(explosion)
                        asteroid.split(asteroids)
                        asteroid.kill()
                        lives -= 1
                        player.kill()
                        player_dead = True
                        respawn_timer = 2.0
                        if lives <= 0:
                            game_over(screen, font, score)
                            return True
                
                
                
        for asteroid in asteroids:
            for bullet in shots:
                if asteroid.check_collision(bullet):
                    explosion = Explosion(asteroid.position, asteroid.radius)
                    explosions.add(explosion)
                    asteroid.split(asteroids)
                    bullet.kill()
                    if asteroid.radius == ASTEROID_MIN_RADIUS:
                        score += 100
                    elif asteroid.radius == ASTEROID_MID_RADIUS:
                        score += 50
                    elif asteroid.radius == ASTEROID_MAX_RADIUS:
                        score += 25
                    break
        if score >= next_powerup_at:
            powerup = ShieldPowerup()
            powerups.add(powerup)
            next_powerup_at += powerup_spawn_score
        
        if score >= next_rapid_at:
            rapid = RapidFirePowerup()
            rapid_powerups.add(rapid)
            next_rapid_at += rapid_spawn_score

        if score != last_score:
            score_text = font.render(f"SCORE: {score}", True, (204, 82, 0))
            last_score = score
        pygame.draw.rect(screen, (32,33,36), (score_x - 10, score_y - 5, 280, 40), border_radius = 8)
        shadow = font.render(f"SCORE: {score}", True, (50, 50, 50))
        screen.blit(shadow, (score_x + 2, score_y + 2))
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            glow = font.render(f"SCORE: {score}", True, (255,255,0))
            screen.blit(glow, (score_x + dx, score_y + dy))
        screen.blit(score_text, (score_x, score_y))
        for i in range(3):
            x = 30 + i * 40
            y = 70
            if i < lives:
                screen.blit(heart_image, (x,y))
            else:
                screen.blit(dimmed_heart, (x,y))
        pygame.display.flip()

def game_over(screen, font, score):
    text1 = font.render("GAME OVER", True, (255, 50, 50))
    text2 = font.render(f"FINAL SCORE: {score}", True, (255, 255, 255))
    text3 = font.render("Press ESC or close window to quit", True, (180, 180, 180))
    text4 = font.render("Press R to restart", True, (160,180,180))
    
    fade_alpha = 0
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0,0,0))
    clock = pygame.time.Clock()
    
    while True:
        screen.fill((20, 20, 20)) 

        screen.blit(text1, (SCREEN_WIDTH // 2 - text1.get_width() // 2, 200))
        screen.blit(text2, (SCREEN_WIDTH // 2 - text2.get_width() // 2, 280))
        screen.blit(text3, (SCREEN_WIDTH // 2 - text3.get_width() // 2, 360))
        screen.blit(text4, (SCREEN_WIDTH // 2 - text4.get_width() // 2, 440))
        if fade_alpha < 255:
            fade_alpha += 5  # increase for faster fade
            fade_surface.set_alpha(255 - fade_alpha)
            screen.blit(fade_surface, (0, 0))
        
        pygame.display.flip()
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    return
                
                
                
class ShieldPowerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/g{i}.png").convert_alpha(),
                (32, 32)
            )
            for i in range(1,6)
        ]

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(
            random.randint(50, 750), random.randint(50, 550)
        )
        self.rect.center = self.position

        self.frame_time = 0.08  
        self.timer = 0

    def update(self, dt, keys=None):
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer = 0
            self.index = (self.index + 1) % len(self.frames)
            self.image = self.frames[self.index]
            self.rect = self.image.get_rect(center=self.position)
                
    def load_shield_frames(size=48):
        return [
            pygame.transform.scale(
            pygame.image.load(f"assets/g{i}.png").convert_alpha(),
            (size, size)
        )
        for i in range(1,6) 
    ]
        
class ShieldBreakBurst(pygame.sprite.Sprite):
    def __init__(self, position):
        super().__init__()
        self.position = pygame.Vector2(position)
        self.radius = 20
        self.max_radius = 70
        self.alpha = 180  
        self.expansion_speed = 300 
        self.fade_speed = 400      

    def update(self, dt, keys=None):
        self.radius += self.expansion_speed * dt
        self.alpha -= self.fade_speed * dt
        if self.alpha <= 0:
            self.kill()

    def draw(self, screen):
        if self.alpha > 0:
            burst_surface = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(
                burst_surface,
                (0, 200, 255, int(self.alpha)),
                (self.max_radius, self.max_radius),
                int(self.radius),
                width=3
            )
            screen.blit(burst_surface, self.position - pygame.Vector2(self.max_radius, self.max_radius))
            
            


class RapidFirePowerup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.idle_frame = pygame.transform.scale(
            pygame.image.load("assets/idle_orb.png").convert_alpha(), 
            (64,64)
        )

        self.activation_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/orb{i}.png").convert_alpha(), 
                (64,64)
            )
            for i in range(1, 8)
        ]
        self.image = self.idle_frame
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(
            random.randint(50, SCREEN_WIDTH - 50),
            random.randint(50, SCREEN_HEIGHT - 50)
        )
        self.rect.center = self.position

        self.activated = False
        self.frame_index = 0
        self.frame_time = 0.08
        self.timer = 0

    def activate(self):
        self.activated = True
        self.timer = 0
        self.frame_index = 0

    def update(self, dt, keys=None):
        if self.activated:
            self.timer += dt
            if self.timer >= self.frame_time:
                self.timer = 0
                self.frame_index += 1
                if self.frame_index >= len(self.activation_frames):
                    self.kill()  
                else:
                    self.image = self.activation_frames[self.frame_index]
                    self.rect = self.image.get_rect(center=self.position)
                
if __name__ == "__main__":
    while True:
        should_restart = main()
        if not should_restart:
            break
