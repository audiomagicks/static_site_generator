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
    copy_src_path = 'static/'
    copy_dst_path = 'public/'
    if os.path.exists(copy_dst_path):
        shutil.rmtree(copy_dst_path)
        print('------------------------------------------')
        print(f'{copy_dst_path} dir cleared successfully')
    os.mkdir(copy_dst_path)
    #clears dst path and copies src to it
    copy_dir(copy_src_path, copy_dst_path, os.listdir(copy_src_path))

    generate_pages_recursive('content/', 'template.html', 'public/', os.listdir('content/'))


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

def extract_title(markdown):
    first_line = markdown.split('\n')
    if first_line[0].startswith('# '):
        return first_line[0][2:]
    raise Exception('h1 header not present on first line')

def generate_page(from_path, dest_path, template_path):
    print(f'generating page from {from_path} to {dest_path} using {template_path}\n')
    with open(from_path) as f:
        md_content = f.read()
    print("First few lines of markdown content:")
    print(md_content[:200])  # Print first 200 chars to verify content is being read
    
    html_node_content = markdown_to_html_node(md_content)
    print("HTML node structure:")
    print(html_node_content)  # Let's see what the node looks like
    
    html_content = html_node_content.to_html()
    print("Generated HTML content:")
    print(html_content[:200])  # Print first 200 chars of generated HTML
    
    print(f'generating page from {from_path} to {dest_path} using {template_path}\n')
    with open(from_path) as f:
        md_content = f.read()
    with open(template_path) as f:
        template = f.read()
    html_node_content = markdown_to_html_node(md_content)
    html_content = html_node_content.to_html()
    title = extract_title(md_content)
    titled_template = template.replace('{{ Title }}', title)
    final_content = titled_template.replace('{{ Content }}', html_content)
    with open(dest_path, 'w')as file:
        file.write(final_content)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, content_dir_list):
    if not content_dir_list:
        print(f'{dir_path_content} copied to {dest_dir_path}')
        print('------------------------------------------')
        return 
    if not os.path.exists(os.path.join(dest_dir_path, content_dir_list[0])):
        if os.path.isdir(os.path.join(dir_path_content, content_dir_list[0])):
            nested_src = os.path.join(dir_path_content, content_dir_list[0])
            nested_dst = os.path.join(dest_dir_path, content_dir_list[0])
            os.mkdir(nested_dst)
            print('------------------------------------------')
            print(f'{nested_dst} succesfully created, copying contents of content')
            generate_pages_recursive(nested_src, template_path, nested_dst, os.listdir(nested_src))

        elif os.path.isfile(os.path.join(dir_path_content, content_dir_list[0])):
            new_filename = content_dir_list[0][:-2] + 'html'
            print(new_filename)
            generate_page(os.path.join(dir_path_content, content_dir_list[0]), os.path.join(dest_dir_path, new_filename), template_path)

            print('------------------------------------------')
            print(os.path.join(dir_path_content, content_dir_list[0]))
            print(f'copied to {dest_dir_path}')
            print(f'{os.path.join(dest_dir_path, new_filename)} successfully created')
            #dang old shortcut of copying my other function don't seem to be werkin
    generate_pages_recursive(dir_path_content, template_path, dest_dir_path, content_dir_list[1:])


main()