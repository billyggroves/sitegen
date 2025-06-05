from enum import Enum
from parentnode import ParentNode
from htmlnode import HTMLNode

class BlockType(Enum):
    PARAGRAPH = "p"
    HEADING_1 = "h1"
    HEADING_2 = "h2"
    HEADING_3 = "h3"
    HEADING_4 = "h4"
    HEADING_5 = "h5"
    HEADING_6 = "h6"
    CODE = "code"
    QUOTE = "blockquote"
    UNORDERED_LIST = "ul"
    ORDERED_LIST = "ol"

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        if block != '':
            continue
        nodes.append((HTMLNode(block_to_block_type(block)), block))

    print(blocks)
    print(nodes)
    pass

def text_to_children(text):
    pass


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
    if block.startswith("# "):
        return BlockType.HEADING_1
    if block.startswith("## "):
        return BlockType.HEADING_2
    if block.startswith("### "):
        return BlockType.HEADING_3
    if block.startswith("#### "):
        return BlockType.HEADING_4
    if block.startswith("##### "):
        return BlockType.HEADING_5
    if block.startswith("###### "):
        return BlockType.HEADING_6
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    
    if "\n" in block:
        lines = block.split("\n")
    else:
        lines = [block]

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