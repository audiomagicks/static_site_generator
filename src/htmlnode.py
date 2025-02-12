class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        #return 'NotImplementedError' #for testing
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ''
        prop_list = []
        for key, value in self.props.items():
            prop_list.append(f' {key}=\"{value}\"')
        return ''.join(prop_list)
    
    def __repr__(self):
        return f"HTMLNode(html tag={self.tag}, string value={self.value}, child HTMLNode list={self.children}, dict of attributes={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)


    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        else:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"