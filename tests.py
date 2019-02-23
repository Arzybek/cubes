import unittest
import cubes
import config as cfg


class OrdersTestCase(unittest.TestCase):
    def setUp(self):
        cfg.map_width = 4
        cfg.map_height = 4
        cfg.count_colors = 2
        self.cubes = cubes.Cubes()
        self.cubes.create_cubes()

    def test_order_height(self):
        self.assertEqual(cfg.map_height, len(self.cubes.cubes))

    def test_order_width(self):
        self.assertEqual(cfg.map_width, len(self.cubes.cubes[0]))


class LogicTestCase(unittest.TestCase):
    def test_simple_two(self):
        cfg.map_width = 2
        cfg.map_height = 2
        cfg.count_colors = 2
        self.cubes = cubes.Cubes()
        self.cubes.create_cubes()
        for x in range(2):
            self.cubes.cubes[0][x].color = 'RED'
        for x in range(2):
            self.cubes.cubes[1][x].color = 'BLUE'
        for x in range(2):
            self.cubes.cubes[0][0].update_map()
            self.cubes.cubes[x][x].cube_search()
            self.cubes.cubes[x][x].on_click()
        for y in range(cfg.map_height):
            for x in range(cfg.map_width):
                with self.subTest(x=x, y=y):
                    self.assertEqual(self.cubes.cubes[y][x].color, "DELETED")

    def test_simple_three(self):
        cfg.map_width = 3
        cfg.map_height = 3
        cfg.count_colors = 3
        self.cubes = cubes.Cubes()
        self.cubes.create_cubes()
        for x in range(3):
            self.cubes.cubes[0][x].color = 'RED'
        for x in range(3):
            self.cubes.cubes[1][x].color = 'BLUE'
        for x in range(3):
            self.cubes.cubes[2][x].color = 'GREEN'
        for x in range(3):
            self.cubes.cubes[0][0].update_map()
            self.cubes.cubes[x][x].cube_search()
            self.cubes.cubes[x][x].on_click()
        for y in range(cfg.map_height):
            for x in range(cfg.map_width):
                with self.subTest(x=x, y=y):
                    self.assertEqual(self.cubes.cubes[y][x].color, "DELETED")

    def test_complicated_four(self):
        cfg.map_width = 4
        cfg.map_height = 4
        cfg.count_colors = 2
        self.cubes = cubes.Cubes()
        self.cubes.create_cubes()
        self.cubes.cubes[0][0].color = 'BLUE'
        self.cubes.cubes[0][3].color = 'BLUE'
        self.cubes.cubes[3][0].color = 'BLUE'
        self.cubes.cubes[3][3].color = 'BLUE'
        for y in [1, 2]:
            for x in range(4):
                self.cubes.cubes[y][x].color = 'RED'
        for y in [0, 3]:
            for x in [1, 2]:
                self.cubes.cubes[y][x].color = 'RED'
        self.cubes.cubes[0][0].update_map()
        self.cubes.cubes[0][1].cube_search()
        self.cubes.cubes[0][1].on_click()
        self.cubes.cubes[0][0].update_map()
        for y in [2, 3]:
            for x in range(2):
                with self.subTest(x=x, y=y):
                    self.assertEqual(self.cubes.cubes[y][x].color, "BLUE")

    def test_its_just_X(self):
        cfg.map_width = 5
        cfg.map_height = 5
        cfg.count_colors = 1
        self.cubes = cubes.Cubes()
        self.cubes.create_cubes()
        for y in range(5):
            self.cubes.cubes[y][y].color = 'GREEN'
        for y in range(5):
            self.cubes.cubes[y][4 - y].color = 'GREEN'
        for y in range(5):
            for x in range(5):
                if (self.cubes.cubes[y][x].color != 'GREEN'):
                    self.cubes.cubes[y][x].color = 'RED'
        for (y, x) in [(0, 2), (2, 1), (2, 3), (4, 1)]:
            self.cubes.cubes[y][x].update_map()
            self.cubes.cubes[y][x].cube_search()
            self.cubes.cubes[y][x].on_click()
        for y in [4, 3]:
            for x in range(5):
                with self.subTest(x=x, y=y):
                    if (x != 2 and y != 3):
                        self.assertEqual(self.cubes.cubes[y][x].color, 'GREEN')
        self.assertEqual(self.cubes.score['score'], 64)

    def test_score_test(self):
        cfg.map_width = 10
        cfg.map_height = 10
        cfg.count_colors = 1
        self.cubes = cubes.Cubes()
        self.cubes.create_cubes()
        self.cubes.cubes[0][0].update_map()
        self.cubes.cubes[0][0].cube_search()
        self.cubes.cubes[0][0].on_click()
        self.assertEqual(self.cubes.score['score'], 10000)


if __name__ == '__main__':
    unittest.main()
