import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq_all(self):
        node = TextNode("This is a test node", TextType.BOLD, "test.com")
        node2 = TextNode("This is a test node", TextType.BOLD, "test.com")
        self.assertEqual(node, node2)

    def test_eq_without_url(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a test node 1", TextType.BOLD)
        node2 = TextNode("This is a test node 2", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_texttype(self):
        node = TextNode("This is a test node", TextType.BOLD)
        node2 = TextNode("This is a test node", TextType.ITAL)
        self.assertNotEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a test node", TextType.BOLD, "test.com")
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_with_url(self):
        node = TextNode("This is a test node", TextType.BOLD, "test.com")
        self.assertEqual(node.url, "test.com")
    
    def test_without_url(self):
        node2 = TextNode("This is a test node", TextType.BOLD)
        self.assertEqual(node2.url, None)

if __name__ == "__main__":
    unittest.main()