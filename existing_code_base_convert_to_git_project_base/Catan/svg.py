from point import Point
import math

__author__ = 'gskluzacek'
__date__ = '4/3/16'

next_name = 1

txt_adj = [Point(-2, 10), Point(-8, 8), Point(-8, 0), Point(-2, -4), Point(4, 0), Point(4, 8)]


def svg_poly(points):
    svg = '<polygon points="'
    poly_pts = []
    text_pts = []
    v = 0
    for pt in points:
        poly_pts.append('%f,%f' % (pt.x, pt.y))
        tx_pt = text_mv(pt, v)
        text_pts.append('<text x="%d" y="%d" fill="red">%s</text>' % (tx_pt.x, tx_pt.y, v + 1))
        v += 1
    svg += ' '.join(poly_pts) + '" stroke="black" stroke-width="1" fill="none"></polygon>'
    svg += ''.join(text_pts)
    svg += '<text x="%d" y="%d" fill="red">%s</text>' % (points[0].x - 4, points[0].y + 50, get_next_name())
    return svg


def text_adj(pt, pos_dir, adj_amt):
    pass


def text_mv(pt, ndx):
    global txt_adj
    return pt.slide_point(txt_adj[ndx])


def hex_calc_ab(c):
    b = (3 * c) / (math.sqrt(28) - 2)
    a = b - (.5 * c)
    return a, b

def get_next_name():
    global next_name
    name = colnum2name(next_name)
    next_name += 1
    return name

def colnum2name(d):
    a = []
    while d:
        d, r = divmod(d - 1, 26)
        a.append(r)
    a.reverse()
    return ''.join([chr(n + 65) for n in a])


c = 50
a, b = hex_calc_ab(c)

hex_poly = [
    Point(b, 0), Point(2 * b, a), Point(2 * b, a + c), Point(b, 2 * a + c), Point(0, a + c), Point(0, a)
]

for i in range(0, 4):
    for j in range(0, 8):
        print svg_poly(Point.slide_points(hex_poly,
                Point(
                    10 + (2 * b) * j,
                    10 + (2 * a + 2 * c) * i
                )))
        print svg_poly(Point.slide_points(hex_poly,
                Point(
                    10 + (2 * b) * j + b,
                    10 + (a + c) + (2 * a + 2 * c) * i
                )))
