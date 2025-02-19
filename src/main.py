from textnode import *
from htmlnode import *
from mytools import *

def main():
    # Using explicit spaces in the markdown string
    markdown2 = (
        "```\n"
        "def hello():\n"
        "    print('hello')\n"  # Make sure there are 4 actual spaces here
        "```"
    )
    print("Raw markdown:", repr(markdown2))
    node2 = markdown_to_html_node(markdown2)
    expected = "<div><pre><code>def hello():\n    print('hello')</code></pre></div>"
    result = node2.to_html() == expected
    print("Result matches:", result)
    print("Expected:", expected)
    print("Got:", node2.to_html())
    



main()