# 🔧 Configuration Git - Guide Complet

**Date** : Décembre 2024  
**Version** : 2.3.0

---

## 🚀 Initialisation Git

### 1. Initialiser le Dépôt

```bash
# Dans le répertoire racine du projet
cd "D:\moteur israelien"
git init
```

### 2. Configurer Git (si pas déjà fait)

```bash
git config --global user.name "Votre Nom"
git config --global user.email "votre.email@example.com"
```

### 3. Ajouter les Fichiers

```bash
# Vérifier les fichiers à ajouter
git status

# Ajouter tous les fichiers (sauf ceux dans .gitignore)
git add .

# Vérifier ce qui sera commité
git status
```

### 4. Premier Commit

```bash
git commit -m "Initial commit - Universal Multi-API Backend v2.3.0"
```

---

## 📦 Créer un Dépôt sur GitHub

### Option 1 : Via l'Interface Web

1. Aller sur [GitHub](https://github.com)
2. Cliquer sur "New repository"
3. Nommer le dépôt (ex: `universal-multi-api-backend`)
4. **Ne pas** initialiser avec README, .gitignore, ou licence
5. Cliquer sur "Create repository"

### Option 2 : Via GitHub CLI

```bash
# Installer GitHub CLI si nécessaire
# Puis:
gh repo create universal-multi-api-backend --public --source=. --remote=origin --push
```

---

## 🔗 Connecter le Dépôt Local à GitHub

### 1. Ajouter le Remote

```bash
# Remplacer par votre URL GitHub
git remote add origin https://github.com/VOTRE_USERNAME/universal-multi-api-backend.git

# Ou avec SSH
git remote add origin git@github.com:VOTRE_USERNAME/universal-multi-api-backend.git
```

### 2. Vérifier le Remote

```bash
git remote -v
```

### 3. Pousser le Code

```bash
# Pousser sur la branche main
git branch -M main
git push -u origin main
```

---

## 📋 Structure Recommandée des Commits

### Format des Messages

```
type(scope): description

[corps optionnel]

[footer optionnel]
```

### Types de Commits

- `feat`: Nouvelle fonctionnalité
- `fix`: Correction de bug
- `docs`: Documentation
- `style`: Formatage, point-virgule, etc.
- `refactor`: Refactoring
- `test`: Tests
- `chore`: Maintenance

### Exemples

```bash
git commit -m "feat(api): Ajout endpoint recherche universelle"
git commit -m "fix(auth): Correction expiration JWT"
git commit -m "docs: Mise à jour guide déploiement"
git commit -m "test: Ajout tests unitaires pour chat"
```

---

## 🌿 Gestion des Branches

### Branches Recommandées

```bash
# Branche principale
main (ou master)

# Branche de développement
develop

# Branches de fonctionnalités
feature/nom-fonctionnalite

# Branches de correction
fix/nom-bug

# Branches de release
release/v2.4.0
```

### Créer une Branche

```bash
# Créer et basculer
git checkout -b feature/nouvelle-api

# Ou avec Git 2.23+
git switch -c feature/nouvelle-api
```

### Pousser une Branche

```bash
git push -u origin feature/nouvelle-api
```

---

## 🔄 Workflow Recommandé

### 1. Travailler sur une Fonctionnalité

```bash
# Créer une branche
git checkout -b feature/ma-fonctionnalite

# Faire des modifications
# ...

# Commit
git add .
git commit -m "feat: Description de la fonctionnalité"

# Pousser
git push -u origin feature/ma-fonctionnalite
```

### 2. Merger dans Main

```bash
# Revenir sur main
git checkout main

# Mettre à jour
git pull origin main

# Merger la branche
git merge feature/ma-fonctionnalite

# Pousser
git push origin main
```

---

## 🔒 Sécurité - Fichiers à NE JAMAIS Commiter

### Fichiers Sensibles

- `.env` - Variables d'environnement
- `*.key`, `*.pem` - Clés privées
- `secrets/` - Dossiers de secrets
- `backend/data/*.db` - Bases de données (si contiennent des données sensibles)

### Vérifier avant de Commiter

```bash
# Voir ce qui sera commité
git status

# Voir les différences
git diff

# Vérifier les fichiers sensibles
git check-ignore -v .env
```

---

## 📝 .gitignore Configuré

Le fichier `.gitignore` est déjà configuré pour exclure :
- Fichiers Python (`__pycache__`, `*.pyc`)
- Environnements virtuels (`venv/`, `env/`)
- Variables d'environnement (`.env`)
- Bases de données (`*.db`, `*.sqlite`)
- Logs (`*.log`, `logs/`)
- Cache (`__pycache__`, `.pytest_cache/`)
- Fichiers IDE (`.vscode/`, `.idea/`)

---

## 🚀 Commandes Rapides

### Workflow Quotidien

```bash
# Voir le status
git status

# Ajouter les modifications
git add .

# Commit
git commit -m "Description des changements"

# Pousser
git push origin main

# Mettre à jour
git pull origin main
```

### Voir l'Historique

```bash
# Historique simple
git log --oneline

# Historique avec graph
git log --oneline --graph --all

# Derniers commits
git log -5
```

### Annuler des Modifications

```bash
# Annuler les modifications non commitées
git checkout -- fichier.py

# Annuler le dernier commit (garder les modifications)
git reset --soft HEAD~1

# Annuler le dernier commit (supprimer les modifications)
git reset --hard HEAD~1
```

---

## 🔐 Authentification GitHub

### Option 1 : HTTPS avec Token

1. Créer un Personal Access Token sur GitHub
2. Utiliser le token comme mot de passe

```bash
git remote set-url origin https://VOTRE_TOKEN@github.com/USERNAME/REPO.git
```

### Option 2 : SSH (Recommandé)

```bash
# Générer une clé SSH
ssh-keygen -t ed25519 -C "votre.email@example.com"

# Ajouter la clé à ssh-agent
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519

# Copier la clé publique
cat ~/.ssh/id_ed25519.pub

# Ajouter sur GitHub : Settings > SSH and GPG keys > New SSH key
```

---

## 📚 Documentation Git

### Ressources Utiles

- [Git Documentation](https://git-scm.com/doc)
- [GitHub Guides](https://guides.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)

---

## ✅ Checklist Initialisation

- [ ] Git initialisé (`git init`)
- [ ] `.gitignore` configuré
- [ ] Premier commit effectué
- [ ] Dépôt GitHub créé
- [ ] Remote ajouté
- [ ] Code poussé sur GitHub
- [ ] Branches configurées (main, develop)
- [ ] README.md à jour

---

## 🎯 Prochaines Étapes

1. ✅ Initialiser Git (FAIT avec ce guide)
2. ⏳ Créer le dépôt GitHub
3. ⏳ Pousser le code
4. ⏳ Configurer les branches
5. ⏳ Configurer CI/CD (optionnel)

---

**Bon développement ! 🚀**

*Dernière mise à jour : Décembre 2024 - v2.3.0*

