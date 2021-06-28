"""
MIT License

Copyright (c) 2021 MhmCats

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import contextlib
from typing import Dict, List, Tuple
import os

with contextlib.redirect_stdout(None):
    import pygame

from application import Application
from sprite import Sprite
from enums import Tile, Direction

TB = List[List[Tile]]
PACMAN_SPEED = 2


class PacManSprite(Sprite):
    current_direction: Direction = Direction.RIGHT
    next_direction: Direction = Direction.RIGHT
    score: int


class PacManApp(Application):
    board: TB


def load(file: str) -> pygame.Surface:
    path = "assets/" + file + ".png"
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


app = PacManApp(caption="PacMan", width=576, height=576,
                icon=PACMAN_OPEN_RIGHT)
board = """\
------------------------
-**********************-
-*--------------------*-
-*-******************-*-
-*-*----------------*-*-
-*-*-**************-*-*-
-*-*-*------------*-*-*-
-*-*-*-**********-*-*-*-
-*-*-*-*--------*-*-*-*-
-*-*-*-*-******-*-*-*-*-
-*-*-*-*-*----*-*-*-*-*-
-*-*-*-*-*-**-*-*-*-*-*-
-*-*-*-*-*-**-*-*-*-*-*-
-*-*-*-*-*--*-*-*-*-*-*-
-*-*-*-*-****-*-*-*-*-*-
-*-*-*-*------*-*-*-*-*-
-*-*-*-********-*-*-*-*-
-*-*-*----------*-*-*-*-
-*-*-************-*-*-*-
-*-*--------------*-*-*-
-*-****************-*-*-
-*------------------*-*-
-**********************-
------------------------"""


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
            app.display.blit(img, (n_item * 24, n_line * 24))


def check_board(direction: Direction, pos: Tuple[int, int], board: TB) -> bool:
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


def eat_coin(pacman: PacManSprite, board: TB) -> TB:
    pos: Tuple[int, int] = pacman.position
    current = board[pos[1] // 24][pos[0] // 24]
    if current == Tile.COIN:
        pacman.score += 1
        pygame.display.set_caption("PacMan: " + str(pacman.score) + " points")
        board[pos[1] // 24][pos[0] // 24] = Tile.BLANK
    return board


def isinverse(directions: Tuple[Direction, Direction]):
    inverse_dict = {
        Direction.RIGHT: Direction.LEFT,
        Direction.LEFT: Direction.RIGHT,
        Direction.UP: Direction.DOWN,
        Direction.DOWN: Direction.UP,
        Direction.NONE: Direction.NONE
    }
    return inverse_dict[directions[0]] == directions[1]


@app.on("start")
def start(app: PacManApp) -> None:
    app.board = parse_board(board)

    app.display.fill((0, 0, 0))
    render_board(app.board)
    pacman = PacManSprite(app.display, PACMAN_OPEN_RIGHT, (24, 24))
    pacman.score = 0
    app.add_sprite(pacman, "pacman")


@app.on("update")
def update(app: PacManApp) -> None:
    app.display.fill((0, 0, 0))

    pacman: PacManSprite = app.get_sprite("pacman")
    render_board(app.board)

    if (pacman.x % 24 == 0 and pacman.y % 24 == 0) or isinverse(
        (pacman.current_direction, pacman.next_direction)
    ):
        direction = pacman.next_direction
        if not check_board(pacman.next_direction, pacman.position, app.board):
            direction = pacman.current_direction
        if not check_board(pacman.current_direction, pacman.position, app.board):
            direction = Direction.NONE
        pacman.current_direction = direction
        if pacman.x % 24 == 0 and pacman.y % 24 == 0:
            app.board = eat_coin(pacman, app.board)
    else:
        direction = pacman.current_direction

    x, y = pacman.x, pacman.y
    img = pacman.image

    if direction == Direction.RIGHT:
        x += PACMAN_SPEED
        if x % 24 < 12:
            img = PACMAN_OPEN_RIGHT
        else:
            img = PACMAN_CLOSED
    elif direction == Direction.LEFT:
        x -= PACMAN_SPEED
        if x % 24 < 12:
            img = PACMAN_OPEN_LEFT
        else:
            img = PACMAN_CLOSED
    elif direction == Direction.UP:
        y -= PACMAN_SPEED
        if y % 24 < 12:
            img = PACMAN_OPEN_UP
        else:
            img = PACMAN_CLOSED
    elif direction == Direction.DOWN:
        y += PACMAN_SPEED
        if y % 24 < 12:
            img = PACMAN_OPEN_DOWN
        else:
            img = PACMAN_CLOSED

    pacman.update(img, (x, y))


@app.on("keydown")
def keydown(app: PacManApp, event: pygame.event.EventType):
    pacman: PacManSprite = app.get_sprite("pacman")
    # pylint: disable=no-member
    if event.key == pygame.K_ESCAPE:
        app.exit(0)

    directions = {
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_UP: Direction.UP,
        pygame.K_RIGHT: Direction.RIGHT,
    }
    # pylint: enable
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
