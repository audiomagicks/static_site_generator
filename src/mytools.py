from textnode import *
from htmlnode import *
import re

def text_node_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode('b', text_node.text, None)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text, None)
        case TextType.CODE:
            return LeafNode('code', text_node.text, None)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href':text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {'src':text_node.url, 'alt':text_node.text})
        case _:
            raise Exception('invalid type')
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
        else:
            count = 0
            for c in node.text:
                if c == delimiter:
                    count += 1
            if count % 2 != 0:
                raise Exception('missing closing delimiter, check markdown syntax')
            else:
                intermediary_nodes = node.text.split(f'{delimiter}')
                formatted_nodes = []
                toggle = TextType.TEXT
                for slice in intermediary_nodes:
                    formatted_nodes.append(TextNode(slice, toggle))
                    toggle = text_type if toggle == TextType.TEXT else TextType.TEXT
                new_nodes.extend(formatted_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

