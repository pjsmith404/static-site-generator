import re

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType
from htmlnode import HTMLNode, ParentNode, LeafNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    
    nodes = []

    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block_text_nodes = text_to_textnodes(block)
            leaf_nodes = [text_node_to_html_node(node) for node in block_text_nodes]
            nodes.append(ParentNode("p", leaf_nodes))
        if block_type == BlockType.HEADING:
            nodes.append(convert_heading_to_htmlnode(block))
        if block_type == BlockType.CODE:
            nodes.append(convert_code_to_htmlnode(block))
        if block_type == BlockType.QUOTE:
            nodes.append(convert_quote_to_htmlnode(block))
        if block_type == BlockType.UNORDERED_LIST:
            nodes.append(convert_list_to_htmlnode(block, False))
        if block_type == BlockType.ORDERED_LIST:
            nodes.append(convert_list_to_htmlnode(block, True))

    parent = ParentNode("div", nodes)

    return parent

def block_text_to_leafnodes(block_text):
    textnodes = text_to_textnodes(block_text)
    leafnodes = [text_node_to_html_node(node) for node in textnodes]

    return leafnodes

def trim_block_lines(block, strip_string):
    lines = block.split("\n")
    trimmed_lines = "\n".join([line.lstrip(strip_string) for line in lines])

    return trimmed_lines

def convert_heading_to_htmlnode(block):
    heading_match = re.match(r"(#{1,6}) (.*)", block)
    tag = f"h{len(heading_match[1])}"
    text = heading_match[2]

    leafnodes = block_text_to_leafnodes(text)
    htmlnode = ParentNode(tag, leafnodes)

    return htmlnode

def convert_code_to_htmlnode(block):
    trimmed_block = block.strip("```")
    leafnodes = block_text_to_leafnodes(trimmed_block)
    code_htmlnode = ParentNode("code", leafnodes)
    pre_htmlnode = ParentNode("pre", [code_htmlnode])

    return pre_htmlnode

def convert_quote_to_htmlnode(block):
    trimmed_lines = trim_block_lines(block, "> ")
    leafnodes = block_text_to_leafnodes(trimmed_lines)
    quote_htmlnode = ParentNode("blockquote", leafnodes)

    return quote_htmlnode

def convert_list_to_htmlnode(block, ordered):
    trimmed_lines = trim_block_lines(trim_block_lines(block, "- "), "* ")
    trimmed_lines = trim_block_lines(trimmed_lines, "1234567890. ")

    lines = trimmed_lines.split("\n")
    list_item_htmlnodes = []
    for line in lines:
        leafnodes = block_text_to_leafnodes(line)
        list_item_htmlnode = ParentNode("li", leafnodes)
        list_item_htmlnodes.append(list_item_htmlnode)

    if ordered:
        list_tag = "ol"
    else:
        list_tag = "ul"

    list_htmlnode = ParentNode(list_tag, list_item_htmlnodes)

    return list_htmlnode
