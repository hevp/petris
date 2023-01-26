from consts import AppCode, DrawCode
from component import BaseComponent
from factory import BaseFactory
from highscores import HighScores
from selector import BaseSelector, SelectorFactory
from settings import AppSettings

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional

import pygame as pg

@dataclass
class MenuItem:
    title: str
    effect: Optional[str] = None
    target: Optional[str] = None
    selector: Optional[BaseSelector] = None

    def handle_key(self, key: int) -> int:
        return AppCode.OK

@dataclass
class BaseMenu(ABC):
    index: int = 0

    @abstractmethod
    def items(self) -> list[MenuItem]: ...

    @property
    def item(self):
        return self.items()[self.index]

    def handle_key(self, key: int) -> int:
        if key == pg.K_UP:
            self.index = (self.index - 1) % len(self.items())
        elif key == pg.K_DOWN:
            self.index = (self.index + 1) % len(self.items())
        elif key in [pg.K_LEFT, pg.K_RIGHT] and self.item.effect == "select":
            self.item.handle_key(key)
        else:
            return AppCode.UNHANDLED

        return AppCode.OK

class MainMenu(BaseMenu):
    def items(self) -> list[MenuItem]:
        return [MenuItem("New game", "start"),
                MenuItem("High scores", "menu", "highscores"),
                MenuItem("Settings", "menu", "settings"),
                MenuItem("Quit", "quit")]

class HighScoresMenu(BaseMenu):
    def items(self) -> list[MenuItem]:
        return [MenuItem("Back", "quit")] + [MenuItem(f"{s['name'].upper()} : {s['value']}") for s in HighScores.items()]

class SettingsMenu(BaseMenu):
    def items(self) -> list[MenuItem]:
        return [MenuItem("Back", "quit")] + [MenuItem(f"{v} : {v}", "select", selector=SelectorFactory.create(v)) for v in AppSettings.items()]

class MenuFactory(BaseFactory[BaseMenu]):
    _module = 'menu'
    _mapping = {
        'main': 'MainMenu',
        'highscores': 'HighScoresMenu',
        'settings': 'SettingsMenu'
    }

@dataclass
class MenuStructure(BaseComponent):
    menu: BaseMenu = MenuFactory.create("main")

    def draw(self) -> bool:
        BaseComponent.screen.fill(self.theme.get_color("background"))

        # draw fixed items
        for i, s in enumerate(self.menu.items()):
            self.draw_text(s.title.upper(), DrawCode.CENTER, BaseComponent.screen.get_height() // 2 - (len(self.menu.items()) // 2 - i) * 30,
                           self.theme.get_color("text" if i != self.menu.index else "selection"))

        return True

    def handle_key(self, key: int) -> int:
        if key == pg.K_RETURN:
            match self.menu.item.effect:
                case "start":
                    return AppCode.START
                case "menu":
                    m = self.menu.item.target
                    if isinstance(m, str):
                        self.menu = MenuFactory.create(m)
                case "quit":
                    if isinstance(self.menu, MainMenu):
                        return AppCode.QUIT
                    else:
                        self.menu = MenuFactory.create("main")
        else:
            return self.menu.handle_key(key)

        return AppCode.OK
