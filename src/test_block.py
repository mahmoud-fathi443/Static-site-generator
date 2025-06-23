import unittest
from block import BlockType, block_to_block_type, markdown_to_html_node


# --- TEST CASES START HERE ---

class TestBlockToBlockType(unittest.TestCase):
    def test_headings(self):
        # Valid headings
        self.assertEqual(block_to_block_type("# A heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Another heading"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Level 6"), BlockType.HEADING)
        
        # Invalid headings (should be paragraphs)
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("####### Too many hashes"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("A normal sentence # with a hash"), BlockType.PARAGRAPH)

    def test_code_blocks(self):
        # Valid code block
        block = "```\nprint('hello')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        
        # Invalid code blocks (should be paragraphs)
        block = "```\nprint('no closing tags')"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "no opening tags\n```"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_blocks(self):
        # Valid quote block
        block = "> This is a quote\n> On multiple lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = ">Just one line" # Still valid as per instructions
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        
        # Invalid quote block (one line is not a quote)
        block = "> This is a quote\nBut this line is not"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_lists(self):
        # Valid unordered list
        block = "- An item\n- Another item"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        
        # Test with a different valid marker (if you choose to support it)
        block = "* An item\n* Another item"
        # Assuming the check is for either '*' or '-'
        # self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        # Invalid list (missing space after dash)
        block = "-An item without space"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Invalid list (one line is not a list item)
        block = "- An item\nThis is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_lists(self):
        # Valid ordered list
        block = "1. First item\n2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        
        # Invalid list (doesn't start at 1)
        block = "2. Second item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
        # Invalid list (sequence is broken)
        block = "1. First item\n3. Third item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # Invalid list (missing space)
        block = "1.First item\n2.Second item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
    def test_paragraphs(self):
        # Standard paragraphs
        block = "This is just a normal paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "A paragraph\nthat spans\nmultiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


    def test_empty_md(self):
        markdown = ""
        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div></div>"

        self.assertEqual(result, expected_result)

    def test_simple_md(self):
        markdown = "hi"
        result = markdown_to_html_node(markdown).to_html()
        expected_result = "<div><p>hi</p></div>"

        self.assertEqual(result, expected_result)

    def test_blockquote(self):
                markdown = """
> This is a
> blockquote block

this is paragraph text

        """

                result = markdown_to_html_node(markdown).to_html()
                expected_result = "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>"
                self.assertEqual(result, expected_result)

    def test_paragraphs(self):
                markdown = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

        """

                result = markdown_to_html_node(markdown).to_html()
                expected_result = "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"
                self.assertEqual(result, expected_result)

    def test_lists(self):
                markdown = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

        """

                result = markdown_to_html_node(markdown).to_html()
                expected_result = "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>"

                self.assertEqual(result, expected_result)

    def test_headings(self):
                markdown = """
        # this is an h1

        this is paragraph text

        ## this is an h2
        """

                result = markdown_to_html_node(markdown).to_html()
                expected_result = "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>"
                self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()