import unittest

from markdown_html import markdown_to_html_node
from htmlnode import HTMLNode

class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_markdown_to_html_node_basic(self):
        markdown = "This is a paragraph of text"
        result = HTMLNode(
            "div",
            None,
            [
                HTMLNode("p", None, [
                    HTMLNode(None, "This is a paragraph of text", None, None)
                ], None)
            ],
            None
        )

        self.assertEqual(markdown_to_html_node(markdown), result)

    def test_markdown_to_html_node(self):
        with open("src/sample_markdown.md", "r") as file:
            sample_markdown = file.read()

        result = HTMLNode("div", None, [
            HTMLNode("h1", None, [HTMLNode(None, "Test Markdown", None, None)], None),
            HTMLNode("p", None, [
                HTMLNode(
                    None,
                    (
                        "This document is "
                        "some test markdown "
                        "to input into our "
                        "markdown conversion tests."
                    ),
                    None,
                    None
                )
            ], None),
            HTMLNode("blockquote", None, [
                HTMLNode("p", None, [HTMLNode(None, "I have a\ndream", None, None)], None)
            ], None),
            HTMLNode("ul", None, [
                HTMLNode("li", None, [HTMLNode(None, "Here's an", None, None)], None),
                HTMLNode("li", None, [HTMLNode(None, "unordered list", None, None)], None)
            ], None),
            HTMLNode("ul", None, [
                HTMLNode("li", None, [HTMLNode(None, "Here's another", None, None)], None),
                HTMLNode("li", None, [HTMLNode(None, "unordered list", None, None)], None)
            ], None),
            HTMLNode("ul", None, [
                HTMLNode("li", None, [HTMLNode(None, "This unordered list", None, None)], None),
                HTMLNode("li", None, [HTMLNode(None, "thing is just", None, None)], None),
                HTMLNode("li", None, [HTMLNode(None, "getting a bit", None, None)], None),
                HTMLNode("li", None, [HTMLNode(None, "silly now", None, None)], None)
            ], None),
            HTMLNode("ol", None, [
                HTMLNode("li", None, [HTMLNode(None, "But how about", None, None)], None),
                HTMLNode("li", None, [HTMLNode(None, "an ordered list", None, None)], None)
            ], None),
            HTMLNode("h2", None, [HTMLNode(None, "Have a subheading", None, None)], None),
            HTMLNode("pre", None, [
                HTMLNode("code", None, [
                    HTMLNode(
                        None,
                        "\n#!/bin/bash\n    echo \"Have a code block too\"\n",
                        None,
                        None
                    )
                ], None)
            ], None),
            HTMLNode("p", None, [
                HTMLNode(None, "Go ", None, None),
                HTMLNode("a", "here", None, {'href': 'https://example.com'}),
                HTMLNode(None, " to read some cool stuff. No ", None, None),
                HTMLNode("b", "really", None, None),
                HTMLNode(None, " it's ", None, None),
                HTMLNode("i", "super", None, None),
                HTMLNode(None, " interesting!", None, None)
            ], None)
        ], None)

        self.assertEqual(markdown_to_html_node(sample_markdown), result)


if __name__ == "__main__":
    unittest.main()

