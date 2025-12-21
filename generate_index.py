import os
import re

# Configuration
DESIGNS_DIR = "designs"
OUTPUT_FILE = "index.html"
README_FILE = "README.md"

def get_metadata(html_path):
    """Extracts title and a custom description comment from HTML."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Find <title>Text</title>
        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "Untitled Design"
        
        # Find desc_match = re.search(r'', content)
        # FIX: Ensure desc_match is checked properly
        description = desc_match.group(1).strip() if desc_match else "No description provided."
        
        return title, description
    except Exception as e:
        return "Error Reading Title", str(e)

def update_readme(links_markdown):
    """Replaces content between two markers in README.md."""
    start_marker = ""
    end_marker = ""
    
    if not os.path.exists(README_FILE):
        return

    with open(README_FILE, 'r', encoding='utf-8') as f:
        readme_content = f.read()

    # Regex to find everything between markers
    pattern = f"{start_marker}.*?{end_marker}"
    replacement = f"{start_marker}\n{links_markdown}\n{end_marker}"
    
    new_content = re.sub(pattern, replacement, readme_content, flags=re.DOTALL)
    
    with open(README_FILE, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    if not os.path.exists(DESIGNS_DIR):
        print(f"Directory {DESIGNS_DIR} not found.")
        return

    html_list_items = ""
    markdown_list_items = ""
    
    # Get all subdirectories in the designs folder
    folders = sorted([f for f in os.listdir(DESIGNS_DIR) if os.path.isdir(os.path.join(DESIGNS_DIR, f))])

    for folder in folders:
        path = f"{DESIGNS_DIR}/{folder}/index.html"
        if os.path.exists(path):
            title, desc = get_metadata(path)
            
            # URL relative to root
            url = f"{DESIGNS_DIR}/{folder}/index.html"
            
            # For the website (index.html)
            html_list_items += f'<li><a href="{url}">{title}</a><p>{desc}</p></li>\n'
            
            # For the README.md
            markdown_list_items += f"* [{title}]({url}) - {desc}\n"

    # Full HTML template for the root index.html
    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Design Gallery</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 40px auto; padding: 0 20px; color: #24292e; }}
        h1 {{ border-bottom: 1px solid #eaecef; padding-bottom: 0.3em; }}
        ul {{ list-style: none; padding: 0; }}
        li {{ margin-bottom: 20px; padding: 15px; border: 1px solid #e1e4e8; border-radius: 6px; }}
        li:hover {{ background-color: #f6f8fa; }}
        a {{ font-weight: 600; color: #0366d6; text-decoration: none; font-size: 1.25rem; }}
        a:hover {{ text-decoration: underline; }}
        p {{ margin: 5px 0 0; color: #586069; }}
    </style>
</head>
<body>
    <h1>Design Explorations</h1>
    <ul>
        {html_list_items}
    </ul>
</body>
</html>"""

    # Write the web index
    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write(full_html)

    # Update the README
    update_readme(markdown_list_items)
    print("Successfully updated index.html and README.md")

if __name__ == "__main__":
    main()
