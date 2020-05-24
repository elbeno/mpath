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
    if normalize:
        levels = sorted(list(set(map(fst, filtered))))
        normMap = dict(map(swap, enumerate(levels)))
        normalized = map(onFst(lambda x: normMap[x]), filtered)
        return normalized
    return filtered

