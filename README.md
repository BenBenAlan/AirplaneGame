# Airplane Game

A simple wave-based airplane shooting game built with [Pygame](https://www.pygame.org/).

## Setup

```bash
pip install -r requirements.txt
```

## Running

```bash
python main.py
```

Use the arrow keys to move the green plane and press **Space** to fire.
Enemies appear in increasing waves; clear one wave to face the next.

For automated testing or headless environments:

```bash
SDL_VIDEODRIVER=dummy python main.py --autoquit 5
```
