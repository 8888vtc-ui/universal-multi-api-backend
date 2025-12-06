
import os
import subprocess
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # backend/
FRONTEND_DATA = os.path.join(os.path.dirname(BASE_DIR), 'frontend', 'data')
TS_FILE = os.path.join(FRONTEND_DATA, 'seo-articles.ts')
JS_FILE = os.path.join(FRONTEND_DATA, 'seo-articles.js')
MIGRATE_SCRIPT = os.path.join(FRONTEND_DATA, 'migrate_js.js')
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'articles')

def convert_ts_to_js():
    print(f"Reading {TS_FILE}...")
    with open(TS_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Simple conversion
    content = content.replace('export const SEO_ARTICLES: Record<string, {', 'const SEO_ARTICLES = {')
    content = content.replace('export const SEO_ARTICLES', 'module.exports')
    # Remove typing stuff loosely
    # content = re.sub(r':\s*[A-Z][a-zA-Z<>]+', '', content) # Too risky
    
    # Just standard replacement of the export line should be enough if valid JS inside
    # The file has `import { ARTICLES }` too maybe? Step 300 says line 1: `import { ARTICLES } from './articles'`
    # We need to handle that import too or remove it if not used in the SEO object?
    # SEO_ARTICLES seems self contained?
    # Step 300: `export const SEO_ARTICLES: Record<...> = { ... }`
    
    # Remove imports and interfaces
    lines = content.split('\n')
    new_lines = []
    
    found_export = False
    seeking_start_brace = False
    
    for line in lines:
        stripped = line.strip()
        
        # Skip imports and interfaces (if not inside export)
        if not found_export and not seeking_start_brace:
            if stripped.startswith('import ') or stripped.startswith('interface '):
                continue
            # Also skip lines that might be inside interface if we want to be safe, 
            # but usually interfaces are contiguous blocks at top.
            # Assuming standard structure.
        
        if 'export const SEO_ARTICLES' in line:
            seeking_start_brace = True
            continue
            
        if seeking_start_brace:
            if '= {' in line or line.strip().endswith('{'):
                new_lines.append('module.exports = {')
                seeking_start_brace = False
                found_export = True
            continue
            
        if not found_export:
            continue
            
        # We are inside the object or after
        new_lines.append(line)
        
    js_content = '\n'.join(new_lines)
    
    # Handle the type annotation on the export line if it wasn't valid JS
    # "module.exports = {" is valid.
    
    with open(JS_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"Saved {JS_FILE}")

def create_migration_script():
    script = f"""
const fs = require('fs');
const path = require('path');
const OUTPUT_DIR = String.raw`{OUTPUT_DIR}`;

if (!fs.existsSync(OUTPUT_DIR)) {{
    fs.mkdirSync(OUTPUT_DIR, {{ recursive: true }});
}}

try {{
    const articles = require('./seo-articles.js');
    console.log(`Loaded articles. Keys: ${{Object.keys(articles).length}}`);
    
    let count = 0;
    for (const [slug, article] of Object.entries(articles)) {{
        const filePath = path.join(OUTPUT_DIR, slug + '.json');
        const data = {{ slug, ...article }};
        fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
        count++;
    }}
    console.log(`Migrated ${{count}} articles.`);
}} catch (e) {{
    console.error("Error migrating:", e);
    process.exit(1);
}}
"""
    with open(MIGRATE_SCRIPT, 'w', encoding='utf-8') as f:
        f.write(script)
    print(f"Saved {MIGRATE_SCRIPT}")

def run_migration():
    print("Running migration...")
    subprocess.run(['node', MIGRATE_SCRIPT], check=True, cwd=FRONTEND_DATA)

def cleanup():
    if os.path.exists(JS_FILE):
        os.remove(JS_FILE)
    if os.path.exists(MIGRATE_SCRIPT):
        os.remove(MIGRATE_SCRIPT)
    print("Cleanup done.")

if __name__ == "__main__":
    try:
        convert_ts_to_js()
        create_migration_script()
        run_migration()
        cleanup()
        print("✅ Migration Success")
    except Exception as e:
        print(f"❌ Migration Failed: {e}")
