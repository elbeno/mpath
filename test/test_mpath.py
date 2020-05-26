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

class Test_parseLayoutStr (unittest.TestCase):

    def test_parsesOneLevel (self):
        layoutStr = "root|/home/user"
        layout = mpath.parseLayoutStr(layoutStr)
        expected = [("root", "/home/user", [])]
        self.assertEquals(layout, expected)

    def test_parsesTwoRoots (self):
        layoutStr = "root|/home/user\nroot2|/usr/bin"
        layout = mpath.parseLayoutStr(layoutStr)
        expected = [("root", "/home/user", []), ("root2", "/usr/bin", [])]
        self.assertEquals(layout, expected)

    def test_parsesTwoLevels (self):
        layoutStr = "root|/home/user\n  proj|myProj/main"
        layout = mpath.parseLayoutStr(layoutStr)
        expected = [("root", "/home/user", [("proj", "myProj/main", [])])]
        self.assertEquals(layout, expected)

    def test_parsesThreeLevels (self):
        layoutStr = "root|/home/user\n  proj|myProj/main\n    readme|README.TXT"
        layout = mpath.parseLayoutStr(layoutStr)
        expected = [("root", "/home/user", [("proj", "myProj/main", [("readme", "README.TXT", [])])])]
        self.assertEquals(layout, expected)

    def test_canFallBackFromLevel1 (self):
        layoutStr = "root|C:/Users/username\n  docs|Documents\nbackup|D:/backup"
        layout = mpath.parseLayoutStr(layoutStr)
        expected = [("root", "C:/Users/username", [("docs", "Documents", [])]), ("backup", "D:/backup", [])]
        self.assertEquals(layout, expected)

    def test_parsesTwoRootsWith2Levels (self):
        layoutStr = "src|D:/repo/game\n  code|code\nexp|Z:/game/export\n  assets|assets"
        layout = mpath.parseLayoutStr(layoutStr)
        expected = [("src", "D:/repo/game", [("code", "code", [])]), ("exp", "Z:/game/export", [("assets", "assets", [])])]
        self.assertEquals(layout, expected)

    def test_parsesTwoItemsUnderRoot (self):
        # layoutStr = "root|/\n  usr|usr\n  boot|boot"
        layoutStr = "srcRoot|C:/game\n    charSrc|art/chars\n    docs|Docs"
        layout = mpath.parseLayoutStr(layoutStr)
        # expected = [("root", "/", [("usr", "usr", []), ("boot", "boot", [])])]
        expected = [("srcRoot", "C:/game", [("charSrc", "art/chars", []), ("docs", "Docs", [])])]
        self.assertEquals(layout, expected)

    def test_2And3Levels (self):
        layoutStr = """
srcRoot|C:/game
    charSrc|art/chars
    docs|Docs
        itemsDoc|items.json
"""
        layout = mpath.parseLayoutStr(layoutStr)
        expected = [("srcRoot", "C:/game", [("charSrc", "art/chars", []), ("docs", "Docs", [("itemsDoc", "items.json", [])])])]
        self.assertEquals(layout, expected)

    def test_buildsTree (self):
        layout = mpath.parseLayoutStr(winALayout)
        expected = [("srcRoot",
                     "C:/game",
                     [("charSrc",
                       "art/chars",
                       []
                      ),
                      ("docs",
                       "Docs",
                       [("itemsDoc",
                         "items.json",
                         []
                        )
                       ]
                      )
                     ]
                    ),
                    ("expRoot",
                     "Z:/game",
                     [("charExp",
                       "assets/chars",
                       []
                      )
                     ]
                    )
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

    def test_iter (self):
        path = mpath.Path("/usr/local/iter")
        it = iter(path)
        first = it.next()
        out = [first]
        for i in it:
            out += i
        self.assertEquals(''.join(out), path)

    def test_canTestMembership (self):
        path = mpath.Path("/usr/share/dict/words")
        self.assertTrue("share" in path)
        self.assertFalse("nope" in path)

    def test_reverse_linux (self):
        pathStr = "/usr/bin/share"
        path = mpath.Path(pathStr)
        self.assertEquals(list(reversed(path)), list(reversed(pathStr)))

    def test_reverse_windows (self):
        pathStr = "C:/Users/user/games"
        path = mpath.Path(pathStr)
        self.assertEquals(list(reversed(path)), list(reversed(pathStr)))

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
        mpaths = mpath.MPaths(mpath.parseLayoutStr(winALayout))
        self.assertEquals(mpaths["srcRoot"], "C:/game")
        self.assertEquals(mpaths["charSrc"], "C:/game/art/chars")
        self.assertEquals(mpaths["itemsDoc"], "C:/game/Docs/items.json")
        self.assertEquals(set(mpaths.keys()), set(["srcRoot", "charSrc", "docs", "itemsDoc", "expRoot", "charExp"]))

    def test_fromLayoutStrFunction (self):
        # this is a helper function, not part of the MPath class
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(mpaths["srcRoot"], "C:/game")
        self.assertEquals(mpaths["charSrc"], "C:/game/art/chars")
        self.assertEquals(mpaths["itemsDoc"], "C:/game/Docs/items.json")
        self.assertEquals(set(mpaths.keys()), set(["srcRoot", "charSrc", "docs", "itemsDoc", "expRoot", "charExp"]))

    def test_fromLayoutStrFunctionDefaultsToEnablingDotSyntax (self):
        # this is a helper function, not part of the MPath class
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(mpaths.srcRoot, "C:/game")
        self.assertEquals(mpaths.charSrc, "C:/game/art/chars")
        self.assertEquals(mpaths.itemsDoc, "C:/game/Docs/items.json")

    def test_fromLayoutStrFunctionDisablingDotSyntax (self):
        # this is a helper function, not part of the MPath class
        mpaths = mpath.fromLayoutStr(winALayout, dotSyntax=False)
        self.assertRaises(AttributeError, lambda: mpaths.srcRoot)
        self.assertRaises(AttributeError, lambda: mpaths.charSrc)
        self.assertRaises(AttributeError, lambda: mpaths.itemsDoc)

    def test_dotSyntaxAllowsForEvenEasierPathLookup (self):
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(mpaths.srcRoot, "C:/game")
        self.assertEquals(mpaths.charSrc, "C:/game/art/chars")
        self.assertEquals(mpaths.itemsDoc, "C:/game/Docs/items.json")

    def test_builtPathsArePathInstances (self):
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(type(mpaths["itemsDoc"]), mpath.Path)

    def test_builtPathsWorkWithDotSyntax (self):
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(type(mpaths.itemsDoc), mpath.Path)

    def test_stringifiesProperly (self):
        mpaths = mpath.fromLayoutStr(winALayout)
        expected = "{ charExp: Z:/game/assets/chars\n, charSrc: C:/game/art/chars\n, docs: C:/game/Docs\n, expRoot: Z:/game\n, itemsDoc: C:/game/Docs/items.json\n, srcRoot: C:/game }"
        self.assertEquals(str(mpaths), expected)

    def test_pformat_createsAPrettifiedString (self):
        mpaths = mpath.fromLayoutStr(winALayout)
        expected = "C:/game (srcRoot)\n    art/chars (charSrc)\n    Docs (docs)\n        items.json (itemsDoc)\nZ:/game (expRoot)\n    assets/chars (charExp)"
        self.assertEquals(mpaths.pformat(), expected)

