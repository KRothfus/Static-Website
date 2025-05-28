import os
import shutil

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
        print(f'Creating Public Directory')
        shutil.rmtree('./public')
    os.mkdir('./public')
    recursive_to_public()

def main():
    copy_files_to_public()
# result = TextNode('this is some anchor text','link','https://www.boot.dev')
# print(result)

if __name__ == '__main__':
    main()