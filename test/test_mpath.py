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

class Test_MPaths (unittest.TestCase):

    def test_cannotConstructEmptyMPaths (self):
        self.assertRaises(TypeError, lambda: mpath.MPaths())

    def test_buildPathsDict_removesTrailingSlashLinux (self):
        mpaths = mpath.MPaths([("root", "/home/gfixler/", [])])
        self.assertEquals(mpaths.pathTable["root"], "/home/gfixler")

    def test_canGetPathsByName (self):
        mpaths = mpath.MPaths(linA)
        self.assertEquals(mpaths.pathTable["root"], "/home/gfixler/proj")
        self.assertEquals(mpaths.pathTable["charSrc"], "/home/gfixler/proj/art/chars")
        self.assertEquals(mpaths.pathTable["charExp"], "/home/gfixler/proj/assets/chars")
        self.assertEquals(set(mpaths.pathTable.keys()), set(["root", "charSrc", "charExp"]))


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

