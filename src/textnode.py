from enum import Enum

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
# need to add the logic to determine if each is actually the thing it is. like for a code block
# we need to check if there is three ` before and after.
def block_to_block_type(markdown):
    if '#' in markdown.split()[0:6]:
        return BlockType.HEADING
    if '`' in markdown:
        return BlockType.CODE
    if '"' in markdown:
        return BlockType.QUOTE
    if '-' in markdown:
        return BlockType.UNORDEREDLIST
    if 'o' in markdown:
        return BlockType.ORDEREDLIST
    return BlockType.PARAGRAPH