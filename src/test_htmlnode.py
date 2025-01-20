import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode("div", "Some text", None, {"href": "https://example.com"})
        self.assertEqual(
            repr(node),
            "HTMLNode(div, Some text, None, {'href': 'https://example.com'})"
        )

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

class TestParentNode(unittest.TestCase):
    leaf_raw = LeafNode(None, "Raw text")
    leaf_bold = LeafNode("b", "Bold text")
    leaf_italic = LeafNode("i", "italic text")

    props_1 = {"foo": "bar"}
    props_2 = {"foo": "bar", "baz": "bay"}

    leaf_raw_props = LeafNode(None, "Raw text", props_1)
    leaf_bold_props = LeafNode("b", "Bold text", props_2)
    leaf_italic_props = LeafNode("i", "italic text", props_1)

    def test_to_html_1(self):
        node = ParentNode("p", [self.leaf_raw])
        self.assertEqual(node.to_html(), "<p>Raw text</p>")

    def test_to_html_2(self):
        node = ParentNode(
            "p",
            [
                self.leaf_bold,
                self.leaf_raw,
                self.leaf_italic,
                self.leaf_raw
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Raw text<i>italic text</i>Raw text</p>"
        )

    def test_to_html_3(self):
        node = ParentNode("p", [self.leaf_raw], self.props_1)
        self.assertEqual(node.to_html(), '<p foo="bar">Raw text</p>')

    def test_to_html_4(self):
        node = ParentNode("p", [self.leaf_raw], self.props_2)
        self.assertEqual(node.to_html(), '<p foo="bar" baz="bay">Raw text</p>')

    def test_to_html_5(self):
        node = ParentNode("p", [self.leaf_raw_props], self.props_1)
        self.assertEqual(node.to_html(), '<p foo="bar">Raw text</p>')

    def test_to_html_6(self):
        node = ParentNode(
            "p",
            [self.leaf_raw_props, self.leaf_bold_props, self.leaf_italic_props],
            {"foo": "bar", "baz": "bay"}
        )
        self.assertEqual(
            node.to_html(),
            '<p foo="bar" baz="bay">Raw text<b foo="bar" baz="bay">Bold text</b><i foo="bar">italic text</i></p>'
        )

    def test_to_html_nested(self):
        child_node = ParentNode("span", [self.leaf_bold])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), '<div><span><b>Bold text</b></span></div>')

    def test_to_html_no_children(self):
        node = ParentNode(None, [self.leaf_raw])
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_children(self):
        node = ParentNode("p", None)
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()
