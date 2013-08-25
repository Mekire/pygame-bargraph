import pygame as pg
from inputbox import Input
from isoblock import Block


LIGHT_GREY = (220,220,220)
BLACK = (0,0,0)

MARGIN = 25
TOTAL_SPACE = 700.0,350.0
SPACER = 10


class BarGraph(object):
    def __init__(self,surface_rect):
        self.screen_rect = surface_rect
        self.font = pg.font.SysFont("TimesNewRoman",20)
        self.active = Input((self.screen_rect.centerx,150),
                            "Number of Bars (2-12)",
                            self.font, BLACK)
        self.state = "NUMBER"
        self.count = None
        self.index = 0
        self.bar_data = []
        self.bars = []
        self.ready = False

    def get_event(self,event):
        if self.active:
            self.active.get_event(event)

    def check_state(self,surface):
        if self.state == "NUMBER":
            self.check_number_mode()
        elif self.state == "NAMES":
            self.check_name_mode()
        elif self.state == "VALUES":
            self.check_values_mode()
        elif self.state == "DISPLAY":
            for bar in self.bars:
                bar.update(surface)

    def check_number_mode(self):
        if self.active.final != None:
            try:
                self.count = int(self.active.final)
                if not (1 < self.count <= 12):
                    raise ValueError
                self.state = "NAMES"
                self.active = Input((self.screen_rect.centerx,150),
                                    "Bar #1 Label",self.font,
                                    BLACK)
            except ValueError:
                self.active.reset()

    def check_name_mode(self):
        if self.active.final != None:
            if self.active.final:
                self.bar_data.append([self.active.final,None])
                self.state = "VALUES"
                self.active = Input((self.screen_rect.centerx,150),
                                    "Value for {}".format(self.active.final),
                                    self.font,
                                    BLACK)
            else:
                self.active.reset()

    def check_values_mode(self):
        if self.active.final != None:
            try:
                self.bar_data[self.index][1] = float(self.active.final)
                self.index += 1
                if self.index < self.count:
                    self.state = "NAMES"
                    self.active = Input((self.screen_rect.centerx,150),
                                    "Bar #{} Label".format(self.index+1),
                                    self.font,
                                    BLACK)
                else:
                    self.active = None
                    self.state = "DISPLAY"
                    self.make_blocks()
            except ValueError:
                self.active.reset()

    def get_scale(self):
        width = (TOTAL_SPACE[0]-SPACER*(self.count-1))//self.count
        largest = max(ele[1] for ele in self.bar_data)
        space = TOTAL_SPACE[1] - width/(3**(.5))
        scale_factor = space/largest
        return (width,scale_factor)

    def make_blocks(self):
        width,scale = self.get_scale()
        bottom = self.screen_rect.height-100
        for i,(label,height) in enumerate(self.bar_data):
            x = MARGIN+(width+SPACER)*i
            height = height*scale + width/(3**(.5))
            self.bars.append(Block(x,bottom,(width,height),label))

    def update(self,surface):
        surface.fill(LIGHT_GREY)
        if self.active:
            self.active.update(surface)
        self.check_state(surface)
