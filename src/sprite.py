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
