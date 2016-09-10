from constants import HEXES, VERTEXES, EDGES, vertex_rel_hex_edge, blah_blah_blah, foo_bar
import rsctyp
import dirpos
from board import Board
from point import Point
from hex import Hex
from edge import Edge
from harbor import Harbor

__author__ = 'gskluzacek'
__date__ = '3/26/16'


class Game:
    def __init__(self, players, hexes, rsc_deck, dev_deck, hex_c_len, prnt_flg=False):
        self.players = players
        self.hexes = hexes
        self.vertexes = []
        self.edges = []
        self.harbors = []
        self.rsc_deck = rsc_deck
        self.dev_deck = dev_deck

        self.max_x, self.max_y = Hex.get_grid_size(self.hexes)
        # Hex.hex_calc_ab(hex_c_len)
        Hex.hex_calc_ab2(hex_c_len)

        #
        # create the board by assigning the hexes to the board's x, y coordinates
        #

        #
        # take the array of hexes passed in and assign them to their x, y coordinates on the board grid
        self.board = Board(self.max_x, self.max_y, self.hexes)

        #
        # link hexes to each other
        #
        for i in range(self.max_y):
            for j in range(self.max_x):
                hext = self.board.get_hex(j, i)
                if hext is not None:
                    for hex_to_hex_pos_dir in HEXES:
                        xr, yr = hext.get_relative(hex_to_hex_pos_dir)
                        hexr = self.board.get_hex(xr, yr)
                        if hexr is not None:
                            hex_to_hex_compl_pos_dir = Hex.from_hex_get_compl_hex_pos_dir(hex_to_hex_pos_dir)
                            hext.set_hex(hex_to_hex_pos_dir, hexr)
                            hexr.set_hex(hex_to_hex_compl_pos_dir, hext)

        #
        # create & link vertextes
        #

        # create vertexes for each hex and 1) link the vertex to the appropriate hexes (up to 3) and
        # 2) link the hexes to the vertexes (up to 3)
        self.board.link()

        #
        # Create & Link Edges
        #

        # create edges and link them to the hexes & vertexes and link
        # the hexes to the edges and the vertex to the edges
        for i in range(self.max_y):
            for j in range(self.max_x):
                hext = self.board.get_hex(j, i)
                if hext is not None:
                    if len(hext.vertexes) != 0:
                        # print 'CRT EDGEs for HEX: %s' % hext.get_name()
                        # [ 1 ] create edges and link
                        #       a) the vertexes to the edge
                        #       b) the edge to the hexes
                        #       c) the hexes to the edge

                        # for each Hex Positional direction
                        for pos_dir in HEXES:
                            # print 'CRT EDGE: %s' % pos_dir
                            # get the complimentary edge name for the hex
                            compl_pos_dir = Hex.from_hex_get_compl_hex_pos_dir(pos_dir)
                            edge = None
                            # get the hex at the current positional direction relative to the current hex
                            hexr = hext.get_hex(pos_dir)
                            if hexr is not None:
                                if hexr.get_rsc_type() != rsctyp.FRAME:
                                    edge = hexr.get_edge(compl_pos_dir)
                            new_edge = False
                            if edge is None:
                                new_edge = True
                                # get the dictionary to lookup stuff
                                pdo = vertex_rel_hex_edge[pos_dir]
                                # get the positional directions for the Left & Right vertexes for the current positional direction pos_dir
                                vl_pd = pdo[dirpos.RELTOHEX][dirpos.LEFT]
                                vr_pd = pdo[dirpos.RELTOHEX][dirpos.RIGHT]
                                # get the left & right vertexes for the current positional direction pos_dir
                                vertex_l = hext.get_vertex(vl_pd)
                                vertex_r = hext.get_vertex(vr_pd)
                                # validate both vertexes exist
                                if vertex_l is None:
                                    raise Exception('Hex: %s Missing Expected Vertex at positional direction:: %s' % (hext.name, vl_pd))
                                if vertex_r is None:
                                    raise Exception('Hex: %s Missing Expected Vertex at positional direction: %s' % (hext.name, vr_pd))
                                # get the  Left & Right positional directions relative to the edge being created
                                el_pd = pdo[dirpos.RELTOEDGE][dirpos.LEFT]
                                er_pd = pdo[dirpos.RELTOEDGE][dirpos.RIGHT]
                                # [1] & (a) create the edge
                                edge = Edge({el_pd: vertex_l, er_pd: vertex_r})
                                # print '\tnew edge: %d' % edge.get_seq()
                            # (b.1) add the edge to the current hex
                            hext.set_edge(pos_dir, edge)
                            # (c.1) add the current hex to the edge
                            edge.set_hex(compl_pos_dir, hext)
                            if hexr is not None:
                                if hexr.get_rsc_type() != rsctyp.FRAME:
                                    if new_edge:
                                        # (b.2) add the edge to the hex
                                        hexr.set_edge(compl_pos_dir, edge)
                                        # (c.2) add the hex to the edge
                                        edge.set_hex(pos_dir, hexr)

        for i in range(self.max_y):
            for j in range(self.max_x):
                hext = self.board.get_hex(j, i)
                if hext is not None:
                    if len(hext.vertexes) != 0:
                        # print 'LINK EDGEs to VERTEXs for HEX: %s' % hext.get_name()
                        # [2] link the edges to the vertexes

                        # for each Vertex Positional Direction (relative to the current hex)
                        for pos_dir in VERTEXES:
                            # print 'LNK TO VERTEX: %s' % pos_dir
                            # get the dictionary to lookup stuff
                            pdo = blah_blah_blah[pos_dir]
                            # get positional directions (relative to the current hex) for the Left & Right Edges for the given vertex positional direction
                            el_pd = pdo[dirpos.RELTOHEX][dirpos.LEFT]
                            er_pd = pdo[dirpos.RELTOHEX][dirpos.RIGHT]
                            # get the positional direction (relative to the hex at the positional direction: er_pd) for the Middle Edge for the given vertex positional direction
                            em_pd = pdo[dirpos.RELTOHEXTOHEX]
                            # get the vertex at the current positional direction
                            vertex = hext.get_vertex(pos_dir)
                            if vertex is None:
                                raise Exception('Hex: %s Missing Expected Vertex at positional direction: %s' % (hext.name, pos_dir))
                            # get the left and right edges
                            edge_l = hext.get_edge(el_pd)
                            edge_r = hext.get_edge(er_pd)
                            if edge_l is None:
                                raise Exception('Hex: %s Missing Expected Edge at positional direction: %s' % (hext.name, el_pd))
                            if edge_r is None:
                                raise Exception('Hex: %s Missing Expected Edge at positional direction: %s' % (hext.name, er_pd))
                            # get the positional direction (relative to the current vertex) to set the edges on the current vertex
                            r2v_el_pd = pdo[dirpos.RELTOVERTEX][dirpos.LEFT]
                            r2v_er_pd = pdo[dirpos.RELTOVERTEX][dirpos.RIGHT]
                            # set the left and right edges on the vertex (using the positional directions)
                            vertex.set_edge(r2v_el_pd, edge_l)
                            vertex.set_edge(r2v_er_pd, edge_r)
                            # get the hex (relative the current hex) that will be used to get the middle (3rd) edge of the vertex
                            hexr = hext.get_hex(er_pd)
                            if hexr is not None:
                                if hexr.get_rsc_type() != rsctyp.FRAME:
                                    # get the middle edge
                                    edge_m = hexr.get_edge(em_pd)
                                    if edge_m is None:
                                        raise Exception('Hex: %s Missing Expected Edge at positional direction: %s' % (hexr.name, em_pd))
                                    # set the middle edge on the vertex (using the positional directions)
                                    vertex.set_edge(pos_dir, edge_m)

        #
        # Scan for Harbors and link them
        #
        for i in range(self.max_y):
            for j in range(self.max_x):
                hext = self.board.get_hex(j, i)
                if hext is not None:
                    if hext.has_harbor():
                        harbor = hext.get_harbor()
                        harbor.set_hex(hext)
                        r2h_edge_pos_dir = harbor.get_edge_pos_dir()
                        edge = hext.get_edge(r2h_edge_pos_dir)
                        edge.set_harbor(harbor)
                        harbor.set_edge(edge)
                        vertexes = edge.get_vertexes()
                        for r2e_vertex_pos_dir, vertex in vertexes.items():
                            vertex.set_harbor(harbor)
                            r2h_vertex_pos_dir = foo_bar[r2h_edge_pos_dir][r2e_vertex_pos_dir]
                            harbor.set_vertexes(r2h_vertex_pos_dir, vertex)

        #
        # gather harbors
        #

        hd = {}
        for i in range(self.max_y):
            for j in range(self.max_x):
                hext = self.board.get_hex(i, j)
                if hext is not None:
                    if hext.has_harbor():
                        harbor = hext.get_harbor()
                        hd[harbor.get_seq()] = harbor

        for k in sorted(hd.keys()):
            self.harbors.append(hd[k])
        #
        # gather vertexes
        #

        # Part 1 of 3 - get list of unique vertexes
        # after the vertexes have been linked with the hexes, walk the board grid and for each hex
        # iterate over the hexes vertexes and add each one to a set (only want one copy of each
        # vertex and a vertex may belong to multiple hexes)
        vs = set()
        for i in range(self.max_y):
            for j in range(self.max_x):
                hext = self.board.get_hex(j, i)
                if hext is not None:
                    for vn in VERTEXES:
                        vertex = hext.get_vertex(vn)
                        if vertex is not None:
                            vs.add(vertex)

        # Part 2 of 3 - add vertex to dictionary w/ vertex seq as the key
        # for each unique vertex in the set of vertexes, get the vertex's
        # sequence and use it as a key to add the vertex to the vertex dictionary
        d = {}
        for v in vs:
            d[v.seq] = v

        # Part 3 of 3 - create list of vertexes sorted by vertex.seq
        # create the final list of vertexes by walking keys the vertex dictionary in SORTED
        # order, adding them to the final list
        for k in sorted(d.keys()):
            self.vertexes.append(d[k])

        #
        # gather edges
        #
        edge_set = set()
        for i in range(self.max_y):
            for j in range(self.max_x):
                hext = self.board.get_hex(j, i)
                if hext is not None:
                    for edge_pos_dir in EDGES:
                        edge = hext.get_edge(edge_pos_dir)
                        if edge is not None:
                            edge_set.add(edge)

        edge_dict = {}
        for edge in edge_set:
            edge_dict[edge.get_seq()] = edge

        for k in sorted(edge_dict.keys()):
            self.edges.append(edge_dict[k])

        #
        # print board state
        #

        if prnt_flg:
            # print the grid of hexes row by row by column
            for i in range(self.max_y):
                print '=' * 100
                for j in range(self.max_x):
                    hext = self.board.get_hex(j, i)
                    if hext is not None:
                        print '-' * 100
                        print '[%d, %d] %s' % (j, i, self.board.get_hex(j, i))

            # print the list of vertexes (in sequence number order)
            for v in self.vertexes:
                print v.dump()

            # print the list of edges (in sequence number order)
            for edge in self.edges:
                print edge

            # print the list of harbors (in sequence number order)
            for harbor in self.harbors:
                print harbor

    @classmethod
    def randomize_hexes(cls, allocation):
        pass

    @classmethod
    def randomize_hexes_std_alloc(cls):
        pass

    @classmethod
    def get_std_hex_layout(cls):
        hexes = [
            # --- row 0: rsctyp.FRAME
            Hex(Point( 4,  1), Hex.get_next_name(), None, rsctyp.FRAME),              # --  A --
            Hex(Point( 6,  1), Hex.get_next_name(), None, rsctyp.FRAME),              # --  B --
            Hex(Point( 8,  1), Hex.get_next_name(), None, rsctyp.FRAME),              # --  C --
            Hex(Point(10,  1), Hex.get_next_name(), None, rsctyp.FRAME),              # --  D --

            # --- row 1
            Hex(Point( 3,  3), Hex.get_next_name(), None, rsctyp.FRAME),              # --  E --
            Hex(Point( 5,  3), Hex.get_next_name(), 10,   rsctyp.ORE, False,          # --  F --    Harbor: [B]
                Harbor(dirpos.NWEST, 3, 1, rsctyp.GENERIC)
            ),
            Hex(Point( 7,  3), Hex.get_next_name(), 2,   rsctyp.WOOL, False,         # --  G --    Harbor: [C]
                Harbor(dirpos.NEAST, 2, 1, rsctyp.GRAIN)
            ),
            Hex(Point( 9,  3), Hex.get_next_name(), 9,    rsctyp.LUMBER),             # --  H --
            Hex(Point(11,  3), Hex.get_next_name(), None, rsctyp.FRAME),              # --  I --

            # --- row 2
            Hex(Point( 2,  5), Hex.get_next_name(), None, rsctyp.FRAME),              # --  J --
            Hex(Point( 4,  5), Hex.get_next_name(), 12,    rsctyp.GRAIN, False,        # --  K --    Harbor: [A]
                Harbor(dirpos.WEST, 2, 1, rsctyp.LUMBER)
            ),
            Hex(Point( 6,  5), Hex.get_next_name(), 6,    rsctyp.BRICK),              # --  L --
            Hex(Point( 8,  5), Hex.get_next_name(), 4,    rsctyp.WOOL),               # --  M --
            Hex(Point(10,  5), Hex.get_next_name(), 10,   rsctyp.BRICK, False,        # --  N --    Harbor: [D]
                Harbor(dirpos.NEAST, 2, 1, rsctyp.ORE)
            ),
            Hex(Point(12,  5), Hex.get_next_name(), None, rsctyp.FRAME),              # --  O --

            # --- row 3
            Hex(Point( 1,  7), Hex.get_next_name(), None, rsctyp.FRAME),              # --  P --
            Hex(Point( 3,  7), Hex.get_next_name(), 9, rsctyp.GRAIN),              # --  Q --
            Hex(Point( 5,  7), Hex.get_next_name(), 11,    rsctyp.LUMBER),             # --  R --
            Hex(Point( 7,  7), Hex.get_next_name(), None,   rsctyp.DESERT, True),       # --  S --
            Hex(Point( 9,  7), Hex.get_next_name(), 3,    rsctyp.LUMBER),             # --  T --
            Hex(Point(11,  7), Hex.get_next_name(), 8,    rsctyp.ORE, False,          # --  U --    Harbor: [E]
                Harbor(dirpos.EAST, 3, 1, rsctyp.GENERIC)
            ),
            Hex(Point(13,  7), Hex.get_next_name(), None, rsctyp.FRAME),              # --  V --

            # --- row 4
            Hex(Point( 2,  9), Hex.get_next_name(), None, rsctyp.FRAME),              # --  W --
            Hex(Point( 4,  9), Hex.get_next_name(), 8,    rsctyp.LUMBER, False,       # --  X --    Harbor: [I]
                Harbor(dirpos.WEST, 2, 1, rsctyp.BRICK)
            ),
            Hex(Point( 6,  9), Hex.get_next_name(), 3,   rsctyp.ORE),                # --  Y --
            Hex(Point( 8,  9), Hex.get_next_name(), 4,    rsctyp.GRAIN),              # --  Z --
            Hex(Point(10,  9), Hex.get_next_name(), 5,    rsctyp.WOOL, False,         # -- AA --    Harbor: [F]
                Harbor(dirpos.SEAST, 2, 1, rsctyp.WOOL)
            ),
            Hex(Point(12,  9), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AB --

            # --- row 5
            Hex(Point( 3, 11), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AC --
            Hex(Point( 5, 11), Hex.get_next_name(), 5,    rsctyp.BRICK, False,        # -- AD --    Harbor: [H]
                Harbor(dirpos.SWEST, 3, 1, rsctyp.GENERIC)
            ),
            Hex(Point( 7, 11), Hex.get_next_name(), 6,    rsctyp.GRAIN, False,        # -- AE --    Harbor: [G]
                Harbor(dirpos.SEAST, 3, 1, rsctyp.GENERIC)
            ),
            Hex(Point( 9, 11), Hex.get_next_name(), 11,   rsctyp.WOOL),               # -- AR --
            Hex(Point(11, 11), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AF --

            # --- row n: rsctyp.FRAME
            Hex(Point( 4, 13), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AG --
            Hex(Point( 6, 13), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AH --
            Hex(Point( 8, 13), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AI --
            Hex(Point(10, 13), Hex.get_next_name(), None, rsctyp.FRAME)               # -- AG --
        ]

        return hexes

    @classmethod
    def get_std_hex_layout3(cls):
        hexes = [
            # --- row 0: rsctyp.FRAME
            Hex(Point( 4,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  A --
            Hex(Point( 6,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  B --
            Hex(Point( 8,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  C --
            Hex(Point(10,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  D --

            # --- row 1
            Hex(Point( 3,  4), Hex.get_next_name(), None, rsctyp.FRAME),              # --  E --
            Hex(Point( 5,  4), Hex.get_next_name(), 11,   rsctyp.ORE),                # --  F --
            Hex(Point( 7,  4), Hex.get_next_name(), 12,   rsctyp.WOOL),               # --  G --
            Hex(Point( 9,  4), Hex.get_next_name(), 9,    rsctyp.LUMBER),             # --  H --
            Hex(Point(11,  4), Hex.get_next_name(), None, rsctyp.FRAME),              # --  I --

            # --- row 2
            Hex(Point( 2,  6), Hex.get_next_name(), None, rsctyp.FRAME),              # --  J --
            Hex(Point( 4,  6), Hex.get_next_name(), 4,    rsctyp.GRAIN),              # --  K --
            Hex(Point( 6,  6), Hex.get_next_name(), 6,    rsctyp.BRICK),              # --  L --
            Hex(Point( 8,  6), Hex.get_next_name(), 5,    rsctyp.WOOL),               # --  M --
            Hex(Point(10,  6), Hex.get_next_name(), 10,   rsctyp.BRICK),              # --  N --
            Hex(Point(12,  6), Hex.get_next_name(), None, rsctyp.FRAME),              # --  O --

            # --- row 3
            Hex(Point( 1,  8), Hex.get_next_name(), None, rsctyp.FRAME),              # --  P --
            Hex(Point( 3,  8), Hex.get_next_name(), None, rsctyp.GRAIN),              # --  Q --
            Hex(Point( 5,  8), Hex.get_next_name(), 3,    rsctyp.LUMBER),             # --  R --
            Hex(Point( 7,  8), Hex.get_next_name(), 11,   rsctyp.DESERT, True),       # --  S --
            Hex(Point( 9,  8), Hex.get_next_name(), 4,    rsctyp.LUMBER),             # --  T --
            Hex(Point(11,  8), Hex.get_next_name(), 8,    rsctyp.ORE),                # --  U --
            Hex(Point(13,  8), Hex.get_next_name(), None, rsctyp.FRAME),              # --  V --

            # --- row 4
            Hex(Point( 2, 10), Hex.get_next_name(), None, rsctyp.FRAME),              # --  W --
            Hex(Point( 4, 10), Hex.get_next_name(), 8,    rsctyp.LUMBER),             # --  X --
            Hex(Point( 6, 10), Hex.get_next_name(), 10,   rsctyp.ORE),                # --  Y --
            Hex(Point( 8, 10), Hex.get_next_name(), 9,    rsctyp.GRAIN),              # --  Z --
            Hex(Point(10, 10), Hex.get_next_name(), 3,    rsctyp.WOOL),               # -- AA --
            Hex(Point(12, 10), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AB --

            # --- row 5
            Hex(Point( 3, 12), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AC --
            Hex(Point( 5, 12), Hex.get_next_name(), 5,    rsctyp.BRICK),              # -- AD --
            Hex(Point( 7, 12), Hex.get_next_name(), 2,    rsctyp.GRAIN),              # -- AE --
            Hex(Point( 9, 12), Hex.get_next_name(), 6,    rsctyp.WOOL),               # -- AR --
            Hex(Point(11, 12), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AF --

            # --- row n: rsctyp.FRAME
            Hex(Point( 4, 14), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AG --
            Hex(Point( 6, 14), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AH --
            Hex(Point( 8, 14), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AI --
            Hex(Point(10, 14), Hex.get_next_name(), None, rsctyp.FRAME)               # -- AG --
        ]

        return hexes

    @classmethod
    def get_std_hex_layout4(cls):
        hexes = [
            # --- row 0: rsctyp.FRAME
            Hex(Point( 5,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  A --
            Hex(Point( 7,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  B --
            Hex(Point( 9,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  C --
            Hex(Point(11,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  D --

            # --- row 1
            Hex(Point( 4,  4), Hex.get_next_name(), None, rsctyp.FRAME),              # --  E --
            Hex(Point( 6,  4), Hex.get_next_name(), 11,   rsctyp.ORE),                # --  F --
            Hex(Point( 8,  4), Hex.get_next_name(), 12,   rsctyp.WOOL),               # --  G --
            Hex(Point(10,  4), Hex.get_next_name(), 9,    rsctyp.LUMBER),             # --  H --
            Hex(Point(12,  4), Hex.get_next_name(), None, rsctyp.FRAME),              # --  I --

            # --- row 2
            Hex(Point( 3,  6), Hex.get_next_name(), None, rsctyp.FRAME),              # --  J --
            Hex(Point( 5,  6), Hex.get_next_name(), 4,    rsctyp.GRAIN),              # --  K --
            Hex(Point( 7,  6), Hex.get_next_name(), 6,    rsctyp.BRICK),              # --  L --
            Hex(Point( 9,  6), Hex.get_next_name(), 5,    rsctyp.WOOL),               # --  M --
            Hex(Point(11,  6), Hex.get_next_name(), 10,   rsctyp.BRICK),              # --  N --
            Hex(Point(13,  6), Hex.get_next_name(), None, rsctyp.FRAME),              # --  O --

            # --- row 3
            Hex(Point( 2,  8), Hex.get_next_name(), None, rsctyp.FRAME),              # --  P --
            Hex(Point( 4,  8), Hex.get_next_name(), None, rsctyp.GRAIN),              # --  Q --
            Hex(Point( 6,  8), Hex.get_next_name(), 3,    rsctyp.LUMBER),             # --  R --
            Hex(Point( 8,  8), Hex.get_next_name(), 11,   rsctyp.DESERT, True),       # --  S --
            Hex(Point(10,  8), Hex.get_next_name(), 4,    rsctyp.LUMBER),             # --  T --
            Hex(Point(12,  8), Hex.get_next_name(), 8,    rsctyp.ORE),                # --  U --
            Hex(Point(14,  8), Hex.get_next_name(), None, rsctyp.FRAME),              # --  V --

            # --- row 4
            Hex(Point( 3, 10), Hex.get_next_name(), None, rsctyp.FRAME),              # --  W --
            Hex(Point( 5, 10), Hex.get_next_name(), 8,    rsctyp.LUMBER),             # --  X --
            Hex(Point( 7, 10), Hex.get_next_name(), 10,   rsctyp.ORE),                # --  Y --
            Hex(Point( 9, 10), Hex.get_next_name(), 9,    rsctyp.GRAIN),              # --  Z --
            Hex(Point(11, 10), Hex.get_next_name(), 3,    rsctyp.WOOL),               # -- AA --
            Hex(Point(13, 10), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AB --

            # --- row 5
            Hex(Point( 4, 12), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AC --
            Hex(Point( 6, 12), Hex.get_next_name(), 5,    rsctyp.BRICK),              # -- AD --
            Hex(Point( 8, 12), Hex.get_next_name(), 2,    rsctyp.GRAIN),              # -- AE --
            Hex(Point(10, 12), Hex.get_next_name(), 6,    rsctyp.WOOL),               # -- AR --
            Hex(Point(12, 12), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AF --

            # --- row n: rsctyp.FRAME
            Hex(Point( 5, 14), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AG --
            Hex(Point( 7, 14), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AH --
            Hex(Point( 9, 14), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AI --
            Hex(Point(11, 14), Hex.get_next_name(), None, rsctyp.FRAME)               # -- AG --
        ]

        return hexes

    @classmethod
    def get_std_hex_layout5(cls):
        hexes = [
            # --- row 0: rsctyp.FRAME
            Hex(Point( 5,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  A --
            Hex(Point( 7,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  B --
            Hex(Point( 9,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  C --
            Hex(Point(11,  2), Hex.get_next_name(), None, rsctyp.FRAME),              # --  D --

            # --- row 1
            Hex(Point( 4,  4), Hex.get_next_name(), None, rsctyp.FRAME),              # --  E --
            Hex(Point( 6,  4), Hex.get_next_name(), 11,   rsctyp.ORE),                # --  F --
            Hex(Point( 8,  4), Hex.get_next_name(), 12,   rsctyp.WOOL),               # --  G --
            Hex(Point(10,  4), Hex.get_next_name(), 9,    rsctyp.LUMBER),             # --  H --
            Hex(Point(12,  4), Hex.get_next_name(), None, rsctyp.FRAME),              # --  I --

            # --- row 2
            Hex(Point( 3,  6), Hex.get_next_name(), None, rsctyp.FRAME),              # --  J --
            Hex(Point( 5,  6), Hex.get_next_name(), 4,    rsctyp.GRAIN),              # --  K --
            Hex(Point( 7,  6), Hex.get_next_name(), 6,    rsctyp.BRICK),              # --  L --
            Hex(Point( 9,  6), Hex.get_next_name(), 5,    rsctyp.WOOL),               # --  M --
            Hex(Point(11,  6), Hex.get_next_name(), 10,   rsctyp.BRICK),              # --  N --
            Hex(Point(13,  6), Hex.get_next_name(), None, rsctyp.FRAME),              # --  O --

            # --- row 3
            Hex(Point( 2,  8), Hex.get_next_name(), None, rsctyp.FRAME),              # --  P --
            Hex(Point( 4,  8), Hex.get_next_name(), None, rsctyp.GRAIN),              # --  Q --
            Hex(Point( 6,  8), Hex.get_next_name(), 3,    rsctyp.LUMBER),             # --  R --
            Hex(Point( 8,  8), Hex.get_next_name(), 11,   rsctyp.DESERT, True),       # --  S --
            Hex(Point(10,  8), Hex.get_next_name(), 4,    rsctyp.LUMBER),             # --  T --
            Hex(Point(12,  8), Hex.get_next_name(), 8,    rsctyp.ORE),                # --  U --
            Hex(Point(14,  8), Hex.get_next_name(), None, rsctyp.FRAME),              # --  V --

            # --- row 4
            Hex(Point( 3, 10), Hex.get_next_name(), None, rsctyp.FRAME),              # --  W --
            Hex(Point( 5, 10), Hex.get_next_name(), 8,    rsctyp.LUMBER),             # --  X --
            Hex(Point( 7, 10), Hex.get_next_name(), 10,   rsctyp.ORE),                # --  Y --
            Hex(Point( 9, 10), Hex.get_next_name(), 9,    rsctyp.GRAIN),              # --  Z --
            Hex(Point(11, 10), Hex.get_next_name(), 3,    rsctyp.WOOL),               # -- AA --
            Hex(Point(13, 10), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AB --

            # --- row 5
            Hex(Point( 4, 12), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AC --
            Hex(Point( 6, 12), Hex.get_next_name(), 5,    rsctyp.BRICK),              # -- AD --
            Hex(Point( 8, 12), Hex.get_next_name(), 2,    rsctyp.GRAIN),              # -- AE --
            Hex(Point(10, 12), Hex.get_next_name(), 6,    rsctyp.WOOL),               # -- AR --
            Hex(Point(12, 12), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AF --

            # --- row n: rsctyp.FRAME
            Hex(Point( 5, 14), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AG --
            Hex(Point( 7, 14), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AH --
            Hex(Point( 9, 14), Hex.get_next_name(), None, rsctyp.FRAME),              # -- AI --
            Hex(Point(11, 14), Hex.get_next_name(), None, rsctyp.FRAME)               # -- AG --
        ]

        return hexes

    @classmethod
    def get_std_hex_layout2(cls):
        hexes = [
            Hex(Point(4, 1), Hex.get_next_name(), None, rsctyp.FRAME),              # --  A --
            Hex(Point(6, 1), Hex.get_next_name(), None, rsctyp.FRAME),              # --  B --
            Hex(Point(8, 1), Hex.get_next_name(), None, rsctyp.FRAME),              # --  C --
            Hex(Point(10, 1), Hex.get_next_name(), None, rsctyp.FRAME),             # --  D --

            Hex(Point(3, 3), Hex.get_next_name(), None, rsctyp.FRAME),              # --  E --
            Hex(Point(5, 3), Hex.get_next_name(), 11, rsctyp.LUMBER),               # --  F --
            Hex(Point(7, 3), Hex.get_next_name(), 12, rsctyp.WOOL),                 # --  G --
            Hex(Point(9, 3), Hex.get_next_name(), 9, rsctyp.GRAIN),                 # --  H --
            Hex(Point(11, 3), Hex.get_next_name(), None, rsctyp.FRAME),             # --  I --

            Hex(Point(2, 5), Hex.get_next_name(), None, rsctyp.FRAME),              # --  J --
            Hex(Point(4, 5), Hex.get_next_name(), 4, rsctyp.BRICK),                 # --  K --
            Hex(Point(6, 5), Hex.get_next_name(), 6, rsctyp.ORE),                   # --  L --
            Hex(Point(8, 5), Hex.get_next_name(), 5, rsctyp.BRICK),                 # --  M --
            Hex(Point(10, 5), Hex.get_next_name(), 10, rsctyp.WOOL),                # --  N --
            Hex(Point(12, 5), Hex.get_next_name(), None, rsctyp.FRAME),             # --  O --

            Hex(Point(1, 7), Hex.get_next_name(), None, rsctyp.FRAME),              # --  P --
            Hex(Point(3, 7), Hex.get_next_name(), None, rsctyp.DESERT, True),       # --  Q --
            Hex(Point(5, 7), Hex.get_next_name(), 3, rsctyp.LUMBER),                # --  R --
            Hex(Point(7, 7), Hex.get_next_name(), 11, rsctyp.GRAIN),                # --  S --
            Hex(Point(9, 7), Hex.get_next_name(), 4, rsctyp.LUMBER),                # --  T --
            Hex(Point(11, 7), Hex.get_next_name(), 8, rsctyp.GRAIN),                # --  U --
            Hex(Point(13, 7), Hex.get_next_name(), None, rsctyp.FRAME),             # --  V --

            Hex(Point(2, 9), Hex.get_next_name(), None, rsctyp.FRAME),              # --  W --
            Hex(Point(4, 9), Hex.get_next_name(), 8, rsctyp.BRICK),                 # --  X --
            Hex(Point(6, 9), Hex.get_next_name(), 10, rsctyp.WOOL),                 # --  Y --
            Hex(Point(8, 9), Hex.get_next_name(), 9, rsctyp.WOOL),                  # --  Z --
            Hex(Point(10, 9), Hex.get_next_name(), 3, rsctyp.ORE),                  # -- AA --
            Hex(Point(12, 9), Hex.get_next_name(), None, rsctyp.FRAME),             # -- AB --

            Hex(Point(3, 11), Hex.get_next_name(), None, rsctyp.FRAME),             # -- AC --
            Hex(Point(5, 11), Hex.get_next_name(), 5, rsctyp.ORE),                  # -- AD --
            Hex(Point(7, 11), Hex.get_next_name(), 2, rsctyp.GRAIN),                # -- AE --
            Hex(Point(9, 11), Hex.get_next_name(), 6, rsctyp.LUMBER),               # -- AR --
            Hex(Point(11, 11), Hex.get_next_name(), None, rsctyp.FRAME),            # -- AF --

            Hex(Point(4, 13), Hex.get_next_name(), None, rsctyp.FRAME),             # -- AG --
            Hex(Point(6, 13), Hex.get_next_name(), None, rsctyp.FRAME),             # -- AH --
            Hex(Point(8, 13), Hex.get_next_name(), None, rsctyp.FRAME),             # -- AI --
            Hex(Point(10, 13), Hex.get_next_name(), None, rsctyp.FRAME)             # -- AG --
        ]

        return hexes
