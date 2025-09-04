import argparse
import random
import pygame

from player import Player
from enemy import Enemy

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
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        if hits:
            player.add_kill(len(hits))
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
