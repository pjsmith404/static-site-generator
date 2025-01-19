import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        node2 = TextNode("This is a text node", TextType.LINK, "https://example.com")
        self.assertEqual(node, node2)

    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_not_eq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, bold, None)")

    def test_invalid_text_type(self):
        try:
            node = TextNode("This is a text node", TextType.INVALID)
        except Exception as err:
            self.assertIsInstance(err, AttributeError)

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text_to_html_1(self):
        node = TextNode("This is a text node", TextType.TEXT)
        leaf_node = LeafNode(None, "This is a text node", None)
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_text_to_html_2(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        leaf_node = LeafNode("b", "This is a bold node", None)
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_text_to_html_3(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        leaf_node = LeafNode("i", "This is an italic node", None)
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_text_to_html_4(self):
        node = TextNode("This is a code node", TextType.CODE)
        leaf_node = LeafNode("code", "This is a code node", None)
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_text_to_html_5(self):
        node = TextNode("This is a link node", TextType.LINK, "https://example.com")
        leaf_node = LeafNode("a", "This is a link node", {"href": "https://example.com"})
        self.assertEqual(text_node_to_html_node(node), leaf_node)

    def test_text_to_html_6(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://example.com")
        leaf_node = LeafNode("img", "", {"src": "https://example.com", "alt": "This is an image node"})
        self.assertEqual(text_node_to_html_node(node), leaf_node)

if __name__ == "__main__":
    unittest.main()
