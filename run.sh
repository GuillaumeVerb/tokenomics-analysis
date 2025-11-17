#!/bin/bash

# Script de lancement pour Tokenomics Analyzer

echo "🪙 Lancement de Tokenomics Analyzer..."

# Vérifier si le venv existe
if [ ! -d "venv" ]; then
    echo "⚠️  Environnement virtuel non trouvé. Création..."
    python3 -m venv venv
    echo "✅ Environnement virtuel créé"
fi

# Activer le venv
source venv/bin/activate

# Installer les dépendances
echo "📦 Installation des dépendances..."
pip install -q -r requirements.txt

# Lancer Streamlit
echo "🚀 Lancement de l'application..."
streamlit run app.py

