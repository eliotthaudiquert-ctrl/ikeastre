"""Liste les produits IKEA France (API de recherche publique) triés par prix.
Usage : python travail/prix_ikea.py "requête" [filtre_texte]"""
import json
import sys
from pathlib import Path
from urllib.parse import quote

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "outils"))
from pages import lire  # noqa: E402

q = sys.argv[1]
filtre = sys.argv[2].lower() if len(sys.argv) > 2 else ""
url = f"https://sik.search.blue.cdtapps.com/fr/fr/search-result-page?q={quote(q)}&types=PRODUCT&size=100"
data = json.loads(lire(url)["texte"])
items = data["searchResultPage"]["products"]["main"]["items"]
rows = []
for it in items:
    p = it.get("product") or {}
    if not p:
        continue
    prix = (p.get("salesPrice") or {}).get("numeral")
    txt = f'{p.get("name")} | {p.get("typeName")} | {p.get("itemMeasureReferenceText")} | {p.get("mainImageAlt", "")}'
    if filtre and filtre not in txt.lower():
        continue
    rows.append((prix if prix is not None else 99999, txt, p.get("pipUrl")))
for prix, txt, u in sorted(rows)[:15]:
    print(prix, "€ |", txt[:140], "|", u)
