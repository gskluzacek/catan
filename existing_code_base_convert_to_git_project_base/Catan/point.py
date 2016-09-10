__author__ = 'gskluzacek'
__date__ = '3/26/16'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return 'POINT x: %d, y: %d' % (self.x, self.y)

    def slide_point(self, offset):
        return Point(self.x + offset.x, self.y + offset.y)

    @classmethod
    def slide_points(cls, points, offset):
        points_slided = []
        for pt in points:
            points_slided.append(pt.slide_point(offset))
        return points_slided
