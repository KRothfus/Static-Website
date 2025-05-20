import unittest

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
if __name__ == "__main__":
    unittest.main()