import pygame
import sys


class Game:
    def __init__(self,
                 caption,
                 width,
                 height,
                 back_color,
                 frame_rate
                 ):
        self.back_color = back_color
        self.frame_rate = frame_rate
        self.game_over = False
        self.objects = []
        pygame.init()
        pygame.font.init()
        self.surface = pygame.display.set_mode((width, height))
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.keydown_handlers = []
        self.mouse_handlers = []

    def update(self):
        pass

    def draw(self):
        for o in self.objects:
            o.draw(self.surface)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                for handler in self.keydown_handlers:
                    handler(event.key, event.unicode)
            elif event.type in (pygame.MOUSEBUTTONDOWN,
                                pygame.MOUSEBUTTONUP,
                                pygame.MOUSEMOTION):
                for handler in self.mouse_handlers:
                    handler(event.type, event.pos)

    def run(self):
        while not self.game_over:
            self.surface.fill(self.back_color)

            self.handle_events()
            self.update()
            self.draw()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
