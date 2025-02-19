from textnode import *
from htmlnode import *
from mytools import *


def main():
    text = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
    new_nodes = text_to_textnodes(text)
    print(new_nodes)

        

main()
