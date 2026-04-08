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
⛔ INTERDIT : Utiliser `cat`, `heredoc`, `EOF`, ou tout autre mécanisme pour écrire du code.
⛔ INTERDIT : Installer des librairies ou vérifier l'environnement.
✅ OBLIGATOIRE : Appeler UNIQUEMENT la commande ci-dessous, une seule fois.

## Commande unique à exécuter

Pour du contenu court (< 500 caractères) :

```bash
python3 /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py "<chat_id>" "Contenu complet ici"
```

Pour du contenu long (>= 500 caractères), utiliser le pipe :

```bash
cat << 'ENDOFCONTENT' | python3 /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py "<chat_id>" -
Contenu complet ici
ENDOFCONTENT
```

Remplace `<chat_id>` par le chat_id réel de l'utilisateur (disponible dans le contexte de la conversation).

## Ce que fait le script (ne pas reproduire)

Le script `/app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py` :
1. Génère un PDF dans `/tmp/output.pdf` via fpdf2
2. L'envoie via `https://api.telegram.org/bot.../sendDocument`
3. Affiche `PDF envoyé ✅` en cas de succès
4. Affiche `Je n'ai pas pu envoyer le PDF, voici le contenu :` en cas d'échec et quitte avec code 1

## Interprétation du résultat

- Si la sortie contient `PDF envoyé ✅` → confirmer à l'utilisateur que le PDF a été envoyé.
- Si la sortie contient `Je n'ai pas pu envoyer le PDF` → relayer ce message verbatim suivi du contenu texte.
- Si code de sortie = 1 → NE PAS dire que le PDF a été envoyé.

## Règles critiques

- N'exécuter la commande qu'**une seule fois**. Ne pas réessayer en boucle.
- Ne JAMAIS affirmer que le PDF a été envoyé si le script retourne une erreur.
- Ne JAMAIS créer de fichier Python intermédiaire.
- Si fpdf2 n'est pas installé : `pip install fpdf2 --quiet` puis relancer la commande une seule fois.
