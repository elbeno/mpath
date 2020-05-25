import re


ident = lambda x: x
true = lambda _: True
fst = lambda (x, _): x
snd = lambda (_, y): y
onFst = lambda f: lambda (x, y): (f(x), y)
swap = lambda (x, y): (y, x)


def parseIndent (line):
    match = re.match("^(\s+)", line)
    if match:
        indent = match.group()
        indentLen = len(indent)
        return (indentLen, line[indentLen:])
    else:
        return (0, line)

def parseHier (string, normalize=True, filterEmpty=True):
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
            curIndent = indent
            indentStack.append(indent)
            normLevel = normLevel + 1
        elif indent < curIndent:
            while True:
                if indentStack == []:
                    raise RuntimeError, "outdent to non-existing indent level in line " + str(linenum + 1) + ": " + str((indent, part))
                curIndent = indentStack.pop()
                if curIndent == indent:
                    break
                normLevel = normLevel - 1
        normalized.append((normLevel, part))
    return normalized

