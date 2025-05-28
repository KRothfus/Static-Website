import unittest

from buildhtml import extract_title
from textnode import *
from textparsing import split_nodes_delimiter
from linkextraction import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_textnoteq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This might be a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_typenoteq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    
    def test_urlNone(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertIs(node.url, None)
        
    def test_delimiter_italic(self):
        node = TextNode("This is an _italic_ text node", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],'_',TextType.ITALIC),[TextNode("This is an ", TextType.TEXT) , TextNode("italic",TextType.ITALIC), TextNode(" text node",TextType.TEXT)])
    
    def test_delimiter_italic(self):
        node = TextNode("This is a `code text node.`", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node],'`',TextType.CODE),[TextNode("This is a ", TextType.TEXT) , TextNode("code text node.",TextType.CODE)])
    
    def test_delimiter_no_close(self):
        node = TextNode("This is a `code text node.", TextType.TEXT)
        with self.assertRaises(Exception) as context:
            split_nodes_delimiter([node], '`', TextType.CODE)
        self.assertTrue('No closing "`" found' in str(context.exception))
        
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)
        
        
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
    )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
        
    def test_split_images_after_text(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) hello",
            TextType.TEXT,
    )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" hello", TextType.TEXT),
            ],
            new_nodes,
        )
            
            
    def test_split_links(self):
        node = TextNode(
            "This is text with an [alt text](google.com) and another [alt text2](google2.com)",
            TextType.TEXT,
    )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("alt text", TextType.LINK, "google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "alt text2", TextType.LINK, "google2.com"
                ),
            ],
            new_nodes,
        )
    
    def test_split_links_after_text(self):
        node = TextNode(
            "This is text with an [alt text](google.com) and another [alt text2](google2.com) hello",
            TextType.TEXT,
    )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("alt text", TextType.LINK, "google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "alt text2", TextType.LINK, "google2.com"
                ),
                TextNode(" hello",TextType.TEXT)
            ],
            new_nodes,
        )
        
    def test_all_the_things(self):
        string = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(string)
        self.maxDiff = None
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev")
            ],
        
        new_nodes,
        )
        
    def test_markdown_to_blocks(self):
        md = """
        This is **bolded** paragraph

        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_markdown_to_empty_blocks(self):
        md = """
        This is **bolded** paragraph



        This is another paragraph with _italic_ text and `code` here
        This is the same paragraph on a new line

        - This is a list
        - with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
        
    def test_block_to_block_type_quote(self):
        md = '>hello\n>world'
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_code(self):
        md = '```hello world```'
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.CODE)
        
    def test_block_to_block_type_header(self):
        md = '### hello world'
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.HEADING)
        
    def test_block_to_block_type_unordered(self):
        md = '- hello\n- world'
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.UNORDEREDLIST)
    def test_block_to_block_type_ordered(self):
        md = '1. hello\n2. world'
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.ORDEREDLIST)
    def test_block_to_block_type_ordered(self):
        md = '1. hello\n3. world'
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)    
    def test_block_to_block_type_paragraph(self):
        md = 'hello world'
        block_type = block_to_block_type(md)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    def test_extracttitle(self):
        md = '# Hello   '
        header = extract_title(md)
        self.assertEqual(header, 'Hello')
        
    def test_extracttitle(self):
        md = '''
        # Hello 
        ## hi
        '''
        header = extract_title(md)
        self.assertEqual(header, 'Hello')
        
    def test_extracttitle(self):
        md = ' Hello '
        with self.assertRaises(Exception) as context:
            extract_title(md)
        self.assertTrue('No header found!' in str(context.exception))

if __name__ == "__main__":
    unittest.main()