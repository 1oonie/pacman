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
from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Tuple

with contextlib.redirect_stdout(None):
    import pygame

if TYPE_CHECKING:
    from application import Application


class Sprite:
    def __init__(
        self, display: pygame.Surface, image: pygame.Surface, pos: Tuple[int, int]
    ):
        self.display: pygame.Surface = display
        display.blit(image, pos)
        self.image: pygame.Surface = image

        self._position: Tuple[int, int] = pos
        self.app: Application

    @property
    def position(self) -> Tuple[int, int]:
        return self._position

    @property
    def x(self) -> int:
        return self._position[0]

    @property
    def y(self) -> int:
        return self._position[1]

    def update(self, image: pygame.Surface, pos: Tuple[int, int]) -> None:
        self.display.blit(image, self._position)
        self._position = pos
        self.image = image