# 🔧 Configuration Git & GitHub

## ✅ Repo Git Initialisé

Le dépôt Git local est déjà initialisé et le premier commit a été effectué.

## 📤 Pousser sur GitHub

### Étape 1 : Créer un repo sur GitHub

1. Aller sur [github.com](https://github.com)
2. Cliquer sur "New repository" (bouton vert)
3. Nommer le repo : `tokenomics-analysis`
4. Description : "🪙 Analyse de tokenomics pour projets crypto/DeFi. Streamlit app avec 15 scénarios préconfigurés."
5. **Laisser vide** (ne pas initialiser avec README/LICENSE/gitignore)
6. Cliquer sur "Create repository"

### Étape 2 : Lier le repo local avec GitHub

```bash
cd /Users/guillaumeverbiguie/Desktop/tokenomics-analysis

# Remplacer TON_USERNAME par votre vrai username GitHub
git remote add origin https://github.com/TON_USERNAME/tokenomics-analysis.git

# Vérifier
git remote -v
```

### Étape 3 : Pousser le code

```bash
# Push sur la branche main
git push -u origin main
```

Si vous avez une erreur d'authentification :

```bash
# Option 1 : HTTPS avec token (recommandé)
# 1. Créer un Personal Access Token sur GitHub :
#    Settings → Developer settings → Personal access tokens → Tokens (classic)
# 2. Utiliser le token comme mot de passe lors du push

# Option 2 : SSH (plus sécurisé)
# 1. Générer une clé SSH si vous n'en avez pas :
ssh-keygen -t ed25519 -C "votre.email@exemple.com"

# 2. Ajouter la clé à GitHub :
#    Settings → SSH and GPG keys → New SSH key
cat ~/.ssh/id_ed25519.pub  # Copier cette clé

# 3. Changer l'URL remote en SSH :
git remote set-url origin git@github.com:TON_USERNAME/tokenomics-analysis.git

# 4. Pousser :
git push -u origin main
```

## 📝 Commits Futurs

Pour les prochaines modifications :

```bash
# Voir le statut
git status

# Ajouter les fichiers modifiés
git add .

# Ou ajouter des fichiers spécifiques
git add app.py tokenomics/scenarios.py

# Commiter avec un message clair
git commit -m "feat: ajout de nouveaux scénarios DeFi"

# Pousser
git push
```

## 🏷️ Bonnes Pratiques

### Conventions de commit

- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `docs:` documentation
- `style:` formatage (sans changement de logique)
- `refactor:` refactoring
- `test:` ajout/modification de tests
- `chore:` maintenance

Exemples :
```bash
git commit -m "feat: ajout scénario Uniswap v4"
git commit -m "fix: correction calcul score inflation"
git commit -m "docs: mise à jour README avec nouveaux screenshots"
```

### Branches

```bash
# Créer une branche pour une nouvelle feature
git checkout -b feature/nouveau-scenario

# Faire vos modifs, puis commit
git add .
git commit -m "feat: ajout scénario Hyperliquid"

# Pousser la branche
git push -u origin feature/nouveau-scenario

# Merger dans main (sur GitHub via Pull Request ou localement)
git checkout main
git merge feature/nouveau-scenario
git push
```

## 🌐 Après le Push

Une fois sur GitHub, vous pouvez :

1. **Ajouter des topics** au repo :
   - `python`
   - `streamlit`
   - `blockchain`
   - `defi`
   - `tokenomics`
   - `cryptocurrency`
   - `data-analysis`

2. **Éditer le README** sur GitHub pour :
   - Ajouter un badge : `![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)`
   - Ajouter vos vrais screenshots

3. **Activer GitHub Pages** (si besoin) :
   - Settings → Pages → Source: main branch

4. **Déployer sur Streamlit Cloud** :
   - [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub repo
   - Select `app.py`
   - Deploy !

## 📊 Badges pour le README (optionnel)

Ajouter en haut du README.md :

```markdown
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
```

Résultat :  
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white) ![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)

---

**✅ Votre repo est prêt à être poussé sur GitHub !**

