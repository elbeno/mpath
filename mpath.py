import os

from . import util


class MPaths (object):

    def __init__ (self, pathTree):
        self.pathTree = pathTree
        self.pathTable = {}
        self.buildPathTable(pathTree)

    def buildPathTable (self, tree, prefix=""):
        for n, r, ps in tree:
            pathSoFar = os.path.normpath(os.path.join(prefix, r))
            self.pathTable[n] = pathSoFar
            self.buildPathTable(ps, prefix=pathSoFar)


def parseLayout (layoutStr):
    layoutList = util.parseHier(layoutStr)
    levels = set([0])
    curLev = 0
    for linenum, (level, part) in enumerate(layoutList):
        if level > curLev:
            levels.add(level)
        elif level == curLev:
            pass
        elif level < curLev:
            if level not in levels:
                raise RuntimeError, "outdent to non-existing indent level in line " + str(linenum + 1) + ": " + str((level, part))
        curLev = level

