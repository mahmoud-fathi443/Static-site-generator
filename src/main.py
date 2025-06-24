from textnode import *
from htmlnode import *
from extract_mk import *
from split_nodes_delimiter import *
from block import *
import os
import shutil
import sys


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def generate_public_files_recursive(src_dir, dest_dir):

    for f in os.listdir(src_dir):
        src_f = os.path.join(src_dir, f)
        dest_f = os.path.join(dest_dir, f)
        if os.path.isfile(src_f):
            shutil.copy(src_f, dest_f)
        else:
            os.mkdir(dest_f)
            generate_public_files_recursive(src_f, dest_f)


def generate_public_files(src_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir)

    generate_public_files_recursive(src_dir, dest_dir)



    
def extract_title(markdown):
    md_title = ""
    for b in markdown.split("\n"):
        if b[0] == "#" and b[1] == " ":
            md_title = b
            break

    return md_title[1:].strip()


def generate_page(from_path, tempelate_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {tempelate_path}")
    mk_file = open(from_path)
    md_text = mk_file.read()
    temp_file = open(tempelate_path)
    temp_text = temp_file.read()
    mk_file.close()
    temp_file.close()

    html_string = markdown_to_html_node(md_text).to_html()
    page_title = extract_title(md_text)

    page = temp_text.replace("{{ Title }}", page_title)
    page = page.replace("{{ Content }}", html_string)
    page = page.replace("href=\"/", f"href=\"{basepath}")
    page = page.replace("src=\"/", f"src=\"{basepath}")


    with open(dest_path, 'w') as f:
        f.write(page)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):

    for f in os.listdir(dir_path_content):
        src_f = os.path.join(dir_path_content, f)
        dest_path = os.path.join(dest_dir_path, f)
        if os.path.isfile(src_f):
            f = f.split(".")[0] + ".html"
            dest_path = os.path.join(dest_dir_path, f)
            generate_page(src_f, template_path, dest_path, basepath)
        else:
            os.mkdir(dest_path)
            generate_pages_recursive(src_f, template_path, dest_path, basepath)







    




def main():
    basepath = ""
    if len(sys.argv) == 2:
        basepath = sys.argv[1]

    
    markdown_dir_path = "content"
    tempelate_path = "tempelate.html"
    dest_dir_path = "docs"

    generate_public_files("static", "docs")
    
    generate_pages_recursive(markdown_dir_path, tempelate_path, dest_dir_path, basepath)





if __name__ == "__main__":
    main()