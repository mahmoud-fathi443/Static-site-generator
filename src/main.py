from textnode import *
from htmlnode import *
from extract_mk import *
from split_nodes_delimiter import *
import os
import shutil



def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def generat_public_files_recursive(src_dir, dest_dir):
    for f in os.listdir(src_dir):
        src_f = os.path.join(src_dir, f)
        dest_f = os.path.join(dest_dir, f)
        if os.path.isfile(src_f):
            shutil.copy(src_f, dest_f)
        else:
            os.mkdir(dest_f)
            generat_public_files_recursive(src_f, dest_f)



    



def generate_public_files(src_dir, dest_dir):
    if os.path.exists(dest_dir):
        shutil.rmtree(dest_dir)

    os.makedirs(dest_dir)

    generat_public_files_recursive(src_dir, dest_dir)

    print(os.listdir(src_dir))
    print(os.listdir(dest_dir))

    



    




def main():
    generate_public_files("static", "public")
    
    



if __name__ == "__main__":
    main()