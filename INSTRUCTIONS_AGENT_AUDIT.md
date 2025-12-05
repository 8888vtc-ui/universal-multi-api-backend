# 🤖 Instructions pour Agent - Audit Complet

## Copier ce prompt pour l'agent :

---

```
Tu es un expert en architecture backend Python/FastAPI. Effectue un AUDIT COMPLET et CRITIQUE de ce projet backend multi-API.

## CONTEXTE
- Backend FastAPI avec 40+ APIs intégrées
- Système de fallback intelligent entre providers
- Services avancés : IA, Video, Assistant, Analytics
- Authentification JWT
- Cache Redis + Cache L1 mémoire

## TA MISSION

Analyse le code et réponds à ces questions :

### 1. SÉCURITÉ (Critique)
- Les tokens JWT sont-ils sécurisés ?
- Y a-t-il des secrets exposés dans le code ?
- La sanitization des inputs est-elle complète ?
- Le rate limiting est-il correctement implémenté ?

### 2. GESTION DES ERREURS
- Tous les appels API ont-ils des try/except ?
- Les messages d'erreur exposent-ils des infos sensibles ?
- Le fallback fonctionne-t-il vraiment ?

### 3. VARIABLES D'ENVIRONNEMENT
- Tous les providers vérifient-ils leurs clés API ?
- Y a-t-il toujours un fallback disponible ?
- Les erreurs de clés manquantes sont-elles claires ?

### 4. PERFORMANCE
- Le connection pooling est-il utilisé partout ?
- Le cache est-il efficace ?
- Y a-t-il des fuites de ressources ?

### 5. ARCHITECTURE
- Le code est-il bien structuré ?
- Y a-t-il du code dupliqué ?
- Les patterns sont-ils cohérents ?

## FORMAT DE RÉPONSE

Pour chaque problème trouvé :
1. **Fichier** : chemin du fichier
2. **Ligne** : numéro approximatif
3. **Problème** : description claire
4. **Sévérité** : 🔴 Critique / 🟡 Important / 🟢 Mineur
5. **Solution** : code corrigé

## RÉSUMÉ FINAL

À la fin, donne :
1. Score global /10
2. Top 5 problèmes critiques
3. Top 5 améliorations recommandées
4. Verdict : Production ready ? Oui/Non

## FICHIERS CLÉS À EXAMINER

Commence par ces fichiers :
- backend/services/auth.py (sécurité)
- backend/services/ai_router.py (fallback)
- backend/services/sanitizer.py (inputs)
- backend/main.py (configuration)
- backend/routers/chat.py (endpoint critique)

Sois CRITIQUE et CONSTRUCTIF. Ne te contente pas de dire "c'est bien", trouve les VRAIS problèmes.
```

---

## Comment Utiliser

### Option 1 : Audit Complet
1. Ouvrir une nouvelle conversation avec l'agent
2. Coller le prompt ci-dessus
3. Ajouter le contenu des fichiers clés (ou demander à l'agent de les lire)

### Option 2 : Audit Ciblé
Demander un audit spécifique :

```
Audite uniquement la SÉCURITÉ de ce projet :
- backend/services/auth.py
- backend/services/sanitizer.py
- backend/main.py

Vérifie :
- JWT sécurisé
- Pas de secrets exposés
- Sanitization complète
```

### Option 3 : Revue de Code
```
Fais une code review de ces fichiers :
[coller le code]

Trouve :
- Bugs
- Problèmes de sécurité
- Améliorations possibles
```

---

## Questions Spécifiques à Poser

### Sécurité
- "Le SECRET_KEY est-il sécurisé ?"
- "Y a-t-il des injections possibles ?"
- "Les tokens JWT ont-ils une expiration correcte ?"

### Fallback
- "Que se passe-t-il si toutes les clés API sont manquantes ?"
- "Le fallback vers Ollama fonctionne-t-il ?"
- "Y a-t-il des cas où aucun fallback n'est disponible ?"

### Performance
- "Y a-t-il des connexions HTTP non fermées ?"
- "Le cache est-il utilisé efficacement ?"
- "Y a-t-il des appels bloquants ?"

### Architecture
- "Le code suit-il les best practices FastAPI ?"
- "Y a-t-il du code dupliqué à factoriser ?"
- "Les responsabilités sont-elles bien séparées ?"

---

## Résultat Attendu

L'agent devrait fournir :

1. **Liste des problèmes** avec sévérité
2. **Solutions concrètes** avec code
3. **Score global** /10
4. **Verdict** : Production ready ?
5. **Plan d'action** priorisé

---

## Après l'Audit

Une fois l'audit reçu :

1. **Trier par sévérité** : Critique → Important → Mineur
2. **Corriger les critiques** en premier
3. **Tester** après chaque correction
4. **Re-auditer** les parties modifiées

---

## Tips pour un Bon Audit

1. **Soyez spécifique** : "Audite auth.py" plutôt que "Audite la sécurité"
2. **Donnez le contexte** : "C'est un backend pour usage personnel"
3. **Demandez des solutions** : "Propose le code corrigé"
4. **Itérez** : Faites plusieurs audits ciblés plutôt qu'un seul énorme

---

**Bonne chance pour l'audit !** 🚀


