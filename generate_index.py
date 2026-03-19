import os
import re
from datetime import datetime
from html import escape

# Configuration
DESIGNS_DIR = "designs"
OUTPUT_FILE = "index.html"
README_FILE = "README.md"
DISPLAY_ORDER = [
    "tech",
    "3d-graphics",
    "ai-galaxy",
    "ai-history",
    "cybersecurity",
    "japan",
    "journalism",
    "modern",
    "pantheon",
    "retro",
    "startup",
    "worldbuilding",
]
DISPLAY_OVERRIDES = {
    "tech": {
        "title": "Static HTML showcase",
        "description": "Fast to open, easy to remix",
    },
    "startup": {
        "description": "CSS: AI Tech Companies",
    },
}


def get_metadata(html_path):
    """Extracts title and a custom description comment from HTML."""
    try:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        title_match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
        title = title_match.group(1).strip() if title_match else "Untitled Design"

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

    folders = sorted(
        [f for f in os.listdir(DESIGNS_DIR) if os.path.isdir(os.path.join(DESIGNS_DIR, f))]
    )
    ordered_folders = [folder for folder in DISPLAY_ORDER if folder in folders]
    ordered_folders.extend(folder for folder in folders if folder not in DISPLAY_ORDER)

    for folder in ordered_folders:
        path = f"{DESIGNS_DIR}/{folder}/index.html"
        if os.path.exists(path):
            title, desc = get_metadata(path)
            override = DISPLAY_OVERRIDES.get(folder, {})
            title = override.get("title", title)
            desc = override.get("description", desc)
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

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    page_title = f"{design_count} Curated Experiments — Design Bureau"
    page_description = (
        f"Browse {design_count} self-contained HTML and CSS design experiments—from "
        "editorial layouts to futuristic storytelling and interactive timelines."
    )

    full_html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">
    <title>{page_title}</title>
    <meta name=\"description\" content=\"{page_description}\">
    <meta name=\"author\" content=\"Design Bureau\">
    <meta property=\"og:title\" content=\"{page_title}\">
    <meta property=\"og:description\" content=\"Design explorations with more personality. Cybersecurity meets architecture.\">
    <meta property=\"og:type\" content=\"website\">
    <meta name=\"twitter:card\" content=\"summary_large_image\">
    <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
    <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
    <link href=\"https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Space+Grotesk:wght@400;500;700&display=swap\" rel=\"stylesheet\">
    <style>
        :root {{
            color-scheme: light dark;
            --background: 0 0% 100%;
            --foreground: 0 0% 0%;
            --card: 0 0% 100%;
            --card-foreground: 0 0% 0%;
            --secondary: 0 0% 96%;
            --muted-foreground: 0 0% 40%;
            --accent: 142 100% 45%;
            --accent-foreground: 0 0% 0%;
            --border: 0 0% 0%;
            --border-subtle: 0 0% 84%;
            --surface-shadow: 0 24px 60px hsl(0 0% 0% / 0.08);
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --background: 0 0% 3%;
                --foreground: 0 0% 95%;
                --card: 0 0% 3%;
                --card-foreground: 0 0% 95%;
                --secondary: 0 0% 12%;
                --muted-foreground: 0 0% 60%;
                --border: 0 0% 20%;
                --border-subtle: 0 0% 22%;
                --surface-shadow: 0 28px 80px hsl(0 0% 0% / 0.4);
            }}
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{
            min-height: 100%;
            background: linear-gradient(180deg, hsl(var(--background)) 0%, hsl(var(--secondary)) 100%);
        }}

        body {{
            font-family: \"Space Grotesk\", -apple-system, BlinkMacSystemFont, \"Segoe UI\", sans-serif;
            line-height: 1.6;
            max-width: 1120px;
            margin: 0 auto;
            padding: 48px 24px 96px;
            color: hsl(var(--foreground));
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
            border: 2px solid hsl(var(--border));
            border-radius: 0;
            background: linear-gradient(135deg, hsl(var(--accent) / 0.12), transparent 38%), hsl(var(--card));
            box-shadow: var(--surface-shadow);
        }}

        .hero::before {{
            content: \"\";
            position: absolute;
            inset: 0;
            background: linear-gradient(90deg, transparent calc(100% - 1px), hsl(var(--border-subtle)) 0),
                        linear-gradient(transparent calc(100% - 1px), hsl(var(--border-subtle)) 0);
            background-size: 18px 18px;
            opacity: 0.35;
            pointer-events: none;
        }}

        .eyebrow,
        .hero-meta span,
        footer {{
            font-family: \"JetBrains Mono\", \"SFMono-Regular\", Consolas, monospace;
        }}

        .eyebrow {{
            position: relative;
            z-index: 1;
            display: inline-flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
            padding: 8px 12px;
            border: 1px solid hsl(var(--border));
            background: hsl(var(--background));
            color: hsl(var(--accent-foreground));
            font-size: 0.78rem;
            font-weight: 500;
            letter-spacing: 0.08em;
            text-transform: uppercase;
        }}

        .eyebrow strong {{
            color: hsl(var(--accent));
        }}

        h1 {{
            position: relative;
            z-index: 1;
            max-width: 12ch;
            font-size: clamp(3rem, 7vw, 5.25rem);
            line-height: 0.92;
            letter-spacing: -0.06em;
            font-weight: 700;
            margin-bottom: 18px;
        }}

        .hero p {{
            position: relative;
            z-index: 1;
            max-width: 58ch;
            color: hsl(var(--muted-foreground));
            font-size: 1.02rem;
            margin: 0;
        }}

        .hero-meta {{
            position: relative;
            z-index: 1;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            margin-top: 24px;
        }}

        .hero-meta span {{
            display: inline-flex;
            align-items: center;
            padding: 8px 12px;
            border: 1px solid hsl(var(--border));
            background: hsl(var(--background));
            color: hsl(var(--muted-foreground));
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
            content: \"\";
            position: absolute;
            inset: 0;
            border: 2px solid hsl(var(--accent));
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
            border: 2px solid hsl(var(--border));
            background: hsl(var(--card));
            box-shadow: 8px 8px 0 hsl(var(--border));
            color: hsl(var(--card-foreground));
            text-decoration: none;
            transition: transform 0.22s ease, box-shadow 0.22s ease;
            font-size: 1.15rem;
            font-weight: 600;
            letter-spacing: -0.03em;
        }}

        a span:last-child {{
            flex-shrink: 0;
            margin-left: 12px;
            color: hsl(var(--accent));
            font-size: 1.1rem;
        }}

        a:hover {{
            transform: translate(-3px, -3px);
            box-shadow: 11px 11px 0 hsl(var(--accent));
        }}

        li p {{
            position: absolute;
            inset: auto 24px 24px;
            color: hsl(var(--muted-foreground));
            font-size: 0.95rem;
            line-height: 1.6;
        }}

        footer {{
            margin-top: 48px;
            padding-top: 24px;
            font-size: 0.82rem;
            color: hsl(var(--muted-foreground));
            text-align: left;
            border-top: 2px solid hsl(var(--border));
        }}

        @media (max-width: 640px) {{
            body {{
                padding: 24px 16px 72px;
            }}

            .hero {{
                padding: 24px;
            }}

            ul {{
                grid-template-columns: 1fr;
            }}

            a {{
                padding: 20px 20px 76px;
            }}

            li p {{
                inset-inline: 20px;
                bottom: 20px;
            }}
        }}
    </style>
</head>
<body>
    <main class=\"shell\">
        <section class=\"hero\">
            <div class=\"eyebrow\"><span>HTML Concepts</span><strong>{design_count} curated experiments</strong></div>
            <h1>{design_count} curated experiments.</h1>
            <p>{page_description}</p>
            <div class=\"hero-meta\">
                <span>Design Bureau</span>
                <span>Cybersecurity meets architecture</span>
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
