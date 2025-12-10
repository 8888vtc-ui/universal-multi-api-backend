"""
Script de migration automatique - NETTOYAGE COMPLET
Remplace TOUS les httpx.AsyncClient par http_client avec DNS personnalisé
"""
import re
import os
from pathlib import Path

def migrate_file(file_path: Path) -> tuple:
    """Migre un fichier Python vers http_client"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        changes = []
        
        # Skip si déjà migré ou si c'est http_client lui-même
        if 'http_client_wrapper' in str(file_path) or 'http_client.py' == file_path.name:
            return False, "Skipped (http_client file)", []
        
        # 1. Vérifier si le fichier utilise httpx.AsyncClient
        if 'httpx.AsyncClient' not in content and 'AsyncClient' not in content:
            return False, "No AsyncClient found", []
        
        # 2. Ajouter l'import http_client si pas présent
        if 'from services.http_client import http_client' not in content:
            # Trouver où ajouter l'import (après les autres imports)
            import_section = re.search(r'^((?:import .*\n|from .* import .*\n)+)', content, re.MULTILINE)
            if import_section:
                insert_pos = import_section.end()
                content = (
                    content[:insert_pos] + 
                    'from services.http_client import http_client\n' + 
                    content[insert_pos:]
                )
                changes.append("Added http_client import")
        
        # 3. Pattern: async with httpx.AsyncClient(...) as client: -> supprimer et dé-indenter
        # On va traiter ligne par ligne pour gérer l'indentation
        lines = content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            
            # Détecter le pattern "async with httpx.AsyncClient"
            match = re.match(r'^(\s*)async with httpx\.AsyncClient\([^)]*\) as (\w+):', line)
            if match:
                base_indent = match.group(1)
                client_var = match.group(2)
                inner_indent = base_indent + '    '
                
                changes.append(f"Replaced async with block (client={client_var})")
                
                # Collecter et dé-indenter le bloc interne
                i += 1
                while i < len(lines):
                    inner_line = lines[i]
                    
                    # Fin du bloc si on revient à l'indentation de base ou moins
                    if inner_line.strip() and not inner_line.startswith(inner_indent):
                        break
                    
                    # Dé-indenter de 4 espaces
                    if inner_line.startswith(inner_indent):
                        dedented = base_indent + inner_line[len(inner_indent):]
                    else:
                        dedented = inner_line
                    
                    # Remplacer client.xxx par http_client.xxx
                    dedented = re.sub(rf'\b{client_var}\.get\(', 'http_client.get(', dedented)
                    dedented = re.sub(rf'\b{client_var}\.post\(', 'http_client.post(', dedented)
                    dedented = re.sub(rf'\b{client_var}\.put\(', 'http_client.put(', dedented)
                    dedented = re.sub(rf'\b{client_var}\.delete\(', 'http_client.delete(', dedented)
                    
                    new_lines.append(dedented)
                    i += 1
                
                continue
            
            new_lines.append(line)
            i += 1
        
        content = '\n'.join(new_lines)
        
        # 4. Remplacer les client.xxx restants (au cas où)
        content = re.sub(r'\bclient\.get\(', 'http_client.get(', content)
        content = re.sub(r'\bclient\.post\(', 'http_client.post(', content)
        
        # 5. Nettoyer l'import httpx si plus utilisé
        if 'httpx.' not in content.replace('httpx.Response', '') and 'import httpx' in content:
            # Garder httpx.Response, supprimer le reste
            pass  # On garde l'import pour httpx.Response si utilisé
        
        if content != original:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return True, f"Migrated ({len(changes)} changes)", changes
        
        return False, "No changes needed", []
        
    except Exception as e:
        return False, f"Error: {e}", []


def main():
    """Migrer tous les fichiers"""
    base_dir = Path(__file__).parent.parent
    
    # Tous les fichiers Python dans services/external_apis
    api_dir = base_dir / "services" / "external_apis"
    
    if not api_dir.exists():
        print(f"Directory not found: {api_dir}")
        return
    
    files = list(api_dir.rglob("*.py"))
    
    # Exclure __pycache__ et __init__.py
    files = [f for f in files if '__pycache__' not in str(f)]
    
    print(f"=" * 60)
    print(f"MIGRATION HTTP_CLIENT - {len(files)} fichiers à traiter")
    print(f"=" * 60)
    
    migrated = []
    skipped = []
    errors = []
    
    for f in sorted(files):
        rel_path = f.relative_to(base_dir)
        success, msg, changes = migrate_file(f)
        
        if success:
            print(f"✅ {rel_path}: {msg}")
            migrated.append((rel_path, changes))
        elif "Error" in msg:
            print(f"❌ {rel_path}: {msg}")
            errors.append(rel_path)
        else:
            print(f"⏭️  {rel_path}: {msg}")
            skipped.append(rel_path)
    
    print(f"\n" + "=" * 60)
    print(f"RÉSUMÉ")
    print(f"=" * 60)
    print(f"✅ Migrés: {len(migrated)}")
    print(f"⏭️  Ignorés: {len(skipped)}")
    print(f"❌ Erreurs: {len(errors)}")
    
    if migrated:
        print(f"\nFichiers migrés:")
        for path, changes in migrated:
            print(f"  - {path}")
            for c in changes:
                print(f"      • {c}")


if __name__ == "__main__":
    main()
