import contextlib
import sys
import os
from typing import List, Tuple

from application import Application
from enums import Direction, Tile
from pacman import PacmanSprite
from ghost import Blinky, Pinky

with contextlib.redirect_stdout(None):
    import pygame


TB = List[List[Tile]]


def load(file: str) -> pygame.Surface:
    path = "../assets/" + file + ".png"
    return pygame.image.load(path)


PACMAN_OPEN_RIGHT = load("pacman_open_right")

BLANK = load("blank")
COIN = load("coin")
WALL = load("wall")


def open_board() -> str:
    board = str()
    try:
        board = input("What level do you want to play? ")
        with open("../levels/" + board + ".board") as f:
            board_data = f.read()
            return board_data
    except FileNotFoundError:
        print("The board '" + board + "' does not exist!")
        print(
            "Possible boards are: "
            + ", ".join(b[:-6] for b in os.listdir("../levels/")),
            end="\n\n",
        )
        return open_board()
    except KeyboardInterrupt:
        sys.exit(0)


board = open_board()

app = Application(caption="PacMan", width=576, height=600, icon=PACMAN_OPEN_RIGHT)


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


@app.on("start")
def start(app) -> None:
    app.board = parse_board(board)

    app.display.fill((0, 0, 0))
    render_board(app.board)
    app.add_sprite(PacmanSprite(app), "pacman")
    app.add_sprite(Blinky(app), "blinky")
    app.add_sprite(Pinky(app), "pinky")


@app.on("update")
def update(app) -> None:
    app.display.fill((0, 0, 0))
    render_board(app.board)
    for sprite in app.sprites:
        app.sprites[sprite].update()


@app.on("keydown")
def keydown(app, event: pygame.event.EventType):
    pacman: PacmanSprite = app.get_sprite("pacman")
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


app.run()
