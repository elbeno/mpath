import os

from . import util


ident = lambda x: x
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


class Path (str):

    def __init__ (self, path):
        self.linuxStyle = True if path[0] == "/" else False
        self.parts = filter(ident, path.split("/"))
        self.userPath = path

    def __str__ (self):
        prefix = "/" if self.linuxStyle else ""
        path = prefix + "/".join(self.parts)
        return path

    def __len__ (self):
        return len(str(self))

    def __eq__ (self, other):
        return str(self) == str(other)

    def __iter__ (self):
        return iter(str(self))

    def __contains__ (self, elem):
        return elem in str(self)

    def __reversed__ (self):
        return reversed(str(self))

    def exists (self):
        return os.path.exists(str(self))

    def isfile (self):
        return os.path.isfile(str(self))

    def isdir (self):
        return os.path.isdir(str(self))


class MPaths (dict):

    def __init__ (self, pathTree, dotSyntax=True):
        self.pathTree = pathTree
        self.dotSyntax = dotSyntax
        self.pathTable = {}
        self.buildPaths(pathTree)

    def __str__ (self):
        toLine = lambda (k, v): str(k) + ": " + str(v)
        lines = map(toLine, sorted(self.items()))
        body = "{ " + "\n, ".join(lines) + " }"
        return body

    def buildPaths (self, tree, prefix=""):
        for n, r, ps in tree:
            pathSoFar = os.path.normpath(os.path.join(prefix, r))
            self[n] = Path(pathSoFar)
            self.buildPaths(ps, prefix=pathSoFar)
        if self.dotSyntax:
            for key in self.keys():
                setattr(self, key, self[key])

    def pprint (self):
        print str(self) # not testable, unfortunately


fromLayoutStr = comp2(MPaths)(parseLayout)

