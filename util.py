import re


ident = lambda x: x
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

def parseHier (string, normalized=True, filterEmpty=True):
    lines = string.splitlines()
    rawindents = map(parseIndent, lines)
    if filterEmpty:
        indents = filter(snd, rawindents)
    else:
        indents = rawindents
    if normalized:
        levels = sorted(list(set(map(fst, indents))))
        normMap = dict(map(swap, enumerate(levels)))
        return map(onFst(lambda x: normMap[x]), indents)
    return indents

