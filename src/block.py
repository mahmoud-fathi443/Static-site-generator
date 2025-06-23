from enum import Enum
from extract_mk import markdown_to_blocks
from htmlnode import HTMLNode, ParentNode, LeafNode
from textnode_to_htmlnode import *
from main import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(markdown_block: str) -> BlockType:
    def isHeader(str):
        for i in range(6, 0, -1):
            if str.startswith("#"*i):
                if str[i] == " ":
                    return True
                
    def isCode(str):
        if str.startswith('```') and str.endswith('```'):
            return True
    def isQuote(str):
        for line in str.split('\n'):
            if not line.startswith('>'):
                return False
        return True
    def isUoList(str):
        for line in str.split('\n'):
            if not line.startswith('- '):
                return False
        return True
    def isOList(str):
        i = 0
        for line in str.split('\n'):
            if not line.startswith(f'{i+1}. '):
                return False
            i+=1
        return True
    
    if isHeader(markdown_block):
        return BlockType.HEADING
    elif isCode(markdown_block):
        return BlockType.CODE
    elif isQuote(markdown_block):
        return BlockType.QUOTE
    elif isUoList(markdown_block):
        return BlockType.UNORDERED_LIST
    elif isOList(markdown_block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    children = []
    # parse markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # parse blocks into HTML
    for block in blocks:
        block_type = block_to_block_type(block)
        node = block_to_html_node(block, block_type)
        children.append(node)

    # return html str
    return ParentNode(tag="div", children=children)


def block_to_html_node(text: str, type: BlockType) -> HTMLNode:
    match type:
        case BlockType.QUOTE:
            return _quote_block_to_html_node(text)
        case BlockType.UNORDERED_LIST:
            return _ul_block_to_html_node(text)
        case BlockType.ORDERED_LIST:
            return _ol_block_to_html_node(text)
        case BlockType.CODE:
            return _code_block_to_html_node(text)
        case BlockType.HEADING:
            return _heading_block_to_html_node(text)
        case BlockType.PARAGRAPH:
            return _paragraph_block_to_html_node(text)
        case _:
            raise Exception(f"Unknown BlockType {type}")


def text_to_html_node(text: str) -> list[LeafNode]:
    # take text and make it into leaf nodes (children of parent)
    # text nodes are our intermediate representation
    text_nodes = text_to_textnodes(text)

    # this is the actual html represetnation
    children = [text_node_to_html_node(node) for node in text_nodes]

    return children

def _quote_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    text = ""
    for line in markdown.split("\n"):
        text += line.strip().strip(">")

    # text needs to be parsed into html nodes (aka leaf nodes)
    children = text_to_html_node(text.strip())
    return ParentNode(tag="blockquote", children=children)

def _code_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    list_elements = []
    text = markdown.strip("```")
    children = text_to_html_node(text)
    list_elements.append(ParentNode("pre", children))

    return ParentNode(tag="code", children=list_elements)


def _heading_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    heading_parts = markdown.split()
    heading, heading_text = heading_parts[0], " ".join(heading_parts[1:])
    heading_num = len(heading)
    # text needs to be parsed into html nodes (aka leaf nodes)
    children = text_to_html_node(heading_text)
    return ParentNode(tag=f"h{heading_num}", children=children)

def _paragraph_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    text = ""
    for line in markdown.split("\n"):
        text += " " + line

    # text needs to be parsed into html nodes (aka leaf nodes)
    children = text_to_html_node(text.strip())
    return ParentNode(tag="p", children=children)


def _ul_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    list_elements = []
    for line in markdown.split("\n"):
        # we know it's a ul, so assume it's the correct format
        children = text_to_html_node(line[2:])
        list_elements.append(ParentNode("li", children))

    return ParentNode(tag="ul", children=list_elements)

def _ol_block_to_html_node(markdown: str) -> HTMLNode:
    # markdown text ready to be made into html text
    list_elements = []
    for line in markdown.split("\n"):
        # we know it's a ol, so assume it's the correct format
        children = text_to_html_node(line[3:])
        list_elements.append(ParentNode("li", children))

    return ParentNode(tag="ol", children=list_elements)