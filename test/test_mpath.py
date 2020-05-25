import unittest
from nose.plugins.attrib import attr


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


class Test_MPaths (unittest.TestCase):

    def test_cannotConstructEmptyMPaths (self):
        self.assertRaises(TypeError, lambda: mpath.MPaths())

    def test_buildPathsDict_removesTrailingSlashLinux (self):
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

    def test_fromLayoutFunction (self):
        # this is a helper function, not part of the MPath class
        mpaths = mpath.fromLayoutStr(winALayout)
        self.assertEquals(mpaths["srcRoot"], "C:/game")
        self.assertEquals(mpaths["charSrc"], "C:/game/art/chars")
        self.assertEquals(mpaths["itemsDoc"], "C:/game/art/chars/Docs/items.json")
        self.assertEquals(set(mpaths.keys()), set(["srcRoot", "charSrc", "docs", "itemsDoc", "expRoot", "charExp"]))

