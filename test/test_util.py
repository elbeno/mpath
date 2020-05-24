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


class Test_parseHier (unittest.TestCase):

    def test_emptystring (self):
        # note: python's str.splitlines turns "" into []
        self.assertEquals(util.parseHier(""), [])

    def test_oneLine (self):
        self.assertEquals(util.parseHier("This is a test."), [(0, "This is a test.")])

    def test_twoLinesOneIndent (self):
        self.assertEquals(util.parseHier("This is\n    a test."), [(0, "This is"), (1, "a test.")])

    def test_twoLinesOneIndentWindowsNewlines (self):
        self.assertEquals(util.parseHier("This is\r\n    a test."), [(0, "This is"), (1, "a test.")])

    def test_multilineString_defaults (self):
        example = """
        This is
            a test
            of
                a multiline
        string
        """
        expected = [(0, "This is"), (1, "a test"), (1, "of"), (2, "a multiline"), (0, "string")]
        self.assertEquals(util.parseHier(example), expected)

    def test_multilineString_nonNormalized (self):
        example = """
        This is
            a test
            of
                a multiline
        string
        """
        expected = [(8, "This is"), (12, "a test"), (12, "of"), (16, "a multiline"), (8, "string")]
        self.assertEquals(util.parseHier(example, normalize=False), expected)

    def test_multilineString_filterEmpty (self):
        example = """
        This is
            a test
            of
                a multiline
        string
        """
        expected = [(0, ""), (1, "This is"), (2, "a test"), (2, "of"), (3, "a multiline"), (1, "string"), (1, "")]
        self.assertEquals(util.parseHier(example, filterEmpty=False), expected)

    def test_multilineString_nonNormalizedFilterEmpty (self):
        example = """
        This is
            a test
            of
                a multiline
        string
        """
        expected = [(0, ""), (8, "This is"), (12, "a test"), (12, "of"), (16, "a multiline"), (8, "string"), (8, "")]
        self.assertEquals(util.parseHier(example, normalize=False, filterEmpty=False), expected)

    def test_worksWithTabsEvenThoughtIHateThem (self):
        tabbedHier = """
home|/home/user
\tp1|projA
\t\tbackup|backup
\tp2|proj2
"""
        expected = [(0, "home|/home/user"), (1, "p1|projA"), (2, "backup|backup"), (1, "p2|proj2")]
        self.assertEquals(util.parseHier(tabbedHier), expected)

