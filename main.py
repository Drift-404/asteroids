import pygame
import sys
from constants import *
from player import Player, Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SCALED)
    pygame.display.set_caption("Asteroids")
    font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()

    score = 0
    last_score = -1
    score_text = font.render(f"SCORE: {score}", True, (255, 255, 255))

    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Shot.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    asteroidfield = AsteroidField()
    asteroidfield.asteroid_group = asteroids

    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, shots)

    while True:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.fill((0, 0, 0))

        updatable.update(clock.get_time() / 1000, keys)
        for sprite in drawable:
            sprite.draw(screen)

        for asteroid in asteroids:
            if asteroid.check_collision(player):
                print("Game Over!")
                return
            for bullet in shots:
                if asteroid.check_collision(bullet):
                    asteroid.split(asteroids)
                    bullet.kill()
                    if asteroid.radius == ASTEROID_MIN_RADIUS:
                        score += 100
                    elif asteroid.radius == ASTEROID_MID_RADIUS:
                        score += 50
                    elif asteroid.radius == ASTEROID_MAX_RADIUS:
                        score += 25
                    break

        if score != last_score:
            score_text = font.render(f"SCORE: {score}", True, (255, 255, 255))
            last_score = score

        screen.blit(score_text, (30, 30))
        

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
