class MPaths (object):

    def __init__ (self, pathTree):
        self.pathsTree = pathTree

    def getRoots (self):
        return map(lambda (_, r, __): r, self.pathsTree)

