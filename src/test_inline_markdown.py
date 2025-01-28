import unittest

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)
from textnode import TextNode, TextType

class TestSplitNode(unittest.TestCase):
    def test_split_non_text(self):
        node = TextNode("This is bold text", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [node])

    def test_split_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.BOLD), result)

    def test_split_italic_text(self):
        node = TextNode("This is *italic* text", TextType.TEXT)
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.ITALIC), result)

    def test_split_bold_and_italic(self):
        node = TextNode("This is **bold** and *italic* text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, result)

    def test_split_image_only(self):
        node = TextNode("![image](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        result = [
            TextNode("image", TextType.IMAGE, "https://example.com"),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_image_none(self):
        node = TextNode("This is some text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        result = [
            TextNode("This is some text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_image_other(self):
        node = TextNode("This is some bold text", TextType.BOLD)
        new_nodes = split_nodes_image([node])
        result = [
            TextNode("This is some bold text", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_image_leading(self):
        node = TextNode("This is an ![image](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        result = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com"),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_image_trailing(self):
        node = TextNode("This is an ![image](https://example.com) node.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        result = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com"),
            TextNode(" node.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, result)

    def test_split_image_duplicate(self):
        node = TextNode(
            "This is an ![image](https://example.com) node doubled ![image](https://example.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_image([node])
        result = [
            TextNode("This is an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com"),
            TextNode(" node doubled ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com"),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_link_only(self):
        node = TextNode("[link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        result = [
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_link_none(self):
        node = TextNode("This is some text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        result = [
            TextNode("This is some text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_link_other(self):
        node = TextNode("This is some bold text", TextType.BOLD)
        new_nodes = split_nodes_link([node])
        result = [
            TextNode("This is some bold text", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_link_leading(self):
        node = TextNode("This is a [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_link_trailing(self):
        node = TextNode("This is a [link](https://example.com) node.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" node.", TextType.TEXT)
        ]
        self.assertEqual(new_nodes, result)

    def test_split_link_duplicate(self):
        node = TextNode(
            "This is a [link](https://example.com) node doubled [link](https://example.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" node doubled ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(new_nodes, result)

    def test_split_link_and_image(self):
        node = TextNode(
            "This is a [link](https://example.com) and ![image](https://example.com)",
            TextType.TEXT
        )
        new_nodes = split_nodes_link([node])
        new_nodes = split_nodes_image(new_nodes)
        result = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com"),
        ]
        self.assertEqual(new_nodes, result)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_extract_markdown_images_2(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )

    def test_extract_markdown_images_3(self):
        text = "This is text with a ![rick roll(https://i.imgur.com/aKaOqIh.gif and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(
            extract_markdown_images(text),
            [
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
            ]
        )


    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_extract_markdown_links_2(self):
        text = "This is text with a link ![to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )

    def test_extract_markdown_links_3(self):
        text = "This is text with a link [to boot dev(https://www.boot.dev and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(
            extract_markdown_links(text),
            [
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        )
