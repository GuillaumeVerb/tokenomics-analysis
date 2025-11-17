# 🚀 Quick Start Guide

## Installation Rapide

### Option 1 : Script automatique (macOS/Linux)
```bash
./run.sh
```

### Option 2 : Installation manuelle

```bash
# 1. Créer l'environnement virtuel
python3 -m venv venv

# 2. Activer l'environnement
source venv/bin/activate  # macOS/Linux
# OU
venv\Scripts\activate     # Windows

# 3. Installer les dépendances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py
```

## Premiers Pas

### 1️⃣ Mode Analyse Rapide
- Sélectionnez "⚡ Analyse Rapide" dans le menu
- Entrez un nom de token : `ethereum`, `bitcoin`, `uniswap`
- Cliquez sur "🔍 Analyser"
- Consultez le score et les visualisations

### 2️⃣ Mode Analyse Manuelle
- Sélectionnez "🔧 Analyse Manuelle"
- Choisissez un scénario préconfigé (optionnel)
- Ajustez les paramètres selon votre projet
- Cliquez sur "📊 Analyser la Tokenomics"

## Scénarios Disponibles

### 📊 Scénarios Structurels
1. **Projet early-stage** - Forte dilution, gouvernance centralisée
2. **Token utilitaire fort** - ETH-like, utilité gas + burn
3. **Modèle DeFi inflationniste** - Curve-like, farming rewards
4. **Modèle Pendle-like** - Faible inflation, fees > emissions
5. **Restaking / EigenLayer-like** - Collatéral, sécurité économique
6. **Gouvernance capturée** - Red flags, concentration élevée
7. **Token mature** - Bitcoin-like, supply quasi complète
8. **Meme coin / Community token** - Fair launch, pas d'utilité, spéculatif
9. **RWA Tokenization** - Actifs réels tokenisés, compliance forte
10. **Modèle Hyperliquid** - 100% community, 0% team/VC (2024)

### 📈 Scénarios Inflationnistes
8. **Inflation stable 2%** - Soutenable long terme
9. **Inflation stable 5%** - Modérée
10. **Inflation stable 10%** - Forte, typique DeFi
11. **Inflation haute 20%** - Farming, insoutenable
12. **Inflation décroissante** - 10% → 7% → 5% → 3% → 1%
13. **Inflation avec halving** - Division par 2 tous les 2 ans
14. **Inflation seasonal farming** - Forte puis réduction
15. **Inflation négative** - Burn > emissions (EIP-1559 like)

## Exemples de Tokens à Analyser

```bash
# L1/L2
ethereum, bitcoin, solana, polygon, avalanche

# DeFi
uniswap, aave, curve-dao-token, compound, maker

# Staking/Restaking
lido-dao, rocket-pool, eigenlayer (si disponible)

# Gouvernance
ens, optimism, arbitrum
```

## Interprétation des Scores

- **80-100** : ✅ Excellent - Tokenomics très solide
- **65-79** : ✅ Bon - Quelques améliorations possibles
- **50-64** : ⚠️ Acceptable - Points de vigilance
- **35-49** : ⚠️ Risqué - Plusieurs red flags
- **0-34** : 🚨 Très risqué - Nombreux problèmes

## Dépannage

### Erreur "Token non trouvé"
- Vérifiez l'orthographe (en minuscules)
- Utilisez le CoinGecko ID exact (ex: `curve-dao-token` pas `curve`)
- Consultez https://www.coingecko.com/ pour trouver l'ID

### Erreur d'import
```bash
pip install --upgrade -r requirements.txt
```

### Port déjà utilisé
```bash
streamlit run app.py --server.port 8502
```

## Support

- 📧 Email : votre.email@exemple.com
- 💼 Malt : [Votre profil]
- 🔗 LinkedIn : [Votre profil]
- 🐛 Issues : [GitHub Issues]

---

Développé avec ❤️ par Guillaume Verbiguié

