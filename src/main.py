from os import path, listdir, makedirs
from shutil import rmtree, copytree
from markdown_lib import *
import time

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read template
    with open(template_path, "r") as file:
        template_content = file.read()

    # Read content files
    content_files = list_files(from_path)
    for md_file in content_files:
        with open(md_file, "r") as file:
            content = file.read()
        html = markdown_to_html_node(content).to_html()
        title = extract_title(content)
        new_template = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)
        new_file_path = md_file.replace("content", "public").replace(".md", ".html")
        makedirs(new_file_path.replace("/index.html", ""), exist_ok=True)
        print(new_file_path)
        with open(new_file_path, "w") as file:
            file.write(new_template)
    return

def list_files(path_to_parent):
    files = []
    for item in listdir(path_to_parent):
        new_path = path.join(path_to_parent, item)
        if path.isfile(new_path):
            files.append(new_path)
        elif path.isdir(new_path):
            files.extend(list_files(new_path))
    return files

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for line in blocks:
        if block_to_block_type(line) == BlockType.HEADING_1:
            return line
    raise Exception("File does not contain a title! (H1 \"# \")")

def delete_public(path_to_public):
    if path.exists(path_to_public) and len(listdir(path_to_public)) > 0:
        print(listdir(path_to_public))
        rmtree(path_to_public)
    return

def copy_files(path_to_static, path_to_public):
    if path.exists(path_to_static) and len(listdir(path_to_static)) > 0:
        print(listdir(path_to_static))
        copytree(path_to_static,path_to_public)
    return

def main():
    path_to_static = "./static/"
    path_to_public = "./public/"
    path_to_content = "./content"
    path_to_template = "./template.html"
    delete_public(path_to_public)
    copy_files(path_to_static, path_to_public)
    generate_page(path_to_content, path_to_template, path_to_public)


if __name__ == "__main__":
    main()