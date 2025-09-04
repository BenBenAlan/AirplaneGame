"""Bullet implementations for the airplane game."""

from __future__ import annotations

import pygame

# Screen bounds used for bullet cleanup.  They mirror the constants in
# ``main.py`` but are repeated here to avoid a circular import.
WIDTH, HEIGHT = 480, 640


class Bullet(pygame.sprite.Sprite):
    """Generic projectile fired in the game.

    Bullets can move in any direction by supplying a directional vector.
    They are also configurable in colour and size so different plane types can
    easily create unique projectiles and special attacks.
    """

    def __init__(
        self,
        x: int,
        y: int,
        *,
        speed: int = 8,
        dx: float = 0,
        dy: float = -1,
        color: tuple[int, int, int] = (255, 255, 0),
        size: tuple[int, int] = (5, 10),
    ) -> None:
        super().__init__()
        self.image = pygame.Surface(size)
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.dx = dx
        self.dy = dy

    def update(self) -> None:
        self.rect.x += self.dx * self.speed
        self.rect.y += self.dy * self.speed
        if (
            self.rect.bottom < 0
            or self.rect.top > HEIGHT
            or self.rect.right < 0
            or self.rect.left > WIDTH
        ):
            self.kill()
