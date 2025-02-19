from textnode import *
from htmlnode import *
from mytools import *

def main():
    markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
    """
    block_list = markdown_to_blocks(markdown)
    print(block_list)
    print(f'block 1 = {block_to_block_type(block_list[0])}')
    print(f'block 2 = {block_to_block_type(block_list[1])}')
    print(f'block 3 = {block_to_block_type(block_list[2])}')


main()