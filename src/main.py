from textnode import *
from htmlnode import *
from mytools import *


def main():
    test_node = TextNode('test test', TextType.IMAGE, 'boot.dev')
    print(text_node_html_node(test_node))


        

main()
