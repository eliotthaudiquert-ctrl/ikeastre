"""Transforme le JSON validé en livrable : tableau Excel sourcé et daté (+ CSV + Markdown).

Usage : python outils/tableur.py travail/mission-1-verification.json <dossier_livrables>"""
import csv
import json
import sys
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

sys.stdout.reconfigure(encoding="utf-8")

BLEU, JAUNE, CREME = "0058A3", "FFDA1A", "F5F3EE"
COULEUR_STATUT = {"Confirmé": "D7EBDD", "Relevé": "D7EBDD", "Nuancé": "FFF1B3", "Infirmé": "F6D2CC",
                  "Non trouvé": "E4E4E4"}
COLONNES = [("id", "Id", 10), ("theme", "Thème", 18), ("sujet", "Sujet", 16), ("question", "Question / critère", 36),
            ("reponse", "Réponse", 52), ("chiffre", "Chiffre clé", 16), ("statut", "Statut", 12),
            ("confiance", "Confiance", 11), ("controle", "Contrôle de l'extrait", 18), ("source_titre", "Source", 34),
            ("editeur", "Éditeur", 18), ("source_url", "Lien", 40), ("date_source", "Date de la source", 14),
            ("date_consultation", "Consulté le", 12), ("extrait", "Extrait exact", 60), ("calcul", "Calcul", 26),
            ("limite", "Limite", 40)]
TITRES = {"verification": "Mission 1 · Vérification de nos hypothèses", "veille": "Mission 2 · Veille concurrentielle Gen Z"}


def libelle_controle(d):
    if not d:
        return ""
    v = d.get("verdict_extrait") or ""
    return {"exact": "Retrouvé mot pour mot", "proche": f"Retrouvé ({int((d.get('score') or 0) * 100)} %)",
            "absent": "Non retrouvé"}.get(v, v.capitalize() if v else "—")


def main():
    src = Path(sys.argv[1])
    out_dir = Path(sys.argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    data = json.loads(src.read_text(encoding="utf-8"))
    ctrl_path = src.with_suffix(".controle.json")
    ctrl = json.loads(ctrl_path.read_text(encoding="utf-8")) if ctrl_path.exists() else {}
    det = {d["id"]: d for d in ctrl.get("detail", [])}
    mission = data.get("mission", "mission")
    jour = data.get("date_execution", "")
    base = out_dir / f"IKEA_Agent_{'Mission1_Verification' if mission == 'verification' else 'Mission2_Veille'}_{jour}"
    lignes = data.get("lignes", [])
    for l in lignes:
        l["controle"] = libelle_controle(det.get(l.get("id")))

    wb = Workbook()
    ws = wb.active
    ws.title = "Tableau sourcé"
    fin = Side(style="thin", color="D9D6CF")
    ws["A1"] = TITRES.get(mission, mission)
    ws["A1"].font = Font(name="Noto Sans", bold=True, size=16, color=BLEU)
    ws["A2"] = (f"Exécuté le {jour} par l'agent Fika · {len(lignes)} lignes · "
                f"contrôle automatique : {'accepté' if ctrl.get('accepte') else 'à revoir'} · "
                "Concept académique, non affilié à IKEA · Données collectées par un agent IA, contrôlées automatiquement puis relues.")
    ws["A2"].font = Font(name="Noto Sans", size=9, color="5B5F66")
    for j, (_, nom, larg) in enumerate(COLONNES, 1):
        c = ws.cell(row=4, column=j, value=nom)
        c.font = Font(name="Noto Sans", bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor=BLEU)
        c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(j)].width = larg
    ws.row_dimensions[4].height = 30
    for i, l in enumerate(lignes, 5):
        for j, (cle, _, _) in enumerate(COLONNES, 1):
            v = l.get(cle, "")
            c = ws.cell(row=i, column=j, value=v)
            c.font = Font(name="Noto Sans", size=9)
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c.border = Border(bottom=fin)
            if cle == "source_url" and str(v).startswith("http"):
                c.hyperlink = v
                c.font = Font(name="Noto Sans", size=9, color=BLEU, underline="single")
            if cle == "statut":
                c.fill = PatternFill("solid", fgColor=COULEUR_STATUT.get(v, "FFFFFF"))
                c.font = Font(name="Noto Sans", size=9, bold=True)
            if cle == "id":
                c.font = Font(name="Noto Sans", size=9, bold=True, color=BLEU)
    ws.freeze_panes = "C5"
    ws.auto_filter.ref = f"A4:{get_column_letter(len(COLONNES))}{4 + len(lignes)}"

    s = wb.create_sheet("Synthèse")
    s.column_dimensions["A"].width = 120
    s["A1"] = "Ce que les données changent pour notre campagne"
    s["A1"].font = Font(name="Noto Sans", bold=True, size=14, color=BLEU)
    r = 3
    for p in data.get("synthese", []):
        s.cell(row=r, column=1, value="• " + p).alignment = Alignment(wrap_text=True, vertical="top")
        r += 1
    r += 1
    s.cell(row=r, column=1, value="À creuser sur le terrain").font = Font(name="Noto Sans", bold=True, size=12, color=BLEU)
    for p in data.get("a_creuser", []):
        r += 1
        s.cell(row=r, column=1, value="• " + p).alignment = Alignment(wrap_text=True, vertical="top")
    r += 2
    s.cell(row=r, column=1, value="Plan suivi par l'agent").font = Font(name="Noto Sans", bold=True, size=12, color=BLEU)
    for p in data.get("plan", []):
        r += 1
        s.cell(row=r, column=1, value="• " + p).alignment = Alignment(wrap_text=True, vertical="top")

    k = wb.create_sheet("Contrôle")
    k.column_dimensions["A"].width = 120
    k["A1"] = f"Contrôle automatique : {'ACCEPTÉ' if ctrl.get('accepte') else 'À REVOIR'}"
    k["A1"].font = Font(name="Noto Sans", bold=True, size=14, color=BLEU)
    k["A2"] = f"Statuts : {ctrl.get('statuts', {})} · lignes valides : {ctrl.get('lignes_valides')}/{ctrl.get('nb_lignes')}"
    r = 4
    for titre, items in (("Erreurs", ctrl.get("erreurs", [])), ("Points à contrôler à la main", ctrl.get("alertes", []))):
        k.cell(row=r, column=1, value=titre).font = Font(name="Noto Sans", bold=True, color=BLEU)
        for it in items or ["Aucun"]:
            r += 1
            k.cell(row=r, column=1, value="• " + it).alignment = Alignment(wrap_text=True)
        r += 2
    wb.save(base.with_suffix(".xlsx"))

    with open(base.with_suffix(".csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow([n for _, n, _ in COLONNES])
        for l in lignes:
            w.writerow([l.get(c, "") for c, _, _ in COLONNES])

    md = [f"# {TITRES.get(mission, mission)}", "", f"Exécuté le {jour} par l'agent Fika. Contrôle automatique : "
          f"{'accepté' if ctrl.get('accepte') else 'à revoir'}. Concept académique, non affilié à IKEA.", "",
          "## Synthèse", ""] + [f"- {p}" for p in data.get("synthese", [])] + ["", "## Tableau sourcé et daté", "",
          "| Id | Question | Réponse | Statut | Source | Date |", "|---|---|---|---|---|---|"]
    for l in lignes:
        src_md = f"[{l.get('editeur') or 'source'}]({l.get('source_url')})" if l.get("source_url") else "—"
        cell = lambda x: str(x or "").replace("|", "/").replace("\n", " ")
        md.append(f"| {cell(l.get('id'))} | {cell(l.get('question'))} | {cell(l.get('reponse'))} | {cell(l.get('statut'))} | {src_md} | {cell(l.get('date_source'))} |")
    md += ["", "## À creuser", ""] + [f"- {p}" for p in data.get("a_creuser", [])]
    base.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print(f"Livrable : {base.with_suffix('.xlsx')}")


if __name__ == "__main__":
    main()
