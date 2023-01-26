import copy
from dataclasses import dataclass, field
from itertools import count
import pygame as pg
from random import randint

from component import BaseComponent
from consts import AppCode, DrawCode, State
from grid import Grid
from theme import Color

@dataclass
class Figure:
    rotations: int
    icoords: list[tuple]
    color: int = field(default_factory=count().__next__)
    x: int = 0
    y: int = 0
    rotation: int = 0

    def __post_init__(self):
        self.coords: list[tuple] = copy.copy(self.icoords)

    def rotate(self, rotation):
        self.coords = copy.copy(self.icoords)

        if rotation > 0:
            for r in range(rotation):
                for i in range(1, len(self.coords)):
                    x = self.coords[i][1]
                    y = self.coords[i][0]
                    self.coords[i] = (-x, y)

        return self.coords

FIGURES = [
    Figure(2, [(0, 0), (0, -1), (0, 1), (0, 2)]),
    Figure(4, [(0, 0), (0, -1), (0, 1), (1, 1)]),
    Figure(4, [(0, 0), (0, -1), (0, 1), (-1, 1)]),
    Figure(4, [(0, 0), (0, -1), (-1, 0), (1, 0)]),
    Figure(2, [(0, 0), (0, -1), (1, 0), (1, 1)]),
    Figure(2, [(0, 0), (0, -1), (-1, 0), (-1, 1)]),
    Figure(1, [(0, 0), (1,  0), (1, 1), (0, 1)])
]

class Tetris(BaseComponent):
    x: int = 90
    y: int = 40
    size: int = 26
    figure: Figure

    def __init__(self, width, height, size=25):
        self.width = width
        self.height = height
        self.size = size

    def set_theme(self, source: str):
        super().set_theme(source)

        self.texts = {
            State.PAUSE: self.theme.get_font("large").render("GAME PAUSED", True, self.theme.get_color("text")),
            State.GAMEOVER: self.theme.get_font("normal").render("Game over!", True, self.theme.get_color("text")),
            State.GAMEOVER + 1: self.theme.get_font("large").render("Press ESC", True, self.theme.get_color("text"))
        }

    def reset(self):
        self.state = State.START
        self.grid = Grid(self.width, self.height)

        self.score = 0
        self.level = 1

        self.nextfigure = self.create_figure()
        self.next_figure()

    def get_time_scaling(self) -> int:
        return self.level

    def create_figure(self) -> Figure:
        return copy.deepcopy(FIGURES[randint(0, len(FIGURES) - 1)])

    def next_figure(self):
        if self.state == State.GAMEOVER:
            return

        self.figure = copy.deepcopy(self.nextfigure)
        self.figure.x = self.grid.width // 2
        self.figure.y = 1
        self.nextfigure = self.create_figure()

        if self.grid.intersects(self.figure.x, self.figure.y, self.figure.coords):
            self.state = State.GAMEOVER

    def update(self):
        if self.figure is None:
            self.next_figure()

        match self.state:
            case State.START:
                self.state = State.RUNNING
            case State.PAUSE:
                return

        self.down()

    def drop(self):
        while self.down():
            pass

    def down(self):
        if self.grid.intersects(self.figure.x, self.figure.y + 1, self.figure.coords):
            return self.freeze() and False
        else:
            self.score += 1
            self.figure.y += 1
            return True

    def freeze(self):
        self.grid.burn(self.figure.x, self.figure.y, self.figure.coords, self.figure.color + 1)
        self.score += (self.grid.break_lines() ** 2) * 100

        self.next_figure()

    def side(self, dx):
        if not self.grid.intersects(self.figure.x + dx, self.figure.y, self.figure.coords):
            self.figure.x += dx

    def rotate(self):
        rotation = (self.figure.rotation + 1) % self.figure.rotations

        if not self.grid.intersects(self.figure.x, self.figure.y, self.figure.rotate(rotation)):
            self.figure.rotation = rotation
        else:
            self.figure.rotate(self.figure.rotation)

    def handle_key(self, key: int) -> int:
        if self.state == State.GAMEOVER:
            return AppCode.OK

        if key == pg.K_UP:
            self.rotate()
        elif key == pg.K_DOWN:
            self.down()
        elif key == pg.K_LEFT:
            self.side(-1)
        elif key == pg.K_RIGHT:
            self.side(1)
        elif key == pg.K_SPACE:
            self.drop()
        elif key == pg.K_p:
            self.state = State.PAUSE if self.state == State.RUNNING else State.RUNNING
        else:
            return AppCode.UNHANDLED

        return AppCode.OK

    def draw_block(self, color: Color, x: int, y: int, w: int, h: int):
        pg.draw.rect(BaseComponent.screen, color, (x, y, w, h))
        pg.draw.line(BaseComponent.screen, color.lighten(0.5), (x, y), (x, y + h))
        pg.draw.line(BaseComponent.screen, color.lighten(0.5), (x, y), (x + w, y))
        pg.draw.line(BaseComponent.screen, color.darken(0.5), (x + w, y), (x + w, y + h))
        pg.draw.line(BaseComponent.screen, color.darken(0.5), (x, y + h), (x + w, y + h))

    def draw_figure(self, figure, x, y):
        for i, j in figure.coords:
            self.draw_block(self.theme.get_color("figures", figure.color),
                            x + self.size * (i + figure.x) + 1, y + self.size * (j + figure.y) + 1, self.size - 1, self.size - 1)

    def draw(self) -> bool:
        BaseComponent.screen.fill(self.theme.get_color("background"))

        # draw grid
        for i in range(self.grid.height + 1):
            pg.draw.line(BaseComponent.screen, self.theme.get_color("line"),
                         (self.x, self.y + self.size * i), (self.x + self.size * self.grid.width, self.y + self.size * i))
        for j in range(self.grid.width + 1):
            pg.draw.line(BaseComponent.screen, self.theme.get_color("line"),
                         (self.x + self.size * j, self.y), (self.x + self.size * j, self.y + self.size * self.grid.height))

        # fill non-zero
        for i, j, c in self.grid.nonzero():
            self.draw_block(self.theme.get_color("figures", c - 1),
                            self.x + self.size * i + 1, self.y + self.size * j + 1, self.size - 1, self.size - 1)

        # fill current and next figure
        self.draw_figure(self.figure, self.x, self.y)
        self.draw_figure(self.nextfigure, 30, 50)

        return self.draw_texts()

    def draw_texts(self) -> bool:
        # render level and score
        self.draw_text(f"Level: {self.level:2}  Score: {self.score}",
                       DrawCode.CENTER, BaseComponent.screen.get_height() - 30, self.theme.get_color("text"))

        # display game over texts
        match self.state:
            case State.PAUSE:
                self.draw_text(self.texts[State.PAUSE], DrawCode.CENTER, DrawCode.CENTER)
            case State.GAMEOVER:
                self.draw_text(self.texts[State.GAMEOVER], DrawCode.CENTER, 20)
                self.draw_text(self.texts[State.GAMEOVER + 1], DrawCode.CENTER, DrawCode.CENTER)

        return True
