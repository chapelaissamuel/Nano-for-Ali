---
name: create_pdf
description: Generate a PDF from text content and send it to the user via Telegram.
metadata: {"nanobot":{"emoji":"📝","requires":{"bins":["python3"]}}}
---

# Create PDF

Generate a PDF file from text content and deliver it directly to the user via the Telegram Bot API.

## When to use

Use this skill when the user asks to:
- Create a PDF
- Send something as a PDF
- Export content to PDF

## RÈGLE ABSOLUE — NE JAMAIS DÉVIER

⛔ INTERDIT : Créer, réécrire ou modifier un script Python. Le script existe déjà.
⛔ INTERDIT : Utiliser `cat <<<` (herestring) ou tout heredoc inline.
⛔ INTERDIT : Installer des librairies ou vérifier l'environnement avant d'essayer.
⛔ INTERDIT : Réessayer en boucle. Une seule tentative.
✅ OBLIGATOIRE : Utiliser UNIQUEMENT la séquence de 2 commandes ci-dessous, dans l'ordre.

## Séquence exacte (2 commandes, pas plus)

Étape 1 — Écrire le contenu dans un fichier temporaire :

printf '%s' "Contenu complet du résumé ici" > /tmp/pdf_content.txt

Étape 2 — Appeler le script :

python3 /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py "<chat_id>" - < /tmp/pdf_content.txt

Remplace <chat_id> par le chat_id réel de l'utilisateur.
⚠️ printf '%s' gère les sauts de ligne. Ne pas utiliser echo.

## Ce que fait le script (ne pas reproduire)

1. Génère un PDF dans /tmp/output.pdf via fpdf2
2. L'envoie via Telegram sendDocument
3. Affiche `PDF envoyé ✅` en cas de succès
4. Affiche `Je n'ai pas pu envoyer le PDF, voici le contenu :` en cas d'échec

## Interprétation du résultat

- Sortie contient `PDF envoyé ✅` → confirmer à l'utilisateur.
- Sortie contient `Je n'ai pas pu envoyer le PDF` → relayer ce message verbatim.
- Code de sortie = 1 → NE PAS dire que le PDF a été envoyé.

## Règles critiques

- Une seule tentative. Pas de boucle.
- Ne jamais créer de fichier Python intermédiaire.
- Ne jamais affirmer que le PDF a été envoyé si le script retourne une erreur.
