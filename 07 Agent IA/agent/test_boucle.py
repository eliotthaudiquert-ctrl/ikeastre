"""Test du garde-fou : on sabote une copie du livrable (un faux chiffre, une date dans le futur),
le contrôleur la refuse, on la renvoie à l'agent avec la liste des erreurs, il reboucle et répare.
Usage : python test_boucle.py   (journal dans journal/…_test-boucle.md)"""
import json
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
from lancer import Journal, tour, trouver_claude  # noqa: E402

SAB = "travail/test-garde-fou/mission-1-sabotee.json"
REP = "travail/test-garde-fou/mission-1-reparee.json"


def controle(chemin):
    subprocess.run([sys.executable, str(ICI / "outils" / "verifier.py"), chemin], cwd=ICI)
    return json.loads((ICI / chemin).with_suffix(".controle.json").read_text(encoding="utf-8"))


def main():
    claude = trouver_claude()
    j = Journal(ICI / "journal" / f"{datetime.now():%Y-%m-%d_%H%M}_test-boucle.md")
    j.f.write("# Test du garde-fou : livrable saboté, l'agent doit reboucler\n")
    shutil.copy(ICI / SAB, ICI / REP)
    session = None
    for boucle in range(1, 4):
        j.titre(f"4 · Vérifier (tour {boucle})")
        r = controle(REP)
        if r["accepte"]:
            j.ecrire("4 · Vérifier", f"oui · {r['lignes_valides']}/{r['nb_lignes']} lignes valides")
            break
        j.ecrire("4 · Vérifier", f"non · {len(r['erreurs'])} erreurs → on reboucle")
        for e in r["erreurs"]:
            j.ecrire("  erreur", e)
        j.titre(f"Tour {boucle} · l'agent reprend")
        prompt = (f"Date du jour : {datetime.now():%Y-%m-%d}. Le contrôleur automatique a REFUSÉ le livrable {REP}. "
                  "Reprends la boucle (planifier, agir, observer, vérifier) uniquement pour les lignes en erreur : "
                  "rouvre la source avec outils/lire_page.py, recopie l'extrait exact, corrige le chiffre, la réponse et la date "
                  f"d'après la page, puis réécris {REP} en entier (les autres lignes inchangées) et relance "
                  f"python outils/verifier.py {REP}.\n\nErreurs :\n- " + "\n- ".join(r["erreurs"]))
        session, _ = tour(claude, prompt, j, session)
    print("Fin du test.")


if __name__ == "__main__":
    main()
