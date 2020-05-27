import os
import re

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from . import util


ident = lambda x: x


def parseLayoutStr (layoutStr):
    hier = util.parseHierStr(layoutStr)
    layout = []
    layoutStack = [layout]
    curLev = 0
    for (lineNum, (level, namedPart)) in enumerate(hier):
        name, part = namedPart.split("|")
        if level == curLev:
            newEntry = (name, part, [])
            curLayout = layoutStack[-1]
            curLayout.append(newEntry)
        elif level == curLev + 1:
            newEntry = (name, part, [])
            (_, __, curLayout) = layoutStack[-1][-1]
            curLayout.append(newEntry)
            layoutStack.append(curLayout)
            curLev = level
        elif level < curLev:
            while curLev > level:
                layoutStack.pop()
                curLev = curLev - 1
            newEntry = (name, part, [])
            curLayout = layoutStack[-1]
            curLayout.append(newEntry)
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

    def extend (self, *args):
        prelimPath = "/".join([self] + list(args))
        noBackslashes = re.sub("\\\\", "/", prelimPath)
        singleSlashes = re.sub("/+", "/", noBackslashes)
        noTrailingSlash = re.sub("/$", "", singleSlashes)
        return noTrailingSlash


class MPaths (object):

    def __init__ (self, pathTree, dotSyntax=True, *args, **kwargs):
        self.pathTree = pathTree
        self.dotSyntax = dotSyntax
        self.paths = {}
        self.buildPaths(pathTree)

    def __str__ (self):
        toLine = lambda (k, v): str(k) + ": " + str(v)
        lines = map(toLine, sorted(self.paths.items()))
        body = "{ " + "\n, ".join(lines) + " }"
        return body

    def __getitem__ (self, item):
        if item in self.paths:
            return self.paths[item]
        raise KeyError, "No path with the name \"" + item + "\" in MPaths"

    def __setitem__ (self, _, __):
        raise KeyError, "Item assignemt on MPaths instance not allowed (but if you must, do so on the instance's .paths property)"

    def keys (self):
        return self.paths.keys()

    def values (self):
        return self.paths.values()

    def items (self):
        return self.paths.items()

    def buildPaths (self, tree, prefix=""):
        for name, part, subParts in tree:
            pathSoFar = os.path.normpath(os.path.join(prefix, part))
            self.paths[name] = Path(pathSoFar.replace("\\", "/"))
            self.buildPaths(subParts, prefix=pathSoFar)
        if self.dotSyntax:
            for key in self.paths.keys():
                setattr(self, key, self.paths[key])

    def pformat (self, indent=4, *args, **kwargs):
        indstr = " " * indent
        def pfStep (level):
            def pfStepSub ((name, part, subParts)):
                rendInd = indstr * level
                if self.paths[name].exists():
                    if self.paths[name].isdir():
                        rendPart = part + "/"
                    else:
                        rendPart = part
                else:
                    rendPart = part
                rendLine = rendInd + rendPart + " (" + name + ")"
                return "\n".join([rendLine] + map(pfStep(level + 1), subParts))
            return pfStepSub
        return "\n".join(map(pfStep(0), self.pathTree))

    # untestable methods (UI, printing) follow

    def pprint (self, *args, **kwargs):
        print self.pformat(*args, **kwargs)

    def mayaForm (self, indent=8):
        win = cmds.window(title="MPaths Path Editor", widthHeight=(400, 300))
        cmds.showWindow()
        cmds.scrollLayout(childResizable=True)
        form = cmds.formLayout()
        box_part = cmds.frameLayout(label="Path Part", parent=form)
        box_name = cmds.frameLayout(label="Part Name", parent=form)
        cmds.formLayout(form, edit=True, attachPosition=( (box_part, "right", 1, 70)
                                                        , (box_name, "left", 1, 70) )
                                       , attachForm=( (box_part, "left", 2)
                                                    , (box_name, "right", 2) )
                       )
        pretty = self.pformat(indent=indent)
        last_row = box_name
        for line in pretty.split("\n"):
            m = re.match("^( *)(.*) \((.*)\)$", line)
            indent, part, name = m.groups()
            txt_indent = cmds.text(label=indent, parent=form)
            txt_part = cmds.textField(text=part, parent=form)
            txt_name = cmds.textField(text=name, parent=form)
            cmds.formLayout(form, edit=True, attachForm=( (txt_indent, "left", 1)
                                                        , (txt_name, "right", 1) )
                                            , attachPosition=( (txt_name, "left", 1, 70)
                                                             , (txt_part, "right", 1, 70) )
                                            , attachControl=( (txt_part, "left", 0, txt_indent)
                                                            , (txt_indent, "top", 1, last_row)
                                                            , (txt_part, "top", 1, last_row)
                                                            , (txt_name, "top", 1, last_row) )
                           )
            last_row = txt_name


def fromLayoutStr (layoutStr, *args, **kwargs):
    return MPaths(parseLayoutStr(layoutStr), *args, **kwargs)

