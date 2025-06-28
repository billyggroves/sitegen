from enum import Enum
from parentnode import ParentNode
from htmlnode import HTMLNode
from converter_lib import text_to_textnodes
from textnode import *
import re

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

def text_to_children(text):
    nodes = []
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        nodes.append(text_node_to_html_node(node))
    return nodes

def block_to_paragraph(block):
    block = block.replace("\n", " ")
    grand_kids = text_to_children(block)
    if grand_kids == []:
        return LeafNode("p", block)
    return ParentNode("p", grand_kids)

def block_to_heading(block, heading_level):
    new_block = block.lstrip("# ")
    return LeafNode("h" + str(heading_level), new_block)

def block_to_code(block):
    block = block.replace("```", "").lstrip("\n")
    code_node = LeafNode("code", block)
    return ParentNode("pre", [code_node])

def block_to_quote(block):
    new_block = block.lstrip("> ")
    new_block = new_block.replace("\n", "")
    new_block = new_block.replace(">", "")
    return LeafNode("blockquote", new_block)

def block_to_list(block, b_type):
    li_list = []
    li_values = block.split("\n")
    for val in li_values:
        if b_type == BlockType.UNORDERED_LIST: 
            text = val.lstrip("- ")
        else:
            text = re.sub(r"\d. ", "", val, count=1)
        li_item = ParentNode("li", text_to_children(text))
        li_list.append(li_item)
    return li_list

def make_block_nodes(block):
    b_type = block_to_block_type(block)
    match b_type:
        case BlockType.PARAGRAPH:
            return block_to_paragraph(block)
        case BlockType.HEADING_1:
            return block_to_heading(block, 1)
        case BlockType.HEADING_2:
            return block_to_heading(block, 2)
        case BlockType.HEADING_3:
            return block_to_heading(block, 3)
        case BlockType.HEADING_4:
            return block_to_heading(block, 4)
        case BlockType.HEADING_5:
            return block_to_heading(block, 5)
        case BlockType.HEADING_6:
            return block_to_heading(block, 6)
        case BlockType.CODE:
            return block_to_code(block)
        case BlockType.QUOTE:
            return block_to_quote(block)
        case BlockType.UNORDERED_LIST:
            grand_kids = block_to_list(block, b_type)
            return ParentNode("ul", grand_kids)
        case BlockType.ORDERED_LIST:
            grand_kids = block_to_list(block, b_type)
            return ParentNode("ol", grand_kids)
        case _:
            raise Exception("Block is not formatted correctly")
