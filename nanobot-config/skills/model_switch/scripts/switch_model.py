#!/usr/bin/env python3
"""
switch_model.py — Change le modèle LLM actif dans config.json et redémarre nanobot.

Usage:
  python3 switch_model.py claude   → anthropic/claude-haiku-4.5
  python3 switch_model.py gemma    → google/gemma-4-31b-it

Le processus nanobot (PID 1) est tué 3 secondes après la réponse.
Railway relance automatiquement avec le nouveau modèle.
"""

import sys
import json
import subprocess

CONFIG_PATH = "/app/nanobot-config/config.json"

MODELS = {
    "claude": "anthropic/claude-haiku-4.5",
    "gemma":  "google/gemma-4-31b-it",
}

def main():
    target = sys.argv[1].lower() if len(sys.argv) > 1 else ""

    if target not in MODELS:
        print(f"Modèle inconnu : '{target}'")
        print(f"Commandes valides : /model gemma  |  /model claude")
        sys.exit(1)

    new_model = MODELS[target]

    try:
        config = json.load(open(CONFIG_PATH))
    except Exception as e:
        print(f"Erreur lecture config : {e}")
        sys.exit(1)

    current_model = config.get("agents", {}).get("defaults", {}).get("model", "?")

    if current_model == new_model:
        print(f"ℹ️ Modèle déjà actif : {new_model}")
        sys.exit(0)

    config["agents"]["defaults"]["model"] = new_model

    try:
        json.dump(config, open(CONFIG_PATH, "w"), indent=2)
    except Exception as e:
        print(f"Erreur écriture config : {e}")
        sys.exit(1)

    print(f"✅ Modèle changé : {current_model} → {new_model}")
    print(f"🔄 Redémarrage dans 3 secondes... (le bot sera indisponible ~15s)")

    # Tuer PID 1 après 3s dans un processus détaché
    # Railway (on_failure) relance automatiquement sur exit code non-zéro
    subprocess.Popen(
        ["bash", "-c", "sleep 3 && kill -15 1"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        close_fds=True
    )

if __name__ == "__main__":
    main()
