import argparse
import random
import pygame

from player import Player
from enemy import Enemy, Boss

WIDTH, HEIGHT = 480, 640
FPS = 60


def spawn_wave(wave: int, enemies: pygame.sprite.Group, all_sprites: pygame.sprite.Group) -> None:
    """Create a new wave of enemies or a boss every few waves."""
    if wave and wave % 5 == 0:
        boss = Boss(WIDTH // 2, -80, health=10 + wave * 2, speed=2 + wave // 5)
        enemies.add(boss)
        all_sprites.add(boss)
        return

    count = 5 + wave * 2
    for _ in range(count):
        x = random.randint(0, WIDTH - 40)
        y = random.randint(-150, -40)
        speed = random.randint(2, 4) + wave
        enemy_type = random.choice(["straight", "zigzag"])
        enemy = Enemy(x, y, speed, enemy_type)
        enemies.add(enemy)
        all_sprites.add(enemy)
def choose_plane(screen: pygame.Surface) -> str:
    """Display a simple selection screen and return the chosen plane type."""
    font = pygame.font.Font(None, 28)
    options = [
        "Press 1 for Plane A: quick shots & missile",
        "Press 2 for Plane B: double fire & spread",
        "Press 3 for Plane C: heavy shot & beam",
    ]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "A"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "A"
                if event.key == pygame.K_2:
                    return "B"
                if event.key == pygame.K_3:
                    return "C"
        screen.fill((0, 0, 0))
        for i, text in enumerate(options):
            img = font.render(text, True, (255, 255, 255))
            screen.blit(img, (20, 200 + i * 30))
        pygame.display.flip()


def choose_upgrade(screen: pygame.Surface, timeout: int = 3000) -> str:
    """Present three upgrade options and return the chosen one.

    If no choice is made within ``timeout`` milliseconds a random upgrade is
    selected to keep automated tests progressing.
    """
    font = pygame.font.Font(None, 28)
    options = [
        "1: Extra Bullet",
        "2: Speed Up",
        "3: Shield",
    ]
    start = pygame.time.get_ticks()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "none"
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "bullet"
                if event.key == pygame.K_2:
                    return "speed"
                if event.key == pygame.K_3:
                    return "shield"
        if timeout and pygame.time.get_ticks() - start > timeout:
            return random.choice(["bullet", "speed", "shield"])
        screen.fill((0, 0, 0))
        for i, text in enumerate(options):
            img = font.render(text, True, (255, 255, 255))
            screen.blit(img, (40, 200 + i * 30))
        pygame.display.flip()


def main(autoquit: float | None = None, plane: str | None = "A") -> int:
    """Run the game. Return the wave reached."""
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Airplane Shooter")
    clock = pygame.time.Clock()

    if plane is None:
        plane = choose_plane(screen)

    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player(WIDTH // 2, HEIGHT - 60, plane)
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for b in player.shoot():
                        bullets.add(b)
                        all_sprites.add(b)
                elif event.key == pygame.K_x:
                    for b in player.special():
                        bullets.add(b)
                        all_sprites.add(b)

        keys = pygame.key.get_pressed()
        player.update(keys)
        enemies.update()
        bullets.update()

        # Collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for enemy, hit_list in hits.items():
            for b in hit_list:
                if enemy.hit(getattr(b, "damage", 1)):
                    player.add_kill(1)
                    break
        if not enemies:
            wave += 1
            upgrade = choose_upgrade(screen)
            if upgrade == "bullet":
                player.bullet_bonus += 1
            elif upgrade == "speed":
                player.speed += 1
            elif upgrade == "shield":
                player.shield += 1
            spawn_wave(wave, enemies, all_sprites)

        if pygame.sprite.spritecollide(player, enemies, True):
            if player.shield > 0:
                player.shield -= 1
            else:
                player.health -= 1
                if player.health <= 0:
                    running = False

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()
    return wave


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Airplane shooter game")
    parser.add_argument("--autoquit", type=float, default=None, help="Automatically quit after given seconds")
    parser.add_argument(
        "--plane",
        choices=["A", "B", "C"],
        default=None,
        help="Choose plane type (default: ask at start)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    main(args.autoquit, args.plane)
