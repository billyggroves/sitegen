from textnode import *
from leafnode import LeafNode
import re

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    node = split_nodes_delimiter(node, "**", TextType.BOLD)
    node = split_nodes_delimiter(node, "*", TextType.ITAL)
    node = split_nodes_delimiter(node, "_", TextType.ITAL)
    node = split_nodes_delimiter(node, "`", TextType.CODE)
    node = split_nodes_image(node)
    node = split_nodes_link(node)
    return node

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    escaped_delim = re.escape(delimiter)
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            non_text_nodes = re.findall(f"{escaped_delim}(.*?){escaped_delim}", node.text)
            nodes = node.text.split(delimiter)
            created_nodes = create_new_nodes(nodes, non_text_nodes, text_type)
            for each in created_nodes:
                new_nodes.append(each)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            nodes = re.split(r"!\[.*?\]\((.*?)\)", node.text)
            created_nodes = create_new_nodes(nodes, images, TextType.IMAGE)
            for each in created_nodes:
                new_nodes.append(each)
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            nodes = re.split(r"(?<!\!)\[.*?\]\((.*?)\)", node.text)
            created_nodes = create_new_nodes(nodes, links, TextType.LINK)
            for each in created_nodes:
                new_nodes.append(each)
        else:
            new_nodes.append(node)
    return new_nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    # print(blocks)
    for index,block in enumerate(blocks):
        blocks[index] = blocks[index].lstrip("\n").rstrip("\n").strip()
    for index,block in enumerate(blocks):
        if "\n" in blocks[index]:
            blocks[index] = "\n".join(map(str.strip, block.split("\n")))
            continue
    return blocks

def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)
    return links

def create_new_nodes(list_of_text, list_found, text_type):
    new_nodes = []
    for text in list_of_text:
        if text == "":
            continue
        cont = True
        if list_found != [] and (text in list_found or any(text == tup[1] for tup in list_found)):
            if text_type == TextType.IMAGE:
                for image in list_found:
                    if text == image[1]:
                        new_nodes.append(TextNode(image[0], text_type, image[1]))
                        break
                continue
            if text_type == TextType.LINK:
                for link in list_found:
                    if text == link[1]:
                        new_nodes.append(TextNode(link[0], text_type, link[1]))
                        break
                continue
            for item in list_found:
                if text == item:
                    new_nodes.append(TextNode(text, text_type))
                    cont = False
                    break
        if cont == True:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes