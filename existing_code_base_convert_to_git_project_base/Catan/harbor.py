__author__ = 'gskluzacek'
__date__ = '3/26/16'


class Harbor:
    harbor_seq = 1

    def __init__(self, pos_dir, out_ratio, in_ratio, rsc_typ):
        self.seq = Harbor.harbor_seq
        self.pos_dir = pos_dir
        self.out_ratio = out_ratio
        self.in_ratio = in_ratio
        self.rsc_typ = rsc_typ
        self.edge = None
        self.vertexes = {}
        self.hex = None
        Harbor.harbor_seq += 1

    def get_seq(self):
        return self.seq

    def get_rsc_typ(self):
        return self.rsc_typ

    def get_edge_pos_dir(self):
        return self.pos_dir

    def set_edge(self, edge):
        self.edge = edge

    def get_edge(self):
        return self.edge

    def set_vertexes(self, pos_dir, vertex):
        self.vertexes[pos_dir] = vertex

    def set_vertex(self, pos_dir, vertex):
        self.vertexes[pos_dir] = vertex

    def get_vertex(self, pos_dir):
        if pos_dir not in self.vertexes:
            return None
        return self.vertexes[pos_dir]

    def set_hex(self, hext):
        self.hex = hext

    def get_hex(self):
        return self.hex

    def get_ratio(self):
        return self.out_ratio, self.in_ratio

    def get_exchange_ratio(self):
        return self.out_ratio, self.in_ratio

    def __str__(self):
        s = 'Harbor [%d]:\n' % self.get_seq()
        s += '\tExchange Ratio: %d to %d\n' % self.get_exchange_ratio()
        s += '\tResource Type: %s\n' % self.rsc_typ
        s += '\tHex: %s\n' % self.get_hex().get_name()
        s += '\tEdge [%d]: %s\n' % (self.get_edge().get_seq(), self.get_edge_pos_dir())
        s += '\tVertexes:'
        for k, v in self.vertexes.items():
            s += '\n\t\t%s: %d' % (k, v.get_seq())
        return s