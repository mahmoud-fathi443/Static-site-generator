from textnode import *
from extract_mk import extract_markdown_images, extract_markdown_links
def split_nodes_delimiter(old_nodes: list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    lst = []
    
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            lst.append(node)
            continue

        i_arr = []
        for i, d in enumerate(node.text):
            if d == delimiter:
                i_arr.append(i)   
        if len(i_arr) % 2 != 0:
            raise Exception("Invalid markdown syntax!")
        
        str_arr = node.text.split(delimiter)

        for i, str in enumerate(str_arr):
            if str == "":
                continue
            if i % 2 == 0:
                node = TextNode(str, TextType.NORMAL)
                lst.append(node)
            else:
                node = TextNode(str, text_type)
                lst.append(node)
    return lst

        
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.NORMAL))
    return new_nodes
