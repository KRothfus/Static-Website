from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes,delimiter,text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
            continue
        text = node.text
        start_index = text.find(delimiter)
        if start_index == -1:
            result.append(node)
            continue
        end_index = text.find(delimiter, start_index + len(delimiter))
        if end_index == -1:
            raise Exception(f'No closing "{delimiter}" found')
        if start_index > 0:
            result.append(TextNode(text[:start_index], TextType.TEXT))
        between_text = text[start_index + len(delimiter):end_index]
        result.append(TextNode(between_text,text_type))
        
        remaining_text = text[end_index+len(delimiter):]
        if delimiter in remaining_text:
            remaining_nodes = split_nodes_delimiter([TextNode(remaining_text, TextType.TEXT)],delimiter,text_type)
            result.extend(remaining_nodes)
        elif remaining_text:
            result.append(TextNode(remaining_text,TextType.TEXT))
    return result