import argparse
import os
import random
import sys
import pygame

from player import Player
from enemy import Enemy
from bullet import Bullet

WIDTH, HEIGHT = 480, 640
FPS = 60


def spawn_wave(wave: int, enemies: pygame.sprite.Group, all_sprites: pygame.sprite.Group) -> None:
    """Create a new wave of enemies."""
    count = 5 + wave * 2
    for _ in range(count):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-150, -40)
        speed = random.randint(2, 4) + wave
        enemy = Enemy(x, y, speed)
        enemies.add(enemy)
        all_sprites.add(enemy)


def main(autoquit: float | None = None) -> int:
    """Run the game. Return the wave reached."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Airplane Shooter")
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player(WIDTH // 2, HEIGHT - 60)
    all_sprites.add(player)

    wave = 0
    spawn_wave(wave, enemies, all_sprites)

    running = True
    elapsed = 0
    while running:
        dt = clock.tick(FPS)
        if autoquit is not None:
            elapsed += dt
            if elapsed >= autoquit * 1000:
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = Bullet(player.rect.centerx, player.rect.top)
                bullets.add(bullet)
                all_sprites.add(bullet)

        keys = pygame.key.get_pressed()
        player.update(keys)
        enemies.update()
        bullets.update()

        # Collisions
        pygame.sprite.groupcollide(enemies, bullets, True, True)
        if not enemies:
            wave += 1
            spawn_wave(wave, enemies, all_sprites)

        if pygame.sprite.spritecollide(player, enemies, True):
            running = False

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    return wave


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Airplane shooter game")
    parser.add_argument("--autoquit", type=float, default=None, help="Automatically quit after given seconds")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    main(args.autoquit)
