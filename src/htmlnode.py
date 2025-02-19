class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ''
        prop_list = []
        for key, value in self.props.items():
            prop_list.append(f' {key}=\"{value}\"')
        return ''.join(prop_list)
    
    def __repr__(self):
        return f"{type(self)}(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        if value is None:
            raise ValueError('value is None')
        super().__init__(tag, value, None, props)


    def to_html(self):
        if self.tag:
            return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return self.value
        
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if tag is None:
            raise ValueError('missing tag')
        if children is None:
            raise ValueError('missing children')
        if children is None:
            children = []
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError('missing tag')
        if self.children is None:
            raise ValueError('children should not be None')
        if any(child is None for child in self.children):
            raise ValueError('children contains None')

        tagged_children = ''
        for child in self.children:
            tagged_children = tagged_children + child.to_html()
        return f"<{self.tag}>{tagged_children}</{self.tag}>"
