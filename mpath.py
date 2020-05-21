fst = lambda (x, _): x
snd = lambda (_, y): y


class MPaths (object):

    def __init__ (self, paths):
        self.paths = paths

    def getRoots (self):
        return map(fst, self.paths)

