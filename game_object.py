from pygame.rect import Rect


class GameObject:
    def __init__(self, x, y, w, h):
        self.bound = Rect(x, y, w, h)

    @property
    def left(self):
        return self.bound.left

    @property
    def right(self):
        return self.bound.right

    @property
    def top(self):
        return self.bound.top

    @property
    def bottom(self):
        return self.bound.bottom

    @property
    def width(self):
        return self.bound.width

    @property
    def height(self):
        return self.bound.height

    @property
    def center(self):
        return self.bound.center

    @property
    def centerx(self):
        return self.bound.centerx

    @property
    def centery(self):
        return self.bound.centery

    def move(self, dx, dy):
        self.bound = self.bound.move(dx, dy)

    def draw(self, surface):
        pass
