"""Rouvre chaque source de veille.json et cherche l'extrait mot pour mot (texte normalisé)."""
import json, re, sys, unicodedata
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "07 Agent IA" / "agent" / "outils"))
from pages import lire

def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("’", "'").replace("‘", "'").replace("«", '"').replace("»", '"')
    s = re.sub(r"[\u00a0\u202f\s]+", " ", s)
    return s.strip()

d = json.load(open(Path(__file__).with_name("veille.json"), encoding="utf-8"))
srcs = [("Contexte", d["contexte"]["source"])] + [(l["champ"], l["source"]) for l in d["lignes"]]
ok = ko = 0
for champ, s in srcs:
    r = lire(s["url"])
    if not r["ok"]:
        print(f"?  {champ:22} lecture impossible ({r['erreur']}) {s['url'][:70]}"); ko += 1; continue
    hit = norm(s["extrait"]) in norm(r["texte"])
    print(f"{'OK' if hit else 'KO'} {champ:22} {s['organisme'][:40]}")
    ok += hit; ko += (not hit)
print(f"\n{ok} extraits retrouvés, {ko} à contrôler à la main")
