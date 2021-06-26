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

with contextlib.redirect_stdout(None):
    import pygame


class Sprite:
    def __init__(self, display, image, pos):
        self.display = display
        display.blit(image, pos)
        self.image = image

        self._position = pos

    def __setattr__(self, name, value):
        try:
            super().__setattr__(name, value)
        except AttributeError:
            pass

    @property
    def position(self):
        return self._position

    @property
    def x(self):
        return self._position[0]

    @property
    def y(self):
        return self._position[1]

    def update(self, image, pos):
        self.display.blit(image, self._position)
        self._position = pos
        self.image = image
