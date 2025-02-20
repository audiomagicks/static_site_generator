from textnode import *
from htmlnode import *
from mytools import *
import shutil
import os

project_path = '~/workspace/github.com/audiomagicks/static_site_generator/'

# shutil.copy(
#     'static/index.css',
#     'public/index.css'
# ) #confirmed working properly, copies files to a destination

# public_contents = os.listdir('public/')
# static_contents = os.listdir('static/')
# print(public_contents)
# print(static_contents) #confirmed working, lists contents of directory. Keeping prints in for debugging

# os.path.exists('static/images/')
# print(path_existence) #confirmed working, returns true if directory or file exists

# joined = os.path.join('public/', 'images/')
# print(joined)
# os.mkdir(joined)   #this will append the 2nd argument to the first, and create the new dir    

# shutil.rmtree('public/')
# os.mkdir('public/') #confirmed working, removes tree, then remakes it, effectively clearing the dir

# os.path.isfile() and os.path.isdir() will return True if the argument is a file or dir respectively

def main():
    src_path = 'static/'
    dst_path = 'public/'
    if os.path.exists(dst_path):
        shutil.rmtree(dst_path)
        print('------------------------------------------')
        print(f'{dst_path} dir cleared successfully')
    os.mkdir(dst_path)
    
    copy_dir(src_path, dst_path, os.listdir(src_path))


def copy_dir(src_path, dst_path, src_dir_list):
    if not src_dir_list:
        print(f'{src_path} copied to {dst_path}')
        print('------------------------------------------')
        return 
    if not os.path.exists(os.path.join(dst_path, src_dir_list[0])):
        if os.path.isdir(os.path.join(src_path, src_dir_list[0])):
            nested_src = os.path.join(src_path, src_dir_list[0])
            nested_dst = os.path.join(dst_path, src_dir_list[0])
            os.mkdir(nested_dst)
            print('------------------------------------------')
            print(f'{nested_dst} succesfully created, copying contents of src')
            copy_dir(nested_src, nested_dst, os.listdir(nested_src))

        elif os.path.isfile(os.path.join(src_path, src_dir_list[0])):
            shutil.copy(
                os.path.join(src_path, src_dir_list[0]),
                os.path.join(dst_path, src_dir_list[0])
            )
            print('------------------------------------------')
            print(os.path.join(src_path, src_dir_list[0]))
            print(f'copied to {dst_path}')
            print(f'{os.path.join(dst_path, src_dir_list[0])} successfully created')


    copy_dir(src_path, dst_path, src_dir_list[1:])


main()