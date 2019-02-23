import pygame as pg
import string
from game_object import GameObject
from pygame import font
from pygame import Color


class InputBox(GameObject):
    def __init__(self, x, y, w, h, text=''):
        super().__init__(x, y, w, h)
        self.COLOR_INACTIVE = Color('dodgerblue2')
        self.COLOR_ACTIVE = Color('black')
        self.FONT = font.Font(None, 32)
        self.ACCEPTED = string.ascii_letters + string.digits
        self.color = self.COLOR_INACTIVE
        self.text = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.final = False

    def keydown(self, key, unicode):
        if self.active:
            if key == pg.K_RETURN:
                self.final = True
            elif key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
                width = min(self.bound.w, self.txt_surface.get_width())
                self.bound.w = width
            elif unicode in self.ACCEPTED:
                if (len(self.text) >= 35):
                    pass
                else:
                    self.text += unicode
            self.txt_surface = self.FONT.render(self.text, True, self.color)

    def mouse_handle(self, type, pos):
        if type == pg.MOUSEBUTTONDOWN:
            if self.bound.collidepoint(pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

    def draw(self, screen):
        width = max(self.bound.w, self.txt_surface.get_width() + 7)
        self.bound.w = width
        screen.blit(self.txt_surface, (self.bound.x + 5, self.bound.y + 5))
        pg.draw.rect(screen, self.color, self.bound, 2)
