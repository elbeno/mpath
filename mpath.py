import os

from . import util


comp2 = lambda f: lambda g: lambda x: f(g(x))


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


class MPaths (dict):

    def __init__ (self, pathTree, dotSyntax=True):
        self.pathTree = pathTree
        self.dotSyntax = dotSyntax
        self.pathTable = {}
        self.buildPathTable(pathTree)

    def buildPathTable (self, tree, prefix=""):
        for n, r, ps in tree:
            pathSoFar = os.path.normpath(os.path.join(prefix, r))
            self[n] = pathSoFar
            self.buildPathTable(ps, prefix=pathSoFar)
        if self.dotSyntax:
            for key in self.keys():
                setattr(self, key, self[key])


fromLayoutStr = comp2(MPaths)(parseLayout)

