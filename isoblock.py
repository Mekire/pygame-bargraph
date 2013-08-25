import pygame as pg


RED = (255,0,0)
RED_DARK = (150,0,0)
RED_PALE = (255,140,140)
BLACK = (0,0,0)
YELLOW = (150,150,0)


class Block(object):
    def __init__(self,x,bottom,size,label):
        self.label = self.make_label(label)
        self.size = size
        self.current_height = 0
        self.growth_speed = 2
        self.bottom = bottom
        self.x = x
        self.highlight = BLACK
        self.image = self.make_image((self.size[0],self.current_height))
        self.rect = self.image.get_rect(x=self.x,bottom=self.bottom)

    def make_label(self,label):
        font = pg.font.SysFont("TimesNewRoman",30,bold=True)
        rendered = font.render(label,True,BLACK)
        final = pg.transform.rotozoom(rendered,-35,1)
        return final

    def make_image(self,size):
        if size[1] < size[0]/(3**(.5)):
            size = (size[0],size[0]/(3**(.5)))
        rect = pg.Rect((0,0),size)
        image = pg.Surface(rect.size).convert_alpha()
        image.fill((0,0,0,0))
        iso_info = self.get_iso_points(rect)
        pg.draw.polygon(image,RED,iso_info["left"])
        pg.draw.polygon(image,RED_DARK,iso_info["right"])
        pg.draw.polygon(image,RED_PALE,iso_info["top"])
        final_rect = rect.inflate(6,6)
        final_rect.topleft = 0,0
        final_surface = pg.Surface(final_rect.size).convert_alpha()
        final_surface.fill((0,0,0,0))
        final_iso_info = self.get_iso_points(final_rect)
        final_points = final_iso_info["left"]+final_iso_info["right"]
        pg.draw.polygon(final_surface,self.highlight,final_points)
        final_surface.blit(image,(3,3))
        return final_surface

    def grow(self):
        self.current_height = min(self.current_height+self.growth_speed,
                                  self.size[1])
        self.image = self.make_image((self.size[0],self.current_height))
        self.rect = self.image.get_rect(x=self.x,bottom=self.bottom)

    def get_iso_points(self,rect):
        iso_info = {}
        angled = (rect.width/2)/(3**(.5))
        iso_info["left"] = (rect.midtop,
                            rect.midbottom,
                            (0,rect.bottom-angled),
                            (0,rect.y+angled))
        iso_info["right"] = (rect.midtop,
                             rect.midbottom,
                             (rect.right,rect.bottom-angled),
                             (rect.right,rect.y+angled))
        iso_info["top"] = (rect.midtop,
                           (0,angled),
                           (rect.midtop[0],angled*2),
                           (rect.right,angled))
        return iso_info

    def update(self,surface):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.highlight = YELLOW
        else:
            self.highlight = BLACK
        self.grow()
        surface.blit(self.image,self.rect)
        surface.blit(self.label,(self.x+self.rect.width//2,self.bottom-10))
