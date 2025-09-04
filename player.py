"""Player airplane implementations."""

from __future__ import annotations

import pygame

from bullet import Bullet


class Player(pygame.sprite.Sprite):
    """Player-controlled airplane with multiple selectable types."""

    def __init__(self, x: int, y: int, plane_type: str = "A") -> None:
        super().__init__()
        self.plane_type = plane_type
        self.image = pygame.Surface((50, 30))
        colors = {"A": (0, 255, 0), "B": (0, 0, 255), "C": (255, 255, 255)}
        self.image.fill(colors.get(plane_type, (0, 255, 0)))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.kills = 0
        self.special_ready = False
        self.special_threshold = {"A": 5, "B": 7, "C": 10}[plane_type]

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

    # --- Combat helpers -------------------------------------------------

    def add_kill(self, count: int) -> None:
        """Record kills and mark the special attack as ready when needed."""
        self.kills += count
        if self.kills >= self.special_threshold:
            self.special_ready = True
            self.kills = self.special_threshold

    def shoot(self) -> list[Bullet]:
        """Return a list of bullets for the plane's primary attack."""
        bullets: list[Bullet] = []
        if self.plane_type == "A":
            bullets.append(Bullet(self.rect.centerx, self.rect.top))
        elif self.plane_type == "B":
            bullets.append(Bullet(self.rect.centerx - 15, self.rect.top))
            bullets.append(Bullet(self.rect.centerx + 15, self.rect.top))
        elif self.plane_type == "C":
            bullets.append(
                Bullet(
                    self.rect.centerx,
                    self.rect.top,
                    speed=6,
                    size=(8, 15),
                    color=(255, 165, 0),
                )
            )
        return bullets

    def special(self) -> list[Bullet]:
        """Return bullets for the plane's special attack if ready."""
        if not self.special_ready:
            return []
        bullets: list[Bullet] = []
        if self.plane_type == "A":
            bullets.append(
                Bullet(
                    self.rect.centerx,
                    self.rect.top,
                    speed=12,
                    size=(10, 20),
                    color=(255, 128, 0),
                )
            )
        elif self.plane_type == "B":
            for dx in (-2, -1, 0, 1, 2):
                bullets.append(
                    Bullet(
                        self.rect.centerx,
                        self.rect.top,
                        dx=dx,
                        dy=-1,
                        speed=8,
                        color=(0, 255, 255),
                    )
                )
        elif self.plane_type == "C":
            bullets.append(
                Bullet(
                    240,
                    self.rect.top,
                    speed=15,
                    size=(480, 10),
                    color=(255, 0, 255),
                )
            )

        self.special_ready = False
        self.kills = 0
        return bullets
