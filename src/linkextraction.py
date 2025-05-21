import re
from textnode import TextType, TextNode

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)


def split_nodes_image(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        images = extract_markdown_images(old_node.text)
        if not images:
            result.append(old_node)
            continue
            
        # Handle the first image
        alt_text, url = images[0]
        parts = old_node.text.split(f"![{alt_text}]({url})", 1)
        
        if parts[0]:
            result.append(TextNode(parts[0], TextType.TEXT))
        
        result.append(TextNode(alt_text, TextType.IMAGE, url))
        
        if parts[1]:
            # Process the remaining text recursively
            remaining_nodes = split_nodes_image([TextNode(parts[1], TextType.TEXT)])
            result.extend(remaining_nodes)
            
    return result

def split_nodes_link(old_nodes):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
            
        images = extract_markdown_links(old_node.text)
        if not images:
            result.append(old_node)
            continue
            
        # Handle the first image
        alt_text, url = images[0]
        parts = old_node.text.split(f"[{alt_text}]({url})", 1)
        
        if parts[0]:
            result.append(TextNode(parts[0], TextType.TEXT))
        
        result.append(TextNode(alt_text, TextType.LINK, url))
        
        if parts[1]:
            # Process the remaining text recursively
            remaining_nodes = split_nodes_link([TextNode(parts[1], TextType.TEXT)])
            result.extend(remaining_nodes)
            
    return result