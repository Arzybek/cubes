class Point():
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __str__(self):
        return 'X = {} Y = {}'.format(self.X, self.Y)

    def __repr__(self):
        return 'X = {} Y = {}'.format(self.X, self.Y)

    def __cmp__(self, other):
        return self.X == other.X and self.Y == other.Y

    def __eq__(self, other):
        return self.X == other.X and self.Y == other.Y

    def __hash__(self):
        return (self.X - 5) ** 2 + (self.Y - 5) ** 3
