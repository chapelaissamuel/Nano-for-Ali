---
name: send_pdf_telegram
description: send_pdf_telegram — Generate ANY PDF (résumé, rapport, compte-rendu, devis, document, fiche, questionnaire) and send it to the user via Telegram Bot API.
metadata: {"nanobot":{"emoji":"📝","requires":{"bins":["python3"]}}}
---

# Send PDF via Telegram

Génère un fichier PDF depuis du contenu texte et l'envoie directement à l'utilisateur via Telegram.

## When to use

Utilise ce skill pour TOUTE demande impliquant un PDF, quelle que soit la formulation :
- "fais moi un résumé pdf"
- "envoie moi ça en pdf"
- "compte-rendu pdf"
- "rapport pdf"
- "devis pdf"
- "fiche pdf"
- "questionnaire pdf"
- "résumé de match pdf"
- Toute autre demande contenant le mot "pdf" ou impliquant un fichier à envoyer

## RÈGLES ABSOLUES — NE JAMAIS DÉVIER

⛔ INTERDIT : Créer, réécrire ou exécuter un script Python custom (make_devis.py, generate_match_pdf.py, make_pdf.py, ou tout autre nom inventé).
⛔ INTERDIT : Utiliser write_file pour créer un script Python.
⛔ INTERDIT : Utiliser cat <<<, heredoc, ou tout mécanisme inline pour écrire du code.
⛔ INTERDIT : Utiliser le tool `message` avec un paramètre `media` pour envoyer un PDF.
⛔ INTERDIT : Générer un fichier PDF avec un nom custom dans /tmp/ (devis_koza.pdf, resume_match.pdf, etc).
⛔ INTERDIT : Référencer un fichier PDF par un chemin relatif ou un nom custom pour l'envoi.
⛔ INTERDIT : Réessayer en boucle. Une seule tentative.
⛔ INTERDIT : Dire que le PDF a été envoyé si le script retourne une erreur.
✅ Le seul chemin de sortie valide est /tmp/output.pdf, géré automatiquement par generate_pdf.py.
✅ Le seul moyen d'envoyer est la séquence de 2 commandes ci-dessous. Rien d'autre.

## Séquence exacte (2 commandes, pas plus)

Étape 1 — Écrire le contenu dans un fichier temporaire :

printf '%s' "Contenu complet ici" > /tmp/pdf_content.txt

Étape 2 — Appeler le script existant avec redirection :

python3 /app/nanobot-config/skills/send_pdf_telegram/scripts/generate_pdf.py "<chat_id>" - < /tmp/pdf_content.txt

Remplace <chat_id> par le chat_id réel de l'utilisateur disponible dans le contexte.
⚠️ Utilise printf '%s' et jamais echo.

## Ce que fait le script (ne pas reproduire, ne pas recréer)

Le script /app/nanobot-config/skills/send_pdf_telegram/scripts/generate_pdf.py :
1. Lit le token depuis /tmp/.tg_token (écrit par start.sh au démarrage du container)
2. Génère le PDF dans /tmp/output.pdf via fpdf2
3. L'envoie via api.telegram.org/bot{TOKEN}/sendDocument (une seule tentative, timeout=30s)
4. Affiche "PDF envoyé ✅" en cas de succès
5. Affiche "Je n'ai pas pu envoyer le PDF, voici le contenu :" en cas d'échec

## Interprétation du résultat

- Sortie contient "PDF envoyé ✅" → confirmer à l'utilisateur que le PDF a été envoyé.
- Sortie contient "Je n'ai pas pu envoyer le PDF" → relayer ce message verbatim suivi du contenu texte.
- Code de sortie = 1 → NE PAS dire que le PDF a été envoyé.

## Règles critiques finales

- Une seule tentative. Jamais de boucle.
- Le script generate_pdf.py existe déjà et fonctionne. Ne jamais le recréer.
- Le PDF est toujours généré dans /tmp/output.pdf. Ne jamais utiliser un autre chemin ou nom de fichier.
- Si fpdf2 manque : pip install fpdf2 --quiet puis relancer une seule fois.
