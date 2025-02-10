import unittest

from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        result = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            (
                "* This is the first list item in a list block\n"
                "* This is a list item\n"
                "* This is another list item"
            ),
        ]
        self.assertEqual(markdown_to_blocks(markdown), result)

    def test_markdown_to_blocks_more_white(self):
        markdown = """# This is a heading


This is a paragraph of text.
It has some **bold** and *italic* words inside of it.





* This is the first list item in a list block
* This is a list item
* This is another list item

"""
        result = [
            "# This is a heading",
            "This is a paragraph of text.\nIt has some **bold** and *italic* words inside of it.",
            (
                "* This is the first list item in a list block\n"
                "* This is a list item\n"
                "* This is another list item"
            ),
        ]
        self.assertEqual(markdown_to_blocks(markdown), result)

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph of text"
        result = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_heading(self):
        blocks = [
            "# Heading",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
        ]
        result = BlockType.HEADING
        for block in blocks:
            self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_heading_invalid(self):
        blocks = [
            "Head# ing",
            "Heading 2 ## ",
            "###Heading 3",
        ]
        result = BlockType.PARAGRAPH
        for block in blocks:
            self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_code(self):
        block = """```
This is a block of code
On multiple lines
```"""
        result = BlockType.CODE
        self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_code_invalid(self):
        block = """```
This is an invalid block of code
On multiple lines"""
        result = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_quote(self):
        block = """> This is a multi line
> block quote"""
        result = BlockType.QUOTE
        self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_quote_invalid(self):
        invalid_block = """> This is not a valid
block quote"""
        result = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(invalid_block), result)

    def test_block_to_block_type_unordered_list(self):
        blocks = [
            "* This is an\n* unordered list",
            "- This is an\n- unordered list",
            "* This is an\n- unordered list",
        ]
        result = BlockType.UNORDERED_LIST
        for block in blocks:
            self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_unordered_list_invalid(self):
        blocks = [
            "* This is an invalid\nunordered list",
            "- This is an invalid\n-unordered list",
        ]
        result = BlockType.PARAGRAPH
        for block in blocks:
            self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_ordered_list(self):
        block = """1. This is
2. an ordered
3. list"""
        result = BlockType.ORDERED_LIST
        self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_ordered_list_invalid(self):
        block = """1. This is
3. an invalid ordered
2. list"""
        result = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), result)

    def test_block_to_block_type_ordered_list_invalid(self):
        block = """3. This is
3. an invalid ordered
2. list"""
        result = BlockType.PARAGRAPH
        self.assertEqual(block_to_block_type(block), result)

if __name__ == "__main__":
    unittest.main()

