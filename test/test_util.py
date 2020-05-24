import unittest
from nose.plugins.attrib import attr


from .. import util


class Test_parseIndent (unittest.TestCase):

    def test_level0 (self):
        self.assertEquals(util.parseIndent("zero"), (0, "zero"))

    def test_level1 (self):
        self.assertEquals(util.parseIndent(" one"), (1, "one"))

    def test_level2 (self):
        self.assertEquals(util.parseIndent("  two"), (2, "two"))

    def test_level5 (self):
        self.assertEquals(util.parseIndent("     five"), (5, "five"))

    def test_level15 (self):
        self.assertEquals(util.parseIndent("               fifteen"), (15, "fifteen"))

