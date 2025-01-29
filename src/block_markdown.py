def markdown_to_blocks(markdown):
    blocks = []

    split_markdown = markdown.split("\n\n")

    for line in split_markdown:
        if line:
            blocks.append(line.strip()) 

    return blocks
