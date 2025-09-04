import pygame

class Player(pygame.sprite.Sprite):
    """Player-controlled airplane."""
    def __init__(self, x: int, y: int) -> None:
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self, keys: pygame.key.ScancodeWrapper) -> None:
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        # Clamp to screen bounds
        self.rect.x = max(0, min(self.rect.x, 480 - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, 640 - self.rect.height))
