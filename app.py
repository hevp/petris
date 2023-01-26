from component import BaseComponent
from consts import AppCode

import pygame as pg

class App:
    component: BaseComponent
    fps: int

    def __init__(self, title, w, h):
        pg.init()
        self.screen = pg.display.set_mode((w, h))
        self.clock = pg.time.Clock()
        self.fps = 25

        BaseComponent.screen = self.screen
        pg.display.set_caption(title)

    def set_component(self, component: BaseComponent):
        self.component = component

    def run(self):
        self.component.reset()
        counter = 0

        while True:
            counter += 1
            if counter % (self.fps // self.component.get_time_scaling()) == 1:
                self.component.update()

            for e in pg.event.get():
                if e.type == pg.QUIT:
                    return self.quit()
                elif e.type == pg.KEYDOWN:
                    r = self.component.handle_key(e.key)
                    match r:
                        case AppCode.OK:
                            break
                        case AppCode.UNHANDLED:
                            if e.key == pg.K_ESCAPE:
                                return self.exit()
                        case _:
                            return r

            pg.display.flip()
            self.clock.tick(self.fps)
            self.draw()

    def quit(self) -> AppCode:
        pg.quit()
        return AppCode.QUIT

    def exit(self) -> AppCode:
        return AppCode.EXIT

    def draw(self):
        self.component.draw()
