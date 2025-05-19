# from htmlnode import HTMLNode
# from leafnode import LeafNode

# class ParentNode(HTMLNode):
#     def __init__(self, tag, children, props=None):
#         super().__init__(tag, children, props)
#         self.tag = tag
#         self.children = children
#         self.props = props
#     def to_html(self):
#         if self.tag == None:
#             raise ValueError('Missing tag')
#         if len(self.children) == 0:
#             raise ValueError('Missing children')
#         child_result = ''
#         for child in self.children:
#             if type(child) != LeafNode:
#                 child_result += child.to_html()
#             else:
#                 child_result += f'<{child.tag}>{child.value}</{child.tag}>'
#         return f'<{self.tag}>{child_result}</{self.tag}>'