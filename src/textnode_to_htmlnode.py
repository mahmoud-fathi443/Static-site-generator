from textnode import *
from htmlnode import *

def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case text_node.text_type.NORMAL:
            return LeafNode(None, text_node.text)
        case text_node.text_type.BOLD:
            return LeafNode('b', text_node.text)
        case text_node.text_type.ITALIC:
            return LeafNode('i', text_node.text)
        case text_node.text_type.CODE:
            return LeafNode('code', text_node.text)
        case text_node.text_type.LINK:
            return LeafNode('a', text_node.text, {"href":text_node.url})
        case text_node.text_type.IMAGE:
            return LeafNode('img', "", {"src":text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Not a standard text type!")