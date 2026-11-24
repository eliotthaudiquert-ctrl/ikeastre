# Fika · l'agent de recherche IKÉASTRE

Projet IKEA × Gen Z (B3CPD, Ynov). Concept académique indépendant, non affilié à IKEA. Agent, analyses, slides et vidéo réalisés avec l'aide de l'IA, puis relus par l'équipe.

## Ce qu'il fait
Fika applique la boucle du cours : **Mission → 1 Planifier → 2 Agir (outils) → 3 Observer → 4 Vérifier → non : on reboucle / oui : livrable**.

- **Mission 1 · Vérification** : répond aux questions de l'atelier « le brief déconstruit » (accès sans voiture, prix ou livraison, humour, budgets de 700 € et 350 €, chiffres de notre dossier à revérifier).
- **Mission 2 · Veille** : compare IKEA, Maisons du Monde, Conforama, But, Action et Leboncoin sur 6 critères (réseau, petits formats, livraison, offre jeunes, fidélité et seconde main, TikTok).
- **Livrable** : un tableau Excel sourcé et daté (et une version CSV et Markdown) dans `livrables/`.

## Le lancer
Double-clic sur **`Lancer l'agent Fika.cmd`**, puis 1, 2 ou 3. Il travaille seul, affiche chaque étape, et ouvre le dossier `livrables` à la fin.
Il faut : Python, et Claude Code connecté à un compte Claude (le « modèle qui raisonne »).
Sans rien installer : `Prompt à coller (ChatGPT ou Claude).md` (sans contrôleur automatique).

## Ce qu'il y a dans le dossier
| Dossier / fichier | Rôle dans la boucle |
|---|---|
| `agent/SYSTEME.md` | Les règles permanentes : sourçage, statuts, format de sortie |
| `agent/missions/` | Les deux fiches mission (rôle, sources, format, règles) |
| `agent/lancer.py` | Le chef d'orchestre : lance le modèle, journalise chaque étape, contrôle, reboucle (3 tours max) |
| `agent/outils/lire_page.py` | Outil : texte exact d'une page web ou d'un PDF |
| `agent/outils/calcul.py` | Outil : calculatrice sûre (totaux de prix, écarts au budget) |
| `agent/outils/verifier.py` | Étape 4 : ouvre chaque source et cherche l'extrait mot pour mot, contrôle dates et couverture |
| `agent/outils/tableur.py` | Livrable : Excel mis en forme (tableau, synthèse, contrôle) |
| `agent/journal/` | Le journal de chaque lancement : chaque action, chaque résultat, chaque vérification |
| `livrables/` | Les tableaux sourcés et datés |
| `slides/` | La présentation (PDF + HTML) ; `build.py` la régénère à partir des derniers résultats |
| `video/` | La vidéo motion (Remotion) ; rendu final dans ce dossier |

## Garde-fous
- Zéro chiffre sans page ouverte ; sinon « Non trouvé ».
- Extrait copié mot pour mot et retrouvé dans la page par le contrôleur.
- Sites qui bloquent les robots (TikTok…) : signalés « à contrôler à la main ».
- Aucun compte, aucun formulaire, aucune donnée personnelle.
- Les prix et les abonnés sont des relevés datés : relancer l'agent pour les mettre à jour.

## Crédits de la vidéo
Musique : Vivaldi, Les Quatre Saisons, L'Été, Presto · The Modena Chamber Orchestra (Musopen), domaine public (Wikimedia Commons). Bruitages : Mixkit (licence gratuite). Police : Noto Sans / Noto Sans Mono (Google Fonts, OFL). Aucune image générée par IA.
