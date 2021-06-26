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
import math

from pygame.constants import K_LEFT, K_RIGHT

with contextlib.redirect_stdout(None):
    import pygame
    from pygame import gfxdraw

from application import Application
from images import sprites, tiles
from sprite import Sprite
from enums import Tile, Direction

app = Application(
    caption="PacMan", width=600, height=600, icon=sprites.pacman_open_right
)
board = """\
------------------------
-**********************-
-**-------*************-
-**********************-
-******-****--------***-
-*******-**************-
-**********************-
-*****---*---********-*-
-*****-*****-***------*-
-*******--**-**********-
-***********-**********-
-****************---***-
-****----*********-****-
-****-************-****-
-****-*****************-
-****-*******-*-*******-
-************-*-*******-
-***-******---*-*******-
-***-**********-*******-
-***-******-----*******-
-***-******************-
-*********----*********-
-**********************-
------------------------"""


def parse_board(board):
    tiles_dict = {"-": Tile.WALL, "*": Tile.COIN, " ": Tile.BLANK}
    res = []
    for row in board.split("\n"):
        line = []
        for item in row:
            line.append(tiles_dict[item])
        res.append(line)
    return res


def render_board(app):
    for n_line, line in enumerate(app.board):
        for n_item, item in enumerate(line):
            if item == Tile.WALL:
                img = tiles.wall
            elif item == Tile.COIN:
                img = tiles.coin
            elif item == Tile.BLANK:
                continue
            app.display.blit(img, (n_item * 25, n_line * 25))


@app.on("start")
def start(app):
    app.board = parse_board(board)

    app.display.fill((0, 0, 0))
    render_board(app)
    pacman = Sprite(app.display, sprites.pacman_open_right, (25, 25))
    pacman.direction = Direction.RIGHT
    app.add_sprite(pacman, "pacman")


@app.on("update")
def update(app):
    ...


@app.on("keydown")
def keydown(app, event):
    pacman = app.get_sprite("pacman")
    # pylint: disable=no-member
    if event.key == pygame.K_ESCAPE:
        app.exit(0)

    directions = {
        pygame.K_DOWN: Direction.DOWN,
        pygame.K_LEFT: Direction.LEFT,
        pygame.K_UP: Direction.UP,
        pygame.K_RIGHT: Direction.RIGHT
    }
    # pylint: enable
    direction = directions.get(event.key, None)
    if direction:
        pacman.direction = direction


app.run()
