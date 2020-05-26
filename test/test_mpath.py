import unittest
from nose.plugins.attrib import attr
import tempfile


from .. import mpath


linA = [ ( "root"
         , "/home/gfixler/proj"
         , [ ( "charSrc", "art/chars", [] )
           , ( "charExp", "assets/chars", [] )
           ]
         )
       ]

winA = [ ( "srcRoot"
         , "C:/game"
         , [ ( "charSrc", "art/chars", [] )
           , ( "docs"
             , "Docs"
             , [ ( "itemsDoc", "items.json", [] )
               ]
             )
           ]
         )
       , ( "expRoot"
         , "Z:/game"
         , [ ( "charExp", "assets/chars", [] )
           ]
         )
       ]

winALayout = """
srcRoot|C:/game
    charSrc|art/chars
    docs|Docs
        itemsDoc|items.json
expRoot|Z:/game
    charExp|assets/chars
"""

class Test_parseLayout (unittest.TestCase):

    def test_buildsTree (self):
        layout = mpath.parseLayout(winALayout)
        expected = [('srcRoot',
                     'C:/game',
                     [('charSrc',
                       'art/chars',
                       [('docs',
                         'Docs',
                         [('itemsDoc',
                           'items.json',
                           [('charExp',
                             'assets/chars',
                             []
                            )]
                          )]
                        )]
                      )]
                    ),
                    ('expRoot',
                     'Z:/game',
                     [])
                   ]
        self.assertEquals(layout, expected)


class Test_Path (unittest.TestCase):

    def test_strYieldsPassedString (self):
        path = mpath.Path("root")
        self.assertEquals(str(path), "root")

    def test_pathLength_linux (self):
        path = mpath.Path("/home/user/stuff")
        self.assertEquals(len(path), 16)

    def test_pathLength_windows (self):
        path = mpath.Path("C:/Users/user/games")
        self.assertEquals(len(path), 19)

    def test_equalityWorksWithStrings (self):
        path = mpath.Path("root")
        self.assertEquals(path, "root")

    def test_inequalityWorksWithStrings (self):
        path = mpath.Path("same")
        self.assertNotEquals(path, "different")

    def test_equalityWorksWithOtherPathInstances (self):
        partA = mpath.Path("root")
        partB = mpath.Path("root")
        self.assertEquals(partA, partB)

    def test_inequalityWorksWithOtherPathInstances (self):
        partA = mpath.Path("same")
        partB = mpath.Path("different")
        self.assertNotEquals(partA, partB)

    def test_canGetParts_linux (self):
        path = mpath.Path("/home/user/proj")
        self.assertEquals(path.parts, ["home", "user", "proj"])

    def test_canGetParts_linux_ignoresTrailing (self):
        path = mpath.Path("/home/user/proj/")
        self.assertEquals(path.parts, ["home", "user", "proj"])

    def test_canGetParts_windows (self):
        path = mpath.Path("C:/Users/user/projects")
        self.assertEquals(path.parts, ["C:", "Users", "user", "projects"])

    def test_canGetParts_windows_ignoresTrailing (self):
        path = mpath.Path("C:/Users/user/projects///")
        self.assertEquals(path.parts, ["C:", "Users", "user", "projects"])

    def test_knowsPathExists (self):
        tmpfile = tempfile.NamedTemporaryFile("w", suffix=".tmp")
        path = mpath.Path(tmpfile.name)
        self.assertTrue(path.exists())

    def test_knowsPathDoesNotExist (self):
        tmpfile = tempfile.NamedTemporaryFile("w")
        path = mpath.Path(tmpfile.name + "DoesNotExist.tmp")
        self.assertFalse(path.exists())

    def test_knowsExistingFileIsAFile (self):
        tmpfile = tempfile.NamedTemporaryFile("w", suffix=".tmp")
        path = mpath.Path(tmpfile.name)
        self.assertTrue(path.isfile())

    def test_knowsNonExistingFileIsNotAFile (self):
        path = mpath.Path(tempfile.gettempdir() + "/madeUp.fil")
        self.assertFalse(path.isfile())

    def test_knowsExistingDirIsNotAFile (self):
        path = mpath.Path(tempfile.gettempdir())
        self.assertFalse(path.isfile())

    def test_knowsExistingDirIsADir (self):
        path = mpath.Path(tempfile.gettempdir())
        self.assertTrue(path.isdir())

    def test_knowsExistingFileIsNotADir (self):
        tmpfile = tempfile.NamedTemporaryFile("w", suffix=".tmp")
        path = mpath.Path(tmpfile.name)
        self.assertFalse(path.isdir())

    def test_knowsNonExistingDirIsNotADir (self):
        path = mpath.Path( "/DoesNotExist")
        self.assertFalse(path.isdir())


class Test_MPaths (unittest.TestCase):

    def test_cannotConstructEmptyMPaths (self):
        self.assertRaises(TypeError, lambda: mpath.MPaths())

    def test_buildPaths_removesTrailingSlashLinux (self):
        mpaths = mpath.MPaths([("root", "/home/gfixler/", [])])
        self.assertEquals(mpaths["root"], "/home/gfixler")

    def test_canGetPathsByName (self):
        mpaths = mpath.MPaths(linA)
        self.assertEquals(mpaths["root"], "/home/gfixler/proj")
        self.assertEquals(mpaths["charSrc"], "/home/gfixler/proj/art/chars")
        self.assertEquals(mpaths["charExp"], "/home/gfixler/proj/assets/chars")
        self.assertEquals(set(mpaths.keys()), set(["root", "charSrc", "charExp"]))

    def test_canMakeFromParsedLayout (self):
        # this one is more of an integration test
        mpaths = mpath.MPaths(mpath.parseLayout(winALayout))
        self.assertEquals(mpaths["srcRoot"], "C:/game")
        self.assertEquals(mpaths["charSrc"], "C:/game/art/chars")
        self.assertEquals(mpaths["itemsDoc"], "C:/game/art/chars/Docs/items.json")
        self.assertEquals(set(mpaths.keys()), set(["srcRoot", "charSrc", "docs", "itemsDoc", "expRoot", "charExp"]))

    def test_fromLayoutStrFunction (self):
        # this is a helper function, not part of the MPath class
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(mpaths["srcRoot"], "C:/game")
        self.assertEquals(mpaths["charSrc"], "C:/game/art/chars")
        self.assertEquals(mpaths["itemsDoc"], "C:/game/art/chars/Docs/items.json")
        self.assertEquals(set(mpaths.keys()), set(["srcRoot", "charSrc", "docs", "itemsDoc", "expRoot", "charExp"]))

    def test_dotSyntaxAllowsForEvenEasierPathLookup (self):
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(mpaths.srcRoot, "C:/game")
        self.assertEquals(mpaths.charSrc, "C:/game/art/chars")
        self.assertEquals(mpaths.itemsDoc, "C:/game/art/chars/Docs/items.json")

    def test_builtPathsArePathInstances (self):
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(type(mpaths["itemsDoc"]), mpath.Path)

    def test_builtPathsWorkWithDotSyntax (self):
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(type(mpaths.itemsDoc), mpath.Path)

