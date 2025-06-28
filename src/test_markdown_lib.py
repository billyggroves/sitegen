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

    def test_headings(self):
        md = """
                # Heading 1

                ## Heading 2

                ### Heading 3

                #### Heading 4

                ##### Heading 5

                ###### Heading 6
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6></div>",
        )

    def test_quote(self):
        md = """
                > This is a quote.

                > testing quote...
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote.</blockquote><blockquote>testing quote...</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
                - Item 1 ![alt text for image](url/of/image.jpg)
                - Item 2 This is an _italic_ word.
                - Item 3 This is a paragraph with a [link](https://www.google.com).
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>Item 1 <img src=\"url/of/image.jpg\" alt=\"alt text for image\"/></li><li>Item 2 This is an <i>italic</i> word.</li><li>Item 3 This is a paragraph with a <a href=\"https://www.google.com\">link</a>.</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
                1. Item 1 ![alt text for image](url/of/image.jpg)
                2. Item 2 This is an _italic_ word.
                3. Item 3 This is a paragraph with a [link](https://www.google.com).
            """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>Item 1 <img src=\"url/of/image.jpg\" alt=\"alt text for image\"/></li><li>Item 2 This is an <i>italic</i> word.</li><li>Item 3 This is a paragraph with a <a href=\"https://www.google.com\">link</a>.</li></ol></div>",
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