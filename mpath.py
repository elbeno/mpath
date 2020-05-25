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
    hier = util.parseHier(layoutStr)
    layout = []
    layoutStack = [layout]
    subEntry = None
    curLev = 0
    for (lineNum, (level, namedPart)) in enumerate(hier):
        name, part = namedPart.split("|")
        if level == curLev:
            subEntry = []
            newEntry = (name, part, subEntry)
            curLayout = layoutStack[-1]
            curLayout.append(newEntry)
        elif level == curLev + 1:
            oldSubEntry = subEntry
            subEntry = []
            newEntry = (name, part, subEntry)
            oldSubEntry.append(newEntry)
            layoutStack.append(subEntry)
            curLev = level
        elif level < curLev:
            n = curLev - level
            for _ in range(n):
                layoutStack.pop()
            newEntry = (name, part, [])
            curLayout = layoutStack[-1]
            curLayout.append(newEntry)
            layoutStack.append(newEntry)
            curLev = level
        elif level > curLev + 1:
            raise RuntimeError, "Level increase from " + str(curLev) + " to " + str(level) + " in hierarchy line " + str(lineNum) + ": " + str((level, namedPart))
    return layout

