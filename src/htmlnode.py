

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_hmtl(self):
        return ' '.join(f" {key}=\"{value}\"" for key, value in self.props.items()).replace("  ", " ") # type: ignore
    
    def __repr__(self):
        return f"HTMLNode({self.tag},{self.value},{self.children},{self.props})"