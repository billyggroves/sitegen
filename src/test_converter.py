import unittest
from textnode import *
from converter_lib import *

class TestConverter(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node2 = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node2)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_ital(self):
        node2 = TextNode("This is a italics node", TextType.ITAL)
        html_node = text_node_to_html_node(node2)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italics node")

    def test_code(self):
        node2 = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node2)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node2 = TextNode("This is a link node", TextType.LINK, "test.com")
        html_node = text_node_to_html_node(node2)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href":"test.com"})

    def test_img(self):
        node2 = TextNode("This is a image node", TextType.IMAGE, "/images/test.png")
        html_node = text_node_to_html_node(node2)
        # print(node2)
        # print(html_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src":"/images/test.png", "alt":"This is a image node"})

    def test_incorrect_text_type(self):
        node = TextNode("This is a text node", "doesn't exist")
        with self.assertRaises(Exception):
            text_node_to_html_node(node)
    
    def test_split_bold(self):
        node = TextNode("**This** is text with a **code block** **word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes, 
            [TextNode("This",TextType.BOLD,None), 
             TextNode(" is text with a ",TextType.TEXT,None), 
             TextNode("code block",TextType.BOLD,None), 
             TextNode(" ",TextType.TEXT,None), 
             TextNode("word",TextType.BOLD,None)]
             )
        
    def test_split_ital(self):
        node = TextNode("_This_ is text with a _code block_ _word_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITAL)
        self.assertEqual(
            new_nodes, 
            [TextNode("This",TextType.ITAL,None), 
             TextNode(" is text with a ",TextType.TEXT,None), 
             TextNode("code block",TextType.ITAL,None), 
             TextNode(" ",TextType.TEXT,None), 
             TextNode("word",TextType.ITAL,None)]
             )
    
    def test_split_ital_2(self):
        node = TextNode("*This* is text with a *code block* *word*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITAL)
        self.assertEqual(
            new_nodes, 
            [TextNode("This",TextType.ITAL,None), 
             TextNode(" is text with a ",TextType.TEXT,None), 
             TextNode("code block",TextType.ITAL,None), 
             TextNode(" ",TextType.TEXT,None), 
             TextNode("word",TextType.ITAL,None)]
             )

    def test_split_code(self):
        node = TextNode("`This` is text with a `code block` `word`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes, 
            [TextNode("This",TextType.CODE,None), 
             TextNode(" is text with a ",TextType.TEXT,None), 
             TextNode("code block",TextType.CODE,None), 
             TextNode(" ",TextType.TEXT,None), 
             TextNode("word",TextType.CODE,None)]
             )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to youtube", "https://www.youtube.com/@bootdotdev")], matches)      

    def test_extract_markdown_links_with_image_also(self):
        matches = extract_markdown_links(
            """This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)
                 and [to youtube](https://www.youtube.com/@bootdotdev)"""
        )        
        self.assertListEqual([("to youtube", "https://www.youtube.com/@bootdotdev")], matches)      

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_image_with_link_also(self):
        matches = extract_markdown_images(
            """This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)
                 and [to youtube](https://www.youtube.com/@bootdotdev)"""
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with a link ![image](https://i.imgur.com/zjjcJKZ.png) and ![local image](./src/image.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "local image", TextType.IMAGE, "./src/image.png"
            ),
        ])

    def test_split_link(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ])

    def test_text_to_textnode(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITAL),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

if __name__ == "__main__":
    unittest.main()