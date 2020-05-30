import re


ident = lambda x: x
true = lambda _: True
fst = lambda (x, _): x
snd = lambda (_, y): y
onFst = lambda f: lambda (x, y): (f(x), y)
swap = lambda (x, y): (y, x)


def parseIndent (line):
    stripped = line.lstrip()
    level = len(line) - len(stripped)
    return (level, stripped)

def parseHierStr (string, normalize=True, filterEmpty=True):
    lines = string.splitlines()
    withIndents = map(parseIndent, lines)
    p = snd if filterEmpty else true
    filtered = filter(p, withIndents)

    if not normalize:
        return filtered

    curIndent = -1
    indentStack = []
    normLevel = -1
    normalized = []
    for linenum, (indent, part) in enumerate(filtered):
        if indent > curIndent:
            indentStack.append(curIndent)
            curIndent = indent
            normLevel = normLevel + 1
        elif indent < curIndent:
            while curIndent > indent:
                if indent not in indentStack:
                    raise RuntimeError, "outdent to non-existing indent level in line " + str(linenum + 1) + ": " + str((indent, part))
                curIndent = indentStack.pop()
                normLevel = normLevel - 1
        normalized.append((normLevel, part))
    return normalized

