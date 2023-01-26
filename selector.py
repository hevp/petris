from consts import AppCode
from factory import BaseFactory

from dataclasses import dataclass, field
from typing import Generic, TypeVar

import pygame as pg

T = TypeVar('T', int, bool, str, None)

@dataclass
class SelectorItem(Generic[T]):
    title: str
    value: T

@dataclass
class BaseSelector(Generic[T]):
    items: list[SelectorItem[T]] = field(default_factory=list)
    index: int = 0

    def handle_key(self, key: int) -> int:
        if key == pg.K_LEFT:
            self.index = (self.index - 1) % len(self.items)
        elif key == pg.K_RIGHT:
            self.index = (self.index + 1) % len(self.items)
        else:
            return AppCode.UNHANDLED

        return AppCode.OK

class NoneSelector(BaseSelector[None]):
    def handle_key(self, key: int) -> int:
        return AppCode.UNHANDLED

class IntSelector(BaseSelector[int]):
    pass

class StringSelector(BaseSelector[str]):
    pass

class BooleanSelector(BaseSelector[bool]):
    items: list[SelectorItem[bool]] = [SelectorItem("On", True), SelectorItem("Off", False)]

class SelectorFactory(BaseFactory[BaseSelector]):
    _module = 'selector'
    _mapping = {
        'bool': 'BooleanSelector',
        'int': 'IntSelector',
        'str': 'StringSelector'
    }
