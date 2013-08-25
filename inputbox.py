import pygame as pg
from string import ascii_letters, digits, punctuation


RED = (255,0,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

ACCEPT = ascii_letters+digits+punctuation+" "


class Input(object):
    def __init__(self,location,prompt,font,bg_color=BLACK):
        self.rect = pg.Rect((0,0),(200,75))
        self.rect.center = location
        self.input_rect = pg.Rect(0,0,100,25)
        self.input_rect.center = (self.rect.centerx,self.rect.y+50)
        self.font = font
        self.prompt,self.prompt_rect = self.render_text(prompt,
                                            (self.rect.centerx,self.rect.y+20))
        self.image = self.make_image(bg_color)
        self.string = []
        self.final = None

    def render_text(self,prompt,center,color=WHITE,background_color=BLACK):
        prompt = self.font.render(prompt,True,color,background_color)
        prompt_rect = prompt.get_rect(center=center)
        return prompt,prompt_rect

    def make_image(self,bg_color):
        surface = pg.Surface(self.rect.size).convert()
        surface.fill(bg_color)
        return surface

    def reset(self):
        self.string = []
        self.final = None

    def get_event(self,event):
        if event.type == pg.KEYDOWN:
            if self.final == None:
                if event.key in (pg.K_KP_ENTER, pg.K_RETURN):
                    self.final = "".join(self.string)
                elif event.key == pg.K_BACKSPACE:
                    if self.string:
                        self.string.pop()
                elif event.unicode in ACCEPT:
                    self.string.append(event.unicode)

    def update(self,surface):
        surface.blit(self.image,self.rect)
        pg.draw.rect(surface,BLUE,self.rect,3)
        surface.blit(self.prompt,self.prompt_rect)
        pg.draw.rect(surface,RED,self.input_rect,1)
        current = "".join(self.string)
        msg,msg_rect = self.render_text(current,(0,0))
        if msg_rect.width > self.input_rect.width-5:
            blit_rect = pg.Rect((msg_rect.width-self.input_rect.width+5,0),
                                self.input_rect.size)
            surface.blit(msg,self.input_rect.move(3,1),blit_rect)
        else:
            surface.blit(msg,self.input_rect.move(3,1))
