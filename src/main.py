import os
import shutil


def copy_files(src: str, dest: str):
    if not os.path.exists(dest):
        os.mkdir(dest)
    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dest_path = os.path.join(dest, entry)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dest_path)
        else:
            copy_files(src_path, dest_path)


def main():
    # Copy files from static to public
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    shutil.rmtree(public_dir)
    copy_files(static_dir, public_dir)


if __name__ == "__main__":
    main()
