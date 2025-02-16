import os
import shutil

from copy_static import copy_files

def main():
    shutil.rmtree("./public", ignore_errors=True)
    os.mkdir("./public")

    copy_files("./static", "./public")

main()
