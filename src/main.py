from textnode import *
from htmlnode import *


def main():
    test_node = TextNode('test test', 'italic', 'boot.dev')
    print(test_node)

def text_node_html_node(text_node):
    match text_node.TextType:
        case TextType.NORMAL:
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
        

main()
