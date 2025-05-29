import unittest

from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_parent_with_props(self):
        grandchild_node = LeafNode("a", "grandchild", {"href":"test.com"})
        child_node = ParentNode("span", [grandchild_node], {"test1":"test1","test2":"test2"})
        parent_node = ParentNode("div", [child_node], {"test3":"test3", "test4":"test4", "test5":"test5"})
        self.assertEqual(
            parent_node.to_html(),
            "<div test3=\"test3\" test4=\"test4\" test5=\"test5\"><span test1=\"test1\" test2=\"test2\"><a href=\"test.com\">grandchild</a></span></div>",
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_no_child(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()