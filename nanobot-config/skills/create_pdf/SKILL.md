---
name: create_pdf
description: Génère un fichier PDF depuis du texte et l'envoie directement à l'utilisateur via Telegram Bot API.
metadata: {"nanobot":{"emoji":"📝","requires":{"bins":["python3"]}}}
---

# Create PDF

Génère un PDF et l'envoie via Telegram. Séquence exacte, aucune déviation.

## When to use

Utilise ce skill pour TOUTE demande impliquant un PDF :
- "fais moi un résumé pdf"
- "envoie moi ça en pdf"
- "compte-rendu pdf", "rapport pdf", "devis pdf"
- Toute formulation contenant "pdf"

## RÈGLES ABSOLUES

⛔ INTERDIT : Créer un script Python custom (make_pdf.py, generate.py, ou tout autre nom)
⛔ INTERDIT : Utiliser cat <<<, heredoc, ou echo pour écrire du contenu multi-ligne
⛔ INTERDIT : Générer un PDF avec un nom autre que /tmp/output.pdf
⛔ INTERDIT : Réessayer en boucle — une seule tentative
⛔ INTERDIT : Dire que le PDF a été envoyé si le script retourne une erreur

## Séquence exacte — 2 commandes

**Étape 1** — écrire le contenu dans un fichier temporaire :

```
printf '%s' "Contenu complet du PDF ici" > /tmp/pdf_content.txt
```

**Étape 2** — appeler le script avec redirection stdin :

```
python3 /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py "<chat_id>" - < /tmp/pdf_content.txt
```

Remplace `<chat_id>` par le chat_id réel de l'utilisateur.
⚠️ Utilise `printf '%s'` — jamais `echo`.

## Interprétation du résultat

- Contient `"PDF envoyé ✅"` → confirmer à l'utilisateur que le PDF a été envoyé
- Contient `"Je n'ai pas pu envoyer le PDF"` → relayer ce message verbatim suivi du contenu texte
- Code de sortie 1 → NE PAS dire que le PDF a été envoyé

## Règles finales

- Une seule tentative. Jamais de boucle.
- Le script existe déjà. Ne jamais le recréer.
- Output toujours dans /tmp/output.pdf. Aucun autre chemin.
