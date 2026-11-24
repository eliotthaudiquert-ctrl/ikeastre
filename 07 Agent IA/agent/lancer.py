"""Fika · l'agent de recherche IKÉASTRE. Fait tourner la boucle du cours :

  Mission -> 1 Planifier -> 2 Agir (outils) -> 3 Observer -> 4 Vérifier
                 ^------------- non : on reboucle ----------------|
                                            oui -> Livrable : tableau sourcé et daté

Le « modèle qui raisonne » est Claude (Claude Code en mode autonome, abonnement de l'utilisateur).
L'étape Vérifier est double : l'agent se relit, puis outils/verifier.py ouvre chaque source et
cherche l'extrait dans la page. Tant qu'il y a des erreurs (max 3 tours), on reboucle.

Usage : python lancer.py 1 | 2 | 12   (mission 1, mission 2, ou les deux à la suite)
"""
import json
import shutil
import subprocess
import sys
import time
from datetime import date, datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
MISSIONS = {"1": ("1-verification.md", "travail/mission-1-verification.json"),
            "2": ("2-veille.md", "travail/mission-2-veille.json")}
MAX_BOUCLES = 3
OUTILS_AUTORISES = [
    "WebSearch", "WebFetch", "Read", "Write", "Edit", "Glob", "Grep",
    "Bash(python outils/lire_page.py:*)", "Bash(python outils/calcul.py:*)", "Bash(python outils/verifier.py:*)",
]


def trouver_claude():
    for nom in ("claude", "claude.cmd", "claude.exe"):
        p = shutil.which(nom)
        if p:
            return p
    sys.exit("Claude Code introuvable. Installe-le (npm i -g @anthropic-ai/claude-code) puis connecte-toi avec « claude ».")


def court(x, n=160):
    s = x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)
    s = " ".join(s.split())
    return s if len(s) <= n else s[: n - 1] + "…"


class Journal:
    def __init__(self, chemin: Path):
        self.f = open(chemin, "a", encoding="utf-8")
        self.compteurs = {"planifier": 0, "agir": 0, "observer": 0, "verifier": 0}
        self.outils = {}

    def ecrire(self, etape, texte, console=True):
        h = datetime.now().strftime("%H:%M:%S")
        self.f.write(f"- `{h}` **{etape}** · {texte}\n")
        self.f.flush()
        if console:
            print(f"{h}  {etape:<14} {court(texte, 110)}", flush=True)

    def titre(self, t):
        self.f.write(f"\n## {t}\n\n")
        self.f.flush()
        print(f"\n=== {t} ===", flush=True)


def tour(claude, prompt, journal, session=None):
    cmd = [claude, "-p", prompt, "--output-format", "stream-json", "--verbose",
           "--append-system-prompt", (ICI / "SYSTEME.md").read_text(encoding="utf-8"),
           "--permission-mode", "dontAsk", "--allowedTools", *OUTILS_AUTORISES,
           "--disallowedTools", "PowerShell", "--strict-mcp-config", "--model", "opus"]
    if session:
        cmd += ["--resume", session]
    proc = subprocess.Popen(cmd, cwd=ICI, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                            text=True, encoding="utf-8", errors="replace")
    sid, final = session, ""
    noms = {}
    for ligne in proc.stdout:
        try:
            ev = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        t = ev.get("type")
        if t == "system" and ev.get("subtype") == "init":
            sid = ev.get("session_id", sid)
        elif t == "assistant":
            for c in ev.get("message", {}).get("content", []):
                if c.get("type") == "text" and c.get("text", "").strip():
                    journal.compteurs["planifier"] += 1
                    journal.ecrire("1 · Raisonner", c["text"].strip(), console=len(c["text"]) < 400)
                elif c.get("type") == "tool_use":
                    nom, inp = c.get("name"), c.get("input", {})
                    noms[c.get("id")] = nom
                    journal.compteurs["agir"] += 1
                    journal.outils[nom] = journal.outils.get(nom, 0) + 1
                    quoi = inp.get("query") or inp.get("url") or inp.get("command") or inp.get("file_path") or inp
                    journal.ecrire("2 · Agir", f"{nom} → {court(quoi, 200)}")
        elif t == "user":
            for c in ev.get("message", {}).get("content", []) if isinstance(ev.get("message", {}).get("content"), list) else []:
                if c.get("type") == "tool_result":
                    contenu = c.get("content")
                    if isinstance(contenu, list):
                        contenu = " ".join(x.get("text", "") for x in contenu if isinstance(x, dict))
                    journal.compteurs["observer"] += 1
                    etat = "erreur" if c.get("is_error") else "ok"
                    journal.ecrire("3 · Observer", f"{noms.get(c.get('tool_use_id'), 'outil')} ({etat}) : {court(contenu or '', 220)}",
                                   console=False)
        elif t == "result":
            final = ev.get("result", "") or ""
            sid = ev.get("session_id", sid)
            journal.ecrire("Fin du tour", f"{ev.get('num_turns', '?')} échanges, {round((ev.get('duration_ms') or 0) / 60000, 1)} min · {court(final, 200)}")
    proc.wait()
    err = proc.stderr.read()
    if proc.returncode and err:
        journal.ecrire("Incident", court(err, 400))
    return sid, final


def mission(num, claude):
    fichier_mission, sortie = MISSIONS[num]
    (ICI / "travail").mkdir(exist_ok=True)
    (ICI / "journal").mkdir(exist_ok=True)
    jour = date.today().isoformat()
    jpath = ICI / "journal" / f"{datetime.now():%Y-%m-%d_%H%M}_mission-{num}.md"
    j = Journal(jpath)
    j.f.write(f"# Journal de Fika · mission {num} · {jour}\n\nChaque ligne est une étape de la boucle : "
              "1 Planifier/raisonner, 2 Agir (outil), 3 Observer (résultat), 4 Vérifier.\n")
    sortie_p = ICI / sortie
    if sortie_p.exists():
        sortie_p.rename(sortie_p.with_name(sortie_p.stem + f".ancien-{datetime.now():%H%M%S}.json"))

    texte_mission = (ICI / "missions" / fichier_mission).read_text(encoding="utf-8")
    prompt = (f"Date du jour : {jour}.\n\n{texte_mission}\n\n"
              f"Commence par l'étape 1 : écris ton plan dans travail/plan-mission-{num}.md (notes dans travail/notes-mission-{num}.md). Ensuite cherche, lis les pages "
              "(outils/lire_page.py te donne le texte exact que le contrôleur verra), note, calcule avec outils/calcul.py, "
              f"puis écris {sortie}. Avant de finir, lance toi-même python outils/verifier.py {sortie} et corrige les erreurs.")
    j.titre("Mission")
    j.ecrire("Mission", f"{fichier_mission} → {sortie}")
    debut = time.time()
    session = None
    accepte = False
    for boucle in range(1, MAX_BOUCLES + 1):
        j.titre(f"Tour {boucle}")
        session, _ = tour(claude, prompt, j, session)
        j.titre(f"4 · Vérifier (tour {boucle})")
        if not sortie_p.exists():
            rapport = {"accepte": False, "erreurs": [f"le fichier {sortie} n'a pas été écrit"], "alertes": []}
        else:
            subprocess.run([sys.executable, str(ICI / "outils" / "verifier.py"), sortie], cwd=ICI)
            rapport = json.loads(sortie_p.with_suffix(".controle.json").read_text(encoding="utf-8"))
        j.compteurs["verifier"] += 1
        if rapport["accepte"]:
            j.ecrire("4 · Vérifier", f"oui · {rapport.get('lignes_valides')}/{rapport.get('nb_lignes')} lignes valides, "
                                    f"{len(rapport.get('alertes', []))} points à contrôler à la main")
            accepte = True
            break
        j.ecrire("4 · Vérifier", f"non · {len(rapport['erreurs'])} erreurs → on reboucle")
        for e in rapport["erreurs"][:40]:
            j.ecrire("  erreur", e, console=False)
        prompt = ("Le contrôleur automatique a REFUSÉ ton livrable. Reprends la boucle pour chaque ligne en erreur : "
                  "replanifie, cherche une meilleure source ou recopie l'extrait exact avec outils/lire_page.py, "
                  f"puis réécris {sortie} en entier et relance le contrôleur.\n\nErreurs :\n- " + "\n- ".join(rapport["erreurs"][:60]))

    j.titre("Livrable")
    if sortie_p.exists():
        subprocess.run([sys.executable, str(ICI / "outils" / "tableur.py"), sortie, str(RACINE / "livrables")], cwd=ICI)
        shutil.copy(sortie_p, RACINE / "livrables" / sortie_p.name)
    duree = round((time.time() - debut) / 60, 1)
    bilan = (f"{'Accepté' if accepte else 'Rendu avec erreurs restantes'} · {duree} min · "
             f"{j.compteurs['agir']} actions ({', '.join(f'{k} {v}' for k, v in sorted(j.outils.items(), key=lambda x: -x[1]))}) · "
             f"{j.compteurs['verifier']} vérification(s)")
    j.ecrire("Bilan", bilan)
    (ICI / "journal" / f"bilan-mission-{num}.json").write_text(json.dumps(
        {"mission": num, "date": jour, "accepte": accepte, "duree_min": duree, "compteurs": j.compteurs,
         "outils": j.outils, "boucles": j.compteurs["verifier"], "journal": jpath.name}, ensure_ascii=False, indent=2),
        encoding="utf-8")
    return accepte


def main():
    choix = sys.argv[1] if len(sys.argv) > 1 else "12"
    claude = trouver_claude()
    for num in choix:
        if num in MISSIONS:
            mission(num, claude)
    print("\nTerminé. Les tableaux sont dans le dossier « livrables ».")


if __name__ == "__main__":
    main()
