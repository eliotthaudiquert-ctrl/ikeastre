"""Étape 4 de la boucle : VÉRIFIER. Contrôle automatique du livrable de l'agent.

Usage : python outils/verifier.py travail/mission-1-verification.json
Écrit <fichier>.controle.json et affiche un rapport. Code de sortie 0 = livrable accepté,
1 = des erreurs bloquantes (on reboucle)."""
import json
import re
import sys
from datetime import date
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
from pages import lire, trouver_extrait  # noqa: E402

CHAMPS = ["id", "theme", "question", "sujet", "reponse", "chiffre", "calcul", "statut", "confiance",
          "source_titre", "editeur", "source_url", "date_source", "date_consultation", "extrait", "limite"]
STATUTS = {"Confirmé", "Nuancé", "Infirmé", "Non trouvé", "Relevé"}
CONFIANCES = {"Haute", "Moyenne", "Faible"}
DATE_RE = re.compile(r"^(\d{4})(-\d{2})?(-\d{2})?$")
# sites qui bloquent les robots : extrait non vérifiable automatiquement (avertissement, pas erreur)
BLOQUEURS = ("tiktok.com", "instagram.com", "facebook.com", "x.com", "twitter.com", "linkedin.com")

ATTENDU = {
    "verification": ["Q1.a", "Q1.b", "Q1.c", "Q2.a", "Q2.b", "Q3.a", "Q3.b", "Q4.a", "Q4.a-total", "Q4.b",
                     "Q5.a", "Q5.b", "Q5.c", "Q5.d"],
    "veille": [f"V{c}.{a}" for c in range(1, 7)
               for a in ["IKEA", "Maisons du Monde", "Conforama", "But", "Action", "Leboncoin"]],
}


def norm_id(s):
    return re.sub(r"\s+", "", s or "").lower()


def controler(chemin: Path) -> dict:
    erreurs, alertes, lignes_ok = [], [], 0
    try:
        data = json.loads(chemin.read_text(encoding="utf-8"))
    except Exception as e:
        return {"accepte": False, "erreurs": [f"JSON illisible : {e}"], "alertes": [], "detail": []}

    mission = data.get("mission", "")
    lignes = data.get("lignes") or []
    if mission not in ATTENDU:
        erreurs.append(f"champ mission = « {mission} », attendu verification ou veille")
    if not lignes:
        erreurs.append("aucune ligne dans le tableau")
    if not data.get("synthese"):
        erreurs.append("synthèse vide")

    # couverture : chaque id attendu doit avoir au moins une ligne (préfixe accepté, ex. Q1.a-2)
    ids = [norm_id(l.get("id")) for l in lignes]
    for att in ATTENDU.get(mission, []):
        a = norm_id(att)
        if not any(i == a or i.startswith(a + "-") or i.startswith(a + "_") for i in ids):
            if not (att == "Q4.a-total" and any(i.startswith("q4.a-tot") for i in ids)):
                erreurs.append(f"{att} : aucune ligne pour cette question / case")

    detail = []
    aujourd_hui = date.today().isoformat()
    for l in lignes:
        lid = l.get("id", "?")
        d = {"id": lid, "verdict_extrait": "", "score": None, "http": None, "problemes": []}
        manquants = [c for c in CHAMPS if c not in l]
        if manquants:
            d["problemes"].append(("erreur", f"champs manquants : {', '.join(manquants)}"))
        statut = l.get("statut", "")
        if statut not in STATUTS:
            d["problemes"].append(("erreur", f"statut « {statut} » non autorisé"))
        if l.get("confiance") not in CONFIANCES:
            d["problemes"].append(("erreur", f"confiance « {l.get('confiance')} » non autorisée"))
        if not (l.get("reponse") or "").strip():
            d["problemes"].append(("erreur", "réponse vide"))
        dc = l.get("date_consultation", "")
        if not DATE_RE.match(dc or ""):
            d["problemes"].append(("erreur", f"date_consultation « {dc} » invalide"))
        elif dc > aujourd_hui:
            d["problemes"].append(("erreur", f"date_consultation dans le futur ({dc})"))

        if statut != "Non trouvé":
            url = (l.get("source_url") or "").strip()
            ds = l.get("date_source", "")
            if not (ds == "inconnue" or DATE_RE.match(ds or "")):
                d["problemes"].append(("erreur", f"date_source « {ds} » invalide (AAAA-MM-JJ, AAAA-MM, AAAA ou inconnue)"))
            elif ds == "inconnue":
                d["problemes"].append(("alerte", "date de la source inconnue"))
            elif ds[:10] > aujourd_hui:
                d["problemes"].append(("erreur", f"date_source dans le futur ({ds})"))
            if not url.startswith("http"):
                d["problemes"].append(("erreur", "source_url manquante alors que la ligne n'est pas « Non trouvé »"))
            ext = (l.get("extrait") or "").strip()
            if len(ext) < 25:
                d["problemes"].append(("erreur", "extrait trop court ou absent (40 à 300 caractères copiés de la page)"))
            if url.startswith("http") and len(ext) >= 25:
                if any(b in url for b in BLOQUEURS):
                    d["verdict_extrait"] = "non vérifiable (réseau social)"
                    d["problemes"].append(("alerte", "réseau social : extrait non vérifiable automatiquement, à contrôler à la main"))
                else:
                    page = lire(url)
                    d["http"] = page.get("statut_http")
                    if not page["ok"]:
                        d["verdict_extrait"] = "page illisible"
                        d["problemes"].append(("alerte", f"page illisible par le contrôleur ({page['erreur']}) : à contrôler à la main"))
                    else:
                        v, s = trouver_extrait(ext, page["texte"])
                        d["verdict_extrait"], d["score"] = v, s
                        if v == "absent":
                            d["problemes"].append(("erreur", f"extrait introuvable dans la page (score {s}) : recopie-le mot pour mot avec outils/lire_page.py, ou change de source"))
            # le chiffre annoncé doit se retrouver dans l'extrait ou le calcul
            ch = re.findall(r"\d[\d\s.,]*\d|\d", l.get("chiffre") or "")
            base = re.sub(r"[\s  ]", "", (ext + " " + (l.get("calcul") or "") + " " + (l.get("reponse") or "")))
            for c in ch:
                cc = re.sub(r"[\s  ]", "", c)
                if cc and cc not in base and cc.replace(",", ".") not in base and cc.replace(".", ",") not in base:
                    d["problemes"].append(("alerte", f"le chiffre « {c} » n'apparaît ni dans l'extrait ni dans le calcul"))
                    break
        for niveau, msg in d["problemes"]:
            (erreurs if niveau == "erreur" else alertes).append(f"{lid} : {msg}")
        if not any(n == "erreur" for n, _ in d["problemes"]):
            lignes_ok += 1
        detail.append(d)

    stats = {}
    for l in lignes:
        stats[l.get("statut", "?")] = stats.get(l.get("statut", "?"), 0) + 1
    return {"accepte": not erreurs, "mission": mission, "nb_lignes": len(lignes), "lignes_valides": lignes_ok,
            "statuts": stats, "erreurs": erreurs, "alertes": alertes, "detail": detail,
            "date_controle": aujourd_hui}


def main():
    chemin = Path(sys.argv[1])
    rapport = controler(chemin)
    out = chemin.with_suffix(".controle.json")
    out.write_text(json.dumps(rapport, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Contrôle : {'ACCEPTÉ' if rapport['accepte'] else 'REFUSÉ'} · {rapport.get('lignes_valides', 0)}/{rapport.get('nb_lignes', 0)} lignes valides")
    for e in rapport["erreurs"]:
        print("  ✗", e)
    for a in rapport["alertes"]:
        print("  !", a)
    sys.exit(0 if rapport["accepte"] else 1)


if __name__ == "__main__":
    main()
