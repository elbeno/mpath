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

def normalizeIndents (indents, withIndents):
    if not withIndents:
        return []
    (indent, line) = withIndents[0]
    if not indents:
        indents = [indent]
    if indent == indents[-1]:
        return [(len(indents) - 1, line)] + normalizeIndents(indents, withIndents[1:])
    if indent > indents[-1]:
        return [(len(indents), line)] + normalizeIndents(indents + [indent], withIndents[1:])
    if indent < indents[-1]:
        if indent not in indents:
            raise RuntimeError, "outdent to non-existing indent level in " +  str((indent, line))
        return normalizeIndents(indents[:-1], withIndents)

def parseHierStr (string, normalize=True, filterEmpty=True):
    lines = string.splitlines()
    withIndents = map(parseIndent, lines)
    p = snd if filterEmpty else true
    filtered = filter(p, withIndents)
    if normalize:
        return normalizeIndents([], filtered)
    else:
        return filtered

