"""Outil de l'agent : lire le texte exact d'une page (HTML ou PDF).

Usage :
  python outils/lire_page.py <url>                  -> début du texte
  python outils/lire_page.py <url> "mot1" "mot2"    -> passages exacts autour des mots-clés

Les passages renvoyés sont le texte que le contrôleur verra : un extrait copié
d'ici sera toujours retrouvé."""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
from pages import lire  # noqa: E402


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    url, mots = sys.argv[1], sys.argv[2:]
    r = lire(url)
    if not r["ok"]:
        print(f"ÉCHEC de lecture ({r['erreur'] or r['statut_http']}). Essaie WebFetch ou une autre source.")
        return
    t = r["texte"]
    print(f"OK · {len(t)} caractères · {r['type'][:40]}")
    if not mots:
        print(t[:4000])
        return
    vus = 0
    for mot in mots:
        for m in re.finditer(re.escape(mot), t, flags=re.I):
            a, b = max(0, m.start() - 350), min(len(t), m.end() + 350)
            print(f"\n--- « {mot} » ---\n{t[a:b]}")
            vus += 1
            if vus >= 12:
                return
    if not vus:
        print("Aucun des mots-clés n'apparaît dans le texte de la page.")


if __name__ == "__main__":
    main()
