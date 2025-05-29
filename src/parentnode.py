from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, value=None, children=children, props=props)
        self.tag = tag
        self.children = children
        self.props = props

    def to_html(self):
        if self.tag == None:
            raise ValueError("all parent nodes must have a tag")
        if self.children == None:
            raise ValueError("all parent nodes must have children")
        if self.props == None:
            html = f"<{self.tag}>"
        else:
            html = f"<{self.tag}{self.props_to_hmtl()}>"
        for child in self.children:
            html += child.to_html()
        html += f"</{self.tag}>"
        return html
        

