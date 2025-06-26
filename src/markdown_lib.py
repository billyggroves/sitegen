from enum import Enum
from parentnode import ParentNode
from htmlnode import HTMLNode
from converter_lib import text_to_textnodes
from textnode import *

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

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    for index,block in enumerate(blocks):
        blocks[index] = blocks[index].lstrip("\n").rstrip("\n").strip()
    for index,block in enumerate(blocks):
        if "\n" in blocks[index]:
            blocks[index] = "\n".join(map(str.strip, block.split("\n")))
            continue
    return list(filter(None, blocks))

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

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    child_nodes = []
    for block in blocks:
        child_nodes.append(make_block_nodes(block))
    return ParentNode("div", child_nodes)

def make_block_nodes(block):
    b_type = block_to_block_type(block)
    match b_type:
        case BlockType.PARAGRAPH:
            block = block.replace("\n", " ")
            grand_kids = text_to_children(block)
            return ParentNode("p", grand_kids)
        case BlockType.HEADING_1:
            grand_kids = text_to_children(block)
            return ParentNode("h1", grand_kids)
        case BlockType.HEADING_2:
            grand_kids = text_to_children(block)
            return ParentNode("h2", grand_kids)
        case BlockType.HEADING_3:
            grand_kids = text_to_children(block)
            return ParentNode("h3", grand_kids)
        case BlockType.HEADING_4:
            grand_kids = text_to_children(block)
            return ParentNode("h4", grand_kids)
        case BlockType.HEADING_5:
            grand_kids = text_to_children(block)
            return ParentNode("h5", grand_kids)
        case BlockType.HEADING_6:
            grand_kids = text_to_children(block)
            return ParentNode("h6", grand_kids)
        case BlockType.CODE:
            block = block.replace("```", "").lstrip("\n")
            code_node = LeafNode("code", block)
            return ParentNode("pre", [code_node])
        case BlockType.QUOTE:
            grand_kids = text_to_children(block)
            return ParentNode("blockquote", grand_kids)
        case BlockType.UNORDERED_LIST:
            grand_kids = text_to_children(block)
            return ParentNode("ul", grand_kids)
        case BlockType.ORDERED_LIST:
            grand_kids = text_to_children(block)
            return ParentNode("ol", grand_kids)
        case _:
            raise Exception("Block is not formatted correctly")



def text_to_children(text):
    nodes = []
    # print(text)
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        nodes.append(text_node_to_html_node(node))
    return nodes
