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
             , [ ( "items", "items.json", [] )
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


class Test_MPaths (unittest.TestCase):

    def test_cannotConstructEmptyMPaths (self):
        self.assertRaises(TypeError, lambda: mpath.MPaths())

    def test_canGetRoots_uniroot (self):
        mpaths = mpath.MPaths(linA)
        self.assertEquals(mpaths.getRoots(), ["/home/gfixler/proj"])

    def test_canGetRoots_multiroot (self):
        mpaths = mpath.MPaths(winA)
        self.assertEquals(mpaths.getRoots(), ["C:/game", "Z:/game"])

    def test_canGetPathsByName (self):
        mpaths = mpath.MPaths(linA)
        self.assertEquals(mpaths.pathTable["root"], "/home/gfixler/proj")
        self.assertEquals(mpaths.pathTable["charSrc"], "/home/gfixler/proj/art/chars")
        self.assertEquals(mpaths.pathTable["charExp"], "/home/gfixler/proj/assets/chars")
        self.assertEquals(set(mpaths.pathTable.keys()), set(["root", "charSrc", "charExp"]))

