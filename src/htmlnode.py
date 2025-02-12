class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        return 'NotImplementedError'
        #raise NotImplementedError
    
    def props_to_html(self):
        return f" href=\"{self.props['href']}\" target=\"{self.props['target']}\""
    
    def __repr__(self):
        return f"HTMLNode(html tag={self.tag}, string value={self.value}, child HTMLNode list={self.children}, dict of attributes={self.props})"