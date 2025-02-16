import os
import shutil

def copy_files(src, dst):
    contents = os.listdir(src)

    for c in contents:
        src_path = os.path.join(src, c)
        dst_path = os.path.join(dst, c)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} to {dst_path}") 
            shutil.copy(src_path, dst_path)
        else:
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            copy_files(src_path, dst_path)
