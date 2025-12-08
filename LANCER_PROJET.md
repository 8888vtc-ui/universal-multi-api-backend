# 🚀 Comment Lancer le Projet

## Méthode 1: Script Automatique (Recommandé)

### Windows (PowerShell)
```powershell
.\START_ALL.ps1
```

### Windows (CMD)
```cmd
START_ALL.bat
```

## Méthode 2: Lancement Manuel

### Terminal 1 - Backend
```bash
cd backend
python main.py
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install    # Première fois uniquement
npm run dev
```

## 📍 URLs

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **Documentation** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/api/health |

## ✅ Vérification

1. Ouvrir http://localhost:3000
2. Le dashboard doit afficher "70+ APIs"
3. Tester le chat IA
4. Explorer les APIs

## 🔧 Dépannage

### Le frontend ne démarre pas
```bash
cd frontend
rm -rf node_modules
npm install
npm run dev
```

### Le backend ne démarre pas
```bash
cd backend
pip install -r requirements.txt
python main.py
```

### Erreur CORS
Le fichier `next.config.js` configure automatiquement le proxy vers le backend.

## 🎯 Prochaines Étapes

1. **Local** : Tester toutes les fonctionnalités
2. **Déploiement** : Configurer le serveur de production
3. **Domaine** : Ajouter un nom de domaine personnalisé






