import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_defaulturl(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT, None)
        self.assertEqual(node, node2)

    def test_texttype(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC_TEXT)
        self.assertNotEqual(node, node2)

    def test_print(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        text_node = print(node)
        text_node2 = print(node2)
        self.assertEqual(text_node, text_node2)


if __name__ == "__main__":
    unittest.main()