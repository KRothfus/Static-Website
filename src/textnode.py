from enum import Enum


class TextType(Enum):
        
    BOLD = '**Bold text**'
    ITALIC = '_Italic text_'
    CODE = '`Code text`'
    LINKS = '[anchor text](url)'
    IMAGES = '![alt text](url)'

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
    