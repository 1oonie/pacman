from __future__ import annotations
import contextlib
import traceback
from typing import Any, Callable, Dict, Optional, TYPE_CHECKING, TypeVar, Union, List

with contextlib.redirect_stdout(None):
    import pygame

if TYPE_CHECKING:
    from sprite import Sprite

    T = TypeVar("T", bound=Sprite)

from enums import Tile

TB = List[List[Tile]]

class EventNotFound(Exception):
    ...


class Application:
    def __init__(
        self, *, caption: str, width: int, height: int, icon: pygame.Surface
    ) -> None:
        pygame.init()
        self.width: int = width
        self.height: int = height
        self.caption: str = caption

        self.display: pygame.Surface = pygame.display.set_mode((width, height))
        pygame.display.set_icon(icon)
        pygame.display.set_caption(caption)

        self.events: Dict[Union[int, str], Callable] = dict()
        self.sprites = dict()

        self.stopped: bool = False
        self.clock: pygame.time.Clock = pygame.time.Clock()
        self.board: TB

    def __repr__(self) -> str:
        return "<Application width={0} height={1} caption={2}>".format(
            self.width, self.height, self.caption
        )

    def send(self, type_: Any, event: Optional[pygame.event.EventType] = None) -> None:
        try:
            e = self.events[type_]
        except KeyError:
            return
        if type_ in ("start", "update"):
            e(self)

        else:
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
        pygame.quit()
        self.stopped = True
    

    def run(self, *, fps: int = 60) -> None:
        self.send("start")
        pygame.display.update()

        def handle_pygame_error(error) -> None:
            if str(error) == "display Surface quit":
                return
            traceback.print_exception(type(error), error, error.__traceback__)

        while True:
            if self.stopped:
                break

            for event in pygame.event.get():
                try:
                    self.send(event.type, event)
                except pygame.error as message:
                    handle_pygame_error(message)
                if event.type == pygame.QUIT:
                    self.stopped = True
            try:
                self.send("update")
            except pygame.error as message:
                handle_pygame_error(message)
            else:
                pygame.display.update()
                self.clock.tick(fps)

        pygame.quit()

    def add_sprite(self, sprite: T, name: str) -> None:
        sprite.app = self
        self.sprites[name] = sprite

    def get_sprite(self, name: str) -> T:
        res = self.sprites[name]
        return res
