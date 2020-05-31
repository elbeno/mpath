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

def normalizeIndents(lines, expectedIndent=0, level=0):
    normalized = []
    while lines:
        (indent, line) = lines[0]
        if indent > expectedIndent:
            raise RuntimeError, "outdent to non-existing indent level in line " + str((indent, line))
        elif indent < expectedIndent:
            return (normalized, lines)

        normalized.append((level, line))
        (children, lines) = normalizeSubtree(lines[1:], expectedIndent, level+1)
        normalized.extend(children)

    return (normalized, lines)

def normalizeSubtree (lines, expectedIndent=-1, level=0):
    if lines:
        (nextIndent, _) = lines[0]
        if nextIndent > expectedIndent:
            return normalizeIndents(lines, nextIndent, level)
    return ([], lines)

def parseHierStr(string, normalize=True, filterEmpty=True):
    lines = string.splitlines()
    withIndents = map(parseIndent, lines)
    p = snd if filterEmpty else true
    filtered = filter(p, withIndents)
    if not normalize:
        return filtered
    n, _ = normalizeSubtree(filtered)
    return n
