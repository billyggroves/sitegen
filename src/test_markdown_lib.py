import unittest
from markdown_lib import *

class TestMarkdownLib(unittest.TestCase):
    def test_paragraphs(self):
        md = """
                This is **bolded** paragraph
                text in a p
                tag here

                This is another paragraph with _italic_ text and `code` here

            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
                ```
                This is text that _should_ remain
                the **same** even with inline stuff
                ```
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

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
            "# this is heading1",
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
                BlockType.HEADING_1,
                BlockType.HEADING_2,
                BlockType.HEADING_3,
                BlockType.HEADING_4,
                BlockType.HEADING_5,
                BlockType.HEADING_6,
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