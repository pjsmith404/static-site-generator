import os
import shutil

def copy_static(src, dst):
    contents = os.listdir(src)
    print(f"Emptying {dst}")
    shutil.rmtree(dst, ignore_errors=True)
    os.mkdir(dst)

    for c in contents:
        src_path = os.path.join(src, c)
        dst_path = os.path.join(dst, c)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} to {dst_path}") 
            shutil.copy(src_path, dst_path)
        else:
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            copy_static(src_path, dst_path)
