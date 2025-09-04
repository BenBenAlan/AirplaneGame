# Airplane Game

A simple wave-based airplane shooting game built with [Pygame](https://www.pygame.org/).

Each cleared wave now offers a roguelike upgrade choice such as extra
projectiles, increased speed, or a temporary shield.  Enemy patterns vary per
wave and a boss appears every few waves with increasing difficulty.  The game
ends when the player's health reaches zero.

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

You can optionally skip the selection screen by providing `--plane A`, `B` or
`C`.  Each plane has a unique primary weapon and a special attack triggered
with **X** after destroying enough enemies.

Use the arrow keys to move and press **Space** to fire the primary weapon.
Enemies appear in increasing waves; clear one wave to face the next.

For automated testing or headless environments:

```bash
SDL_VIDEODRIVER=dummy python main.py --autoquit 5
```
