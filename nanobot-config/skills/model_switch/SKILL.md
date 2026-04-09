---
name: model_switch
description: Switch the active LLM model at runtime. Supports /model claude and /model gemma commands.
metadata: {"nanobot":{"emoji":"🔀","requires":{"bins":["python3"]}}}
---

# Model Switch

Change le modèle IA actif sans redéploiement. Le bot redémarre automatiquement avec le nouveau modèle.

## When to use

Utilise ce skill immédiatement quand l'utilisateur envoie :
- `/model claude` — passer sur Claude Haiku 4.5 (Anthropic)
- `/model gemma` — passer sur Gemma 4 31B (Google, modèle par défaut)
- `/model` suivi de tout autre mot-clé lié à un changement de modèle

## Séquence exacte

```
python3 /app/nanobot-config/skills/model_switch/scripts/switch_model.py <cible>
```

Où `<cible>` est `claude` ou `gemma`.

## Modèles disponibles

| Commande | Modèle | Description |
|---|---|---|
| `/model gemma` | `google/gemma-4-31b-it` | Défaut — 31B, contexte 262k, rapide |
| `/model claude` | `anthropic/claude-haiku-4.5` | Claude Haiku 4.5, excellent pour la rédaction |

## Interprétation du résultat

- Contient `✅` → confirmer le changement et dire que le bot redémarre
- Contient `Modèle inconnu` → indiquer les commandes valides : `/model gemma` ou `/model claude`
- Code de sortie 1 → signaler l'erreur

## Règles

- Une seule exécution. Pas de retry.
- Le bot sera indisponible ~15 secondes pendant le redémarrage — prévenir l'utilisateur.
- Après redémarrage, le nouveau modèle est actif jusqu'au prochain redéploiement Railway.
