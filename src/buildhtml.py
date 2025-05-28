from htmlnode import LeafNode, ParentNode, text_node_to_html_node, HTMLNode
from textnode import BlockType, TextNode, TextType, block_to_block_type, markdown_to_blocks, text_to_textnodes
from textparsing import split_nodes_delimiter
import re
def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    block_to_html_node = []
    for block in markdown_blocks:
        block_of_type = block_to_block_type(block)
        block_to_html_node.append(block_type_to_html_node(block_of_type,block))
    return ParentNode('div',children=block_to_html_node)


def block_type_to_html_node(type,text_block):
    match type:
        case BlockType.HEADING:
            heading_count = 0
            for char in text_block:
                if char == '#':
                    heading_count += 1
                else:
                     break
            childs = text_to_children(text_block[heading_count+1:])
            return ParentNode(f'h{heading_count}', children=childs)
        case BlockType.CODE:
            strip_lines = text_block.split('\n')
            joined_lines = '\n'.join(strip_lines[1:-1]) + '\n'
            return ParentNode('pre',children=[LeafNode('code', joined_lines)])
        case BlockType.QUOTE:
            quote_split = text_block.split('\n')
            quote_lines = []
            for line in quote_split:
                if line.startswith('> '):
                    quote_lines.append(line[2:])
                else:
                    quote_lines.append(line)
            text_quote = ''.join(quote_lines)+'\n'
            childs = text_to_children(text_quote)
            return ParentNode('blockquote',children=childs)
        case BlockType.UNORDEREDLIST:
            split_text = text_block.split('\n')
            list_item = []
            for line in split_text:
                strip_line = re.split(r'\- ', line,maxsplit=1)
                childs = text_to_children(strip_line[1])
                list_item.append(ParentNode('li',childs))
            return ParentNode('ul',children=list_item)
        case BlockType.ORDEREDLIST:
            split_text = text_block.split('\n')
            list_item = []
            for line in split_text:
                strip_line = re.split(r'\d\. ', line,maxsplit=1)
                childs = text_to_children(strip_line[1])
                list_item.append(ParentNode('li',childs))
            return ParentNode('ol',children=list_item)
        case BlockType.PARAGRAPH:
            text = text_block.split('\n')
            text_joined = ' '.join(text)
            childs = text_to_children(text_joined)
            return ParentNode('p', children=childs)
        case _:
            return

def text_to_children(text):
    nodes_of_text = text_to_textnodes(text)
    nodes_of_html = []
    for node in nodes_of_text:
        nodes_of_html.append(text_node_to_html_node(node))
    return nodes_of_html

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
        if line.startswith('# '):
            return line[2:].strip(' ')
    raise Exception('No header found!')