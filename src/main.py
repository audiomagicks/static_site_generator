from textnode import *
from htmlnode import *
from mytools import *


def main():
    test_node = TextNode('this is a *bold* test, with *two* bolds.', TextType.TEXT)
    print(split_nodes_delimiter([test_node], '*', TextType.BOLD))


        

main()
