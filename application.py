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
from typing import Any, Callable, Dict, Optional, Tuple, Union

with contextlib.redirect_stdout(None):
    import pygame

from sprite import Sprite

# As you can see, pylint got a bit grumpy


class EventNotFound(Exception):
    ...


class Application:
    def __init__(self, *, caption: str, width: int, height: int, icon: pygame.Surface):
        pygame.init()  # pylint: disable=no-member
        self.width: int = width
        self.height: int = height
        self.caption: str = caption

        self.display: pygame.Surface = pygame.display.set_mode((width, height))
        pygame.display.set_icon(icon)
        pygame.display.set_caption(caption)

        self.events: Dict[int, Callable] = dict()
        self.sprites: Dict[str, Sprite] = dict()

        self.stopped: bool = False
        self.clock: pygame.time.Clock = pygame.time.Clock()

    def __setattr__(self, name: str, value: Any) -> None:
        try:
            super().__setattr__(name, value)
        except AttributeError:
            pass

    def __repr__(self) -> str:
        return "<Application width={0} height={1} caption={2}>".format(
            self.width, self.height, self.caption
        )

    @property
    def dimensions(self) -> Tuple[int, int]:
        return (self.width, self.height)

    def send(self, type_: Union[str, int], event: Optional[pygame.event.EventType] = None) -> None:
        if type_ in ("start", "update"):
            e = self.events.get(type_, None)
            if not e:
                return
            e(self)
            return
        e = self.events.get(type_, None)
        if e:
            e(self, event)

    def on(self, ev: str) -> Callable:
        def deco(func) -> Callable:
            if ev in ("start", "update"):
                self.events[ev] = func
                return func

            res = getattr(pygame, ev.upper(), None)
            if not res:
                raise EventNotFound("the event '{0}' doesn't exist".format(ev))
            self.events[res] = func
            return func

        return deco

    def exit(self, code: int = 0) -> None:
        if self.stopped:
            raise RuntimeError("the app has already stopped")
        pygame.quit()  # pylint: disable=no-member
        self.stopped = True

    def run(self, *, fps: int = 60):
        self.send("start")
        pygame.display.update()

        while not self.stopped:
            for event in pygame.event.get():
                self.send(event.type, event)
                if event.type == pygame.QUIT:  # pylint: disable=no-member
                    self.stopped = True

            self.send("update")
            pygame.display.update()
            self.clock.tick(fps)

        pygame.quit()  # pylint: disable=no-member

    def add_sprite(self, sprite: Sprite, name: str) -> None:
        self.sprites[name] = sprite

    def get_sprite(self, name: str) -> Optional[Sprite]:
        res = self.sprites.get(name, None)
        return res
