import pygame
import sys
from constants import *
from player import Player,Shot
from asteroid import Asteroid
from asteroidfield import AsteroidField
from circleshape import CircleShape
def main():
    pygame.init()
    clock = pygame.time.Clock()
    dt = 0
    print("Starting Asteroids!")
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    asteroids = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    shots = pygame.sprite.Group()
    Player.containers = (updatable,drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    asteroid = AsteroidField()
    player = Player(x = SCREEN_WIDTH/2, y = SCREEN_HEIGHT/2,shots_group = shots)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        pygame.Surface.fill(screen,(0,0,0))
        updatable.update(dt)
        for element in drawable:
            element.draw(screen)
        for shot in shots:
            shot.draw(screen)
            shot.update(dt)
        for obj in asteroids:
            if obj.check_collision(player) == True:
                print("Game over!")
                sys.exit()
            for bullet in shots:
                if obj.check_collision(bullet) == True:
                  obj.split(asteroids)
                  bullet.kill() 
        pygame.display.flip()
        dt = clock.tick(60)/1000
        
if __name__ == "__main__":
    main()
    