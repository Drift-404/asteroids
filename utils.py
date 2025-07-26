import pygame


def load_shield_frames(size=48):
        return [
            pygame.transform.scale(
            pygame.image.load(f"assets/g{i}.png").convert_alpha(),
            (size, size)
        )
        for i in range(1,6) 
    ]