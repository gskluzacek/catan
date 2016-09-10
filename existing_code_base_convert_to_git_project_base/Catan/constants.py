from dirpos import NORTH, NEAST, EAST, SEAST, SOUTH, SWEST, WEST, NWEST
from dirpos import RELTOHEX, RELTOVERTEX, RELTOEDGE, RELTOHEXTOHEX
from dirpos import LEFT, RIGHT

__author__ = 'gskluzacek'
__date__ = '3/26/16'

# the list of directional hex positions
HEXES = [NEAST, EAST, SEAST, SWEST, WEST, NWEST]

# the list of directional edge positions
EDGES = [NEAST, EAST, SEAST, SWEST, WEST, NWEST]

# the list of directional vertex positions
VERTEXES = [NORTH, NEAST, SEAST, SOUTH, SWEST, NWEST]

#
# edge constants
#

r2e_edge_vertexes = {
    NEAST: [NWEST, SEAST],
    EAST: [NORTH, SOUTH],
    SEAST: [NEAST, SWEST],
    SWEST: [SEAST, NWEST],
    WEST: [SOUTH, NORTH],
    NWEST: [SWEST, NEAST]
}

#
# hex constants
#

compl_hex_to_hex = {
    NEAST: SWEST,
    EAST: WEST,
    SEAST: NWEST,
    SWEST: NEAST,
    WEST: EAST,
    NWEST: SEAST
}

# board grid relative offsets for each positional direction
relative_offset = {
    NEAST: {'x': 1, 'y': -2},
    EAST: {'x': 2, 'y': 0},
    SEAST: {'x': 1, 'y': 2},
    SWEST: {'x': -1, 'y': 2},
    WEST: {'x': -2, 'y': 0},
    NWEST: {'x': -1, 'y': -2}
}

foo_bar = {
    NEAST:   {NWEST: NORTH,   SEAST: NEAST},
    EAST:    {NORTH: NEAST,   SOUTH: SEAST},
    SEAST:   {NEAST: SEAST,   SWEST: SOUTH},
    SWEST:   {SEAST: SOUTH,   NWEST: SWEST},
    WEST:    {SOUTH: SWEST,   NORTH: NWEST},
    NWEST:   {SWEST: NWEST,   NEAST: NORTH}
}

vertex_rel_hex_edge = {
    NEAST: {
        RELTOHEX: {LEFT: NORTH, RIGHT: NEAST},
        RELTOEDGE: {LEFT: NWEST, RIGHT: SEAST}
    },
    EAST: {
        RELTOHEX: {LEFT: NEAST, RIGHT: SEAST},
        RELTOEDGE: {LEFT: NORTH, RIGHT: SOUTH}
    },
    SEAST: {
        RELTOHEX: {LEFT: SEAST, RIGHT: SOUTH},
        RELTOEDGE: {LEFT: NEAST, RIGHT: SWEST}
    },
    SWEST: {
        RELTOHEX: {LEFT: SOUTH, RIGHT: SWEST},
        RELTOEDGE: {LEFT: SEAST, RIGHT: NWEST}
    },
    WEST: {
        RELTOHEX: {LEFT: SWEST, RIGHT: NWEST},
        RELTOEDGE: {LEFT: SOUTH, RIGHT: NORTH}
    },
    NWEST: {
        RELTOHEX: {LEFT: NWEST, RIGHT: NORTH},
        RELTOEDGE: {LEFT: SWEST, RIGHT: NEAST}
    }
}

blah_blah_blah = {
    NORTH: {
        RELTOHEX: {LEFT: NWEST, RIGHT: NEAST},
        RELTOVERTEX: {LEFT: SWEST, RIGHT: SEAST},
        RELTOHEXTOHEX: WEST
    },
    NEAST: {
        RELTOHEX: {LEFT: NEAST, RIGHT: EAST},
        RELTOVERTEX: {LEFT: NWEST, RIGHT: SOUTH},
        RELTOHEXTOHEX: NWEST
    },
    SEAST: {
        RELTOHEX: {LEFT: EAST, RIGHT: SEAST},
        RELTOVERTEX: {LEFT: NORTH, RIGHT: SWEST},
        RELTOHEXTOHEX: NEAST
    },
    SOUTH: {
        RELTOHEX: {LEFT: SEAST, RIGHT: SWEST},
        RELTOVERTEX: {LEFT: NEAST, RIGHT: NWEST},
        RELTOHEXTOHEX: EAST
    },
    SWEST: {
        RELTOHEX: {LEFT: SWEST, RIGHT: WEST},
        RELTOVERTEX: {LEFT: SEAST, RIGHT: NORTH},
        RELTOHEXTOHEX: SEAST
    },
    NWEST: {
        RELTOHEX: {LEFT: WEST, RIGHT: NWEST},
        RELTOVERTEX: {LEFT: SOUTH, RIGHT: NEAST},
        RELTOHEXTOHEX: SWEST
    }
}

#
# vertex constants
#

# for each vertex, there is a hex that bound each side of it (in additional to the hex the vertex is relative to
hex_rel_bndg_hexes = {
        NORTH: [NWEST, NEAST],
        NEAST: [NEAST, EAST],
        SEAST: [EAST,  SEAST],
        SOUTH: [SEAST, SWEST],
        SWEST: [SWEST, WEST],
        NWEST: [WEST,  NWEST]
}
#
compl_vertexes = {
    NEAST: {NORTH: SWEST, NEAST: SOUTH},
    EAST:  {NEAST: NWEST, SEAST: SWEST},
    SEAST: {SEAST: NORTH, SOUTH: NWEST},
    SWEST: {SOUTH: NEAST, SWEST: NORTH},
    WEST:  {SWEST: SEAST, NWEST: NEAST},
    NWEST: {NWEST: SOUTH, NORTH: SEAST}
}

compl_hexes = {
    NORTH: SOUTH,
    NEAST: SWEST,
    SEAST: NWEST,
    SOUTH: NORTH,
    SWEST: NEAST,
    NWEST: SEAST
}

# this is a comment
vrtx_rel_bndg_vrtxs = {
    NORTH: [SEAST, SWEST],
    NEAST: [SOUTH, NWEST],
    SEAST: [SWEST, NORTH],
    SOUTH: [NWEST, NEAST],
    SWEST: [NORTH, SEAST],
    NWEST: [NEAST, SOUTH]
}

# There are 2 type of vertexes, even (NE=2, S=4, NW=6) & odd (N=1, SE=3, SW=5)
EVEN = 'E'
ODD = 'O'

# Hexes exist at the following 'directional positions' relative to a given vertex
# hexes = {
even_odd_hexes = {
        EVEN: [NORTH, SEAST, SWEST],
        ODD: [NEAST, SOUTH, NWEST]
}
