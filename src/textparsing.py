from textnode import TextType

#I think i want to use recursion here. need to return by calling this function until there
# are is no text available to parse through. 
def split_nodes_delimiteter(old_nodes,delimiter,text_type):
    result = []
    if text_type != TextType.TEXT:
        result.append((old_nodes.value,text_type))
    old_nodes = old_nodes.value.split(delimiter)
    match  (text_type,delimiter):
        case (TextType.CODE,'`'):
            return old_nodes.value.split(delimiter)
        case (TextType.BOLD,'**'):
            return old_nodes.value.split(delimiter)
        case (TextType.ITALIC,'_'):
            return old_nodes.value.split(delimiter)
        case _:
            raise Exception('Invalid markdown syntax')
        