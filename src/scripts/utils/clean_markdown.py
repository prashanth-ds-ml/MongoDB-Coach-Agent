import os
import re
import glob

def clean_markdown_tables(text):
    """Converts simple HTML tables into Markdown tables."""
    def repl_table(match):
        table_html = match.group(0)
        
        # Extract rows
        trs = re.findall(r'<tr.*?>(.*?)</tr>', table_html, re.DOTALL | re.IGNORECASE)
        if not trs: 
            return table_html
        
        md_lines = []
        for i, tr in enumerate(trs):
            # Extract cells (th or td)
            cells = re.findall(r'<(th|td).*?>(.*?)</\1>', tr, re.DOTALL | re.IGNORECASE)
            
            row_data = []
            for tag, content in cells:
                # Clean cell content: replace newlines with spaces and strip
                cleaned = re.sub(r'\s+', ' ', content).strip()
                row_data.append(cleaned)
                
            if row_data:
                md_lines.append('| ' + ' | '.join(row_data) + ' |')
                if i == 0: # Add header separator after first row
                    md_lines.append('| ' + ' | '.join(['---'] * len(row_data)) + ' |')
                
        return '\n'.join(md_lines) + '\n'

    # Find all <table>...</table>
    return re.sub(r'<table.*?>.*?</table>', repl_table, text, flags=re.DOTALL | re.IGNORECASE)

def clean_markdown_file(filepath, output_dir):
    """Applies the cleaning pipeline to a single markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    # 1. Remove intro boilerplate
    text = re.sub(r'This page documents a \[.*?\]\(.*?\) method\. To see the equivalent method in a MongoDB driver, see the corresponding page for your programming language:', '', text, flags=re.DOTALL)

    # 2. Remove Compatibility section entirely
    text = re.sub(r'## Compatibility.*?## Syntax', '## Syntax', text, flags=re.DOTALL)

    # 3. Remove Learn More section at the bottom
    text = re.sub(r'## Learn More.*', '', text, flags=re.DOTALL)

    # 4. Strip Links but keep Anchor Text
    # e.g., [write concern](https://...) -> write concern
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # 5. Convert HTML Tables to Markdown Tables
    text = clean_markdown_tables(text)

    # 6. Fix formatting artifacts
    # Fix missing spaces like "insertMany()This" -> "insertMany() This"
    text = re.sub(r'(\w\(\))([A-Z])', r'\1 \2', text)
    # Collapse multiple blank lines into max 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Ensure no leading/trailing whitespace
    text = text.strip() + '\n'

    # Save to output directory
    filename = os.path.basename(filepath)
    output_path = os.path.join(output_dir, filename)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(text)
        
    return output_path

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    raw_dir = os.path.join(base_dir, 'data', 'raw_markdowns')
    cleaned_dir = os.path.join(base_dir, 'data', 'cleaned_markdowns')
    
    # Create output directory if it doesn't exist
    os.makedirs(cleaned_dir, exist_ok=True)
    
    md_files = glob.glob(os.path.join(raw_dir, '*.md'))
    
    if not md_files:
        print(f"No markdown files found in {raw_dir}")
        return
        
    print(f"Found {len(md_files)} files. Starting cleaning pipeline...")
    
    for file in md_files:
        out_path = clean_markdown_file(file, cleaned_dir)
        print(f"Cleaned: {os.path.basename(file)} -> {out_path}")
        
    print(f"\nSuccessfully cleaned {len(md_files)} files. Saved to {cleaned_dir}")

if __name__ == "__main__":
    main()
