import os
import re
from datetime import datetime
from html import escape

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
        
        # Find <!-- description: ... -->
        desc_match = re.search(r'<!--\s*description:\s*(.*?)\s*-->', content, re.IGNORECASE)
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
    design_count = 0
    
    folders = sorted([f for f in os.listdir(DESIGNS_DIR) if os.path.isdir(os.path.join(DESIGNS_DIR, f))])

    for folder in folders:
        path = f"{DESIGNS_DIR}/{folder}/index.html"
        if os.path.exists(path):
            title, desc = get_metadata(path)
            url = f"{DESIGNS_DIR}/{folder}/index.html"
            safe_title = escape(title)
            safe_desc = escape(desc)
            safe_url = escape(url, quote=True)
            html_list_items += (
                f'<li><a href="{safe_url}"><span>{safe_title}</span>'
                f'<span aria-hidden="true">↗</span></a><p>{safe_desc}</p></li>\n'
            )
            markdown_list_items += f"* [{title}]({url}) - {desc}\n"
            design_count += 1

    # Generate timestamp
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Design Gallery</title>
    <style>
        :root {{
            color-scheme: light;
            --bg: #f4f3ef;
            --surface: rgba(255, 255, 255, 0.86);
            --surface-strong: #ffffff;
            --border: rgba(15, 23, 42, 0.1);
            --border-strong: rgba(15, 23, 42, 0.16);
            --text: #111827;
            --muted: #5b6472;
            --accent: #5b6cff;
            --accent-soft: rgba(91, 108, 255, 0.12);
            --shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{
            min-height: 100%;
            background:
                radial-gradient(circle at top left, rgba(91, 108, 255, 0.18), transparent 28%),
                radial-gradient(circle at top right, rgba(14, 165, 233, 0.14), transparent 26%),
                linear-gradient(180deg, #fbfaf7 0%, var(--bg) 100%);
        }}

        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; 
            line-height: 1.6; 
            max-width: 1120px; 
            margin: 0 auto; 
            padding: 48px 24px 96px;
            color: var(--text);
            min-height: 100vh;
        }}

        .shell {{
            position: relative;
        }}

        .hero {{
            position: relative;
            overflow: hidden;
            margin-bottom: 32px;
            padding: 36px;
            border: 1px solid var(--border);
            border-radius: 28px;
            background: linear-gradient(145deg, rgba(255, 255, 255, 0.92), rgba(255, 255, 255, 0.72));
            box-shadow: var(--shadow);
            backdrop-filter: blur(18px);
        }}

        .hero::before {{
            content: "";
            position: absolute;
            inset: auto -80px -120px auto;
            width: 260px;
            height: 260px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(91, 108, 255, 0.22), transparent 70%);
            pointer-events: none;
        }}

        .eyebrow {{
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
            padding: 8px 14px;
            border-radius: 999px;
            background: var(--accent-soft);
            color: var(--accent);
            font-size: 0.78rem;
            font-weight: 600;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .eyebrow strong {{
            color: var(--text);
        }}

        h1 {{
            max-width: 11ch;
            font-size: clamp(3rem, 7vw, 5.5rem);
            line-height: 0.95;
            letter-spacing: -0.06em;
            font-weight: 700;
            margin-bottom: 18px;
        }}

        .hero p {{
            max-width: 58ch;
            color: var(--muted);
            font-size: 1.02rem;
            margin: 0;
        }}

        .hero-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 24px;
        }}

        .hero-meta span {{
            display: inline-flex;
            align-items: center;
            padding: 8px 12px;
            border: 1px solid var(--border);
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.74);
            color: var(--muted);
            font-size: 0.9rem;
        }}

        ul {{
            list-style: none; 
            padding: 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 18px;
        }}

        li {{
            position: relative;
            min-height: 100%;
        }}

        li::before {{
            content: "";
            position: absolute;
            inset: 0;
            border-radius: 22px;
            border: 1px solid transparent;
            background: linear-gradient(135deg, rgba(91, 108, 255, 0.14), rgba(14, 165, 233, 0.06)) border-box;
            opacity: 0;
            transition: opacity 0.25s ease;
            pointer-events: none;
        }}

        li:hover::before {{
            opacity: 1;
        }}

        a {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            min-height: 100%;
            padding: 22px 24px 78px;
            border: 1px solid var(--border);
            border-radius: 22px;
            background: linear-gradient(180deg, var(--surface-strong), var(--surface));
            box-shadow: 0 12px 30px rgba(15, 23, 42, 0.05);
            color: var(--text);
            text-decoration: none;
            transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
            font-size: 1.15rem;
            font-weight: 600;
            letter-spacing: -0.03em;
        }}

        a span:last-child {{
            flex-shrink: 0;
            margin-left: 12px;
            color: var(--accent);
            font-size: 1.1rem;
        }}

        a:hover {{
            transform: translateY(-3px);
            border-color: var(--border-strong);
            box-shadow: 0 18px 36px rgba(15, 23, 42, 0.08);
        }}

        li p {{
            position: absolute;
            inset: auto 24px 24px;
            color: var(--muted);
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        footer {{ 
            margin-top: 48px;
            padding-top: 24px;
            font-size: 0.82rem;
            color: var(--muted);
            text-align: left;
            border-top: 1px solid var(--border);
        }}

        @media (max-width: 640px) {{
            body {{
                padding: 24px 16px 72px;
            }}

            .hero {{
                padding: 24px;
                border-radius: 24px;
            }}

            ul {{
                grid-template-columns: 1fr;
            }}

            a {{
                padding: 20px 20px 76px;
                border-radius: 20px;
            }}

            li p {{
                inset-inline: 20px;
                bottom: 20px;
            }}
        }}
    </style>
</head>
<body>
    <main class="shell">
        <section class="hero">
            <div class="eyebrow"><span>HTML Concepts</span><strong>{design_count} curated experiments</strong></div>
            <h1>Design explorations with more personality.</h1>
            <p>Browse a growing set of self-contained HTML and CSS concepts—from editorial layouts and retro interfaces to futuristic storytelling and interactive timelines.</p>
            <div class="hero-meta">
                <span>Static HTML showcase</span>
                <span>Fast to open, easy to remix</span>
            </div>
        </section>
        <ul>
            {html_list_items}
        </ul>
        <footer>
            Last built on: {now} (UTC)
        </footer>
    </main>
</body>
</html>"""

    with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
        f.write(full_html)

    update_readme(markdown_list_items)
    print(f"Successfully updated at {now}")

if __name__ == "__main__":
    main()
