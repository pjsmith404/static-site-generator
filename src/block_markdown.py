import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []

    split_markdown = markdown.split("\n\n")

    for line in split_markdown:
        if line:
            blocks.append(line.strip()) 

    return blocks

def block_to_block_type(block):
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif (block[:3] == "```" and block[-3:] == "```"):
        return BlockType.CODE
    elif is_quote_block(block):
        return BlockType.QUOTE
    elif is_unordered_list(block):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def is_quote_block(block):
    lines = block.split("\n")
    for line in lines:
        if line[:2] != "> ":
            return False

    return True

def is_unordered_list(block):
    lines = block.split("\n")
    for line in lines:
        if line[:2] != "* " and line[:2] != "- ":
            return False

    return True

def is_ordered_list(block):
    line_numbers = re.findall(r"(\d). ", block)

    if len(line_numbers) <= 0:
        return False

    if int(line_numbers[0]) != 1:
        return False

    if all(line_numbers[i] < line_numbers[i + 1] for i in range(len(line_numbers) - 1)):
        return True

    return False

