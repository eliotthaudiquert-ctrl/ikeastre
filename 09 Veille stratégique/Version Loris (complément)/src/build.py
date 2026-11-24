# -*- coding: utf-8 -*-
"""Génère la grille de veille IKÉASTRE en HTML (→ PDF via Chrome headless) et en Excel."""
import html, subprocess, sys
from pathlib import Path
from collections import OrderedDict
from data import ROWS, QUESTIONS, CONSULT

HERE = Path(__file__).parent
OUT = HERE.parent
BASE = "IKEASTRE_Veille-strategique_Grille_2026-11-24"
e = html.escape

CHAMPS = ["Tendances lourdes", "Innovations", "Durabilité", "Accessibilité",
          "Inclusion", "Évolutions des usages", "Réglementation", "Signaux faibles"]
TAG = {"Documenté": "doc", "Projection": "proj", "Signal faible": "sf"}

CSS = """
@page { size: A4 landscape; margin: 11mm 11mm 12mm; }
* { box-sizing: border-box; }
body { font-family: 'Noto Sans', 'Helvetica Neue', Arial, sans-serif; color: #111; font-size: 8.4pt; line-height: 1.35; margin: 0; }
.blue { color: #0058A3; }
.cover { height: 186mm; display: flex; flex-direction: column; justify-content: space-between; page-break-after: always; }
.band { background: #0058A3; color: #fff; padding: 14mm 14mm 12mm; border-radius: 3mm; }
.band .k { color: #FFDB00; font-weight: 700; letter-spacing: .08em; font-size: 9pt; }
.band h1 { font-size: 30pt; margin: 4mm 0 3mm; line-height: 1.05; }
.band p { font-size: 11pt; margin: 0; max-width: 200mm; }
.grid3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6mm; }
.box { border: 1px solid #d5dde6; border-radius: 2mm; padding: 4mm 5mm; }
.box h3 { margin: 0 0 2mm; font-size: 10pt; color: #0058A3; }
.box ul { margin: 0; padding-left: 4mm; } .box li { margin-bottom: 1mm; }
.meta { font-size: 8pt; color: #555; }
h2 { font-size: 15pt; margin: 0 0 1mm; }
.sub { color: #555; margin: 0 0 4mm; }
table { width: 100%; border-collapse: collapse; table-layout: fixed; }
thead th { background: #0058A3; color: #fff; text-align: left; padding: 2mm; font-size: 8.4pt; }
td { border-bottom: 1px solid #d5dde6; padding: 2mm; vertical-align: top; }
tr { page-break-inside: avoid; }
td.champ { background: #F2F6FA; font-weight: 700; color: #0058A3; }
td.champ .n { display: block; font-weight: 400; color: #555; font-size: 7.6pt; margin-top: 1mm; }
.tag { display: inline-block; font-size: 6.8pt; font-weight: 700; padding: .4mm 1.6mm; border-radius: 1mm; margin-top: 1.4mm; }
.tag.doc { background: #E3F1E6; color: #1E6B34; } .tag.proj { background: #FFF5C2; color: #6B5600; } .tag.sf { background: #F3E5F5; color: #6A1B7A; }
td.src a { color: #0058A3; word-break: break-all; font-size: 7.2pt; }
tr.first td { border-top: 2px solid #0058A3; }
.pb { page-break-before: always; }
.q td { font-size: 8.8pt; }
.legend span { margin-right: 6mm; }
.foot { margin-top: 4mm; font-size: 7.4pt; color: #666; }
"""

def cover():
    counts = OrderedDict((c, sum(1 for r in ROWS if r["champ"] == c)) for c in CHAMPS)
    lis = "".join(f"<li><b>{e(c)}</b> — {n} information{'s' if n > 1 else ''}</li>" for c, n in counts.items())
    return f"""
<section class="cover">
  <div class="band">
    <div class="k">IKÉASTRE · IKEA × GEN Z · LIVRABLE INTERMÉDIAIRE</div>
    <h1>Veille stratégique<br>en huit champs</h1>
    <p>Ce qui bouge autour d'IKEA et des 18-25 ans qui s'installent : faits sourcés, lecture critique et conséquences pour notre projet « Garder la génération Z entre deux cartons ».</p>
  </div>
  <div class="grid3">
    <div class="box"><h3>Ce que contient la grille</h3><ul>{lis}</ul>
      <p class="meta">{len(ROWS)} informations · {len(QUESTIONS)} questions à creuser</p></div>
    <div class="box"><h3>Comment la lire</h3><ul>
      <li><span class="tag doc">Documenté</span> fait publié, vérifiable par le lien.</li>
      <li><span class="tag proj">Projection</span> objectif ou calendrier annoncé, pas encore réalisé.</li>
      <li><span class="tag sf">Signal faible</span> fait isolé ; c'est notre interprétation qui en fait un signal.</li>
      <li>Colonne « Analyse critique » : limites de la source, ce qu'elle ne prouve pas.</li>
      <li>Colonne « Impact » : lien explicite avec les personas (Léa, Noah, Inès), le VPC et la campagne.</li></ul></div>
    <div class="box"><h3>Rappel du projet</h3><ul>
      <li>Brief : « Nos 18-25 ans ne reviennent pas après leur premier emménagement. On veut une carte étudiante à −10 %. »</li>
      <li>Notre lecture : le prix n'est pas la seule cause ; l'enjeu est de rester présent entre deux moments de vie.</li>
      <li>Promesse de travail : « Un premier chez-soi qui vous ressemble, avec un budget compris et une installation préparée. »</li></ul></div>
  </div>
  <p class="meta">Tobias Ringot, Eliott Haudiquert & Loris Demeaux · B3 · Veille stratégique, business model & arbitrages budgétaires · Sources consultées le {CONSULT}. Projet académique indépendant, sans commande ni validation d'IKEA. Personas = profils de travail fictifs, aucun entretien terrain à ce jour.</p>
</section>"""

def grid():
    rows, prev = [], None
    for r in ROWS:
        first = r["champ"] != prev
        prev = r["champ"]
        rows.append(f"""<tr class="{'first' if first else ''}">
<td class="champ">{e(r['champ'])}<span class="n">{e(r['n'])}</span><span class="tag {TAG[r['statut']]}">{e(r['statut'])}</span></td>
<td>{e(r['info'])}</td>
<td class="src">{e(r['src'])}<br><a href="{e(r['url'])}">{e(r['url'])}</a></td>
<td>{e(r['analyse'])}</td>
<td>{e(r['impact'])}</td></tr>""")
    return f"""
<h2>La grille de veille</h2>
<p class="sub">Une ligne par information. Les tendances lourdes comptent cinq évolutions distinctes, comme demandé ; chaque autre champ en compte deux ou trois.</p>
<table>
<colgroup><col style="width:11%"><col style="width:23%"><col style="width:18%"><col style="width:23%"><col style="width:25%"></colgroup>
<thead><tr><th>Champ de veille</th><th>Information / tendance identifiée</th><th>Source fiable et date</th><th>Analyse critique</th><th>Impact pour le projet</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table>"""

def questions():
    trs = "".join(f"<tr><td class='champ'>{e(c)}</td><td>{e(q)}</td></tr>" for c, q in QUESTIONS)
    return f"""
<section class="pb">
<h2>Ce qu'il reste à chercher</h2>
<p class="sub">Les questions qui nécessitent des recherches complémentaires, classées par champ. Elles alimentent la suite du module (business model, arbitrages budgétaires).</p>
<table class="q"><colgroup><col style="width:16%"><col></colgroup>
<thead><tr><th>Champ</th><th>Question ouverte et piste de source</th></tr></thead><tbody>{trs}</tbody></table>
<div class="grid3" style="margin-top:6mm">
  <div class="box"><h3>Trois enseignements pour le projet</h3><ul>
    <li>Le concurrent principal reste l'occasion, et elle devient aussi simple que le neuf (TL2, SF2).</li>
    <li>Le prix seul ne suffit pas : le meilleur prix IKEA est souvent réservé au magasin, donc aux clients motorisés (AC1, AC2).</li>
    <li>IKEA a déjà les preuves (compacts, KOMPISHÄNG, Kreativ, reprise) : le travail est de les rendre visibles là où la Gen Z cherche (US1, US2).</li></ul></div>
  <div class="box"><h3>Corrections par rapport aux dossiers précédents</h3><ul>
    <li>Billy à 34,99 € = prix magasin seulement, pas une baisse générale (dossier V3, p. 9).</li>
    <li>IKEA Preowned : toujours pas annoncé en France au 24/11/2026.</li>
    <li>ThisAbles : projet israélien de 2019, à ne pas présenter comme une offre actuelle.</li></ul></div>
  <div class="box"><h3>Règles suivies</h3><ul>
    <li>Huit champs traités, au moins une information par champ.</li>
    <li>Chaque source : organisme, titre, date, lien.</li>
    <li>Informations reformulées avec nos mots ; chiffres repris tels que publiés.</li>
    <li>Tendance documentée ≠ projection ≠ signal faible (étiquette sur chaque ligne).</li></ul></div>
</div>
<p class="foot">Quand une date de publication exacte n'a pas pu être retrouvée, le mois ou l'année est indiqué. Les liens ont été consultés le {CONSULT}.</p>
</section>"""

def build_html():
    doc = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>IKÉASTRE · Veille stratégique</title>
<style>{CSS}</style></head><body>{cover()}{grid()}{questions()}</body></html>"""
    p = HERE / "grille.html"
    p.write_text(doc, encoding="utf-8")
    return p

def build_pdf(src):
    chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    pdf = OUT / f"{BASE}.pdf"
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={pdf}", src.as_uri()], check=True, capture_output=True)
    return pdf

def build_xlsx():
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    wb = Workbook(); ws = wb.active; ws.title = "Grille de veille"
    head = ["Champ de veille", "N°", "Statut", "Information / tendance identifiée", "Source (organisme, titre, date)",
            "Lien", "Analyse critique", "Impact pour le projet"]
    ws.append(head)
    for r in ROWS:
        ws.append([r["champ"], r["n"], r["statut"], r["info"], r["src"], r["url"], r["analyse"], r["impact"]])
    widths = [18, 6, 12, 55, 40, 40, 50, 55]
    blue = PatternFill("solid", fgColor="0058A3"); thin = Side(style="thin", color="D5DDE6")
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + i)].width = w
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = blue
        c.alignment = Alignment(wrap_text=True, vertical="center")
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top"); c.border = Border(bottom=thin)
        row[0].font = Font(bold=True, color="0058A3")
        row[5].hyperlink = row[5].value; row[5].font = Font(color="0058A3", underline="single")
    ws.freeze_panes = "B2"; ws.auto_filter.ref = ws.dimensions
    q = wb.create_sheet("Questions à creuser")
    q.append(["Champ", "Question ouverte et piste de source"])
    for c, t in QUESTIONS:
        q.append([c, t])
    q.column_dimensions["A"].width = 20; q.column_dimensions["B"].width = 120
    for c in q[1]:
        c.font = Font(bold=True, color="FFFFFF"); c.fill = blue
    for row in q.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    m = wb.create_sheet("Lisez-moi")
    for line in [
        "IKÉASTRE · Veille stratégique (livrable intermédiaire) · sources consultées le " + CONSULT,
        "Statut : Documenté = fait publié et vérifiable ; Projection = objectif/calendrier annoncé ; Signal faible = fait isolé, interprété par le groupe.",
        "Projet académique indépendant, sans commande ni validation d'IKEA. Personas fictifs de travail, aucun entretien terrain.",
    ]:
        m.append([line])
    m.column_dimensions["A"].width = 140
    p = OUT / f"{BASE}.xlsx"; wb.save(p); return p

if __name__ == "__main__":
    h = build_html()
    print(build_pdf(h)); print(build_xlsx())
