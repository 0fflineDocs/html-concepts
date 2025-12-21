import os
import re

DESIGNS_DIR = "designs"
INDEX_FILE = "index.html"
README_FILE = "README.md"

def get_metadata(html_path):
    """Extracts title and a custom description comment from HTML."""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Find <title>Text</title>
    title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    title = title_match.group(1) if title_match else "Untitled Design"
    
    # Find desc_match = re.search(r'', content)
    description = desc_match.group(1) if desc_match else "No description provided."
    
    return title, description

def update_readme(links_markdown):
    """Replaces content between two markers in README.md."""
    start_marker = ""
    end_marker = ""
    
    with open(README_FILE, 'r') as f:
        readme_content = f.read()

    pattern = f"{start_marker}.*?{end_marker}"
    replacement = f"{start_marker}\n{links_markdown}\n{end_marker}"
    
    new_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
    
    with open(README_FILE, 'w') as f:
        f.write(new_content)

def main():
    if not os.path.exists(DESIGNS_DIR):
        return

    html_list_items = ""
    markdown_list_items = ""
    
    folders = sorted([f for f in os.listdir(DESIGNS_DIR) if os.path.isdir(os.path.join(DESIGNS_DIR, f))])

    for folder in folders:
        path = f"{DESIGNS_DIR}/{folder}/index.html"
        if os.path.exists(path):
            title, desc = get_metadata(path)
            
            # For the website (index.html)
            html_list_items += f'<li><a href="{path}">{title}</a> - {desc}</li>\n'
            
            # For the README.md
            markdown_list_items += f"* [{title}]({path}) - {desc}\n"

    # Save index.html (the code from the previous step goes here)
    # ... [Insert the HTML template logic from the previous reply] ...

    # Update README
    update_readme(markdown_list_items)

if __name__ == "__main__":
    main()
