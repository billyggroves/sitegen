import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("a", "hello world", ["node1"], {"href": "test.com"})
        # print(node)
        self.assertEqual(node, node)

    def test_to_html(self):
        node = HTMLNode("a", "hello world", ["node1"], {"href": "test.com"})
        self.assertRaises(NotImplementedError,node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("a", "hello world", ["node1"], {"href": "test.com", "test": "test2.com"})
        # print(node.props_to_hmtl())
        self.assertEqual(node.props_to_hmtl(), " href=\"test.com\" test=\"test2.com\"")

if __name__ == "__main__":
    unittest.main()