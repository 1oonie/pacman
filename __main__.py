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

app = Application(
    caption="PacMan", width=600, height=600, icon=sprites.pacman_open_right
)


@app.on("start")
def start(app):
    app.display.fill((0, 0, 0))
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
    for n_line, line in enumerate(board.split("\n")):
        for n_item, item in enumerate(line):
            if item == "-":
                img = tiles.wall
            elif item == "*":
                img = tiles.coin
            elif item == " ":
                continue
            app.display.blit(img, (n_item * 25, n_line * 25))


@app.on("keydown")
def keydown(app, event):
    if event.key == pygame.K_ESCAPE:
        app.exit(0)

app.run()
