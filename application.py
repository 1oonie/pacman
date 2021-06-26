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
import sys

with contextlib.redirect_stdout(None):
    import pygame

# As you can see, pylint got a bit grumpy


class EventNotFound(Exception):
    ...


class Application:
    def __init__(self, *, caption, width, height, icon):
        pygame.init()  # pylint: disable=no-member
        self.width = width
        self.height = height
        self.caption = caption

        self.display = pygame.display.set_mode((width, height))
        pygame.display.set_icon(icon)
        pygame.display.set_caption(caption)

        self.events = dict()
        self.sprites = dict()

        self.stopped = False
        self.clock = pygame.time.Clock()

    def __setattr__(self, name, value):
        super().__setattr__(name, value)

    def __repr__(self):
        return "<Application width={0} height={1} caption={2}>".format(
            self.width, self.height, self.caption
        )

    @property
    def dimensions(self):
        return (self.width, self.height)

    def send(self, type_, event=None):
        if type_ in ("start", "update"):
            e = self.events.get(type_, None)
            if not e:
                return
            e(self)
            return
        e = self.events.get(type_, None)
        if e:
            e(self, event)

    def on(self, ev):
        def deco(func):
            if ev in ("start", "update"):
                self.events[ev] = func
                return func

            res = getattr(pygame, ev.upper(), None)
            if not res:
                raise EventNotFound("the event '{0}' doesn't exist".format(ev))
            self.events[res] = func
            return func

        return deco

    def exit(self, code=0):
        if self.stopped:
            raise RuntimeError("the app has already stopped")
        pygame.quit()  # pylint: disable=no-member
        sys.exit(code)
        self.stopped = True

    def run(self, *, fps=60):
        self.send("start")

        while not self.stopped:
            for event in pygame.event.get():
                self.send(event.type, event)
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    self.stopped = True

            self.send("update")
            pygame.display.update()
            self.clock.tick(fps)

        pygame.quit()  # pylint: disable=no-member
        sys.exit(0)

    def add_sprite(self, sprite, name):
        self.sprites[name] = sprite

    def get_sprite(self, name):
        res = self.sprites.get(name, None)
        if not res:
            raise AttributeError("no sprite exists called '{0}'".format(name))
        return res
