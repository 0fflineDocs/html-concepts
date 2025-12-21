import os

# Configuration
DESIGNS_DIR = "designs"
OUTPUT_FILE = "index.html"

def generate_index():
    links_html = ""
    
    # Sort folders by name (or date)
    folders = sorted([f for f in os.listdir(DESIGNS_DIR) if os.path.isdir(os.path.join(DESIGNS_DIR, f))])

    for folder in folders:
        display_name = folder.replace("-", " ").title()
        path = f"{DESIGNS_DIR}/{folder}/index.html"
        links_html += f'<li><a href="{path}">{display_name}</a></li>\n'

    # The HTML template
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Design Gallery</title>
        <style>
            body {{ font-family: sans-serif; padding: 2rem; line-height: 1.6; }}
            ul {{ list-style: none; padding: 0; }}
            li {{ margin-bottom: 10px; border-bottom: 1px solid #eee; padding-bottom: 10px; }}
            a {{ text-decoration: none; color: #007bff; font-weight: bold; font-size: 1.2rem; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <h1>My Design Explorations</h1>
        <ul>
            {links_html}
        </ul>
    </body>
    </html>
    """

    with open(OUTPUT_FILE, "w") as f:
        f.write(html_content)

if __name__ == "__main__":
    generate_index()
