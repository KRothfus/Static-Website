import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(props = {'href':"https://www.google.com",'target':'_parent'})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_parent"')
        
    def test_repr(self):
        node = HTMLNode('p','This is a paragraph',['child1','child2'],{'href':"https://www.google.com",'target':"_parent"})
        print('here',node.__repr__())
        self.assertEqual(node.__repr__(),"HTMLNode(tag = p,value = This is a paragraph,children = ['child1', 'child2'],props = {'href': 'https://www.google.com', 'target': '_parent'})")

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )
        
        
if __name__ == "__main__":
    unittest.main()