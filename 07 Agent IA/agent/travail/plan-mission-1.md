# Plan · Mission 1 · Vérifier nos hypothèses (2026-11-05)

| Case | Requêtes à tester | Source visée |
|---|---|---|
| Q1.a | "IKEA France nombre de magasins 2025", "IKEA France points de contact studio planification centre-ville", "Ingka IKEA France chiffres clés" | IKEA France newsroom / Ingka (niveau 2) |
| Q1.b | "part des 18-24 ans titulaires du permis de conduire Insee", "jeunes sans voiture SDES enquête mobilité", "taux de permis 18-24 ans" | Insee, SDES (niveau 1), sinon ministère/Crédoc |
| Q1.c | "IKEA Lyon Vénissieux accès tram", "IKEA Lille Lomme accès métro bus", pages magasin ikea.com/fr/stores | Page magasin IKEA (niveau 2) |
| Q2.a | "IKEA livraison tarif à partir de", ikea.com/fr/fr/customer-service/services/delivery | Page service IKEA France (relevé daté) |
| Q2.b | "Fevad frais de livraison abandon panier", "Baymard cart abandonment extra costs" | Fevad / Médiamétrie, sinon Baymard (international, le dire) |
| Q3.a | "Oracle Happiness Report humour marques 2022", "humour marketing Gen Z étude achat" | Étude institut (Oracle/Gretchen Rubin, Kantar) |
| Q3.b | "TikTok made me buy it étude", "Gen Z découverte produits réseaux sociaux étude France" | Institut / TikTok / Médiamétrie / Ifop |
| Q4.a | ikea.com/fr pages produits les moins chers : lit (MALM/NEIDEN/SNIGLAR...), sommier (LURÖY), matelas (ÅFJÄLL/ VADSÖ), bureau (LINNMON/MICKE), chaise (ADDE/TEODORES), penderie (BRIMNES/RAKKESTAD/ MULIG) | ikea.com/fr (relevé du jour) |
| Q4.a-total | calcul.py somme, comparaison 700/350 | calcul |
| Q4.b | "coût de la rentrée étudiante UNEF 2025 frais d'installation", "OVE budget étudiants installation", "FAGE indicateur coût de la rentrée" | UNEF/FAGE (niveau 3), OVE (niveau 1) |
| Q5.a | "Insee mobilité résidentielle jeunes 18-29 ans déménagent", "Insee Première mobilité résidentielle 2024" | Insee national |
| Q5.b | "Ipea un meuble sur quatre occasion", "Ipea marché meuble occasion 2024" | Ipea / presse spécialisée |
| Q5.c | "IKEA Family members millions 2024 2025", "Ingka annual summary IKEA Family members" | Ingka annual summary |
| Q5.d | "Insee Première 2090", "79 % ménages moins de 30 ans installés depuis moins de 4 ans" | insee.fr |

Méthode : WebSearch → lire_page.py pour l'extrait exact → notes → JSON → verifier.py.
