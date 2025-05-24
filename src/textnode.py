from enum import Enum
import re
class TextType(Enum):
    
    TEXT = ''    
    BOLD = '**Bold text**'
    ITALIC = '_Italic text_'
    CODE = '`Code text`'
    LINK = '[anchor text](url)'
    IMAGE = '![alt text](url)'

class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        
    def __eq__(self, other):
        result = False
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            result = True
        return result
    
    def __repr__(self):
        return f'TextNode({self.text}, {self.text_type}, {self.url})'

class BlockType(Enum):
    PARAGRAPH = ''
    HEADING = '#'
    CODE = '``'
    QUOTE = '""'
    UNORDEREDLIST = '-'
    ORDEREDLIST = 'o'


from linkextraction import split_nodes_image, split_nodes_link
from textparsing import split_nodes_delimiter
def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    result = []
    blocks = markdown.split('\n\n')
    for block in blocks:
        result_lines = []
        lines = block.split('\n')
        for line in lines:
            line = line.strip()
            if line != '':                
                result_lines.append(line)
        if result_lines:
            result.append('\n'.join(result_lines))
    return result

def block_to_block_type(markdown):
    if markdown.startswith('#'):
        level = 0
        for char in markdown:
           if char == '#':
               level += 1
           else:
               break
        if level <= 6 and markdown[level:level+1] == ' ':
            return BlockType.HEADING
    
    if markdown.startswith('```') and markdown.endswith('```'):
        return BlockType.CODE
    
    #quotes
    lines = markdown.split('\n')
    quotes_are_lines = True
    for line in lines:
        if not line.startswith('>'):
            quotes_are_lines = False
            break
    if quotes_are_lines:
        return BlockType.QUOTE
    
    #unordered list
    list_lines = True
    for line in lines:
        if not line.startswith('- '):
            list_lines = False
            break
    if list_lines:
        return BlockType.UNORDEREDLIST
    
    #ordered list
    order_list_lines = True
    for i, line in enumerate(lines):
        if not line.startswith(f'{i+1}. '):
            order_list_lines = False
            break
    if order_list_lines:
        return BlockType.ORDEREDLIST
    
    return BlockType.PARAGRAPH