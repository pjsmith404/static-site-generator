import os
import shutil

from copy_static import copy_files
from generate_page import generate_page, generate_page_recursive

def main():
    shutil.rmtree("./public", ignore_errors=True)
    os.mkdir("./public")
    copy_files("./static", "./public")

    generate_page_recursive("./content", "./template.html", "./public")

main()
