import os
from pathlib import Path
from markdown_blocks import markdown_to_html_node



def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    # List all entries in the current directory
    for entry in os.listdir(dir_path_content):
        # Construct full path
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)        
        # Check if it's a directory
        if os.path.isfile(from_path):
            dest_path = Path(dest_path).with_suffix(".html")
            # Recursively crawl this directory
            generate_page(from_path, template_path, dest_path)
        else:
            generate_pages_recursive(from_path, template_path, dest_path)



def generate_page(from_path, template_path, dest_path):
    print(f" *  {from_path}{template_path} --> {dest_path}")

    f = open(from_path, "r")
    content = f.read()
    f.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(content)
    html = node.to_html()

    title = extract_title(content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)

def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")



    