import pygame
from game_object import GameObject
import config as cfg
import collections
from point import Point
import pickle


class Cube(GameObject):
    def __init__(self, x, y, w, h, row, place, color, list_of_cubes,
                 map, surface, score, finded, index, history, state, pre_score):
        super().__init__(x, y, w, h)
        self.state = 'normal'
        self.color = color
        self.score = score
        self.position = [row, place]
        self.list = list_of_cubes
        self.result = []
        self.map = map
        self.surface = surface
        self.finded = finded
        self.index = index
        self.history = history
        self.state_changed = state
        self.pre_score = pre_score

    @property
    def back_color(self):
        return cfg.cubes[self.color][self.state]

    @property
    def pos_x(self):
        return self.position[1]

    @property
    def pos_y(self):
        return self.position[0]

    def draw(self, surface):
        pygame.draw.rect(surface, self.back_color, self.bound)
        pygame.draw.rect(surface, cfg.BLACK, self.bound, 1)

    def cube_search(self):
        queue = collections.deque()
        current_point = Point(self.pos_x, self.pos_y)
        result = []
        if (self.map[self.pos_y][self.pos_x] == 'DELETED'):
            self.result = result
            return
        queue.append(current_point)
        visited = {}
        while (len(queue) != 0):
            point = queue.popleft()
            visited[str(point)] = 1
            result.append(point)
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    if (dx == 0 and dy == 0):
                        continue
                    if (dx != 0 and dy != 0):
                        continue
                    else:
                        new_point = Point(point.X + dx, point.Y + dy)
                        if (new_point.X < 0 or new_point.X >= cfg.map_width or new_point.Y < 0
                                or new_point.Y >= cfg.map_height):
                            continue
                        if (self.map[new_point.Y][new_point.X] != self.color):
                            continue
                        if (visited.__contains__(str(new_point))):
                            continue
                        queue.append(new_point)
        self.result = list(set(result))

    def handle_mouse_event(self, type, pos):
        if type == pygame.MOUSEMOTION:
            self.handle_mouse_move(pos)
        elif type == pygame.MOUSEBUTTONDOWN:
            self.handle_mouse_down(pos)
        elif type == pygame.MOUSEBUTTONUP:
            self.handle_mouse_up(pos)

    def handle_mouse_move(self, pos):
        if (not self.surface.collidepoint(pos)):
            if (len(self.result) > 1):
                for point in self.result:
                    self.list[point.Y][point.X].state = 'normal'
                    self.pre_score['pre_score'] = 0
        if self.bound.collidepoint(pos):
            if self.state != 'pressed':
                self.cube_search()
                for y in range(cfg.map_height):
                    for x in range(cfg.map_width):
                        self.pre_score['pre_score'] = 0
                        self.list[y][x].state = 'normal'
                if (len(self.result) > 1):
                    self.pre_score['pre_score'] = len(self.result) ** 2
                    for point in self.result:
                        self.list[point.Y][point.X].state = 'hover'

    def handle_mouse_down(self, pos):
        if self.bound.collidepoint(pos):
            self.state = 'pressed'

    def __str__(self):
        return 'X = {} Y = {} C = {}'.format(self.pos_x, self.pos_y, self.color)

    def re_paint(self):
        point = self
        for y in range(point.pos_y, 0, -1):
            point.list[y][point.pos_x].color = point.list[y - 1][point.pos_x].color
        point.list[0][point.pos_x].color = 'DELETED'
        if (point.list[cfg.map_height - 1][point.pos_x].color == 'DELETED'):
            for y in range(cfg.map_height - 1, -1, -1):
                for x in range(point.pos_x, cfg.map_width - 1, 1):
                    point.list[y][x].color = point.list[y][x + 1].color
                point.list[y][cfg.map_width - 1].color = 'DELETED'

    def update_map(self):
        self.map = []
        for y in range(cfg.map_height):
            self.map.append([])
            for x in range(cfg.map_width):
                color = self.list[y][x].color
                self.map[y].append(color)
        for y in range(cfg.map_height):
            for x in range(cfg.map_width):
                self.list[y][x].map = self.map

    def check_for_winner(self):
        for y in range(cfg.map_height):
            for x in range(cfg.map_width):
                point = self.map[y][x]
                if (point == 'DELETED'):
                    continue
                point = self.list[y][x]
                point.cube_search()
                if (len(point.result) > 1):
                    return True
        return False

    def checker(self):
        if (self.state_changed[0] == True):
            self.state_changed[0] = False
            length = len(self.history) - 1 - self.index[0]
            for i in range(length):
                self.history.pop()

    def on_click(self):
        if (len(self.result) > 1):
            x = len(self.result)
            print(x)
            self.score['score'] += x ** 2
            self.result.sort(key=lambda x: x.Y, reverse=False)
            self.result.sort(key=lambda x: x.X, reverse=True)
            for point in self.result:
                self.list[point.Y][point.X].color = 'DELETED'
                self.list[point.Y][point.X].re_paint()
                self.list[point.Y][point.X].state = 'normal'
            self.update_map()
            self.checker()
            self.index[0] += 1
            print("index:{}".format(self.index[0]))
            dict = {'score': self.score}
            dict['map'] = self.map
            self.history.append(pickle.dumps(dict))
            print("dlina:{}".format(len(self.history)))
        flag = self.check_for_winner()
        if flag is False:
            self.finded['finded'] = False

    def handle_mouse_up(self, pos):
        if self.state == 'pressed':
            self.on_click()
