import os

from buildhtml import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path, basepath):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}')
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
        
    markdown_html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace('{{ Title }}',title)
    template = template.replace('{{ Content }}', markdown_html)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, mode='w') as d:
        d.write(template)
        
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    try:
        dir_list = os.listdir(dir_path_content)
    except:
        raise Exception('nothing to parse')
    for dir in dir_list:
        if os.path.isfile(os.path.join(dir_path_content,dir)):
            generate_page(os.path.join(dir_path_content,dir), template_path, os.path.join(dest_dir_path,dir.replace('.md','.html')),basepath)
        else:
            generate_pages_recursive(os.path.join(dir_path_content,dir), template_path,os.path.join(dest_dir_path,dir), basepath)