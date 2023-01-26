from dataclasses import dataclass, field
import json
from random import randrange
from typing import NewType

import pygame as pg

RGBColor = NewType('RGBColor', tuple[int, int, int])

class Color(tuple):
    def darken(self, f: float = 1.) -> tuple:
        return (int(self[0] * f), int(self[1] * f), int(self[2] * f))

    def lighten(self, f: float = 0.) -> tuple[int, int, int]:
        return (int((256 - self[0]) * f + self[0]), int((256 - self[1]) * f + self[1]), int((256 - self[2]) * f + self[2]))

    @staticmethod
    def generate(min: int = 30, max: int = 256) -> tuple[int, int, int]:
        return (randrange(min, max), randrange(min, max), randrange(min, max))

class RandomColors(dict):
    def __getitem__(self, __key: int) -> Color:
        if not __key in self:
            self[__key] = Color.generate()

        return self[__key]

@dataclass
class Theme:
    source: str = ""
    data: dict = field(default_factory=dict)

    def __post_init__(self):
        self.load_theme()

    def load_theme(self):
        if not len(self.source):
            return

        try:
            with open(self.source, 'r') as f:
                self.data = json.loads(f.read())
        except IOError as e:
            print(f"error: {e}")
        except json.JSONDecodeError as e:
            print(f"error: json: {e}")

        if not len(self.data):
            return

        # process color defs
        if self.data['colors']['figures'] == "random":
            self.data['colors']['figures'] = RandomColors()

        # process font definitions
        for name, df in self.data['fonts']['defs'].items():
            if df['source'] in self.data['fonts']['files']:
                self.data['fonts']['defs'][name]['_font'] = pg.font.Font('assets/' + self.data['fonts']['files'][df['source']], df['size'])

    def get_color(self, name: str, idx: int|None = None) -> Color:
        return Color(self.data.get('colors', {})[name] if idx is None else self.data.get('colors', {})[name][idx])

    def get_font(self, name: str) -> pg.font.Font:
        return self.data.get('fonts', {})['defs'][name]['_font']