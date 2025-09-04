import pygame

class Bullet(pygame.sprite.Sprite):
    """Bullet fired by the player."""
    def __init__(self, x: int, y: int, speed: int = 8) -> None:
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed

    def update(self) -> None:
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()
