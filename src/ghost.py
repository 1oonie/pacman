import contextlib

with contextlib.redirect_stdout(None):
    import pygame

from sprite import Sprite
from enums import Direction, GhostMode, Tile

def load(file: str) -> pygame.Surface:
    path = "../assets/" + file + ".png"
    return pygame.image.load(path)

GHOST_RED = load("ghost_red")
GHOST_PINK = load("ghost_pink")

GHOST_SPEED = 1

class Ghost(Sprite):
    def __init__(self, *args, **kwargs):
        self.current_direction: Direction = Direction.RIGHT
        self.mode: GhostMode = GhostMode.CHASE
        super().__init__(*args, **kwargs)

    def find_target(self):
        raise NotImplementedError
    
    def filter_directions(self):
        x, y = self.position
        y -= 24
        inverse_dict = {
            Direction.RIGHT: Direction.LEFT,
            Direction.LEFT: Direction.RIGHT,
            Direction.UP: Direction.DOWN,
            Direction.DOWN: Direction.UP,
            Direction.NONE: Direction.NONE,
        }
        directions =  [
            Direction.UP,
            Direction.DOWN,
            Direction.RIGHT,
            Direction.LEFT
        ]
        directions.remove(inverse_dict[self.current_direction])
        if self.app.board[y // 24 - 1][x // 24] == Tile.WALL:
            directions.remove(Direction.UP)
        if self.app.board[y // 24 + 1][x // 24] == Tile.WALL:
            directions.remove(Direction.DOWN)
        if self.app.board[y // 24][x // 24 + 1] == Tile.WALL:
            directions.remove(Direction.RIGHT)
        if self.app.board[y // 24][x // 24 - 1] == Tile.WALL:
            directions.remove(Direction.LEFT)

        return directions
            
    def calculate_next_direction(self, directions):
        tx, ty = self.find_target()
        x, y = self.position
        y -= 24

        def calc_dist(px, py):
            return (px - tx)**2 + (py - ty)**2

        positions = []
        for direction in directions:
            nx, ny = x, y
            if direction == Direction.RIGHT:
                nx += GHOST_SPEED
            elif direction == Direction.LEFT:
                nx -= GHOST_SPEED
            elif direction == Direction.UP:
                ny -= GHOST_SPEED
            elif direction == Direction.DOWN:
                ny += GHOST_SPEED
            positions.append((direction, calc_dist(nx, ny)))
       
        final_direction = min(positions, key=lambda item: item[1])
        return final_direction[0]

    def update(self):
        x, y = self.position
        y -= 24
        if (x % 24 == 0 and y % 24 == 0):
            self.current_direction = self.calculate_next_direction(self.filter_directions())
        
        direction = self.current_direction
        if direction == Direction.RIGHT:
            x += GHOST_SPEED
        elif direction == Direction.LEFT:
            x -= GHOST_SPEED
        elif direction == Direction.UP:
            y -= GHOST_SPEED
        elif direction == Direction.DOWN:
            y += GHOST_SPEED
        super().update(self.image, (x, y+24))

class Blinky(Ghost):
    def __init__(self, app):
        super().__init__(app, app.display, GHOST_RED, (552-24, 48))

    def find_target(self):
        pacman = self.app.get_sprite("pacman")
        if self.mode == GhostMode.CHASE:
            return pacman.position
        else:
            return (552, 48)
