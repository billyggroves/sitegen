import unittest

from textnode import BlockType, TextNode, TextType, markdown_to_blocks, block_to_block_type

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

    def test_markdown_to_blocks(self):
        md = """
                This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
            """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        md = [
            "# this is heading",
            "## this is heading2",
            "### this is heading3",
            "#### this is heading4",
            "##### this is heading5",
            "###### this is heading6",
            "####### this is not heading",
            "######this is not heading",
            "this# is not heading",

            "```this is code block```",
            "``` this is also code block ```",
            "``` this\n is also code block ```",
            "`this is not code block`",
            "`` this is not code block ``",
            "``` this is not code block",
            "``` this is not code block ``",
            "`` this is not code block ```",
            "this is not code block ```",

            "> this is quote 18",
            "> this is\n> quote",
            "< this is not quote",
            "> this is\n< not quote",
            "> this is\n not quote",

            "- this is unordered list",
            "- this is\n- unordered list",
            "-this is not unordered list",
            "- this is\n not unordered list",
            "- this is\n-not unordered list",

            "1. this is ordered list",
            "1. this is\n2. ordered list",
            "1.this is\n2.not ordered list",
            "1. this is\n2.not ordered list",
            "1. this is\nnot ordered list",
            "1. this is\n3. not ordered list",
            "5. this is not ordered list",
        ]
        block_types = list(map(block_to_block_type, md))
        # print(block_types)
        self.assertEqual(
            block_types,
            [
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.HEADING,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,

                BlockType.CODE,
                BlockType.CODE,
                BlockType.CODE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,

                BlockType.QUOTE,
                BlockType.QUOTE,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,

                BlockType.UNORDERED_LIST,
                BlockType.UNORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                
                BlockType.ORDERED_LIST,
                BlockType.ORDERED_LIST,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
                BlockType.PARAGRAPH,
            ],
        )

if __name__ == "__main__":
    unittest.main()