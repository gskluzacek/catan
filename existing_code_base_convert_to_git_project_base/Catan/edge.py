__author__ = 'gskluzacek'
__date__ = '3/26/16'


class Edge:
    edge_seq = 1

    def __init__(self, vertexes):
        self.seq = Edge.edge_seq
        self.vertexes = vertexes
        self.hexes = {}
        self.harbor = None
        Edge.edge_seq += 1

    def set_hex(self, pos_dir, hext):
        self.hexes[pos_dir] = hext

    def get_hex(self, pos_dir):
        if pos_dir not in self.hexes:
            hext = None
        else:
            hext = self.hexes[pos_dir]
        return hext

    def set_vertex(self, pos_dir, vertex):
        self.vertexes[pos_dir] = vertex

    def get_vertex(self, pos_dir):
        if pos_dir not in self.vertexes:
            raise Exception('Missing Vertex at Positional Direction: %s for Edge: %d' % (pos_dir, self.seq))
        return self.vertexes[pos_dir]

    def get_vertexes(self):
        return self.vertexes

    def get_seq(self):
        return self.seq

    def __str__(self):
        s = 'Edge [%d]\n\tVertexes:: ' % self.seq
        for pos_dir, vertex in self.vertexes.items():
            s += '%s: [%d] ' % (pos_dir, vertex.get_seq())
        s += '\n\tHexes:: '
        for pos_dir, hext in self.hexes.items():
            s += '%s: %s ' % (pos_dir, hext.get_name())
        s += '\n\tHabor: '
        if self.has_harbor():
            s += str(self.get_harbor().get_seq())
        else:
            s += 'NONE'
        return s

    def set_harbor(self, harbor):
        self.harbor = harbor

    def get_harbor(self):
        return self.harbor

    def has_harbor(self):
        if self.harbor is not None:
            return True
        else:
            return False
