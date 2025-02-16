import os

from markdown_html import markdown_to_html_node

def extract_title(markdown):
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:]

    raise Exception("No title header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path) as file:
        markdown = file.read()

    with open(template_path) as file:
        template = file.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)

    content = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "x") as file:
        file.write(content)

