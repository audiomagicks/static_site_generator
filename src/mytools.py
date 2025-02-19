from textnode import *
from htmlnode import *
import re

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
            for image in extracted_images:
                count = 1
                image_alt = image[0]
                image_link = image[1]
                sections = original_text.split(f"![{image_alt}]({image_link})", 1)
                before_image = sections[0]
                after_image = sections[1]
                if count == len(extracted_images):
                    formatted_nodes.append(TextNode(before_image, TextType.TEXT))
                    formatted_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                    formatted_nodes.append(TextNode(after_image, TextType.TEXT))
                else:
                    count += 1
                    formatted_nodes.append(TextNode(before_image, TextType.TEXT))
                    formatted_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
                    original_text = after_image

            new_nodes.extend(formatted_nodes)
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
                    formatted_nodes.append(TextNode(before_link, TextType.TEXT))
                    formatted_nodes.append(TextNode(link_alt, TextType.LINK, link_link))
                    formatted_nodes.append(TextNode(after_link, TextType.TEXT))
                else:
                    count += 1
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