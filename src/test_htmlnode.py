import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):


    def test_propstohtml(self):
        test_dict = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode("h1", 'this is a test header', None, test_dict)
        test1 = node.props_to_html()
        test2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(test1, test2)

    def test_tohtml(self):
        with self.assertRaises(NotImplementedError):
            node = HTMLNode("h1", 'this is a test header', None, None)
            node.to_html()


    def test_leafnodeprint(self):
        test_dict = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        leafnode = LeafNode("a", 'click me!', test_dict)
        result = leafnode.to_html()
        self.assertTrue(result.startswith('<a'))
        self.assertTrue(result.endswith('</a>'))
        self.assertIn(' href="https://www.google.com"', result)
        self.assertIn(' target="_blank"', result)
        self.assertIn('>click me!<', result)

    def test_parentnode(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
            ],
        )
        result = node.to_html()
        self.assertTrue(result == '<p><b>Bold text</b>Normal text<i>italic text</i></p>')
        node2 = ParentNode(
            "div",
            [
                ParentNode("p", [LeafNode(None, "Nested text")]),
                LeafNode("span", "Some text"),
            ],
        )
        result2 = node2.to_html()
        self.assertTrue(result2 == '<div><p>Nested text</p><span>Some text</span></div>')
        with self.assertRaises(ValueError) as context:
            node = ParentNode("p", None)  # Invalid node: missing children
            node.to_html()
        self.assertEqual(str(context.exception), 'missing children')

        # Check 'missing tag' error
        with self.assertRaises(ValueError) as context:
            node = ParentNode(None, [  # Invalid node: missing tag
                LeafNode('span', 'some text'),
                LeafNode(None, "Normal text")
            ])
            node.to_html()
        self.assertEqual(str(context.exception), 'missing tag')

if __name__ == "__main__":
    unittest.main()