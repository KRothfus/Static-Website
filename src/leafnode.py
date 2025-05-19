# from htmlnode import HTMLNode

# class LeafNode(HTMLNode):
#     def __init__(self, tag, value, props=None):
#         super().__init__(tag, value, props)
#         self.tag = tag
#         self.value = value
#         self.props = props
        
#     def to_html(self):
#         if not self.value:
#             raise ValueError('All leaf nodes must have a value')
#         if self.tag == None:
#             return self.value
#         return f'<{self.tag}>{self.value}</{self.tag}>'