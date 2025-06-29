from enum import Enum
from leafnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITAL = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

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