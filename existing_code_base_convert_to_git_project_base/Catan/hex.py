import math
from constants import HEXES, EDGES, VERTEXES, relative_offset, compl_hex_to_hex, r2e_edge_vertexes
import dirpos
import rsctyp
from point import Point

__author__ = 'gskluzacek'
__date__ = '3/26/16'


class Hex:
    next_name = 1
    a = 0
    b = 0
    c = 0
    hex_poly = []
    hex_midpt = []
    hex_harbor = {}
    x_fctr = 0
    y_fctr = 0
    x_offset = 10
    y_offset = 10
    v_txt_adj = {
        dirpos.NORTH: {'pt_ndx': 0, 'offset': Point(0, 12)},
        dirpos.NEAST: {'pt_ndx': 1, 'offset': Point(-6, 8)},
        dirpos.SEAST: {'pt_ndx': 2, 'offset': Point(-6, -2)},
        dirpos.SOUTH: {'pt_ndx': 3, 'offset': Point(0, -4)},
        dirpos.SWEST: {'pt_ndx': 4, 'offset': Point(7, -2)},
        dirpos.NWEST: {'pt_ndx': 5, 'offset': Point(7, 8)}
    }
    e_txt_adj = {
        dirpos.NEAST: {'pt_ndx': 0, 'offset': Point(-6, 8)},
        dirpos.EAST: {'pt_ndx': 1, 'offset': Point(-6, 2)},
        dirpos.SEAST: {'pt_ndx': 2, 'offset': Point(-6, -2)},
        dirpos.SWEST: {'pt_ndx': 3, 'offset': Point(6, -2)},
        dirpos.WEST: {'pt_ndx': 4, 'offset': Point(6, 2)},
        dirpos.NWEST: {'pt_ndx': 5, 'offset': Point(6, 8)}
    }
    h_txt_adj = {
        dirpos.NEAST: {'pt_ndx': 0, 'offset': Point(0, 10), 'anchor': 'start'},
        dirpos.EAST:  {'pt_ndx': 0, 'offset': Point(-15, 14), 'anchor': 'start'},
        dirpos.SEAST: {'pt_ndx': 3, 'offset': Point(0, -4), 'anchor': 'start'},
        dirpos.SWEST: {'pt_ndx': 0, 'offset': Point(0, -4), 'anchor': 'end'},
        dirpos.WEST:  {'pt_ndx': 3, 'offset': Point(15, 14), 'anchor': 'end'},
        dirpos.NWEST: {'pt_ndx': 3, 'offset': Point(0, 10), 'anchor': 'end'}
    }

    @classmethod
    def hex_calc_ab(cls, c):
        Hex.c = c
        Hex.b = (3 * Hex.c) / (math.sqrt(28) - 2)
        Hex.a = Hex.b - (.5 * Hex.c)

        Hex.x_fctr = 2 * Hex.b
        Hex.y_fctr = (2 * Hex.a) + (2 * Hex.c)

        Hex.hex_poly = [
            Point(1.0 * Hex.b, (0.0 * Hex.a) + (0.0 * Hex.c)),
            Point(2.0 * Hex.b, (1.0 * Hex.a) + (0.0 * Hex.c)),
            Point(2.0 * Hex.b, (1.0 * Hex.a) + (1.0 * Hex.c)),
            Point(1.0 * Hex.b, (2.0 * Hex.a) + (1.0 * Hex.c)),
            Point(0.0 * Hex.b, (1.0 * Hex.a) + (1.0 * Hex.c)),
            Point(0.0 * Hex.b, (1.0 * Hex.a) + (0.0 * Hex.c))
        ]

        Hex.hex_midpt = [
            Point(1.5 * Hex.b, (0.5 * Hex.a) + (0.0 * Hex.c)),
            Point(2.0 * Hex.b, (1.0 * Hex.a) + (0.5 * Hex.c)),
            Point(1.5 * Hex.b, (1.5 * Hex.a) + (1.0 * Hex.c)),
            Point(0.5 * Hex.b, (1.5 * Hex.a) + (1.0 * Hex.c)),
            Point(0.0 * Hex.b, (1.0 * Hex.a) + (0.5 * Hex.c)),
            Point(0.5 * Hex.b, (0.5 * Hex.a) + (0.0 * Hex.c))
        ]

    @classmethod
    def hex_calc_ab2(cls, c):
        Hex.c = c
        Hex.b = math.sqrt(.75) * Hex.c
        Hex.a = .5 * Hex.c

        Hex.x_fctr = 2 * Hex.b
        Hex.y_fctr = (2 * Hex.a) + (2 * Hex.c)

        Hex.hex_poly = [
            Point(1.0 * Hex.b, (0.0 * Hex.a) + (0.0 * Hex.c)),
            Point(2.0 * Hex.b, (1.0 * Hex.a) + (0.0 * Hex.c)),
            Point(2.0 * Hex.b, (1.0 * Hex.a) + (1.0 * Hex.c)),
            Point(1.0 * Hex.b, (2.0 * Hex.a) + (1.0 * Hex.c)),
            Point(0.0 * Hex.b, (1.0 * Hex.a) + (1.0 * Hex.c)),
            Point(0.0 * Hex.b, (1.0 * Hex.a) + (0.0 * Hex.c))
        ]

        Hex.hex_midpt = [
            Point(1.5 * Hex.b, (0.5 * Hex.a) + (0.0 * Hex.c)),
            Point(2.0 * Hex.b, (1.0 * Hex.a) + (0.5 * Hex.c)),
            Point(1.5 * Hex.b, (1.5 * Hex.a) + (1.0 * Hex.c)),
            Point(0.5 * Hex.b, (1.5 * Hex.a) + (1.0 * Hex.c)),
            Point(0.0 * Hex.b, (1.0 * Hex.a) + (0.5 * Hex.c)),
            Point(0.5 * Hex.b, (0.5 * Hex.a) + (0.0 * Hex.c))
        ]

        Hex.hex_harbor = {
            dirpos.NEAST: [
                Point(1.5 * Hex.b, (-0.5 * Hex.a) + (0.0 * Hex.c)),
                Point(1.0 * Hex.b, (0.0 * Hex.a) + (0.0 * Hex.c)),
                Point(2.0 * Hex.b, (1.0 * Hex.a) + (0.0 * Hex.c)),
                Point(2.0 * Hex.b, (0.0 * Hex.a) + (0.0 * Hex.c))
            ],
            dirpos.EAST: [
                Point(2.5 * Hex.b, (1.0 * Hex.a) + (0.25 * Hex.c)),
                Point(2.0 * Hex.b, (1.0 * Hex.a) + (0.0 * Hex.c)),
                Point(2.0 * Hex.b, (1.0 * Hex.a) + (1.0 * Hex.c)),
                Point(2.5 * Hex.b, (1.0 * Hex.a) + (0.75 * Hex.c))
            ],
            dirpos.SEAST: [
                Point(2.0 * Hex.b, (2.0 * Hex.a) + (1.0 * Hex.c)),
                Point(2.0 * Hex.b, (1.0 * Hex.a) + (1.0 * Hex.c)),
                Point(1.0 * Hex.b, (2.0 * Hex.a) + (1.0 * Hex.c)),
                Point(1.5 * Hex.b, (2.5 * Hex.a) + (1.0 * Hex.c))
            ],
            dirpos.SWEST: [
                Point(0.5 * Hex.b, (2.5 * Hex.a) + (1.0 * Hex.c)),
                Point(1.0 * Hex.b, (2.0 * Hex.a) + (1.0 * Hex.c)),
                Point(0.0 * Hex.b, (1.0 * Hex.a) + (1.0 * Hex.c)),
                Point(0.0 * Hex.b, (2.0 * Hex.a) + (1.0 * Hex.c))
            ],
            dirpos.WEST: [
                Point(-0.5 * Hex.b, (1.0 * Hex.a) + (0.75 * Hex.c)),
                Point(0.0 * Hex.b, (1.0 * Hex.a) + (1.0 * Hex.c)),
                Point(0.0 * Hex.b, (1.0 * Hex.a) + (0.0 * Hex.c)),
                Point(-0.5 * Hex.b, (1.0 * Hex.a) + (0.25 * Hex.c))
            ],
            dirpos.NWEST: [
                Point(0.0 * Hex.b, (0.0 * Hex.a) + (0.0 * Hex.c)),
                Point(0.0 * Hex.b, (1.0 * Hex.a) + (0.0 * Hex.c)),
                Point(1.0 * Hex.b, (0.0 * Hex.a) + (0.0 * Hex.c)),
                Point(0.5 * Hex.b, (-0.5 * Hex.a) + (0.0 * Hex.c))
            ]
        }

    def __init__(self, loc, name, value, rsc_type, robber_flg=False, harbor=None):
        self.loc = loc
        self.name = name
        self.value = value
        self.rsc_type = rsc_type
        self.robber_flg = robber_flg
        self.edges = {}
        self.vertexes = {}
        self.hexes = {}
        self.harbor = harbor

    def has_harbor(self):
        if self.harbor is not None:
            return True
        else:
            return False

    def get_harbor(self):
        return self.harbor

    def get_vertex(self, pos_dir):
        if pos_dir not in self.vertexes:
            # raise Exception('Missing Vertex at Positional Direction: %s for Hex: %s' % (pos_dir, self.name))
            return None
        return self.vertexes[pos_dir]

    def set_vertex(self, vertex_name, vertex):
        self.vertexes[vertex_name] = vertex

    def get_edge(self, pos_dir):
        if pos_dir not in self.edges:
            # raise Exception('Missing Edge at Positional Direction: %s for Hex: %s' % (pos_dir, self.name))
            return None
        return self.edges[pos_dir]

    def set_edge(self, pos_dir, edge):
        self.edges[pos_dir] = edge

    def set_hex(self, hex_to_hex_pos_dir, hext):
        self.hexes[hex_to_hex_pos_dir] = hext

    def get_hex(self, hex_to_hex_pos_dir):
        if hex_to_hex_pos_dir not in self.hexes:
            hext = None
        else:
            hext = self.hexes[hex_to_hex_pos_dir]
        return hext

    def get_loc(self):
        return self.loc

    def get_name(self):
        return self.name

    def get_value(self):
        return self.value

    def get_rsc_type(self):
        return self.rsc_type

    def is_robbing(self):
        return self.robber_flg

    def get_relative(self, direction):
        x = self.loc.x + relative_offset[direction]['x']
        y = self.loc.y + relative_offset[direction]['y']
        return x, y

    def svg(self):
        svg = []
        loc = self.get_loc()

        if self.get_value() is None:
            val = ' '
        else:
            val = self.get_value()

        if self.get_rsc_type() == rsctyp.FRAME:
            dsp = self.get_name()
        else:
            dsp = '%s(%s):%s' % (self.get_name(), str(val), self.get_rsc_type())
        pos = '[%d,%d]' % (loc.x, loc.y)

        if loc.x % 2 == 0:
            x_offset = Hex.b
            y_offset = 0

            delta_x_fctr = (loc.x / 2) - 1
            delta_y_fctr = (loc.y - 1) / 4
        else:
            x_offset = 0
            y_offset = Hex.a + Hex.c

            delta_x_fctr = (loc.x - 1) / 2
            delta_y_fctr = ((loc.y + 1) / 4) - 1

        delta_x = Hex.x_offset + (Hex.x_fctr * delta_x_fctr) + x_offset
        delta_y = Hex.y_offset + (Hex.y_fctr * delta_y_fctr) + y_offset
        delta_pt = Point(delta_x, delta_y)

        hex_points = Point.slide_points(Hex.hex_poly, delta_pt)
        hex_midpts = Point.slide_points(Hex.hex_midpt, delta_pt)
        hfill = rsctyp.FILL_COLOR[self.get_rsc_type()]
        if self.get_rsc_type() == rsctyp.FRAME:
            hcolor = 'aqua'
        else:
            hcolor = 'black'
        svg.append(Hex.svg_poly(hex_points, hcolor, hfill))

        lbl_loc = hex_points[0].slide_point(Point(0, Hex.c - 6))
        svg.append(Hex.svg_text(lbl_loc, dsp, 'blue'))
        lbl_loc = lbl_loc.slide_point(Point(0, 12))
        svg.append(Hex.svg_text(lbl_loc, pos, 'blue'))

        for pos_dir, vertex in self.vertexes.items():
            txt_adj = Hex.v_txt_adj[pos_dir]
            pt_ndx = txt_adj['pt_ndx']
            offset = txt_adj['offset']
            txt_loc = hex_points[pt_ndx].slide_point(offset)
            svg.append(Hex.svg_text(txt_loc, vertex.get_seq()))

        for pos_dir, edge in self.edges.items():
            txt_adj = Hex.e_txt_adj[pos_dir]
            pt_ndx = txt_adj['pt_ndx']
            offset = txt_adj['offset']
            txt_loc = hex_midpts[pt_ndx].slide_point(offset)
            svg.append(Hex.svg_text(txt_loc, edge.get_seq(), 'darkgreen'))

        if self.has_harbor():
            harbor = self.get_harbor()
            pos_dir = harbor.get_edge_pos_dir()

            harbor_pts = Point.slide_points(Hex.hex_harbor[pos_dir], delta_pt)
            svg.append(Hex.svg_polyline(harbor_pts, 2))

            txt_adj = Hex.h_txt_adj[pos_dir]
            pt_ndx = txt_adj['pt_ndx']
            offset = txt_adj['offset']
            anchor = txt_adj['anchor']
            txt_loc = harbor_pts[pt_ndx].slide_point(offset)

            exchg_out, exchg_in = harbor.get_exchange_ratio()
            harbor_txt = '%d:%d %s' % (exchg_out, exchg_in, harbor.get_rsc_typ())
            svg.append(Hex.svg_text(txt_loc, harbor_txt, 'black', anchor))

        return ''.join(svg)

    @classmethod
    def svg_poly(cls, points, color='black', fill='none'):
        poly_pts = []
        for pt in points:
            poly_pts.append('%f,%f' % (pt.x, pt.y))
        return '<polygon points="' + ' '.join(poly_pts) + '" stroke="%s" stroke-width="1" fill="%s"></polygon>' % (color, fill)

    @classmethod
    def svg_text(cls, loc, lbl, color='darkred', anchor=None):
        if anchor is not None:
            txt_anchor = ' style="text-anchor: %s;"' % anchor
        else:
            txt_anchor = ''
        return '<text x="%f" y="%f" fill="%s"%s>%s</text>' % (loc.x, loc.y, color, txt_anchor, lbl)

    @classmethod
    def svg_polyline(cls, points, width):
        poly_pts = []
        for pt in points:
            poly_pts.append('%f,%f' % (pt.x, pt.y))
        return '<polyline points="' + ' '.join(poly_pts) + '" stroke="black" stroke-width="%d" fill="none" />' % width


    @classmethod
    def get_grid_size(cls, hexes):
        max_x = 0
        max_y = 0
        for h in hexes:
            loc = h.get_loc()
            if loc.x > max_x:
                max_x = loc.x
            if loc.y > max_y:
                max_y = loc.y

        return max_x + 1, max_y + 1

    @classmethod
    def from_hex_get_compl_hex_pos_dir(cls, hex_to_hex_pos_dir):
        return compl_hex_to_hex[hex_to_hex_pos_dir]

    def __str__(self):
        if len(self.vertexes) != 0:
            vertexes = '\n'.join(['\t%s: %s' % (k, self.vertexes[k]) for k in VERTEXES])
        else:
            vertexes = '\tNONE'

        if len(self.hexes) != 0:
            hexes = []
            for k in HEXES:
                if k in self.hexes:
                    hex_name = self.hexes[k].name
                else:
                    hex_name = 'NONE'
                hexes.append('\t%s: %s' % (k, hex_name))
            hex_list = '\n'.join(hexes)
        else:
            hex_list = '\tNONE ?!!'

        if len(self.edges) != 0:
            edges = []
            for k in EDGES:
                if k in self.edges:
                    edge = self.get_edge(k)
                    edge_vertexes = r2e_edge_vertexes[k]
                    v1 = edge.get_vertex(edge_vertexes[0])
                    v2 = edge.get_vertex(edge_vertexes[1])
                    edge_desc = '\t%s:: [%d] v1: %d, v2: %d' % (k, edge.seq, v1.seq, v2.seq)
                else:
                    edge_desc = '\tNONE'
                edges.append(edge_desc)
            edge_list = '\n'.join(edges)
        else:
            edge_list = "\tNONE ?!!"

        if self.has_harbor():
            h_seq = '[%d] : %s' % (self.get_harbor().get_seq(), self.get_harbor().get_edge_pos_dir())
        else:
            h_seq = 'NONE'

        return '[%s] Name: %s Type: %s Value: %s Robber: %s\nVertexes:\n%s\nHexes:\n%s\nEdges:\n%s\nHarbor %s' % (
            self.loc, self.name, self.rsc_type, self.value, self.robber_flg, vertexes, hex_list, edge_list, h_seq)

    @classmethod
    def get_next_name(cls):
        name = cls.colnum2name(cls.next_name)
        cls.next_name += 1
        return name

    @classmethod
    def colnum2name(cls, d):
        a = []
        while d:
            d, r = divmod(d - 1, 26)
            a.append(r)
        a.reverse()
        return ''.join([chr(n + 65) for n in a])
