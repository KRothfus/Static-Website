from htmlnode import text_node_to_html_node, HTMLNode
from textnode import BlockType, TextNode, TextType, block_to_block_type, markdown_to_blocks, text_to_textnodes
from textparsing import split_nodes_delimiter

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    print('blocks',markdown_blocks,'Full',markdown)

    for block in markdown_blocks:
        block_of_type = block_to_block_type(block)
        block_to_html_node = block_type_to_html_node(block_of_type,block)



def block_type_to_html_node(type,text_block):
    match type:
        case BlockType.HEADING:
            heading_count = 0
            for char in text_block:
                if char == '#':
                    heading_count += 1
                else:
                     break
            return HTMLNode("h" + heading_count,text_block.strip(['#','##','###','####','#####','######']))
        case BlockType.CODE:
            return HTMLNode('pre',children=[HTMLNode('code', text_block.strip("```"))])
        case BlockType.QUOTE:
            childs = text_to_children(type, text_block)
            return HTMLNode('blockquote',children=[childs])
        case BlockType.UNORDEREDLIST:
            return HTMLNode('ul',children=[HTMLNode('li',text_block.strip('-'))])
        case BlockType.ORDEREDLIST:
            return HTMLNode('ol', children=[HTMLNode('li',text_block.strip(r'\d\. '))])
        case BlockType.PARAGRAPH:
            return HTMLNode('p',text_block)
        case _:
            return

def text_to_children(type, text):
    nodes_of_text = text_to_textnodes(text)
    nodes_of_html = []
    for node in nodes_of_text:
        nodes_of_html.append(text_node_to_html_node(node)) 
    match type:
        case BlockType.HEADING:
            return nodes_of_html
        case BlockType.QUOTE:
            
            return nodes_of_html
        case BlockType.UNORDEREDLIST:
            return nodes_of_html
        case BlockType.ORDEREDLIST:
            return nodes_of_html
        case BlockType.PARAGRAPH:
            return nodes_of_html
        case _:
            return