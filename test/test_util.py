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


class Test_parseHierStr (unittest.TestCase):

    def test_emptystring (self):
        # note: python's str.splitlines turns "" into []
        self.assertEquals(util.parseHierStr(""), [])

    def test_oneLine (self):
        self.assertEquals(util.parseHierStr("This is a test."), [(0, "This is a test.")])

    def test_twoLinesOneIndent (self):
        self.assertEquals(util.parseHierStr("This is\n    a test."), [(0, "This is"), (1, "a test.")])

    def test_twoLinesOneIndentWindowsNewlines (self):
        self.assertEquals(util.parseHierStr("This is\r\n    a test."), [(0, "This is"), (1, "a test.")])

    def test_multilineString_defaults (self):
        example = """
        This is
            a test
            of
                a multiline
        string
        """
        expected = [(0, "This is"), (1, "a test"), (1, "of"), (2, "a multiline"), (0, "string")]
        self.assertEquals(util.parseHierStr(example), expected)

    def test_multilineString_nonNormalized (self):
        example = """
        This is
            a test
            of
                a multiline
        string
        """
        expected = [(8, "This is"), (12, "a test"), (12, "of"), (16, "a multiline"), (8, "string")]
        self.assertEquals(util.parseHierStr(example, normalize=False), expected)

    def test_multilineString_filterEmpty (self):
        example = """
        This is
            a test
            of
                a multiline
        string
        """
        expected = [(0, ""), (1, "This is"), (2, "a test"), (2, "of"), (3, "a multiline"), (1, "string"), (1, "")]
        self.assertEquals(util.parseHierStr(example, filterEmpty=False), expected)

    def test_multilineString_nonNormalizedFilterEmpty (self):
        example = """
        This is
            a test
            of
                a multiline
        string
        """
        expected = [(0, ""), (8, "This is"), (12, "a test"), (12, "of"), (16, "a multiline"), (8, "string"), (8, "")]
        self.assertEquals(util.parseHierStr(example, normalize=False, filterEmpty=False), expected)

    def test_indentingAndOutdentingSeveralTimes (self):
        hierStr = "a\n  b\nc\n  d\ne"
        layout = util.parseHierStr(hierStr)
        expected = [(0, "a"), (1, "b"), (0, "c"), (1, "d"), (0, "e")]
        self.assertEquals(layout, expected)

    def test_worksWithTabsEvenThoughtIHateThem (self):
        tabbedHier = """
home|/home/user
\tp1|projA
\t\tbackup|backup
\tp2|proj2
"""
        expected = [(0, "home|/home/user"), (1, "p1|projA"), (2, "backup|backup"), (1, "p2|proj2")]
        self.assertEquals(util.parseHierStr(tabbedHier), expected)

    def test_raisesOnOutdentToNonExistingPriorIndentLevel (self):
        badLayout = """
root|C:/
    dir|folder
  bad|uhoh
"""
        self.assertRaises(RuntimeError, lambda: util.parseHierStr(badLayout))

    def test_sectionsCanHaveTheirOwnIndentLevels (self):
        hier = """
root|Z:/
    game|game
      art|art
    docs|docs
        doc1|doc1.txt
"""
        expected = [(0, "root|Z:/"), (1, "game|game"), (2, "art|art"), (1, "docs|docs"), (2, "doc1|doc1.txt")]
        self.assertEquals(util.parseHierStr(hier), expected)

