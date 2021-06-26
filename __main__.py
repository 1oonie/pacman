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


def render_board(board):
    for n_line, line in enumerate(board):
        for n_item, item in enumerate(line):
            if item == Tile.WALL:
                img = tiles.wall
            elif item == Tile.COIN:
                img = tiles.coin
            elif item == Tile.BLANK:
                continue
            app.display.blit(img, (n_item * 25, n_line * 25))


def check_board(direction, pos, board):
    if direction == Direction.RIGHT:
        return (board[pos[1] // 25][pos[0] // 25 + 1] != Tile.WALL)
    elif direction == Direction.LEFT:
        return (board[pos[1] // 25][pos[0] // 25 - 1] != Tile.WALL)
    elif direction == Direction.DOWN:
        return (board[pos[1] // 25 + 1][pos[0] // 25] != Tile.WALL)
    elif direction == Direction.UP:
        return (board[pos[1] // 25 - 1][pos[0] // 25] != Tile.WALL)
    elif direction == Direction.NONE:
        return True


@app.on("start")
def start(app):
    app.board = parse_board(board)

    app.display.fill((0, 0, 0))
    render_board(app.board)
    pacman = Sprite(app.display, sprites.pacman_open_right, (25, 25))
    pacman.next_direction = Direction.RIGHT
    pacman.current_direction = Direction.RIGHT
    app.add_sprite(pacman, "pacman")


@app.on("update")
def update(app):
    app.display.fill((0, 0, 0))
    render_board(app.board)

    pacman = app.get_sprite("pacman")

    if (
        pacman.x % 25 == 0
        and pacman.y % 25 == 0
    ):
        direction = pacman.next_direction
        print(check_board(pacman.current_direction, pacman.position, app.board))
        if not check_board(pacman.next_direction, pacman.position, app.board):
            direction = pacman.current_direction
        if not check_board(pacman.current_direction, pacman.position, app.board):
            direction = Direction.NONE
        pacman.current_direction = direction
    else:
        direction = pacman.current_direction

    x, y = pacman.x, pacman.y
    img = pacman.image

    if direction == Direction.RIGHT:
        x += 1
        if x % 25 < 12.5:
            img = sprites.pacman_open_right
        else:
            img = sprites.pacman_closed
    elif direction == Direction.LEFT:
        x -= 1
        if x % 25 < 12.5:
            img = sprites.pacman_open_left
        else:
            img = sprites.pacman_closed
    elif direction == Direction.UP:
        y -= 1
        if y % 25 < 12.5:
            img = sprites.pacman_open_top
        else:
            img = sprites.pacman_closed
    elif direction == Direction.DOWN:
        y += 1
        if y % 25 < 12.5:
            img = sprites.pacman_open_bottom
        else:
            img = sprites.pacman_closed

    pacman.update(img, (x, y))


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
        pygame.K_RIGHT: Direction.RIGHT,
    }
    # pylint: enable
    direction = directions.get(event.key, None)
    if direction:
        pacman.next_direction = direction


app.run()
