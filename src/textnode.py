from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITAL = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, text_node): # type: ignore
        if (self.text == text_node.text
            and self.text_type == text_node.text_type
            and self.url == text_node.url):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text},{self.text_type.value},{self.url})"
        
def text_node_to_html_node(text_node):
    if text_node.text_type == None:
        raise Exception("text node must have a Text Type")
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITAL:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href":text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src":text_node.url, "alt":text_node.text})
        case _:
            raise Exception("text node must have a Text Type")
        
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for index,block in enumerate(blocks):
        blocks[index] = blocks[index].lstrip("\n").rstrip("\n").strip()
    for index,block in enumerate(blocks):
        if "\n" in blocks[index]:
            blocks[index] = "\n".join(map(str.strip, block.split("\n")))
            continue
    return blocks

def block_to_block_type(block):
    if block.startswith(("# ", "## " , "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    if "\n" in block:
        lines = block.split("\n")
    else:
        lines = [block]

    if "1. this is\n2. ordered list" == block:
        print(block)
        print(lines)

    if block.startswith(">"):
        quote = block_type_check(lines, ">")
        if quote:
            return BlockType.QUOTE
    if block.startswith("- "):
        unordered_list = block_type_check(lines, "- ")
        if unordered_list:
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        ordered_list = block_type_check(lines, "number")
        if ordered_list:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def block_type_check(lines, prefix):
    if len(lines) == 1:
        return True
    if prefix == "number":
        for index, line in enumerate(lines):
            if line[:3] != f"{index + 1}. ":
                return False
    else:
        for line in lines:
            if not line.startswith(prefix):
                return False
    return True