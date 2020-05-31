import re


ident = lambda x: x
true = lambda _: True
fst = lambda (x, _): x
snd = lambda (_, y): y
onFst = lambda f: lambda (x, y): (f(x), y)
swap = lambda (x, y): (y, x)


def parseIndent (line):
    stripped = line.lstrip()
    indent = len(line) - len(stripped)
    return (indent, stripped)

def normalizeIndents(lines, index=0, curIndent=0, level=0):
    normalized = []
    while index < len(lines):
        (indent, line) = lines[index]
        if indent > curIndent:
            raise RuntimeError, "outdent to non-existing indent level in line " + str(index) + ": " + str((indent, line))
        elif indent < curIndent:
            return (normalized, index)

        normalized.append((level, line))
        (children, index) = normalizeSubtree(lines, index+1, curIndent, level+1)
        normalized.extend(children)

    return (normalized, index)

def normalizeSubtree (lines, index=0, curIndent=-1, level=0):
    if index < len(lines):
        (nextIndent, _) = lines[index]
        if nextIndent > curIndent:
            return normalizeIndents(lines, index, nextIndent, level)
    return ([], index)

def parseHierStr(string, normalize=True, filterEmpty=True):
    lines = string.splitlines()
    withIndents = map(parseIndent, lines)
    p = snd if filterEmpty else true
    filtered = filter(p, withIndents)
    if not normalize:
        return filtered
    n, _ = normalizeSubtree(filtered)
    return n
