#!/usr/bin/env python3
"""
Script to generate HTML documentation from Markdown files.
"""

import os
import sys
import markdown
import shutil
from pathlib import Path


def generate_html(markdown_file, output_dir):
    """
    Generate HTML from a Markdown file.
    
    Args:
        markdown_file: Path to the Markdown file
        output_dir: Directory to write the HTML file to
    """
    # Read the Markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Convert Markdown to HTML
    html_content = markdown.markdown(
        md_content,
        extensions=['tables', 'fenced_code', 'codehilite', 'toc']
    )
    
    # Create HTML file with basic styling
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Task Manager Documentation</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
        }}
        h1, h2, h3, h4, h5, h6 {{
            margin-top: 24px;
            margin-bottom: 16px;
            font-weight: 600;
            line-height: 1.25;
        }}
        h1 {{
            font-size: 2em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        h2 {{
            font-size: 1.5em;
            border-bottom: 1px solid #eaecef;
            padding-bottom: 0.3em;
        }}
        a {{
            color: #0366d6;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
        pre {{
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 16px;
            overflow: auto;
        }}
        code {{
            background-color: #f6f8fa;
            border-radius: 3px;
            padding: 0.2em 0.4em;
            font-family: SFMono-Regular, Consolas, "Liberation Mono", Menlo, monospace;
        }}
        pre code {{
            background-color: transparent;
            padding: 0;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin-bottom: 16px;
        }}
        table, th, td {{
            border: 1px solid #dfe2e5;
        }}
        th, td {{
            padding: 8px 16px;
            text-align: left;
        }}
        tr:nth-child(even) {{
            background-color: #f6f8fa;
        }}
        .navigation {{
            background-color: #f6f8fa;
            padding: 10px;
            margin-bottom: 20px;
            border-radius: 3px;
        }}
    </style>
</head>
<body>
    <div class="navigation">
        <a href="index.html">Home</a> |
        <a href="installation.html">Installation</a> |
        <a href="usage/cli.html">CLI Usage</a> |
        <a href="usage/web.html">Web Usage</a> |
        <a href="api/models.html">Models API</a> |
        <a href="api/services.html">Services API</a> |
        <a href="api/utils.html">Utils API</a> |
        <a href="development.html">Development</a> |
        <a href="contributing.html">Contributing</a>
    </div>
    {html_content}
</body>
</html>
"""
    
    # Determine the output file path
    rel_path = os.path.relpath(markdown_file, os.path.dirname(os.path.dirname(markdown_file)))
    output_file = os.path.join(output_dir, os.path.splitext(rel_path)[0] + '.html')
    
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated {output_file}")


def main():
    """Main function to generate HTML documentation."""
    # Get the docs directory
    docs_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create the output directory
    output_dir = os.path.join(docs_dir, 'html')
    os.makedirs(output_dir, exist_ok=True)
    
    # Find all Markdown files in the docs directory
    markdown_files = []
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                markdown_files.append(os.path.join(root, file))
    
    # Generate HTML for each Markdown file
    for markdown_file in markdown_files:
        generate_html(markdown_file, output_dir)
    
    print(f"\nDocumentation generated in {output_dir}")
    print("Open index.html in your browser to view the documentation.")


if __name__ == "__main__":
    main()