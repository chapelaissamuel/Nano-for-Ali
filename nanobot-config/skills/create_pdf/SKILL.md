---
name: create_pdf
description: Generate ANY PDF — résumé, rapport, compte-rendu, document, fiche, questionnaire — and send it to the user via Telegram.
metadata: {"nanobot":{"emoji":"📝","requires":{"bins":["python3"]}}}
---

# Create PDF

Génère un fichier PDF depuis du contenu texte et l'envoie directement à l'utilisateur via Telegram.

## When to use

Utilise ce skill pour TOUTE demande impliquant un PDF, quelle que soit la formulation :
- "fais moi un résumé pdf"
- "envoie moi ça en pdf"
- "compte-rendu pdf"
- "rapport pdf"
- "fiche pdf"
- "questionnaire pdf"
- "résumé de match pdf"
- Toute autre demande contenant le mot "pdf" ou impliquant un fichier à envoyer

## RÈGLES ABSOLUES — NE JAMAIS DÉVIER

⛔ INTERDIT : Créer, réécrire ou exécuter un script Python custom (generate_match_pdf.py, make_pdf.py, ou tout autre nom).
⛔ INTERDIT : Utiliser write_file pour créer un script Python.
⛔ INTERDIT : Utiliser cat <<<, heredoc, ou tout mécanisme inline pour écrire du code.
⛔ INTERDIT : Utiliser python3 sur un fichier que tu viens de créer.
⛔ INTERDIT : Référencer un fichier PDF par un chemin relatif pour l'envoi.
⛔ INTERDIT : Réessayer en boucle. Une seule tentative.
⛔ INTERDIT : Dire que le PDF a été envoyé si le script retourne une erreur.
✅ OBLIGATOIRE : Utiliser UNIQUEMENT la séquence de 2 commandes ci-dessous, dans l'ordre, peu importe le type de contenu.

## Séquence exacte (2 commandes, pas plus)

Étape 1 — Écrire le contenu dans un fichier temporaire :

printf '%s' "Contenu complet ici" > /tmp/pdf_content.txt

Étape 2 — Appeler le script existant avec redirection :

python3 /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py "<chat_id>" - < /tmp/pdf_content.txt

Remplace <chat_id> par le chat_id réel de l'utilisateur disponible dans le contexte.
⚠️ Utilise printf '%s' et jamais echo. printf gère les sauts de ligne et caractères spéciaux.

## Ce que fait le script (ne pas reproduire, ne pas recréer)

Le script /app/nanobot-config/skills/create_pdf/scripts/generate_pdf.py :
1. Génère le PDF dans /tmp/output.pdf via fpdf2
2. L'envoie via api.telegram.org/bot{TOKEN}/sendDocument
3. Affiche "PDF envoyé ✅" en cas de succès
4. Affiche "Je n'ai pas pu envoyer le PDF, voici le contenu :" en cas d'échec et quitte avec code 1

## Interprétation du résultat

- Sortie contient "PDF envoyé ✅" → confirmer à l'utilisateur que le PDF a été envoyé.
- Sortie contient "Je n'ai pas pu envoyer le PDF" → relayer ce message verbatim suivi du contenu texte.
- Code de sortie = 1 → NE PAS dire que le PDF a été envoyé.

## Règles critiques finales

- Une seule tentative. Jamais de boucle.
- Le script generate_pdf.py existe déjà et fonctionne. Ne jamais le recréer.
- Le PDF est toujours généré dans /tmp/output.pdf. Ne jamais utiliser un autre chemin.
- Si fpdf2 manque : pip install fpdf2 --quiet puis relancer une seule fois.
