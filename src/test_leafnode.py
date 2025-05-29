import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_with_all(self):
        node = LeafNode("a", "Hello, world!", {"href": "test.com", "test": "test2.com"})
        self.assertEqual(node.to_html(), "<a href=\"test.com\" test=\"test2.com\">Hello, world!</a>")

if __name__ == "__main__":
    unittest.main()