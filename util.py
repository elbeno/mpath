import re


def parseIndent (line):
    match = re.match("^(\s+)", line)
    if match:
        indent = match.group()
        indentLen = len(indent)
        return (indentLen, line[indentLen:])
    else:
        return (0, line)

