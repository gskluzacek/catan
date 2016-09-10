__author__ = 'gskluzacek'
__date__ = '3/26/16'


class Site:
    def __init__(self):
        self.harbor = None
        self.rsc_qty = 0

    def set_habor(self, harbor):
        self.harbor = harbor

    def get_harbor(self):
        return self.harbor

    def has_harbor(self):
        if self.harbor is not None:
            return True
        else:
            return False


class Settlement(Site):
    def __init__(self):
        Site.__init__(self)
        self.rsc_qty = 1


class City(Site):
    def __init__(self):
        Site.__init__(self)
        self.rsc_qty = 2
