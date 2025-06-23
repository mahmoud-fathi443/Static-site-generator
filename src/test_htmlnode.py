import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        dict = {
            "href": "https://www.google.com",
            "target": "_blank",
            }   
        node = HTMLNode('a', 'link', props=dict)
        node1 = HTMLNode('a', 'link')
        
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')
        self.assertEqual(node1.props_to_html(), '')

    def test_repr(self):
        dict = {
            "href": "https://www.google.com",
            "target": "_blank",
            }   
        node = HTMLNode('a', 'link', props=dict)
        node1 = HTMLNode('a', 'link')

        expected = "HTMLNode(a, link, None, {'href': 'https://www.google.com', 'target': '_blank'})"
        expected2 = "HTMLNode(a, link, None, None)"
        
        self.assertEqual(node.__repr__(), expected)
        self.assertEqual(node1.__repr__(), expected2)

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
