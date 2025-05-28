import os
import shutil

from pagegeneration import generate_pages_recursive

def copy_files_to_public():
    def recursive_to_public(initial_dir = './static'):
        if os.path.exists(initial_dir):
            dirs = os.listdir(initial_dir)
            for dir in dirs:
                if os.path.isfile(initial_dir +'/'+dir):
                    print(f'Copying file: {initial_dir.replace('static','public')+'/'+dir}')
                    shutil.copy(initial_dir+'/'+dir,initial_dir.replace('static','public')+'/'+dir)
                else:
                    print(f'Making directory: {initial_dir.replace('static','public')+'/'+dir}')
                    os.mkdir(initial_dir.replace('static','public')+'/'+dir)
                    recursive_to_public(initial_dir+'/'+dir)
    if os.path.exists('./public'):
        print(f'Removing Public Directory')
        shutil.rmtree('./public')
    print('Creating Public Directory')
    os.mkdir('./public')
    recursive_to_public()

def main():
    copy_files_to_public()
    generate_pages_recursive('content','template.html','public')
# result = TextNode('this is some anchor text','link','https://www.boot.dev')
# print(result)

if __name__ == '__main__':
    main()