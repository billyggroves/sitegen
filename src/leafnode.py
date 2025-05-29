from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, children=None, props=props)
        self.tag = tag
        self.value = value
        self.children = None
        self.props = props

    def to_html(self):
        if self.value == None:
            raise ValueError("all leaf nodes must have a value")
        if self.tag == None:
            return f"{self.value}"
        if self.props == None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag}{self.props_to_hmtl()}>{self.value}</{self.tag}>"