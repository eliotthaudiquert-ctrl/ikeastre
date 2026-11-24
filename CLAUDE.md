# IKÉASTRE · Projet IKEA × Gen Z (B3CPD, Ynov)

Ce fichier est lu par le Claude de chaque membre de l'équipe. Il sert de mémoire commune : **c'est la source de vérité sur l'état du projet**.

## Cours en cours
Veille stratégique, business model & arbitrages budgétaires (B3, 2026-27) : dossier PFR Bloc 1 de 10 à 12 pages, en PDF et en groupe (veille, synthèse décisionnelle, business model, budget en 2 scénarios « minimal viable » et « ambitieux », arbitrages, recommandations). Session 1 faite (voir `09 Veille stratégique`).

## Équipe
Loris, Tobias, Eliott (groupe « PFR IKÉASTRE » sur Teams). Projet académique indépendant, non affilié à IKEA.

## Règle de synchro (pour chaque Claude)
1. **Avant de travailler** : `git pull` (ou double-clic sur `Synchroniser.cmd`).
2. **Après une modif** : mettre à jour la section « Journal » plus bas (date, qui, quoi), puis commit + push (ou `Synchroniser.cmd`).
3. Un livrable validé par l'équipe est verrouillé : on n'y touche plus sans accord des trois.
4. Ne jamais supprimer le travail d'un autre membre. En cas de conflit git, demander avant d'écraser.

## Règles de fond
- **Rien d'inventé** : chaque chiffre a une source (lien + date de relevé). Sinon on écrit « à confirmer ».
- **Pas d'images générées par IA** : photos et vidéos réelles, libres de droits.
- **DA de groupe** à garder : bleu IKEA `#0058A3`, jaune `#FFDA1A`, police Noto Sans. Garder exactement le design existant des documents de groupe.
- Mention IA exacte dans les rendus (ce qui a été fait avec l'IA, relu par l'équipe).

## Structure du dossier
| Dossier | Contenu |
|---|---|
| `01 Consignes et cours` | Consigne EFN B3CPD |
| `02 Dossier et oral Gen Z` | Dossier, synthèse 5 slides, sources ; `Versions Codex (copies)` = dossier stratégique d'équipe `B3CPD_IKEA_Equipe.pdf` et variantes |
| `03 Personas` | Personas Léa et Noah en texte (les personas complets, dont Inès, sont dans les PDF du dossier 02) |
| `04 Pilotage agile` | Kit de pilotage (charte, RACI, backlog) `B3CPD_IKEA_Kit_Pilotage_Agile.xlsx`, tableau des 37 livrables en 4 phases |
| `05 Campagne` | Vidéo « Des meubles pour tous les rebondissements » (`Vidéo IKEA/`) + projet Remotion (`IKEA Reel/reel`) |
| `06 Atelier brief déconstruit` | Slide de l'atelier (HTML, PDF, PNG) |
| `07 Agent IA` | Agent de recherche « Fika » : missions vérification + veille, livrables Excel, slides, vidéo. Voir son `LISEZ-MOI.md` |
| `08 Segmentation` | Segmentation Gen Z (PDF + slides HTML + corpus chiffres/verbatims sourcés) ; `Première version (12-10-2026)` = 1re segmentation du marché IKEA (PPTX + PDF) |
| `09 Veille stratégique` | Session 1 du cours Veille stratégique : grille des 8 champs (magasins compacts, angle MARKET). Données dans `veille.json`, `python build.py` régénère Excel + PDF, `python verifier_veille.py` rouvre chaque source et contrôle les extraits |
| `10 Hypothèses clients` | Fiche d'hypothèses tirées d'avis en ligne (HTML, imprimable), aucune validée : à tester auprès de vrais clients |
| `IKEA - Envoi livrables PFR` | Les livrables PFR envoyés le 23/11/2026 |

Pas dans le dépôt (droits ou poids) : reel d'inspiration, rushs et bruitages Mixkit bruts, fichiers .wav, doublons. Le rendu vidéo final, lui, est bien là.

## État des livrables PFR (au 24/11/2026)
| # | Livrable | État |
|---|---|---|
| 01 | Segmentation | Fait (`IKEA - Envoi livrables PFR`) |
| 02 | Personas | Fait |
| 03 | Veille concurrentielle sourcée | Fait (Excel issu de l'agent Fika) |
| 04 | Positionnement | Pas de version dédiée : couvert en partie par le dossier stratégique (mapping p. 6-7) |
| 05-06 | Canvas, promesse | Dans le dossier stratégique (canvas p. 12, promesse p. 13) |
| 07 | Note d'arbitrage | **À faire** : pas de version dédiée |

Livrables de campagne sans responsable attribué (au 03/11) : affiche, carrousel, vidéo, X, indicateurs, conformité, sources, mention IA. À répartir.

## Journal
- 24/11/2026 · Tobias : ajout de la première segmentation (12/10, PPTX + PDF) dans `08 Segmentation/Première version (12-10-2026)` et de la fiche hypothèses dans `10 Hypothèses clients`.
- 24/11/2026 · Eliott : veille stratégique Session 1 (17 informations, 8 champs sur 8, sources contrôlées) dans `09 Veille stratégique`. Concept retenu : magasins compacts. Brique digitale encore à définir.
- 24/11/2026 · Eliott : création du dépôt commun.
- 23/11/2026 · Eliott : envoi à Loris des livrables 01, 02, 03 et du dossier stratégique.
- 05/11/2026 · Eliott : agent Fika (missions 1 et 2 passées au contrôle), dossier IKEA unifié.
