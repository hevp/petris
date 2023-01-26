from consts import DrawCode
from theme import Color, Theme

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import cast

import pygame as pg

@dataclass
class BaseComponent(ABC):
    screen: pg.surface.Surface
    theme: Theme = Theme()

    @abstractmethod
    def draw(self) -> bool: ...

    def draw_text(self, text: str|pg.surface.Surface,
                  x: int|DrawCode = DrawCode.CENTER, y: int|DrawCode = DrawCode.CENTER, color: Color = Color([0,0,0]),
                  font: str = "normal", antialias: bool = True) -> bool:
        r = self.theme.get_font(font).render(text, antialias, color) if isinstance(text, str) else text

        x = x if x != DrawCode.CENTER else (BaseComponent.screen.get_width() - r.get_width()) // 2
        y = y if y != DrawCode.CENTER else (BaseComponent.screen.get_height() - r.get_height()) // 2

        self.screen.blit(r, [cast(int, x), cast(int, y)])

        return True

    @abstractmethod
    def handle_key(self, key: int) -> int: ...

    def reset(self):
        self.update()

    def update(self):
        pass

    def get_time_scaling(self):
        return 1

    def set_theme(self, source: str) -> bool:
        self.theme = Theme(source)
        return True
