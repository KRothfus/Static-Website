import os
import shutil
import sys

from pagegeneration import generate_pages_recursive



def copy_files_to_public():
    def recursive_to_public(initial_dir = './static'):
        if os.path.exists(initial_dir):
            dirs = os.listdir(initial_dir)
            for dir in dirs:
                if os.path.isfile(initial_dir +'/'+dir):
                    print(f'Copying file: {initial_dir.replace('static','docs')+'/'+dir}')
                    shutil.copy(initial_dir+'/'+dir,initial_dir.replace('static','docs')+'/'+dir)
                else:
                    print(f'Making directory: {initial_dir.replace('static','docs')+'/'+dir}')
                    os.mkdir(initial_dir.replace('static','docs')+'/'+dir)
                    recursive_to_public(initial_dir+'/'+dir)
    if os.path.exists('./docs'):
        print(f'Removing docs Directory')
        shutil.rmtree('./docs')
    print('Creating docs Directory')
    os.mkdir('./docs')
    recursive_to_public()

def main():
    basepath = sys.argv
    print(basepath)
    copy_files_to_public()
    generate_pages_recursive('content','template.html','docs',basepath)
# result = TextNode('this is some anchor text','link','https://www.boot.dev')
# print(result)

if __name__ == '__main__':
    main()