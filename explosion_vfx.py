import pygame


class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, radius):
        super().__init__()

       
        self.frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/f{i}.png").convert_alpha(),
                (int(radius * 2), int(radius * 2))
            )
            for i in range(1,11)
        ]

        self.index = 0
        self.image = self.frames[self.index]
        self.rect = self.image.get_rect(center=position)

        self.timer = 0
        self.frame_duration = 0.08 

    def update(self, dt, keys=None):
        self.timer += dt
        if self.timer >= self.frame_duration:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.kill()
            else:
                self.image = self.frames[self.index]
                self.rect = self.image.get_rect(center=self.rect.center)

    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
