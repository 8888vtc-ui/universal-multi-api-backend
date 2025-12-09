"""
Script pour corriger automatiquement les conflits Git dans les fichiers Python
Supprime les marqueurs de conflit Git et garde la version la plus récente
"""
import os
import re
from pathlib import Path

def fix_git_conflicts_in_file(file_path: Path) -> bool:
    """Corrige les conflits Git dans un fichier"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern pour détecter les conflits Git
        conflict_pattern = r'.*?'
        
        if re.search(conflict_pattern, content, re.DOTALL):
            # Remplacer par rien (supprimer le conflit)
            # On garde la version après ======= (stashed changes)
            new_content = re.sub(
                r'\s*',
                '',
                content,
                flags=re.DOTALL
            )
            new_content = re.sub(
                r'\s*',
                '',
                new_content,
                flags=re.DOTALL
            )
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Corrigé: {file_path}")
            return True
        return False
    except Exception as e:
        print(f"❌ Erreur avec {file_path}: {e}")
        return False

def main():
    """Corrige tous les conflits Git dans le projet"""
    backend_dir = Path(__file__).parent.parent
    
    # Fichiers Python uniquement
    python_files = list(backend_dir.rglob("*.py"))
    
    fixed_count = 0
    for py_file in python_files:
        if fix_git_conflicts_in_file(py_file):
            fixed_count += 1
    
    print(f"\n✅ {fixed_count} fichiers corrigés")

if __name__ == "__main__":
    main()

