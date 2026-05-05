---
name: model_switch
description: Switch the active LLM model at runtime. Supports /model gemini and /model gemma commands.
metadata: {"nanobot":{"emoji":"🔀","always":true,"requires":{"bins":["python3"]}}}
---

# Model Switch

Change le modèle IA actif sans redéploiement. Le bot redémarre automatiquement avec le nouveau modèle.

## When to use

Utilise ce skill immédiatement quand l'utilisateur envoie :
- `/model gemini` — passer sur Gemini 2.5 Flash (défaut)
- `/model gemma` — passer sur Gemma 3 27B (Google, open-weights)
- `/model` suivi de tout autre mot-clé lié à un changement de modèle

## Séquence exacte

```
python3 /app/nanobot-config/skills/model_switch/scripts/switch_model.py <cible>
```

Où `<cible>` est `gemini` ou `gemma`.

## Modèles disponibles

| Commande | Modèle | Description |
|---|---|---|
| `/model gemini` | `gemini/gemini-2.5-flash` | Défaut — Gemini 2.5 Flash, rapide et intelligent |
| `/model gemma` | `gemini/gemma-3-27b-it` | Gemma 3 27B, open-weights Google |

## Interprétation du résultat

- Contient `✅` → confirmer le changement et dire que le bot redémarre
- Contient `Modèle inconnu` → indiquer les commandes valides : `/model gemini` ou `/model gemma`
- Code de sortie 1 → signaler l'erreur

## Règles

- Une seule exécution. Pas de retry.
- Le bot sera indisponible ~15 secondes pendant le redémarrage — prévenir l'utilisateur.
- Après redémarrage, le nouveau modèle est actif jusqu'au prochain redéploiement Railway.
