import random
import pygame

# Screen bounds to govern movement
WIDTH, HEIGHT = 480, 640


class Enemy(pygame.sprite.Sprite):
    """Enemy airplane with simple movement patterns."""

    def __init__(self, x: int, y: int, speed: int, enemy_type: str = "straight") -> None:
        super().__init__()
        self.enemy_type = enemy_type
        self.image = pygame.Surface((40, 30))
        colour = (255, 0, 0) if enemy_type == "straight" else (255, 128, 0)
        self.image.fill(colour)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.health = 1
        # Horizontal movement for zigzag enemies
        self.dx = random.choice([-1, 1]) * (speed // 2)

    def update(self) -> None:
        if self.enemy_type == "zigzag":
            self.rect.x += self.dx
            if self.rect.left < 0 or self.rect.right > WIDTH:
                self.dx *= -1
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

    def hit(self, damage: int) -> bool:
        """Apply damage and return True if the enemy was destroyed."""
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False


class Boss(Enemy):
    """A larger enemy that takes multiple hits to destroy."""

    def __init__(self, x: int, y: int, health: int, speed: int) -> None:
        super().__init__(x, y, speed, enemy_type="boss")
        self.image = pygame.Surface((80, 60))
        self.image.fill((255, 0, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.health = health
        self.dx = 2

    def update(self) -> None:
        self.rect.x += self.dx
        if self.rect.left < 0 or self.rect.right > WIDTH:
            self.dx *= -1
        self.rect.y += self.speed // 2
        if self.rect.top > HEIGHT:
            self.kill()
