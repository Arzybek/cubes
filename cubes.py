from game import Game
import config as cfg
import random
from cube import Cube
from text_object import TextObject
from button import Button
import pygame
import time
from pathlib import Path
from TextBox import InputBox
import pickle


class Cubes(Game):
    def __init__(self):
        Game.__init__(self, 'Cubes', cfg.screen_width, cfg.screen_height, cfg.back_color, cfg.fps)
        self.score = {'score': 0}
        self.cubes = []
        self.finded = {"finded": True}
        self.menu_buttons = []
        self.game_running = False
        self.objects = []
        self.map = []
        self.common_surface = pygame.Rect(0, 0, 0, 0)
        self.color_buttons = []
        self.order_buttons = []
        self.create_menu()
        self.flag_for_textbox = False
        self.index = [0]
        self.history = []
        self.state_changed = [False]
        self.pre_score = {'pre_score': 0}

    def restart(self):
        self.score['score'] = 0
        self.cubes = []
        self.finded['finded'] = True
        self.menu_buttons = []
        self.game_running = False
        self.objects = []
        self.map = []
        self.common_surface = pygame.Rect(0, 0, 0, 0)
        self.color_buttons = []
        self.order_buttons = []
        self.keydown_handlers = []
        self.mouse_handlers = []
        self.create_menu()
        self.flag_for_textbox = False
        self.index = [0]
        self.history = []
        self.state_changed = [False]
        self.pre_score = {'pre_score': 0}

    def create_cubes(self):
        w = cfg.cube_width
        h = cfg.cube_height
        cube_count = cfg.map_width
        offset_x = 3
        offset_y = 3
        row_count = cfg.map_height
        for row in range(row_count):
            self.cubes.append([])
            for place in range(cube_count):
                cube_color = random.randint(0, cfg.count_colors - 1)
                cube_color = cfg.colors[cube_color]
                cube = Cube(offset_x + place * w,
                            offset_y + row * h,
                            w,
                            h,
                            row,
                            place,
                            cube_color,
                            self.cubes,
                            self.map,
                            self.common_surface,
                            self.score,
                            self.finded,
                            self.index,
                            self.history,
                            self.state_changed,
                            self.pre_score
                            )
                self.cubes[row].append(cube)
                self.objects.append(cube)
                self.mouse_handlers.append(cube.handle_mouse_event)

    def update_surface(self):
        first = self.cubes[0][0]
        self.common_surface = pygame.Rect(first.bound.x, first.bound.y,
                                          cfg.map_width * cfg.cube_width, cfg.map_height * cfg.cube_height)
        for y in range(cfg.map_height):
            for x in range(cfg.map_width):
                self.cubes[y][x].surface = self.common_surface

    def create_map(self):
        for y in range(cfg.map_height):
            self.map.append([])
            for x in range(cfg.map_width):
                color = self.cubes[y][x].color
                self.map[y].append(color)
        dict = {'score': self.score}
        dict['map'] = self.map
        self.history.append(pickle.dumps(dict))

    def create_backs(self):
        def undo(button):
            if (self.index[0] == 0):
                return
            self.index[0] -= 1
            self.state_changed[0] = True
            print('index:{}'.format(self.index[0]))
            print('dlina:{}'.format(len(self.history)))
            for list in self.cubes:
                for cube in list:
                    self.mouse_handlers.remove(cube.handle_mouse_event)
                    self.objects.remove(cube)
            self.cubes = []
            w = cfg.cube_width
            h = cfg.cube_height
            cube_count = cfg.map_width
            offset_x = 3
            offset_y = 3
            row_count = cfg.map_height
            dict = pickle.loads(self.history[self.index[0]])
            self.map = dict['map']
            self.score = dict['score']
            for y in range(row_count):
                self.cubes.append([])
                for x in range(cube_count):
                    cube_color = self.map[y][x]
                    cube = Cube(offset_x + x * w,
                                offset_y + y * h,
                                w,
                                h,
                                y,
                                x,
                                cube_color,
                                self.cubes,
                                self.map,
                                self.common_surface,
                                self.score,
                                self.finded,
                                self.index,
                                self.history,
                                self.state_changed,
                                self.pre_score
                                )
                    self.cubes[y].append(cube)
                    self.objects.append(cube)
                    self.mouse_handlers.append(cube.handle_mouse_event)

        def redo(button):
            if (self.index[0] + 1 == len(self.history)):
                return
            self.state_changed[0] = True
            self.index[0] += 1
            print('index:{}'.format(self.index[0]))
            print('dlina:{}'.format(len(self.history)))
            for list in self.cubes:
                for cube in list:
                    self.mouse_handlers.remove(cube.handle_mouse_event)
                    self.objects.remove(cube)
            self.cubes = []
            w = cfg.cube_width
            h = cfg.cube_height
            cube_count = cfg.map_width
            offset_x = 3
            offset_y = 3
            row_count = cfg.map_height
            dict = pickle.loads(self.history[self.index[0]])
            self.map = dict['map']
            self.score = dict['score']
            for y in range(row_count):
                self.cubes.append([])
                for x in range(cube_count):
                    cube_color = self.map[y][x]
                    cube = Cube(offset_x + x * w,
                                offset_y + y * h,
                                w,
                                h,
                                y,
                                x,
                                cube_color,
                                self.cubes,
                                self.map,
                                self.common_surface,
                                self.score,
                                self.finded,
                                self.index,
                                self.history,
                                self.state_changed,
                                self.pre_score
                                )
                    self.cubes[y].append(cube)
                    self.objects.append(cube)
                    self.mouse_handlers.append(cube.handle_mouse_event)

        undo = Button(cfg.score_offset - 10,
                      cfg.score_offset_y + 33,
                      50,
                      26,
                      "UNDO",
                      undo,
                      padding=1,
                      size=20)
        redo = Button(cfg.score_offset + 45,
                      cfg.score_offset_y + 33,
                      50,
                      26,
                      "REDO",
                      redo,
                      padding=1,
                      size=20)
        self.objects.append(undo)
        self.menu_buttons.append(undo)
        self.mouse_handlers.append(undo.handle_mouse_event)
        self.objects.append(redo)
        self.menu_buttons.append(redo)
        self.mouse_handlers.append(redo.handle_mouse_event)

    def create_game(self):
        self.game_running = True
        self.create_cubes()
        self.create_map()
        self.update_surface()
        self.create_labels()
        self.create_backs()
        self.create_saves()

    def create_saves(self):
        my_file = Path("saves.txt")
        if my_file.is_file():
            return
        else:
            f = open("saves.txt", "w+")
            f.close()

    def create_orders(self):
        choose_text = TextObject(cfg.screen_width / 2 - 70,
                                 30,
                                 'Select field sizes')

        def orders(button):
            cfg.map_width = int(button.text_easy[0:2])
            cfg.map_height = int(button.text_easy[3:])
            for b in self.order_buttons:
                self.objects.remove(b)
            self.objects.remove(choose_text)
            self.order_buttons = []
            self.mouse_handlers = []
            self.create_colors()

        self.objects.append(choose_text)
        for i, (text, handler) in enumerate((('09x12', orders),
                                             ('12x15', orders),
                                             ('15x18', orders),
                                             ('18x21', orders)
                                             )):
            width = cfg.screen_width / 4.5 + 2 * i * (cfg.menu_button_w + 3)
            b = Button(width,
                       cfg.screen_height / 3 + (cfg.menu_button_h + 3),
                       cfg.menu_button_w,
                       cfg.menu_button_h,
                       text,
                       handler,
                       padding=5)
            self.objects.append(b)
            self.order_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def create_colors(self):
        choose_text = TextObject(cfg.screen_width / 2 - 100,
                                 30,
                                 'Choose count of colors')

        def colors(button):
            cfg.count_colors = int(button.text_easy)
            for b in self.color_buttons:
                self.objects.remove(b)
            self.objects.remove(choose_text)
            self.color_buttons = []
            self.mouse_handlers = []
            self.create_game()

        self.objects.append(choose_text)
        for i, (text, handler) in enumerate((
                ('3', colors),
                ('4', colors),
                ('5', colors)
        )):
            width = cfg.screen_width / 3.5 + 2 * i * (cfg.menu_button_w + 3)
            b = Button(width,
                       cfg.screen_height / 3 + (cfg.menu_button_h + 3),
                       cfg.menu_button_w,
                       cfg.menu_button_h,
                       text,
                       handler,
                       padding=5)
            self.objects.append(b)
            self.color_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def create_menu(self):
        def on_play(button):
            for b in self.menu_buttons:
                self.objects.remove(b)
            self.menu_buttons = []
            self.mouse_handlers = []
            self.create_orders()

        def on_quit(button):
            self.game_over = True
            self.game_running = False

        def get_back(button):
            self.objects = []
            self.menu_buttons = []
            self.mouse_handlers = []
            self.create_menu()

        def open_records(button):
            self.objects = []
            self.menu_buttons = []
            self.mouse_handlers = []

            back = Button(cfg.menu_offset_x, cfg.menu_offset_y + 100, cfg.start_menu_w, cfg.start_menu_h, "Back",
                          get_back, padding=5)
            self.objects.append(back)
            self.menu_buttons.append(back)
            self.mouse_handlers.append(back.handle_mouse_event)

            f = open("saves.txt", 'r')
            lines = f.readlines()
            f.close()
            example = TextObject(28, 5, "Order    Colors    Nick    Score", font_size=30,
                                 color=cfg.cubes['BLUE']['normal'])
            self.objects.append(example)
            for i, line in enumerate(lines):
                tmp = line.split(";")
                string = "{0}    {1}     {2}     {3}".format(*tmp)
                record = TextObject(30, 45 * (i + 1), string, 25)
                self.objects.append(record)

        for i, (text, handler) in enumerate((('PLAY', on_play),
                                             ('RECORDS', open_records),
                                             ('QUIT', on_quit)
                                             )):
            b = Button(cfg.menu_offset_x,
                       cfg.menu_offset_y + (cfg.menu_button_h + 3) * i,
                       cfg.start_menu_w,
                       cfg.start_menu_h,
                       text,
                       handler,
                       padding=5)
            self.objects.append(b)
            self.menu_buttons.append(b)
            self.mouse_handlers.append(b.handle_mouse_event)

    def create_labels(self):
        self.score_label = TextObject(cfg.score_offset,
                                      cfg.score_offset_y,
                                      "",
                                      text_func=lambda: 'SCORE: {}'.format(self.score['score']))
        self.objects.append(self.score_label)
        self.pre_score_label = TextObject(cfg.score_offset,
                                          cfg.score_offset_y + 100,
                                          "",
                                          text_func=lambda: 'PLUS: {}'.format(self.pre_score['pre_score']))
        self.objects.append(self.pre_score_label)

    def show_message(self,
                     text,
                     color=cfg.text_color,
                     font_name=cfg.font_name,
                     font_size=cfg.font_size):
        message = TextObject(cfg.screen_width // 2 - 40,
                             (cfg.screen_height // 2) - 40,
                             text,
                             font_size,
                             color,
                             font_name)
        self.draw()
        message.draw(self.surface)
        pygame.display.update()
        time.sleep(3)

    def remake_saves(self, nick):
        f = open("saves.txt", 'r')
        records = []
        for line in f:
            cleanedLine = line.strip()
            if cleanedLine:
                records.append(cleanedLine)
        f.close()
        order = "{}x{}".format(cfg.map_width, cfg.map_height)
        if (len(records) == 0):
            records.append("{0};{1};{2};{3}".format(order, cfg.count_colors, nick, self.score['score']))
            return records
        if (len(records) < 12):
            k = 0
            for i in records:
                tmp = i.split(';')
                if (order == tmp[0]):
                    if (cfg.count_colors == int(tmp[1])):
                        k += 1
            if (k < 1):
                records.append("{0};{1};{2};{3}".format(order, cfg.count_colors, nick, self.score['score']))
                return records
        oneOrder = []
        for k, line in enumerate(records):
            tmp = line.split(';')
            if (order == tmp[0]):
                if (cfg.count_colors == int(tmp[1])):
                    oneOrder.append(tuple((k, tmp)))
        oneOrder.sort(key=lambda x: int(x[1][3]))
        for i in range(len(oneOrder)):
            tmp = oneOrder[i]
            if (self.score['score'] > (int)(tmp[1][3])):
                string = "{0};{1};{2};{3}".format(order, cfg.count_colors, nick, self.score['score'])
                var = string.split(';')
                oneOrder[i] = tuple((tmp[0], var))
                break
        for i in range(len(oneOrder)):
            index = oneOrder[i][0]
            records[index] = ';'.join(oneOrder[i][1])
        return records

    def rewrite_saves(self, records):
        with open('saves.txt', 'w') as f:
            for line in records:
                f.write(line)
                f.write("\n")

    def check_saves(self):
        file = open("saves.txt", "r")
        records = file.readlines()
        order = "{}x{}".format(cfg.map_width, cfg.map_height)
        k = 0
        for i in records:
            tmp = i.split(';')
            if (tmp[0] == order):
                if (int(tmp[1]) == cfg.count_colors):
                    k += 1
                    if (self.score['score'] > int(tmp[3])):
                        return True
        if (k < 1):
            return True
        return False

    def make_input(self):
        self.textbox = InputBox(30, 45, 100, 30)
        self.objects.append(self.textbox)
        self.mouse_handlers.append(self.textbox.mouse_handle)
        self.keydown_handlers.append(self.textbox.keydown)

    def update(self):
        if not self.game_running:
            return
        if self.finded['finded'] is False:
            if (self.check_saves()):
                if (not self.flag_for_textbox):
                    self.show_message('NEW RECORD!')
                    for y in range(cfg.map_height):
                        for x in range(cfg.map_width):
                            self.objects.remove(self.cubes[y][x])
                    label = TextObject(30,
                                       10,
                                       'INPUT YOUR NICKNAME:')
                    self.objects.append(label)
                    self.make_input()
                    self.flag_for_textbox = True
                if (self.textbox.final == True):
                    nickname = self.textbox.text
                    records = self.remake_saves(nickname)
                    self.rewrite_saves(records)
                    self.game_running = False
                    self.restart()
            else:
                self.show_message('GAME OVER')
                self.restart()
            return


def main():
    Cubes().run()


if __name__ == '__main__':
    main()
