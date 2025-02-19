import unittest
from textnode import *
from htmlnode import *
from mytools import *

heading_block = """# This is a level 1 heading
## This is a level 2 heading
### This is a level 3 heading
#### This is a level 4 heading
##### This is a level 5 heading
###### This is a level 6 heading"""

invalid_heading_block_7 = """####### This has 7 hashes and is invalid"""
invalid_heading_block_nohash = """No hashes at the start"""
invalid_heading_nospace = """#NoSpaceAfterHash
"""
triple_backtick = "```"
code_block = f"{triple_backtick}\ndef hello_world():\nprint('Hello, World!)\n{triple_backtick}"

invalid_code_block_single_backtick = """`code snippet`"""
invalid_code_block_no_close = """```Code block missing ending backticks"""

single_line_quote = """> This is a single line quote."""
single_line_quote_nospace = """>This is a single line quote with no spacing after >."""
double_line_quote = """> This is a
> double line quote."""
invalid_quote = """this is invalid"""
invalid_double_line_quote = """> This is a
double line quote without a > on the 2nd line."""

class TestBlockToBlockType(unittest.TestCase):
    def test_heading_block(self):
        self.assertEqual(block_to_block_type('# This is a level 1 heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type('#### This is a level 4 heading'), BlockType.HEADING)
        self.assertEqual(block_to_block_type(invalid_heading_block_7), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(invalid_heading_block_nohash), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(invalid_heading_nospace), BlockType.PARAGRAPH)

    def test_code_block(self):
        self.assertEqual(block_to_block_type(code_block), BlockType.CODE)
        self.assertEqual(block_to_block_type(invalid_code_block_no_close), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(invalid_code_block_single_backtick), BlockType.PARAGRAPH)

    def test_quote_block(self):
        self.assertEqual(block_to_block_type(single_line_quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(double_line_quote), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(single_line_quote_nospace), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(invalid_quote), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(invalid_double_line_quote), BlockType.PARAGRAPH)

    def test_unordered_block(self):
        self.assertEqual(block_to_block_type('* item 1\n* item 2\n* item 3'), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type('- item 1\n- item 2\n- item 3'), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type('*item 1\n*item 2\n*item 3'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('* item 1\n- item 2\n* item 3'), BlockType.PARAGRAPH)
    
    def test_ordered_block(self):
        self.assertEqual(block_to_block_type('1.item 1\n2. item 2\n3. item 3'), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type('1.item 1\n2. item 2\n3. item 3'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('1.item 1\n3. item 2\n2. item 3'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('item 1\n2. item 2\n3. item 3'), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()