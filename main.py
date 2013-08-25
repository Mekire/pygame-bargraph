import os
import sys
import pygame as pg
import graph


class Control(object):
    def __init__(self):
        os.environ["SDL_VIDEO_CENTERED"] = '1'
        pg.init()
        pg.key.set_repeat(100,100)
        self.screen = pg.display.set_mode((750,500))
        self.screen_rect = self.screen.get_rect()
        self.clock = pg.time.Clock()
        self.done = False
        self.fps = 60.0
        self.graph = graph.BarGraph(self.screen_rect)

    def event_loop(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.done = True
            self.graph.get_event(event)

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.graph.update(self.screen)
            pg.display.update()
            self.clock.tick(self.fps)


if __name__ == "__main__":
    run_it = Control()
    run_it.main_loop()
    pg.quit()
    sys.exit()
