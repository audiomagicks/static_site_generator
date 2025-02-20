from textnode import *
from htmlnode import *
import re
from enum import Enum

def text_node_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text, None)
        case TextType.BOLD:
            return LeafNode('b', text_node.text, None)
        case TextType.ITALIC:
            return LeafNode('i', text_node.text, None)
        case TextType.CODE:
            return LeafNode('code', text_node.text, None)
        case TextType.LINK:
            return LeafNode('a', text_node.text, {'href':text_node.url})
        case TextType.IMAGE:
            return LeafNode('img', '', {'src':text_node.url, 'alt':text_node.text})
        case _:
            raise Exception('invalid type')
        
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT or delimiter not in node.text:
            new_nodes.append(node)
        elif text_type == TextType.ITALIC and node.text.startswith('* '):
            new_nodes.append(node)
        else:
            count = 0
            for c in node.text:
                if c == delimiter:
                    count += 1
            if count % 2 != 0:
                raise Exception('missing closing delimiter, check markdown syntax')
            else:
                intermediary_nodes = node.text.split(f'{delimiter}')
                formatted_nodes = []
                toggle = TextType.TEXT
                for slice in intermediary_nodes:
                    formatted_nodes.append(TextNode(slice, toggle))
                    toggle = text_type if toggle == TextType.TEXT else TextType.TEXT
                new_nodes.extend(formatted_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if "![" in node.text:
            original_text = node.text
            open_parenthasis = 0
            closed_parenthasis = 0
            open_bracket = 0
            closed_bracket = 0
            for c in original_text:
                match c:
                    case '(':
                        open_parenthasis += 1
                    case ')':
                        closed_parenthasis += 1
                    case '[':
                        open_bracket += 1
                    case ']':
                        closed_bracket += 1
                    case _:
                        pass         
            if open_parenthasis != closed_parenthasis or open_bracket != closed_bracket:
                raise Exception('missing closing parenthasis or bracket, check markdown syntax')
            elif open_parenthasis == 0:
                new_nodes.append(node)
            else:
                extracted_images = extract_markdown_images(original_text)
                formatted_nodes = []
                count = 1
                for image in extracted_images:
                    image_alt = image[0]
                    image_link = image[1]
                    sections = original_text.split(f"![{image_alt}]({image_link})", 1)
                    before_image = sections[0]
                    after_image = sections[1]
                    if count == len(extracted_images):
                        if before_image.strip():
                            formatted_nodes.append(TextNode(before_image, TextType.TEXT))
                        formatted_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                        if before_image.strip():
                            formatted_nodes.append(TextNode(after_image, TextType.TEXT))
                    else:
                        count += 1
                        if before_image.strip():
                            formatted_nodes.append(TextNode(before_image, TextType.TEXT))
                        formatted_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                        original_text = after_image

                new_nodes.extend(formatted_nodes)
        else:
            new_nodes.append(node)
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        original_text = node.text
        open_parenthasis = 0
        closed_parenthasis = 0
        open_bracket = 0
        closed_bracket = 0
        for c in original_text:
            match c:
                case '(':
                    open_parenthasis += 1
                case ')':
                    closed_parenthasis += 1
                case '[':
                    open_bracket += 1
                case ']':
                    closed_bracket += 1
                case _:
                    pass         
        if open_parenthasis != closed_parenthasis or open_bracket != closed_bracket:
            raise Exception('missing closing parenthasis or bracket, check markdown syntax')
        elif open_parenthasis == 0:
            new_nodes.append(node)
        else:
            extracted_links = extract_markdown_links(original_text)
            formatted_nodes = []
            for image in extracted_links:
                count = 1
                link_alt = image[0]
                link_link = image[1]
                sections = original_text.split(f"[{link_alt}]({link_link})", 1)
                before_link = sections[0]
                after_link = sections[1]
                if count == len(extracted_links):
                    if before_link.strip():
                        formatted_nodes.append(TextNode(before_link, TextType.TEXT))
                    formatted_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
                    if after_link.strip():
                        formatted_nodes.append(TextNode(after_link, TextType.TEXT))
                else:
                    count += 1
                    if before_link.strip():
                        formatted_nodes.append(TextNode(before_link, TextType.TEXT))
                    formatted_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
                    original_text = after_link

            new_nodes.extend(formatted_nodes)
    return new_nodes

def text_to_textnodes(text):
    text_node = TextNode(text, TextType.TEXT)
    bold_nodes = split_nodes_delimiter([text_node], '**', TextType.BOLD)
    italic_nodes = split_nodes_delimiter(bold_nodes, '*', TextType.ITALIC)
    code_nodes = split_nodes_delimiter(italic_nodes, '`', TextType.CODE)
    image_nodes = split_nodes_image(code_nodes)
    final_nodes = split_nodes_link(image_nodes)
    return final_nodes



# def markdown_to_blocks(markdown):
#     string_list = markdown.split('\n')
#     new_list = []
#     string_block = ''
#     in_code_block = False
#     list_block = None

#     for string in string_list:
#         if string.strip() == '```':
#             in_code_block = not in_code_block
#             if string_block:
#                 string_block += '\n'
#             string_block += string
#         else:
#             if string_block == '':
#                 string_block = string if in_code_block else string.strip()
#             else:
#                 string_block += '\n' + (string if in_code_block else string.strip())
        
#         if string.strip() == '' and not in_code_block:
#             if string_block:
#                 new_list.append(string_block)
#                 string_block = ''
#     if string_block:
#         new_list.append(string_block)
#     return new_list

# def markdown_to_blocks(markdown):
#     string_list = markdown.split('\n')  # Split text into lines
#     new_list = []
#     string_block = ''
#     in_code_block = False
#     list_block = None  # Accumulate list items together

#     for string in string_list:
#         if string.strip() == '```':  # Detect code block start/end
#             if in_code_block:  # Closing a code block
#                 if string_block:
#                     string_block += '\n' + string.strip()  # Add the closing ```
#                     new_list.append(string_block)  # Save the entire code block
#                     string_block = ''
#             else:  # Opening a code block
#                 if string_block:
#                     new_list.append(string_block)  # Save any accumulated non-code block
#                     string_block = ''
#                 string_block = string.strip()  # Start the code block
#             in_code_block = not in_code_block
#         elif in_code_block:  # Inside a code block, preserve line structure
#             string_block += '\n' + string
#         elif re.match(r'^\s*([*\-]\s|(\d+\.)\s)', string):  # Detect list items
#             # Handle list accumulation
#             if list_block is None:
#                 list_block = string.strip()
#             else:
#                 list_block += '\n' + string.strip()
#         else:  # Handle regular blocks
#             # Finalize the list block if leaving a list
#             if list_block:
#                 new_list.append(list_block)
#                 list_block = None
#             if string.strip():  # Add non-empty string as part of a block
#                 if string_block:
#                     string_block += '\n' + string.strip()
#                 else:
#                     string_block = string.strip()
#             else:  # Empty line marks the end of a block
#                 if string_block:
#                     new_list.append(string_block)
#                     string_block = ''

#     # Add remaining blocks
#     if string_block:
#         new_list.append(string_block)
#     if list_block:
#         new_list.append(list_block)

#     return new_list

def markdown_to_blocks(markdown):
    string_list = markdown.split('\n')  # Split text into lines
    new_list = []  
    string_block = ''  
    in_code_block = False  
    list_block = None  # Accumulate list items together

    for string in string_list:
        if re.match(r'^\s*```', string):  # Detect code block delimiter with or without language spec
            if in_code_block:  # Closing a code block
                if string_block:
                    string_block += '\n' + '```'  # Add the closing code block delimiter to the block
                    new_list.append(string_block)  # Save the entire code block
                    string_block = ''
            else:  # Opening a code block
                if string_block:
                    new_list.append(string_block)  # Save any previous non-code block
                string_block = '```'  # Start the new code block
            in_code_block = not in_code_block  # Toggle the in_code_block state
        elif in_code_block:  # Handle lines inside a code block
            string_block += '\n' + string
        elif re.match(r'^\s*([*\-]\s|(\d+\.)\s)', string):  # Detect list items
            # Handle list accumulation
            if list_block is None:
                list_block = string.strip()
            else:
                list_block += '\n' + string.strip()
        else:  # Regular blocks
            # Finalize and save list blocks if leaving a list
            if list_block:
                new_list.append(list_block)
                list_block = None
            if string.strip():  # Handle non-empty lines
                if string_block:
                    string_block += '\n' + string.strip()
                else:
                    string_block = string.strip()
            else:  # Empty lines mark the end of a block
                if string_block:
                    new_list.append(string_block)
                    string_block = ''

    # Add remaining blocks if not yet added
    if string_block:
        new_list.append(string_block)
    if list_block:
        new_list.append(list_block)

    return new_list

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def block_to_block_type(markdown_block):
    markdown_block_lines = markdown_block.split('\n')
    if not markdown_block.strip(): 
        return BlockType.PARAGRAPH
    elif markdown_block_lines[0].startswith('#'):
        if ' ' in markdown_block_lines[0] and 1 <= markdown_block_lines[0].count('#', 0, markdown_block_lines[0].index(' ')) <= 6:
            return BlockType.HEADING
        else:
            return BlockType.PARAGRAPH
    elif markdown_block.startswith('```'):  
        if len(markdown_block_lines) >= 2 and markdown_block_lines[0].startswith('```') and markdown_block_lines[-1] == '```':
            return BlockType.CODE
        return BlockType.PARAGRAPH
    elif markdown_block[0] == '>': 
        for line in markdown_block_lines:
            if not line.strip().startswith('>'):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE  
    elif markdown_block[0] == '*' or markdown_block[0] == '-': 
        symbol = markdown_block[0]
        for line in markdown_block_lines:
            if not line.strip().startswith(symbol + ' '):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST  
    elif markdown_block[0:3] == '1. ': 
        count = 1
        for line in markdown_block_lines:
            if not line.startswith(f'{count}. '):
                return BlockType.PARAGRAPH
            count += 1
        return BlockType.ORDERED_LIST  
    else:
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        parent_node = block_to_htmlnode(block, block_type)
        html_nodes.append(parent_node)
    return ParentNode('div', html_nodes, None)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    final_nodes = []
    for text_node in text_nodes:
        final_nodes.append(text_node_html_node(text_node))
    return final_nodes

def block_to_htmlnode(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            children = text_to_children(block)
            return ParentNode('p', children)
        case BlockType.HEADING:
            level = block.index(' ')
            block = block.split(' ', 1)
            children = text_to_children(block[1])
            return ParentNode(f'h{level}', children,)
        case BlockType.CODE:
            # Get all lines between the backticks, preserving whitespace
            lines = block.split("\n")
            # Skip first and last line (the ```)
            first_content_line = lines[1]
            if first_content_line.startswith("```"):
                # Skip the language specification line
                code_content = "\n".join(lines[2:-1])
            else:
                code_content = "\n".join(lines[1:-1])
            code_node = LeafNode("code", code_content)
            return ParentNode("pre", children=[code_node], props=None)
        case BlockType.QUOTE:
            block_lines = block.split('\n')
            stripped_block_lines = []
            for line in block_lines:
                stripped_block_lines.append(line[1:])
            children = text_to_children('\n'.join(stripped_block_lines))
            return ParentNode('blockquote', children)
        case BlockType.UNORDERED_LIST:
            children = list_item_tagger(block)
            return ParentNode('ul', children)
        case BlockType.ORDERED_LIST:
            children = list_item_tagger(block)
            return ParentNode('ol', children)
        case _:
            raise Exception('Invalid BlockType')
        
def list_item_tagger(block):
    block_lines = block.split('\n')
    stripped_block_lines = []
    final_nodes = []
    for line in block_lines:
        lines = line.split(' ', 1)
        stripped_block_lines.append(lines[1].strip())
    for line in stripped_block_lines:
        final_nodes.append(ParentNode('li', text_to_children(line)))
    return final_nodes
