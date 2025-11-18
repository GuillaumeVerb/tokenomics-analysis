# 🪙 Tokenomics Analyzer

Une application Streamlit professionnelle pour analyser la viabilité de la tokenomics des projets crypto (DeFi, L1/L2, DAO).

## 🎯 Objectif

Évaluer la santé économique d'un token selon **8 piliers** :
- **Inflation & Dilution** (20%) : pression sur le prix via l'émission
- **Distribution** (15%) : concentration et équité de la supply
- **Utilité** (20%) : cas d'usage réels du token
- **Gouvernance** (10%) : décentralisation et sécurité
- **Incitations** (10%) : mécanismes d'engagement (staking, lock, burn)
- **💰 Liquidité** (15%) : volume de trading et facilité d'achat/vente
- **🌍 Adoption** (10%) : traction, market cap, croissance
- **🔐 Sécurité** (5% bonus) : audits smart contracts, bug bounty

L'analyse produit un **Tokenomics Viability Index** (0–100) et des visualisations claires.

## 📊 Fonctionnalités

### 1. ⚡ Mode Analyse Rapide (CoinGecko)
- **Recherche intelligente** : accepte symboles (BTC, ETH, SOL) ou noms complets
- **Boutons rapides** : Bitcoin, Ethereum, Solana, BNB, Cardano, Avalanche
- **27 tokens enrichis** : données réelles pour les cryptos populaires (L1, L2, DeFi, Gaming, Memecoins)
- **Suggestions automatiques** : si un token n'est pas trouvé
- **Badge qualité** : indique si les données sont enrichies ou estimées
- Import automatique des données via l'API CoinGecko
- Visualisations de distribution de supply

### 2. 🔧 Mode Analyse Manuelle Avancée
- Configuration personnalisée de tous les paramètres
- **18 scénarios préconfigurés** :
  - **10 scénarios structurels** (early-stage, ETH-like, Curve-like, Pendle-like, Hyperliquid, meme coins, RWA, etc.)
  - **8 scénarios inflationnistes** (2%, 5%, 10%, 20%, décroissante, halving, seasonal, burn)
- Projection de dilution sur 5 ans
- Analyse approfondie de chaque composante

### 3. ⚖️ Mode Comparaison
- **Comparez 2 tokens côte à côte**
- Tableau comparatif des scores détaillés
- Différences calculées automatiquement
- Visualisation des gagnants par catégorie

### 4. 📥 Export & Historique
- **Export PDF** : téléchargez un rapport complet en HTML (imprimez en PDF)
- **Historique** : consultez les 5 dernières analyses dans la sidebar
- Rechargement rapide des analyses précédentes

### 5. 🌓 Thème Personnalisable
- **Toggle mode sombre/clair**
- Interface adaptée à vos préférences

### 6. 📊 Visualisations
- Camembert de distribution de supply
- Projection de dilution temporelle
- Scores détaillés par catégorie
- Jauge de score final

### 7. 📚 Méthodologie Transparente
- Explication des formules de scoring
- Limites et hypothèses
- Sources et références

## 🛠️ Stack Technique

- **Python 3.8+**
- **Streamlit** : interface web
- **Pandas** : manipulation de données
- **Plotly** : visualisations interactives
- **Requests** : API CoinGecko

## 🚀 Installation

```bash
# Cloner le repo
git clone https://github.com/yourusername/tokenomics-analysis.git
cd tokenomics-analysis

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## 📁 Structure du Projet

```
tokenomics-analysis/
├── app.py                      # Application principale
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
├── .streamlit/
│   └── config.toml            # Configuration Streamlit
└── tokenomics/
    ├── __init__.py
    ├── scenarios.py           # Scénarios préconfigurés
    ├── scoring.py             # Calcul du Viability Index
    ├── api.py                 # Intégration CoinGecko
    └── visualizations.py      # Graphiques Plotly
```

## 🎓 Méthodologie

Le **Tokenomics Viability Index** est calculé selon 5 composantes pondérées :

1. **Inflation (25%)** : Impact de l'émission future sur la dilution
2. **Distribution (20%)** : Équité et décentralisation de la supply
3. **Utilité (25%)** : Cas d'usage réels et demande intrinsèque
4. **Gouvernance (15%)** : Sécurité et décentralisation du contrôle
5. **Incitations (15%)** : Mécanismes d'engagement long terme

Score final : **0–100** (plus élevé = meilleure viabilité)

## 📝 Exemples d'Utilisation

### Analyse Rapide
1. Sélectionner "Mode Analyse Rapide"
2. Entrer un nom de token (ex: "ethereum", "bitcoin", "uniswap")
3. Voir l'analyse instantanée

### Analyse Manuelle
1. Sélectionner "Mode Analyse Manuelle"
2. Choisir un scénario préconfigré (optionnel)
3. Ajuster les paramètres selon le projet
4. Consulter le score et les recommandations

## 🔗 Cas d'Usage

- **Investisseurs** : évaluer la viabilité économique avant d'investir
- **Fondateurs** : benchmarker leur tokenomics contre des modèles éprouvés
- **Analystes** : produire des rapports structurés
- **Développeurs** : comprendre les mécanismes de différents modèles

## ⚠️ Limites

- Les données CoinGecko peuvent être incomplètes
- Certains paramètres qualitatifs nécessitent une recherche manuelle
- Le score est indicatif, pas une recommandation d'investissement
- DYOR (Do Your Own Research) toujours recommandé

## 📸 Screenshots

### Interface Principale
![App Principal](docs/screenshots/app_main.png)

### Mode Analyse Rapide
![Analyse Rapide](docs/screenshots/quick_analysis.png)

### Mode Analyse Manuelle avec Scénarios
![Analyse Manuelle](docs/screenshots/manual_analysis.png)

### Résultats et Visualisations
![Résultats](docs/screenshots/results.png)

---

## 🚀 Déploiement

### Streamlit Cloud (Gratuit)
1. Push ce repo sur GitHub
2. Aller sur [share.streamlit.io](https://share.streamlit.io)
3. Connecter votre repo
4. Sélectionner `app.py` comme fichier principal
5. Déployer !

### Docker (Optionnel)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

---

## 📧 Contact & Liens

**Guillaume Verbiguié**  
Développeur Python • Data • Blockchain • DeFi

- 🌐 **Portfolio** : [guillaumeverbiguie.com](https://guillaumeverbiguie.com)
- 💼 **Malt** : [malt.fr/profile/guillaumeverbiguie](https://www.malt.fr/profile/guillaumeverbiguie)
- 💻 **GitHub** : [github.com/guillaumeverbiguie](https://github.com/guillaumeverbiguie)
- 🔗 **LinkedIn** : [linkedin.com/in/guillaumeverbiguie](https://www.linkedin.com/in/guillaumeverbiguie)

---

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- 🐛 Reporter des bugs
- 💡 Proposer de nouvelles fonctionnalités
- 🔧 Soumettre des pull requests
- ⭐ Mettre une étoile si le projet vous plaît !

## 📄 Licence

MIT License - Libre d'utilisation et modification

Copyright (c) 2025 Guillaume Verbiguié

---

## 🙏 Remerciements

- **CoinGecko** pour l'API gratuite
- **Streamlit** pour le framework
- **Plotly** pour les visualisations
- La communauté **DeFi** pour l'inspiration

---

<div align="center">
  <strong>⚠️ Disclaimer</strong><br>
  Cet outil est fourni à titre éducatif et informatif uniquement.<br>
  Il ne constitue pas un conseil en investissement financier.<br>
  Faites toujours vos propres recherches (DYOR).
</div>

