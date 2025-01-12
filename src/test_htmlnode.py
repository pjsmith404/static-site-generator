import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "Some text", None, {"href": "https://example.com"})
        self.assertEqual(repr(node), "HTMLNode(div, Some text, None, {'href': 'https://example.com'})")

    def test_values(self):
        node = HTMLNode("div", "I wish I could read")
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "I wish I could read")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode(None, None, None, None)
        self.assertEqual(node.props_to_html(), "")


class TestLeafNode(unittest.TestCase):
    def test_to_html_raw_text(self):
        node = LeafNode(None, "This is some raw text")
        self.assertEqual(node.to_html(), "This is some raw text")

    def test_to_html_paragraph(self):
        node = LeafNode("p", "This is a paragraph of text")
        self.assertEqual(node.to_html(), '<p>This is a paragraph of text</p>')

    def test_to_html_hyperlink(self):
        node = LeafNode("a", "Click this link!", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), '<a href="https://example.com">Click this link!</a>')

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()
