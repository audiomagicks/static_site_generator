import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_print(self):
        test_dict = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node2 = HTMLNode()
        node3 = HTMLNode()
        node = HTMLNode("h1", 'this is a test header', [node2, node3], test_dict)

        test1 = print(node)
        test2 = print("HTMLNode(html tag=\'h1\', string value=\'this is a test header\', child HTMLNode list=[node2, node3], dict of attributes=test_dict)")
        self.assertEqual(test1, test2)

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
        node = HTMLNode("h1", 'this is a test header', None, None)
        test1 = node.to_html()
        test2 = 'NotImplementedError'
        self.assertEqual(test1, test2)

if __name__ == "__main__":
    unittest.main()