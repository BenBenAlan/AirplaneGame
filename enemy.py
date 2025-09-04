import random
import pygame

class Enemy(pygame.sprite.Sprite):
    """Enemy airplane that moves downward."""
    def __init__(self, x: int, y: int, speed: int) -> None:
        super().__init__()
        self.image = pygame.Surface((40, 30))
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def update(self) -> None:
        self.rect.y += self.speed
        if self.rect.top > 640:
            self.kill()
