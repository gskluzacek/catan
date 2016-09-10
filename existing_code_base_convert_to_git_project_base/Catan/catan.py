from player import Player
from game import Game
import sys
import rsctyp

hex_c_len = 50

ps = [
    Player('bob'),
    Player('tom'),
    Player('joe')
]
rd = []
dd = []
l = Game.get_std_hex_layout()
g = Game(ps, l, rd, dd, hex_c_len, False)

# sys.exit(0)

for i in range(g.max_y):
    for j in range(g.max_x):
        hext = g.board.get_hex(j, i)
        if hext is not None:
            if hext.get_rsc_type() == rsctyp.FRAME:
                print hext.svg()

for i in range(g.max_y):
    for j in range(g.max_x):
        hext = g.board.get_hex(j, i)
        if hext is not None:
            if hext.get_rsc_type() != rsctyp.FRAME:
                print hext.svg()
