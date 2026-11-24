// Avancement du projet IKÉASTRE : c'est ce fichier qu'affiche Avancement.html.
// Chaque Claude le met à jour après une modif (état, journal), puis synchronise.
// États possibles : "fait", "en cours", "à faire", "à confirmer".
// Liens : chemins relatifs depuis la racine du dépôt.

window.AVANCEMENT = {
  maj: "24/11/2026",
  par: "Tobias",

  prochaine: {
    titre: "Choisir la brique digitale du magasin compact",
    detail: "Le cours demande une expérience digitale pour 2030. La veille donne quatre pistes : scanner sa pièce (IKEA Kreativ), retrait de commandes, reprise des meubles usagés, assistant IA. À trancher à trois avant la Session 2.",
    qui: "L'équipe"
  },

  cours: {
    nom: "Veille stratégique, business model & arbitrages budgétaires",
    rendu: "Dossier PFR Bloc 1 : 10 à 12 pages, PDF, en groupe, avec deux scénarios budgétaires (minimal viable et ambitieux).",
    etapes: [
      { session: "Session 1", titre: "Veille stratégique", detail: "Grille des 8 champs : 17 informations sourcées sur les magasins compacts, angle MARKET. Plus les 5 dimensions, les réponses aux 5 questions MARKET et le plan de veille continue.", etat: "fait",
        liens: [["PDF", "09 Veille stratégique/Veille stratégique IKEA compacts.pdf"], ["Excel", "09 Veille stratégique/Veille stratégique IKEA compacts.xlsx"], ["Grille du cours", "09 Veille stratégique/Grille de veille (modèle du cours).xlsx"], ["Présentation", "09 Veille stratégique/Présentation veille Session 1.pdf"]] },
      { session: "Session 2", titre: "Synthèse décisionnelle", detail: "Hiérarchiser les tendances et en tirer les décisions.", etat: "à faire" },
      { session: "Sessions 3-4", titre: "Business model", detail: "Comment le projet crée de la valeur.", etat: "à faire" },
      { session: "Session 5", titre: "Budget et arbitrages", detail: "Deux scénarios chiffrés, choix justifiés.", etat: "à faire" },
      { session: "Session 6", titre: "Recommandations et dossier final", detail: "Assembler le dossier de 10 à 12 pages.", etat: "à faire" }
    ]
  },

  livrables: [
    { num: "01", titre: "Segmentation", etat: "fait", lien: "IKEA - Envoi livrables PFR/01 Segmentation IKEA Gen Z.pdf" },
    { num: "02", titre: "Personas", etat: "fait", lien: "IKEA - Envoi livrables PFR/02 Personas IKEA Gen Z.pdf" },
    { num: "03", titre: "Veille concurrentielle sourcée", etat: "fait", lien: "IKEA - Envoi livrables PFR/03 Veille concurrentielle sourcee.xlsx" },
    { num: "04", titre: "Positionnement", etat: "en cours", note: "Pas de version dédiée : couvert en partie par le dossier stratégique (mapping p. 6-7).", lien: "IKEA - Envoi livrables PFR/03-06 Dossier strategique (mapping, canvas, promesse).pdf" },
    { num: "05", titre: "Canvas", etat: "fait", note: "Dans le dossier stratégique, p. 12.", lien: "IKEA - Envoi livrables PFR/03-06 Dossier strategique (mapping, canvas, promesse).pdf" },
    { num: "06", titre: "Promesse", etat: "fait", note: "Dans le dossier stratégique, p. 13.", lien: "IKEA - Envoi livrables PFR/03-06 Dossier strategique (mapping, canvas, promesse).pdf" },
    { num: "07", titre: "Note d'arbitrage", etat: "à faire", note: "Pas encore de version dédiée." }
  ],

  campagne: [
    { titre: "Reel « Des meubles pour tous les rebondissements »", etat: "fait", lien: "05 Campagne/Vidéo IKEA/IKEA - Des meubles pour tous les rebondissements.mp4" },
    { titre: "Affiche « 67 raisons de refaire ta déco »", etat: "à confirmer", note: "Notée faite dans le backlog, mais aucun fichier dans le dépôt." },
    { titre: "Carrousel Instagram des faux produits", etat: "à faire" },
    { titre: "Vidéo des noms lus à voix haute", etat: "à faire" },
    { titre: "5 posts décalés sur X", etat: "à faire" },
    { titre: "Indicateurs de campagne", etat: "à faire" },
    { titre: "Contrôle conformité (mention « concept académique »)", etat: "à faire" },
    { titre: "Liste des sources à jour", etat: "à faire" },
    { titre: "Mention IA dans chaque livrable", etat: "à faire" }
  ],

  attente: [
    { quoi: "Accepter l'invitation au dépôt GitHub (compte tbsrgt)", qui: "Tobias" },
    { quoi: "Tester les hypothèses clients auprès de vrais clients : aucune n'est validée", qui: "L'équipe" },
    { quoi: "Répartir les livrables de campagne : aucun responsable attribué", qui: "L'équipe" }
  ],

  documents: [
    ["Dossier stratégique d'équipe", "02 Dossier et oral Gen Z/Versions Codex (copies)/B3CPD_IKEA_Equipe.pdf"],
    ["Synthèse en 5 slides", "02 Dossier et oral Gen Z/IKEA_GenZ_Synthese_5_slides_v2.pdf"],
    ["Segmentation Gen Z", "08 Segmentation/Segmentation IKEA Gen Z.pdf"],
    ["Première segmentation (12/10)", "08 Segmentation/Première version (12-10-2026)/Segmentation IKEA.pdf"],
    ["Fiche hypothèses clients", "10 Hypothèses clients/Fiche hypothèses IKEA.html"],
    ["Atelier brief déconstruit", "06 Atelier brief déconstruit/Atelier brief déconstruit.pdf"],
    ["Kit de pilotage agile", "04 Pilotage agile/B3CPD_IKEA_Kit_Pilotage_Agile.xlsx"],
    ["Agent de recherche Fika", "07 Agent IA/LISEZ-MOI.md"],
    ["Consigne EFN", "01 Consignes et cours/Consigne EFN B3CPD.pdf"]
  ],

  journal: [
    { date: "24/11/2026", qui: "Tobias", quoi: "Présentation orale de la veille Session 1 : 11 slides en PDF (une idée par slide), générée depuis veille.json." },
    { date: "24/11/2026", qui: "Tobias", quoi: "Veille Session 1, compléments MARKET : 5 dimensions, 5 questions MARKET, plan de veille continue (PDF de 9 à 12 pages) et grille du cours remplie." },
    { date: "24/11/2026", qui: "Eliott", quoi: "Page d'avancement du projet (Avancement.html)." },
    { date: "24/11/2026", qui: "Tobias", quoi: "Ajout de la première segmentation (12/10, PPTX + PDF) et de la fiche d'hypothèses clients." },
    { date: "24/11/2026", qui: "Eliott", quoi: "Veille stratégique Session 1 : 17 informations, 8 champs sur 8, sources contrôlées. Concept retenu : magasins compacts." },
    { date: "24/11/2026", qui: "Eliott", quoi: "Création du dépôt commun." },
    { date: "23/11/2026", qui: "Eliott", quoi: "Envoi à Loris des livrables 01, 02, 03 et du dossier stratégique." },
    { date: "05/11/2026", qui: "Eliott", quoi: "Agent Fika (missions 1 et 2 passées au contrôle), dossier IKEA unifié." }
  ]
};
