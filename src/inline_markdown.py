import re

from textnode import TextNode,TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)

            if len(split_text) % 2 == 0:
                raise Exception(f"Invalid markdown: Missing matching delimiter for {delimiter}")

            for i in range(len(split_text)):
                if i % 2 == 0:
                    new_nodes.append(TextNode(split_text[i], TextType.TEXT))
                else:
                    new_nodes.append(TextNode(split_text[i], text_type))

    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            images = extract_markdown_images(node.text)

            if len(images) <= 0:
                new_nodes.append(TextNode(node.text, TextType.TEXT))

            else:
                text = node.text
                for image in images:
                    [leading, trailing] = text.split(f"![{image[0]}]({image[1]})", 1)
                    if leading:
                        new_nodes.append(TextNode(leading, TextType.TEXT))
                    new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                    if trailing:
                        text = trailing
                    else:
                        text = ""

                if text:
                    new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            links = extract_markdown_links(node.text)

            if len(links) <= 0:
                new_nodes.append(TextNode(node.text, TextType.TEXT))

            else:
                text = node.text
                for link in links:
                    [leading, trailing] = text.split(f"[{link[0]}]({link[1]})", 1)
                    if leading:
                        new_nodes.append(TextNode(leading, TextType.TEXT))
                    new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                    if trailing:
                        text = trailing
                    else:
                        text = ""

                if text:
                    new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
