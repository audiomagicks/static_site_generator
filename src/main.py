from textnode import *
from htmlnode import *
from mytools import *


def main():
    node = TextNode("There are no special delimiters here", TextType.TEXT)
    print(split_nodes_delimiter([node], "`", TextType.CODE))

        

main()
