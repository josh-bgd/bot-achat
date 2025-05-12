#!/bin/zsh

cd "$(dirname "$0")"/..  # revient à la racine de ton projet

# Activer le venv
source .venv/bin/activate

# Lancer le GUI
echo "🧠 Lancement de l'interface graphique..."
python bot/gui.py

# Lancer le bot
echo "🤖 Lancement du bot..."
python bot/bot.py
