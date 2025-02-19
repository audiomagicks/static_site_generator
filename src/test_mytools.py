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

markdown = """#### This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in an unordered list block
* This is a list item with **bolding**
* This is an *italic* list item

```
this is code
```

1. This is the first list item in an ordered list block
2. This is a list item with **bolding**
3. This is an *italic* list item

>this is a quote
>on 2 separate lines

this is ![an image](https://www.image.com) of an image

this is [a link](https://www.google.com) to google

    """

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
        self.assertEqual(block_to_block_type('1. item 1\n2. item 2\n3. item 3'), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type('1.item 1\n2. item 2\n3. item 3'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('1. item 1\n3. item 2\n2. item 3'), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type('item 1\n2. item 2\n3. item 3'), BlockType.PARAGRAPH)

class TestTextToHTMLNode(unittest.TestCase):
    def test_heading_block(self):
        # Test a level 2 heading
        markdown = "## This is a heading"
        node = markdown_to_html_node(markdown)
        # Check if it's a div
        self.assertEqual(node.tag, "div")
        # Check if it has one child
        self.assertEqual(len(node.children), 1)
        # Check if the child is an h2
        self.assertEqual(node.children[0].tag, "h2")
        # Check the text content
        self.assertEqual(node.children[0].children[0].value, "This is a heading")

    def test_list_blocks(self):
        # Test unordered list
        markdown_ul = "* First item\n* Second item"
        node_ul = markdown_to_html_node(markdown_ul)
        
        # Check basic structure
        self.assertEqual(node_ul.tag, "div")
        self.assertEqual(len(node_ul.children), 1)
        
        # Check ul tag
        ul_node = node_ul.children[0]
        self.assertEqual(ul_node.tag, "ul")
        
        # Check list items
        self.assertEqual(len(ul_node.children), 2)
        self.assertEqual(ul_node.children[0].tag, "li")
        self.assertEqual(ul_node.children[0].children[0].value, "First item")
        self.assertEqual(ul_node.children[1].children[0].value, "Second item")

        # Test ordered list
        markdown_ol = "1. First item\n2. Second item"
        node_ol = markdown_to_html_node(markdown_ol)
        
        # Check ol structure
        self.assertEqual(node_ol.tag, "div")
        ol_node = node_ol.children[0]
        self.assertEqual(ol_node.tag, "ol")
        
        # Check ordered list items
        self.assertEqual(len(ol_node.children), 2)
        self.assertEqual(ol_node.children[0].tag, "li")
        self.assertEqual(ol_node.children[0].children[0].value, "First item")
        self.assertEqual(ol_node.children[1].children[0].value, "Second item")

    def test_text_formatting(self):
        # Test bold text
        markdown_bold = "This is **bold** text"
        node_bold = markdown_to_html_node(markdown_bold)
        
        # Check paragraph structure
        self.assertEqual(node_bold.tag, "div")
        p_node = node_bold.children[0]
        self.assertEqual(p_node.tag, "p")
        
        # Check bold text structure
        self.assertEqual(len(p_node.children), 3)  # "This is ", "bold", " text"
        self.assertEqual(p_node.children[0].value, "This is ")
        self.assertEqual(p_node.children[1].tag, "b")
        self.assertEqual(p_node.children[1].value, "bold")
        self.assertEqual(p_node.children[2].value, " text")

        # Test italic text
        markdown_italic = "This is *italic* text"
        node_italic = markdown_to_html_node(markdown_italic)
        p_node = node_italic.children[0]
        self.assertEqual(p_node.children[1].tag, "i")
        self.assertEqual(p_node.children[1].value, "italic")

        # Test combined formatting
        markdown_combined = "This is **bold** and *italic* text"
        node_combined = markdown_to_html_node(markdown_combined)
        p_node = node_combined.children[0]
        self.assertEqual(len(p_node.children), 5)  # "This is ", "bold", " and ", "italic", " text"
        self.assertEqual(p_node.children[1].tag, "b")
        self.assertEqual(p_node.children[3].tag, "i")

    def test_links(self):
        # Test basic link
        markdown_link = "This is [a link](https://www.example.com) in text"
        node_link = markdown_to_html_node(markdown_link)
        
        # Check structure
        self.assertEqual(node_link.tag, "div")
        p_node = node_link.children[0]
        self.assertEqual(p_node.tag, "p")
        
        # Check link parts
        self.assertEqual(len(p_node.children), 3)  # "This is ", link node, " in text"
        self.assertEqual(p_node.children[0].value, "This is ")
        
        # Check link node
        link_node = p_node.children[1]
        self.assertEqual(link_node.tag, "a")
        self.assertEqual(link_node.value, "a link")
        self.assertEqual(link_node.props["href"], "https://www.example.com")
        
        self.assertEqual(p_node.children[2].value, " in text")

        # Test multiple links
        markdown_multiple = "[link1](url1) and [link2](url2)"
        node_multiple = markdown_to_html_node(markdown_multiple)
        p_node = node_multiple.children[0]
        self.assertEqual(len(p_node.children), 3)  # link1, " and ", link2
        self.assertEqual(p_node.children[0].tag, "a")
        self.assertEqual(p_node.children[2].tag, "a")

    def test_simple_link(self):
        # Test just a link by itself
        markdown_link = "[link](https://example.com)"
        node = markdown_to_html_node(markdown_link)
        
        # Check basic structure
        self.assertEqual(node.tag, "div")
        self.assertEqual(len(node.children), 1)
        p_node = node.children[0]
        self.assertEqual(p_node.tag, "p")
        
        # Check link node
        self.assertEqual(len(p_node.children), 1)
        link_node = p_node.children[0]
        self.assertEqual(link_node.tag, "a")
        self.assertEqual(link_node.value, "link")
        self.assertEqual(link_node.props["href"], "https://example.com")

    def test_simple_image(self):
        markdown = "![alt text](https://example.com/image.png)"
        node = markdown_to_html_node(markdown)
        p_node = node.children[0]
        img_node = p_node.children[0]
        self.assertEqual(len(p_node.children), 1)
        self.assertEqual(img_node.tag, "img")
        self.assertEqual(img_node.value, "")
        self.assertEqual(img_node.props["src"], "https://example.com/image.png")
        self.assertEqual(img_node.props["alt"], "alt text")

    def test_image_with_text(self):
        markdown = "This is ![alt text](https://example.com/image.png) with text"
        node = markdown_to_html_node(markdown)
        p_node = node.children[0]
        self.assertEqual(len(p_node.children), 3)
        self.assertEqual(p_node.children[0].value, "This is ")
        self.assertEqual(p_node.children[1].tag, "img")
        self.assertEqual(p_node.children[2].value, " with text")

    def test_code_blocks(self):
        # Test simple one-line code block
        markdown1 = "```\nprint('hello')\n```"
        node1 = markdown_to_html_node(markdown1)
        self.assertEqual(
            node1.to_html(),
            "<div><pre><code>print('hello')</code></pre></div>"
        )

        # Test multi-line code block
        markdown2 = "```\ndef hello():\n    print('hello')\n```"
        node2 = markdown_to_html_node(markdown2)
        self.assertEqual(
            node2.to_html(),
            "<div><pre><code>def hello():\n    print('hello')</code></pre></div>"
        )

        # Test code block with language specification
        markdown3 = "```python\nprint('hello')\n```"
        node3 = markdown_to_html_node(markdown3)
        self.assertEqual(
            node3.to_html(),
            "<div><pre><code>print('hello')</code></pre></div>"
        )

if __name__ == "__main__":
    unittest.main()