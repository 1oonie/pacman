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
from typing import Callable, Tuple, Union

with contextlib.redirect_stdout(None):
    import pygame

from PIL import Image
from PIL import ImageDraw


def save_asset(func) -> Callable:
    def deco(*args, filename: str, **kwargs) -> Image.Image:
        ret = func(*args, **kwargs)
        ret = ret.resize((24, 24))
        ret.save("assets/" + filename)
        return ret
    return deco


@save_asset
def _pacman_open(rotate: int = 0) -> Image.Image:
    im = Image.new("RGBA", (50, 50))
    draw = ImageDraw.Draw(im)
    draw.pieslice([0, 0, 50, 50], 45, 360 - 45, (255, 251, 0))
    im = im.rotate(rotate)
    return im


@save_asset
def _pacman_closed() -> Image.Image:
    im = Image.new("RGBA", (50, 50))
    draw = ImageDraw.Draw(im)
    draw.ellipse([0, 0, 50, 50], fill=(255, 251, 0))
    return im


@save_asset
def _ghost(colour: Tuple[int, int, int]) -> Image.Image:
    im = Image.new("RGBA", (50, 50))
    draw = ImageDraw.Draw(im)
    draw.pieslice([0, 0, 50, 50], 180, 0, fill=colour)
    draw.rectangle([0, 25, 50, 40], fill=colour)

    for i in (10, 30):
        draw.ellipse([i, 15, i + 10, 25], fill=(255, 255, 255))
        draw.ellipse([i + 2, 17, i + 8, 23], fill=(0, 72, 255))

    for i in range(1, 4):
        points = [
            (i * (50 / 3) - 50 / 3, 40),
            (i * (50 / 3), 40),
            (i * (50 / 3) - 50 / 3 / 2, 50),
        ]
        # maths which spits out a triangle
        draw.polygon(points, fill=colour)

    return im


@save_asset
def _wall() -> Image.Image:
    im = Image.new("RGBA", (50, 50))
    draw = ImageDraw.Draw(im)
    draw.rectangle([2, 2, 48, 48], outline=(
        18, 50, 239), width=5, fill=(0, 0, 0))
    return im


@save_asset
def _coin(rotate: int = 45) -> Image.Image:
    im = Image.new("RGBA", (50, 50), (0, 0, 0))
    draw = ImageDraw.Draw(im)
    draw.rectangle([21, 21, 29, 29], fill=(255, 251, 0))
    im = im.rotate(rotate)
    return im


@save_asset
def _blank() -> Image.Image:
    im = Image.new("RGBA", (50, 50), (0, 0, 0))
    return im


if __name__ == "__main__":
    # automatically save all the images if we run the file

    # pylint: disable=unexpected-keyword-arg
    _pacman_open(filename="pacman_open_right.png")
    _pacman_open(180, filename="pacman_open_left.png")
    _pacman_open(270, filename="pacman_open_down.png")
    _pacman_open(90, filename="pacman_open_up.png")

    _pacman_closed(filename="pacman_closed.png")

    _ghost((255, 49, 0), filename="ghost_red.png")
    _ghost((255, 204, 0), filename="ghost_orange.png")
    _ghost((0, 252, 255), filename="ghost_blue.png")
    _ghost((254, 171, 210), filename="ghost_pink.png")

    _wall(filename="wall.png")
    _coin(filename="coin.png")
    _blank(filename="blank.png")
    # pylint: enable
