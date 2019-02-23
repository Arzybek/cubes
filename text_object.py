import pygame
import config as cfg


class TextObject:
    def __init__(self,
                 x,
                 y,
                 text,
                 font_size=cfg.font_size,
                 color=cfg.text_color,
                 font_name=cfg.font_name,
                 text_func=None
                 ):
        self.pos = (x, y)
        self.text = text
        if (text_func is None):
            self.text_func = lambda: self.text
        else:
            self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bound = self.get_surface(self.text_func())

    def draw(self, surface):
        text_surface, self.bound = \
            self.get_surface(self.text_func())
        pos = self.pos
        surface.blit(text_surface, pos)

    def get_surface(self, text):
        text_surface = self.font.render(text,
                                        True,
                                        self.color)
        return text_surface, text_surface.get_rect()
