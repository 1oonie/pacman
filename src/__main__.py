import contextlib
import sys
import os
from typing import List, Tuple, Optional, Union

from application import Application
from enums import Direction, Tile
from sprite import Sprite

with contextlib.redirect_stdout(None):
    import pygame


TB = List[List[Tile]]
PACMAN_SPEED = 2


class PacManSprite(Sprite):
    current_direction: Direction = Direction.NONE
    next_direction: Direction = Direction.NONE
    score: int = 0
    won: bool = False


class PacManApp(Application):
    board: TB


class GhostSprite(Sprite):
    direction: Direction = Direction.NONE


def load(file: str) -> pygame.Surface:
    path = "../assets/" + file + ".png"
    return pygame.image.load(path)


PACMAN_OPEN_RIGHT = load("pacman_open_right")
PACMAN_OPEN_LEFT = load("pacman_open_left")
PACMAN_OPEN_DOWN = load("pacman_open_down")
PACMAN_OPEN_UP = load("pacman_open_up")
PACMAN_CLOSED = load("pacman_closed")

GHOST_PINK = load("ghost_pink")
GHOST_RED = load("ghost_red")
GHOST_ORANGE = load("ghost_orange")
GHOST_BLUE = load("ghost_blue")

BLANK = load("blank")
COIN = load("coin")
WALL = load("wall")


def open_board() -> str:
    board = str()
    try:
        board = input("What level do you want to play? ")
        with open("../levels/" + board + ".board") as f:
            board = f.read()
    except FileNotFoundError:
        print("The board '" + board + "' does not exist!")
        print("Possible boards are: " + ", ".join(b[:-6] for b in os.listdir("../levels/")), end="\n\n")
        open_board()
    except KeyboardInterrupt:
        sys.exit(0)
    else:
        return board

board= open_board()

app = PacManApp(caption="PacMan", width=576, height=600, icon=PACMAN_OPEN_RIGHT)
font = pygame.font.SysFont("Font.ttf", 24)

def parse_board(board: str) -> TB:
    tiles_dict = {"-": Tile.WALL, "*": Tile.COIN, " ": Tile.BLANK}
    res = []
    for row in board.split("\n"):
        line = []
        for item in row:
            line.append(tiles_dict[item])
        res.append(line)
    return res


def render_board(board: TB) -> None:
    for n_line, line in enumerate(board):
        for n_item, item in enumerate(line):
            img = WALL
            if item == Tile.WALL:
                img = WALL
            elif item == Tile.COIN:
                img = COIN
            elif item == Tile.BLANK:
                img = BLANK
                # remember, don't "continue" here cause
                # it speeds up when the is no coin
            app.display.blit(img, (n_item * 24, n_line * 24 + 24))


def check_board(direction: Direction, pos: Tuple[int, int], board: TB) -> bool:
    if not (pos[0] % 24 == 0 and pos[1] % 24 == 0):
        return True
    if direction == Direction.RIGHT:
        return board[pos[1] // 24][pos[0] // 24 + 1] != Tile.WALL
    elif direction == Direction.LEFT:
        return board[pos[1] // 24][pos[0] // 24 - 1] != Tile.WALL
    elif direction == Direction.DOWN:
        return board[pos[1] // 24 + 1][pos[0] // 24] != Tile.WALL
    elif direction == Direction.UP:
        return board[pos[1] // 24 - 1][pos[0] // 24] != Tile.WALL
    elif direction == Direction.NONE:
        return True


def eat_coin(pacman: PacManSprite, b: TB) -> TB:
    x, y = pacman.position
    y -= 24

    current = b[y // 24][x // 24]
    if current == Tile.COIN:
        pacman.score += 1
        b[y // 24][x // 24] = Tile.BLANK

        def check() -> bool:
            nonlocal b
            flattened: List[Tile] = [item for sublist in b for item in sublist]
            return Tile.COIN not in flattened

        if check():
            pacman.won = True

    return b


def isinverse(directions: Tuple[Direction, Direction]):
    inverse_dict = {
        Direction.RIGHT: Direction.LEFT,
        Direction.LEFT: Direction.RIGHT,
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.NONE: Direction.NONE,
    }
    return inverse_dict[directions[0]] == directions[1]


@app.on("start")
def start(app: PacManApp) -> None:
    app.board = parse_board(board)

    app.display.fill((0, 0, 0))
    render_board(app.board)
    pacman = PacManSprite(app.display, PACMAN_OPEN_RIGHT, (24, 48))
    app.add_sprite(pacman, "pacman")


@app.on("update")
def update(app: PacManApp) -> None:
    app.display.fill((0, 0, 0))

    pacman: PacManSprite = app.get_sprite("pacman")
    render_board(app.board)

    x, y = pacman.position
    y -= 24

    if (x % 24 == 0 and y % 24 == 0) or isinverse(
        (pacman.current_direction, pacman.next_direction)
    ):
        direction = pacman.next_direction
        if not check_board(pacman.next_direction, (x, y), app.board):
            direction = pacman.current_direction
        if not check_board(pacman.current_direction, (x, y), app.board):
            direction = Direction.NONE
        pacman.current_direction = direction
        if x % 24 == 0 and y % 24 == 0:
            app.board = eat_coin(pacman, app.board)
    else:
        direction = pacman.current_direction

    img = pacman.image

    y += 24
    if direction == Direction.RIGHT:
        x += PACMAN_SPEED
        img = PACMAN_OPEN_RIGHT
    elif direction == Direction.LEFT:
        x -= PACMAN_SPEED
        img = PACMAN_OPEN_LEFT
    elif direction == Direction.UP:
        y -= PACMAN_SPEED
        img = PACMAN_OPEN_UP
    elif direction == Direction.DOWN:
        y += PACMAN_SPEED
        img = PACMAN_OPEN_DOWN

    if x % 24 > 12 or y % 24 > 12:
        img = PACMAN_CLOSED

    pacman.update(img, (x, y))
    if pacman.won:
        surf = font.render("You won!", False, (255, 255, 255))
    else:
        surf = font.render("Score: " + str(pacman.score), False, (255, 255, 255))
    app.display.blit(surf, (5, 5))


@app.on("keydown")
def keydown(app: PacManApp, event: pygame.event.EventType):
    pacman: PacManSprite = app.get_sprite("pacman")
    if event.key == pygame.K_ESCAPE:
        app.exit(0)

    directions = {
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_UP: Direction.UP,
        pygame.K_RIGHT: Direction.RIGHT,
    }
    direction = directions.get(event.key, None)
    if direction:
        pacman.next_direction = direction


@app.on("mousebuttondown")
def mouseclick(app: PacManApp, event):
    pacman: PacManSprite = app.get_sprite("pacman")
    x, y = event.pos
    direction = None
    if x < 192:
        direction = Direction.LEFT
    elif x > 384 and x < 576:
        direction = Direction.RIGHT
    elif x > 192 and x < 384:
        if y < 287:
            direction = Direction.UP
        elif y > 287:
            direction = Direction.DOWN
    if direction:
        pacman.next_direction = direction


app.run()
