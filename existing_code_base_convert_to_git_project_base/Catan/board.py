from constants import VERTEXES, hex_rel_bndg_hexes, compl_vertexes, compl_hexes
import rsctyp
from vertex import Vertex

__author__ = 'gskluzacek'
__date__ = '3/26/16'


class Board:
    def __init__(self, size_x, size_y, hexes):
        self.size_x = size_x
        self.size_y = size_y
        self.board = [[None for z in range(size_x)] for z in range(size_y)]
        for h in hexes:
            loc = h.get_loc()
            if self.validate_location(h):
                self.board[loc.x][loc.y] = h

    def link(self):
        # loop through the x & y board grid, row by row
        for y in range(1, self.size_y):
            for x in range(1, self.size_x):
                # get the hex at a given [x, y] board grid coordinates
                hext = self.get_hex(x, y)
                # if a hext exists at the given coordinates
                if hext is not None:
                    # print 'linking hex %s at coordinates: [%d, %d]' % (hext.name, x, y)
                    # for each vertex name
                    #   1) populate the Potential Working Hex List (p_wrk_hexes)
                    #   2) from the p_wrk_hexes, populate a) the Working Hex List
                    #      (wrk_hexes) and b) the list of unique vertexes
                    for vn in VERTEXES:
                        # print '\tvertex: %s' % vn
                        p_wrk_hexes = {vn: hext}
                        # p_wrk_hexes = {}
                        # add the current hex at the current vertex name
                        # for the given vertex name, get the positional direction for each of the bounding hexes
                        pos_dirs = hex_rel_bndg_hexes[vn]
                        # for each positional direction
                        for pos_dir in pos_dirs:
                            # get the x, y coordinates relative to the current hex at the positional direction given
                            xr, yr = hext.get_relative(pos_dir)
                            # get the hex relative to the current hex
                            hexr = self.get_hex(xr, yr)
                            # if a hext exist at the xr, yr coordinates
                            if hexr is not None:
                                # print '\t\thex %s at relative position %s with coordinates [%d, %d]' % (hexr.name, pos_dir, xr, yr)
                                # if one of the 2 hexes is not a FRAME hex
                                # if hext.rsc_type != Hex.FRAME or hexr.rsc_type != Hex.FRAME:
                                # get the complimentary vertex relative to the positional direction and given vertex name
                                vnc = compl_vertexes[pos_dir][vn]
                                # add the relative hex at the complimentary vertex name
                                p_wrk_hexes[vnc] = hexr
                                # print '\t\t\tP Wrk Hexes: setting compliment vertex %s to hex %s' % (vnc, hexr.name)
                                # print '\t\tsettng compliment vertex of %s for hex %s at relative position %s with coordinates [%d, %d]' % (vnc, hexr.name, pos_dir, xr, yr)
                                # else:
                                # print '\t\t\tP Wrk Hexes: both hexes had a type of FRAME'
                            else:
                                # print '\t\tno hex at relative position %s for coordinates [%d, %d]' % (pos_dir, xr, yr)
                                pass
                        # end for each positional direction
                        # if len(p_wrk_hexes) > 0:
                            # only add hext to potential working hex list if there is at least 1 other hex in the list
                            # p_wrk_hexes[vn] = hext

                        vertex_set = set()
                        wrk_hexes = {}
                        # loop through the Potential Working Hex List to
                        # 1) get the list of hexes where the target vertex (wvn)
                        #    is null
                        # 2) get the list of unique vertexes
                        # print '\tcreating Working Hex List & checking for unique vertex'
                        for wvn, wh in p_wrk_hexes.items():
                            if wh.rsc_type != rsctyp.FRAME:
                                wv = wh.get_vertex(wvn)
                                if wv is None:
                                    # print '\t\tno vertex named %s for hex %s' % (wvn, wh.name)
                                    wrk_hexes[wvn] = wh
                                else:
                                    # print '\t\tfound vertex %d with name of %s for hex %s' % (wv.seq, wvn, wh.name)
                                    vertex_set.add(wv)
                            else:
                                # print '\t\thex %s is a FRAME hex, skipping' % wh.name
                                pass
                        # there must only be 1 vertex for all hexes
                        # print '\tvertex list len: %d, working hex list len: %d' % (len(vertex_set), len(wrk_hexes))
                        if len(vertex_set) > 1:
                            raise Exception('More than 1 vertex object detected for the given intersection')
                        elif len(vertex_set) == 0:
                            # check if at least 1 hex is in the Working Hex List that needs a vertex
                            if len(wrk_hexes) != 0:
                                wv = Vertex()
                                # print '\t\tcreated new vertex %s' % wv.seq
                            else:
                                # print '\t\tNo Hexes eligible for a vertex at given intersection'
                                pass
                        else:
                            # exactly 1 existing vertex was found, get it
                            wv = vertex_set.pop()
                            # print '\t\tusing vertex %s' % wv.seq
                        # for each hex in the Working Vertex list, set its vertex at the vertex name
                        wrk_vertexes = {}
                        for wvn, wh in wrk_hexes.items():
                            # print '\t\t\t>>> setting vertex %s with seq of %d for hex %s <<<' % (wvn, wv.seq, wh.name)
                            wh.set_vertex(wvn, wv)
                            wvnc = compl_hexes[wvn]
                            wrk_vertexes[wvnc] = wh
                        if len(wrk_vertexes) != 0:
                            wv.set_hexes(wrk_vertexes)
                        if len(wrk_hexes) == 0:
                            # print '\t\t\tno hexes need vertexes assigned to them'
                            pass
                    # end for vertex, bounding_hexes in Vertex.hex_rel_bndg_hexes.items():
                else:
                    # print 'skipping linking, no hex at coordinates: [%d, %d]' % (x, y)
                    pass
                # end if hex is not None
            # end for x
        # end for y
    # end def link

    def get_hex(self, x, y):
        if x >= self.size_x or y >= self.size_y or x < 0 or y < 0:
            hext = None
        else:
            hext = self.board[x][y]
        return hext

    def validate_location(self, hext):
        loc = hext.get_loc()
        # print '-' * 100
        # print 'Validating hex: %s at position: %d, %d' % (hex.name, loc.x, loc.y)
        # validate that there is not an existing hex at the new hex's location
        h = self.get_hex(loc.x, loc.y)
        if h is not None:
            raise Exception('cannot place hex: %s at location [%d, %d] because hex: %s already exists at this location' % (hext.name, loc.x, loc.y, h.name))
        # validate that the new hex's x coordinate is greater than 0
        if loc.x <= 0:
            raise Exception('location x coordinate: %d must be greater than 0' % loc.x)
        # validate that the new hex's x coordinate is less than the board's max x coordinate
        if loc.x >= self.size_x:
            raise Exception('location x coordinate: %d must be less than %d' % (self.size_x, loc.x))
        # validate that the new hex's y coordinate is greater than 0
        if loc.y < 0:
            raise Exception('location y coordinate: %d must be greater than 0' % loc.y)
        # validate that the new hex's y coordinate is less than the board's max y coordinate
        if loc.x >= self.size_x:
            raise Exception('location y coordinate: %d must be less than %d' % (self.size_y, loc.y))

        for y in range(1, self.size_y):
            for x in range(1, self.size_x):
                if (loc.y - y + 1) % 2 == 0:
                    # print 'checking: %d %d: ' % (x, y)
                    h = self.get_hex(x, y)
                    if h is not None:
                        raise Exception('cannot place hex: %s at location [%d, %d] because hex: %s already exists at location [%d ,%d]' % (hext.name, loc.x, loc.y, h.name, x, y))
                if (loc.y - y) % 4 == 0:
                    if (loc.x - x + 1) % 2 == 0:
                        # print 'checking: %d %d: ' % (x, y)
                        h = self.get_hex(x, y)
                        if h is not None:
                            raise Exception('cannot place hex: %s at location [%d, %d] because hex: %s already exists at location [%d ,%d]' % (hext.name, loc.x, loc.y, h.name, x, y))
                if (loc.y - y + 2) % 4 == 0:
                    if (loc.x - x) % 2 == 0:
                        # print 'checking: %d %d: ' % (x, y)
                        h = self.get_hex(x, y)
                        if h is not None:
                            raise Exception('cannot place hex: %s at location [%d, %d] because hex: %s already exists at location [%d ,%d]' % (hext.name, loc.x, loc.y, h.name, x, y))
            # print '-' * 10

        return True
