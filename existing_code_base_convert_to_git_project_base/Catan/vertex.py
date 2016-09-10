__author__ = 'gskluzacek'
__date__ = '3/26/16'


class Vertex:
    vertex_seq = 1

    def __init__(self):
        self.seq = Vertex.vertex_seq
        self.hexes = {}
        self.edges = {}
        self.harbor = None
        Vertex.vertex_seq += 1

    def __str__(self):
        return str(self.seq)

    def dump(self):
        s = 'Vertex [%d]:\n\tHexes: ' % self.seq
        for n, h in self.hexes.items():
            s += '%s: %s ' % (n, h.name)
        s += '\n\tEdges: '
        for n, e in self.edges.items():
            s += '%s: %d ' % (n, e.get_seq())
        s += '\n\tHabor: '
        if self.has_harbor():
            s += str(self.get_harbor().get_seq())
        else:
            s += 'NONE'
        return s

    def set_hexes(self, wrk_vertexes):
        for whn, whex in wrk_vertexes.items():
            self.set_hex(whn, whex)

    def set_hex(self, hex_name, hext):
        self.hexes[hex_name] = hext

    def get_hex(self, pos_dir):
        if pos_dir not in self.hexes:
            hext = None
        else:
            hext = self.hexes[pos_dir]
        return hext

    def set_edge(self, pos_dir, edge):
        self.edges[pos_dir] = edge

    def get_edge(self, pos_dir):
        if pos_dir not in self.edges:
            edge = None
        else:
            edge = self.edges[pos_dir]
        return edge

    def get_seq(self):
        return self.seq

    def set_harbor(self, harbor):
        self.harbor = harbor

    def get_harbor(self):
        return self.harbor

    def has_harbor(self):
        if self.harbor is not None:
            return True
        else:
            return False
