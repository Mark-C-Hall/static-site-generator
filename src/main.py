import os
import shutil
from blocks import markdown_to_html_node


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


def extract_title(markdown: str) -> str:
    lines = [line.strip() for line in markdown.split("\n")]
    for line in lines:
        if line.startswith("# "):
            return line.lstrip("# ")
    raise Exception("No title found")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_content = f.read()
    with open(template_path) as f:
        template_content = f.read()
    html_str = markdown_to_html_node(markdown_content).to_html()
    title = extract_title(markdown_content)
    template_content = template_content.replace(r"{{ Title }}", title)
    template_content = template_content.replace(r"{{ Content }}", html_str)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template_content)


def generate_pages_recursive(dir_path_content: str, template_path: str, dest_path: str):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isfile(entry_path):
            if not entry.endswith(".md"):
                continue
            dest_file = os.path.join(dest_path, entry.removesuffix(".md") + ".html")
            generate_page(entry_path, template_path, dest_file)
        else:
            generate_pages_recursive(
                entry_path, template_path, os.path.join(dest_path, entry)
            )


def main():
    # Copy files from static to public
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    static_dir = os.path.join(project_root, "static")
    public_dir = os.path.join(project_root, "public")
    shutil.rmtree(public_dir)
    copy_files(static_dir, public_dir)

    # Generate HTML page
    content_path = os.path.join(project_root, "content")
    template_path = os.path.join(project_root, "template.html")
    generate_pages_recursive(content_path, template_path, public_dir)


if __name__ == "__main__":
    main()
