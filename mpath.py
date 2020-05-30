"""
MPath - Simple handling of projects paths for Autodesk Maya

Description:
    Pronounced "empath" - pathing tools that seem to know what you need.

    This module provides the MPaths class, and a few supporting classes and
    functions. MPaths are collections of project-level paths, important to a
    user, and/or tooling, which can be passed into tools, to give them easy
    access to absolute, project-level paths, with a host of helpful tooling
    around them. Beneath the niceties, the core intention is to free users and
    tool makers from the shackles of hardcoded paths throughout their codebase.

Goals:
    - avoid the brittleness of paths scattered throughout a codebase
    - avoid the decades-old disaster of backslashes as path separators
    - avoid the complications of Python's os.path module
    - replace heuristics and searching, with determinism and knowing
    - replace string substitution with explicit, trustworthy paths
    - centralize important paths, to both folders and files
    - allow easy access to commonly used paths, via simple names
    - create a single source of truth for an entire project's pathing
    - ease certain path needs, like existence and path type checks
    - provide various formatting, outputting, and pretty-printing options
    - enable smart, tool-level, UI access to path editing and overriding
    - allow easy, temporary, recorded/reviewable, local path tweaks

MPaths are specified very succinctly, and without repetition, in a small,
highly constrained DSL, which closely resembles a simple directory tree.

"""
import os
import re
import json

try:
    import maya.cmds as cmds
except ImportError:
    print 'WARNING (%s): failed to load maya.cmds module.' % __file__

from . import util


ident = lambda x: x


def parseLayoutStr (layoutStr):
    """Convert a multiline path layout string to an MPaths style structure.

    This is a mostly internal tool, not intended for library users.

    See the documentation to fromLayoutStr to understand what a layout string
    is, and how to properly create one for use in generating an MPaths object.

    """
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

    def loadJSON (self):
        with open(str(self), "r") as f:
            data = json.loads(f.read())
        return data


class MPaths (object):

    def __init__ (self, pathSetName, pathTree, dotSyntax=True, *args, **kwargs):
        self.pathSetName = pathSetName
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
        raise KeyError, "Item assignment on MPaths instance not allowed (but if you must, do so on the instance's .paths property)"

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

    def createMenuItem (self, label="Edit Paths..."):
        cmds.menuItem(label=label, command=lambda *_: self.mayaForm())


def fromLayoutStr (pathSetName, layoutStr, *args, **kwargs):
    """This is the intended entry point for creating an MPaths object.

    Description:
        This is just a helper function, which delegates all work elsewhere.

    A path layout string is a representation of a file tree in a multiline
    string. The formatting of the string is simple, but very specific.

    Path Layout String Rules:
        - NO backslashes, anywhere, ever
        - use spaces for indentation
            - tabs should work, but are not supported, and are discouraged
        - indents have similar rules to Python code indentation
            - any number of spaces for indentation is fine (4 is standard)
            - indents can be mismatched, provided they're consistent
            - an outdent to a non-existing, local level is an error
        - multiple path parts can exist on one line, separated by slashes (/)
        - EVERY line needs a name, prefixed to the part, joined by a pipe (|)
        - blank lines are okay
        - it doesn't matter if the entire multiline string is indented
        - trailing slashes on folder-terminated parts okay, but not required

    Path Layout String Examples:
        It's helpful to start with a breakdown of the paths themselves:

        '''
        C:/Work/Project
            Game/Main
                Art
                    Character19
                    Character20
                Exports
                    Characters
                Docs
                    characterProps_v3_finalFINAL.xml
                    allClothing_Setups.xml
        Z:/Empath
            Downloads/thirdParty
                ExportTool/v3/doExport.py
        '''

        Now, name EVERY line, via pipe-connected prefix, and store in a var:

        projLayoutStr='''
        proj|C:/Work/Project
            main|Game/Main
                art|Art
                    oldChars|Character19
                    chars|Character20
                exp|Exports
                    charsExp|Characters
                docs|Docs
                    props|characterProps_v3_finalFINAL.xml
                    attires|allClothing_Setups.xml
        server|Z:/Empath
            3rdParty|Downloads/ExternalTools
                exporter|ExportTool/v3/doExport.py
        '''

    MPaths Creation & Usage:
        Now that you have a proper, rule-abiding, multiline string of your
        project layout, you can parse it into a full MPaths instance:

        MPaths.parseLayoutStr(projLayoutStr)

        It's also possible to manually create a project layout (a recursive
        list of 3-tuples), but it's not worth the effort, nor the bugs such
        fiddly work is likely to create. The recommended way to create an
        MPaths instance is with fromLayoutStr.

    """

    return MPaths(pathSetName, parseLayoutStr(layoutStr), *args, **kwargs)

