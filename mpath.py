import os


class MPaths (object):

    def __init__ (self, pathTree):
        self.pathTree = pathTree
        self.pathTable = {}
        self.buildPathTable(pathTree)

    def buildPathTable (self, tree, prefix=""):
        for n, r, ps in tree:
            pathSoFar = os.path.join(prefix, r)
            self.pathTable[n] = pathSoFar
            self.buildPathTable(ps, prefix=pathSoFar)

    def getRoots (self):
        return map(lambda (_, r, __): r, self.pathTree)

