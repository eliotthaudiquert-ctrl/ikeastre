"""Génère la veille stratégique (Session 1) à partir de veille.json :
- Veille stratégique IKEA compacts.xlsx (grille de travail)
- veille.html puis Veille stratégique IKEA compacts.pdf (DA de groupe, pages 16:9)
- Grille de veille (modèle du cours).xlsx : la grille du cours remplie (modèle dans 01 Consignes et cours)
Usage : python build.py"""
import html
import json
import subprocess
import sys
from collections import OrderedDict
from pathlib import Path

ICI = Path(__file__).resolve().parent
D = json.loads((ICI / "veille.json").read_text(encoding="utf-8"))
NOM = "Veille stratégique IKEA compacts"
CHAMPS = ["Tendances lourdes", "Innovations", "Durabilité", "Accessibilité", "Inclusion",
          "Évolutions des usages", "Réglementation", "Signaux faibles"]
import re
e = lambda s: re.sub(r" (%|Md€|m²|millions|»)", lambda m: " " + m.group(1), html.escape(s, quote=True).replace("« ", "« "))


def src_txt(s):
    return f"{s['organisme']}, « {s['titre']} », {s['date']}"


# ---------------------------------------------------------------- Excel
def excel():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter

    BLEU, JAUNE, GRIS = "0058A3", "FFDB00", "F5F5F5"
    f_base = Font(name="Noto Sans", size=10)
    f_tete = Font(name="Noto Sans", size=10, bold=True, color="FFFFFF")
    filet = Border(bottom=Side(style="thin", color="DFDFDF"))
    wrap = Alignment(wrap_text=True, vertical="top")

    wb = Workbook()
    ws = wb.active
    ws.title = "Grille de veille"
    ws["A1"] = D["titre"] + " · " + D["sous_titre"]
    ws["A1"].font = Font(name="Noto Sans", size=14, bold=True)
    ws["A2"] = f"Projet IKÉASTRE · B3CPD · {D['date']} · {D['angle']}"
    ws["A2"].font = Font(name="Noto Sans", size=10, color="484848")
    ws["A3"] = "Contexte : " + D["contexte"]["texte"] + " Source : " + src_txt(D["contexte"]["source"])
    ws["A3"].font = f_base
    ws["A3"].alignment = wrap
    ws.merge_cells("A3:J3")
    ws.row_dimensions[3].height = 48

    cols = [("Champ de veille", 18), ("Nature", 16), ("Information / tendance identifiée", 42),
            ("Source (organisme, titre)", 32), ("Date", 13), ("Lien", 30),
            ("Analyse critique", 40), ("Impact pour le projet", 44), ("À creuser", 32), ("Extrait exact de la source", 40)]
    r0 = 5
    for i, (t, w) in enumerate(cols, 1):
        c = ws.cell(r0, i, t)
        c.font, c.fill, c.alignment = f_tete, PatternFill("solid", fgColor=BLEU), wrap
        ws.column_dimensions[get_column_letter(i)].width = w
    for n, l in enumerate(D["lignes"], 1):
        s = l["source"]
        vals = [l["champ"], l["nature"], l["info"], f"{s['organisme']} · {s['titre']}", s["date"], s["url"],
                l["critique"], l["impact"], l["question"], s["extrait"]]
        r = r0 + n
        for i, v in enumerate(vals, 1):
            c = ws.cell(r, i, v)
            c.font, c.alignment, c.border = f_base, wrap, filet
        ws.cell(r, 1).font = Font(name="Noto Sans", size=10, bold=True)
        ws.cell(r, 1).fill = PatternFill("solid", fgColor=JAUNE)
        lien = ws.cell(r, 6)
        lien.hyperlink = s["url"]
        lien.font = Font(name="Noto Sans", size=10, color=BLEU, underline="single")
        if l["nature"] == "Signal faible":
            ws.cell(r, 2).font = Font(name="Noto Sans", size=10, bold=True, color="CA5008")
        elif l["nature"] == "Obligation légale":
            ws.cell(r, 2).font = Font(name="Noto Sans", size=10, bold=True, color="CC0008")
        else:
            ws.cell(r, 2).font = Font(name="Noto Sans", size=10, bold=True, color=BLEU)
        ws.row_dimensions[r].height = 120
    ws.freeze_panes = ws.cell(r0 + 1, 2)
    ws.auto_filter.ref = f"A{r0}:J{r0 + len(D['lignes'])}"

    w2 = wb.create_sheet("À creuser")
    w2["A1"] = "Questions qui demandent des recherches complémentaires"
    w2["A1"].font = Font(name="Noto Sans", size=13, bold=True)
    w2.column_dimensions["A"].width = 6
    w2.column_dimensions["B"].width = 110
    for i, q in enumerate(D["a_creuser"], 1):
        w2.cell(2 + i, 1, i).font = Font(name="Noto Sans", size=10, bold=True)
        c = w2.cell(2 + i, 2, q)
        c.font, c.alignment = f_base, wrap
        w2.row_dimensions[2 + i].height = 30

    w3 = wb.create_sheet("Couverture des 8 champs")
    w3.append(["Champ", "Nombre d'informations", "Statut"])
    for c in w3[1]:
        c.font, c.fill = f_tete, PatternFill("solid", fgColor=BLEU)
    for ch in CHAMPS:
        n = sum(1 for l in D["lignes"] if l["champ"] == ch)
        w3.append([ch, n, "Traité" if n else "À traiter"])
    for row in w3.iter_rows(min_row=2):
        for c in row:
            c.font = f_base
    w3.column_dimensions["A"].width = 26
    w3.column_dimensions["B"].width = 22
    w3.column_dimensions["C"].width = 14
    def feuille(titre, entetes, lignes, haut=60):
        w = wb.create_sheet(titre)
        for i, (t, larg) in enumerate(entetes, 1):
            c = w.cell(1, i, t)
            c.font, c.fill, c.alignment = f_tete, PatternFill("solid", fgColor=BLEU), wrap
            w.column_dimensions[get_column_letter(i)].width = larg
        for r, vals in enumerate(lignes, 2):
            for i, v in enumerate(vals, 1):
                c = w.cell(r, i, v)
                c.font, c.alignment, c.border = f_base, wrap, filet
            w.cell(r, 1).font = Font(name="Noto Sans", size=10, bold=True)
            w.row_dimensions[r].height = haut
        w.freeze_panes = "B2"
        return w

    feuille("5 dimensions", [("Dimension", 22), ("Évolution à surveiller", 40), ("Exemple concret", 60),
                             ("Impact pour le projet", 50), ("Sources", 40)],
            [[x["dimension"], x["evolution"], x["exemple"], x["impact"], " ; ".join(x["sources"])] for x in D["dimensions"]]
            + [["La plus stratégique", D["dimensions_choix"], "", "", ""]], 75)
    feuille("Regard MARKET", [("Question MARKET", 34), ("Notre réponse", 90), ("Sources", 45)],
            [[x["question"], x["reponse"], " ; ".join(x["sources"])] for x in D["regard_market"]], 90)
    feuille("Plan de veille", [("Question de veille", 36), ("Ce qu'on surveille", 44), ("Sources à suivre", 34),
                               ("Fréquence", 20), ("Décision éclairée", 40)],
            [[x["question"], x["surveiller"], x["sources"], x["frequence"], x["decision"]] for x in D["plan_veille"]]
            + [["Prompt de veille à réutiliser", D["prompt_veille"], "", "", ""]], 70)
    feuille("Sources concurrence", [("Organisme", 30), ("Titre", 50), ("Date", 13), ("Lien", 50),
                                    ("Extrait exact", 60), ("Référence", 36)],
            [[x["organisme"], x["titre"], x["date"], x["url"], x["extrait"], x["ref"]] for x in D["sources_concurrence"]], 45)
    out = ICI / f"{NOM}.xlsx"
    wb.save(out)
    return out


def grille_cours():
    """Remplit la grille d'exemple du cours (Part 1) en gardant sa mise en forme d'origine."""
    from copy import copy
    from openpyxl import load_workbook
    from openpyxl.styles import Alignment
    modele = ICI.parent / "01 Consignes et cours" / "Part1 - Exemple grille veille strat.xlsx"
    wb = load_workbook(modele)
    ws = wb.active
    ws["B5"] = "Grille de travail · Projet IKÉASTRE (magasins IKEA compacts × 18-29 ans) · regard MARKET · " + D["date"]
    gabarit = [copy(ws.cell(8, c)._style) for c in range(2, 7)]
    tete = [copy(ws.cell(8, 2)._style)]
    ws.delete_rows(8, ws.max_row - 7)
    r = 8
    for ch in CHAMPS:
        ls = [l for l in D["lignes"] if l["champ"] == ch]
        debut = r
        for l in ls:
            s = l["source"]
            vals = [ch, f"[{l['nature']}] {l['info']}", f"{s['organisme']}, « {s['titre']} », {s['date']}\n{s['url']}",
                    l["critique"], l["impact"]]
            for i, v in enumerate(vals):
                c = ws.cell(r, 2 + i, v)
                c._style = copy(gabarit[i])
                c.alignment = Alignment(wrap_text=True, vertical="top")
            ws.row_dimensions[r].height = 150
            r += 1
        if r - 1 > debut:
            ws.merge_cells(start_row=debut, start_column=2, end_row=r - 1, end_column=2)
        ws.cell(debut, 2)._style = copy(tete[0])
        ws.cell(debut, 2).alignment = Alignment(wrap_text=True, vertical="top")
    for col, larg in zip("BCDEF", (19, 46, 40, 44, 46)):
        ws.column_dimensions[col].width = larg
    out = ICI / "Grille de veille (modèle du cours).xlsx"
    wb.save(out)
    return out


# ---------------------------------------------------------------- HTML / PDF
def top(page, total, crumb):
    return (f'<div class="topbar"><span><b>Projet IKÉASTRE</b> · B3CPD</span>'
            f'<span class="ctr">Session 1 · Veille stratégique</span><span>Livrable intermédiaire</span></div>'
            f'<div class="nav"><img src="ikea-logo.png" alt="Logo IKEA"><div class="crumbs"><span>Magasins compacts</span>'
            f'<span>Veille</span><span>{e(crumb)}</span></div><span class="num">{page:02d} / {total:02d}</span></div>')


FOOT = ('<div class="foot"><span>Concept académique indépendant, non affilié à IKEA. Veille préparée avec l\'aide de l\'IA, '
        'chaque extrait de source retrouvé mot pour mot sur la page d\'origine.</span></div>')
TAG = {"Tendance documentée": "prio", "Signal faible": "conq", "Obligation légale": "excl"}


def ligne_html(l):
    s = l["source"]
    return (f'<tr><td class="c-info"><span class="tag {TAG[l["nature"]]}">{e(l["nature"])}</span>'
            f'<p class="info">{e(l["info"])}</p></td>'
            f'<td class="c-src"><b>{e(s["organisme"])}</b><br>{e(s["titre"])}<br><span class="dt">{e(s["date"])}</span>'
            f'<br><a href="{e(s["url"])}">{e(s["url"].split("/")[2].replace("www.", ""))}</a></td>'
            f'<td>{e(l["critique"])}</td><td class="c-imp">{e(l["impact"])}</td>'
            f'<td class="c-q">{e(l["question"])}</td></tr>')


def page_table(titre, lead, lignes, page, total, crumb):
    rows = "".join(ligne_html(l) for l in lignes)
    return (f'<section class="slide">{top(page, total, crumb)}<div class="body">'
            f'<div class="eyebrow bleu">{e(crumb)}</div><h1 class="h">{e(titre)}</h1><p class="lead s">{lead}</p>'
            f'<table class="veille mt12"><thead><tr><th style="width:24%">Information</th><th style="width:17%">Source et date</th>'
            f'<th style="width:20%">Analyse critique</th><th style="width:24%">Impact pour le projet</th><th style="width:15%">À creuser</th></tr></thead>'
            f'<tbody>{rows}</tbody></table></div>{FOOT}</section>')


CSS = """
h1.h { font-size: 30px; }
.lead.s { font-size: 14px; margin-top: 6px; max-width: 1100px; }
table.veille td { font-size: 12.5px; line-height: 1.42; padding: 11px 10px; }
table.veille th { font-size: 12.5px; padding: 8px 10px; }
table.veille .info { font-size: 14px; color: var(--noir); font-weight: 600; line-height: 1.38; margin-top: 3px; }
table.veille .tag { font-size: 12px; }
table.veille .c-src { color: var(--gris-texte); }
table.veille .c-src .dt { color: var(--noir); font-weight: 700; }
table.veille a { color: var(--bleu); text-decoration: none; font-weight: 600; }
table.veille .c-imp { color: var(--noir); background: #fffbe0; }
table.veille .c-q { color: var(--gris-texte); font-style: italic; }
.champs { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; }
.champ { background: var(--fond-gris); padding: 12px 14px; min-height: 86px; display: flex; flex-direction: column; }
.champ .n { font-size: 11px; font-weight: 700; color: var(--gris-doux); }
.champ b { font-size: 14px; margin-top: 2px; }
.champ .k { margin-top: auto; font-size: 11.5px; color: var(--bleu); font-weight: 700; }
.crit { display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; }
.crit div { border-top: 4px solid var(--noir); padding-top: 10px; }
.crit .n { font-size: 12px; font-weight: 700; color: var(--gris-doux); }
.legend { display: flex; gap: 28px; }
.legend p { max-width: 330px; }
ol.q { padding-left: 22px; }
ol.q li { font-size: 15.5px; margin-bottom: 9px; color: var(--noir); }
table.veille .info-s { color: var(--noir); font-weight: 600; }
table.dim td, table.plan td { font-size: 12px; padding: 8px 10px; }
table.dim td { padding: 7px 9px; line-height: 1.36; }
table.dim .small { font-size: 10.5px; }
.mk { display: grid; grid-template-columns: repeat(5, 1fr); gap: 16px; }
.mk div { border-top: 4px solid var(--bleu); padding-top: 10px; }
.mk .n { font-size: 12px; font-weight: 700; color: var(--gris-doux); }
.mk h3 { font-size: 14px; margin: 2px 0 8px; min-height: 38px; }
.mk p { font-size: 12.5px; }
.chiffre { font-size: 46px; font-weight: 800; letter-spacing: -1.5px; line-height: 1; }
"""


def html_doc():
    par = OrderedDict((c, [l for l in D["lignes"] if l["champ"] == c]) for c in CHAMPS)
    tl = par["Tendances lourdes"]
    pages_t = [
        ("Ce qui transforme durablement le marché (1/2)", "Les jeunes bougent souvent, achètent dans un marché qui recule et regardent de plus en plus l'occasion.", tl[:3], "Tendances lourdes"),
        ("Ce qui transforme durablement le marché (2/2)", "Le digital progresse et les concurrents adoptent eux aussi les petits formats : le magasin compact seul ne suffira pas à se démarquer.", tl[3:], "Tendances lourdes"),
        ("Innover sans alourdir", "Les outils existent déjà chez IKEA, et l'impact du numérique vient surtout des appareils.", par["Innovations"] + par["Durabilité"], "Innovations · Durabilité"),
        ("Personne ne doit rester à la porte", "Accessibilité numérique obligatoire, publics handicapés, jeunes sans voiture : trois risques d'exclusion pour un magasin compact.", par["Accessibilité"] + par["Inclusion"], "Accessibilité · Inclusion"),
        ("Comment les jeunes préparent leurs achats", "L'IA et les réseaux sociaux deviennent des portes d'entrée, et la loi encadre déjà les assistants IA.", par["Évolutions des usages"] + par["Réglementation"], "Usages · Réglementation"),
        ("Ce qui pourrait changer la donne d'ici 2030", "Trois indices encore émergents : à surveiller, pas à prendre pour acquis.", par["Signaux faibles"], "Signaux faibles"),
    ]
    total = 6 + len(pages_t)
    cx = D["contexte"]
    chips = "".join(
        f'<div class="champ"><span class="n">{i:02d}</span><b>{e(c)}</b><span class="k">{len(par[c])} information{"s" if len(par[c]) > 1 else ""}</span></div>'
        for i, c in enumerate(CHAMPS, 1))
    nb_src = len({l["source"]["url"] for l in D["lignes"]}) + 1
    cover = (f'<section class="slide cover">{top(1, total, "Session 1")}<div class="body" style="justify-content:center">'
             f'<div style="display:grid;grid-template-columns:1fr 1.05fr;gap:48px;align-items:center">'
             f'<div><span class="badge bleu">Session 1</span><h1 class="xl" style="margin-top:12px">Ce qui peut changer la donne.</h1>'
             f'<p class="lead">Veille stratégique sur les <b>8 champs</b> demandés pour notre projet : les <b>magasins IKEA compacts</b> '
             f'au service des jeunes adultes (18-29 ans), en France, à horizon 2030. Regard <b>MARKET</b> d\'abord.</p>'
             f'<div class="row mt24" style="gap:36px"><div><div class="chiffre">{len(D["lignes"])}</div><p>informations retenues</p></div>'
             f'<div><div class="chiffre">{nb_src}</div><p>sources datées, avec lien</p></div>'
             f'<div><div class="chiffre">8/8</div><p>champs traités</p></div></div></div>'
             f'<div class="champs">{chips}</div></div></div>'
             f'<div class="foot"><span>Concept académique indépendant, non affilié à IKEA · Équipe IKÉASTRE · {e(D["date"])}</span></div></section>')
    s = cx["source"]
    methode = (f'<section class="slide">{top(2, total, "Point de départ")}<div class="body">'
               f'<div class="eyebrow bleu">Point de départ</div><h1 class="h">Un format annoncé, une expérience à inventer</h1>'
               f'<div class="box bleu mt16" style="max-width:1100px"><p style="font-size:14.5px">{e(cx["texte"])}</p>'
               f'<p class="small" style="color:#cfe0f0;margin-top:8px">Source : {e(src_txt(s))}</p></div>'
               f'<h3 class="mt24">Comment chaque information a été vérifiée</h3><div class="crit mt12">'
               + "".join(f'<div><span class="n">0{i}</span><h3>{t}</h3><p>{d}</p></div>' for i, (t, d) in enumerate([
                   ("Auteur", "Qui produit l'information : organisme public, fédération, marque ou média."),
                   ("Date", "Date de publication ou de consultation, pour juger si c'est encore actuel."),
                   ("Périmètre", "Quel marché, quel territoire, quel public : ménages, 16-25 ans, France…"),
                   ("Méthode", "Enquête, estimation, déclaration d'entreprise : on le dit dans l'analyse."),
                   ("Corroboration", "Chaque extrait a été retrouvé mot pour mot sur la page d'origine.")], 1))
               + '</div><h3 class="mt24">Comment lire la grille</h3><div class="legend mt8">'
               '<p><span class="tag prio">Tendance documentée</span><br>Évolution déjà mesurée par des données.</p>'
               '<p><span class="tag conq">Signal faible</span><br>Indice émergent, on ne sait pas encore s\'il va s\'installer.</p>'
               '<p><span class="tag excl">Obligation légale</span><br>Règle déjà en vigueur, à intégrer dès la conception.</p>'
               '<p><b style="background:#fffbe0;padding:1px 4px">Impact</b><br>Ce que l\'information change pour les magasins compacts.</p>'
               f'</div></div>{FOOT}</section>')
    corps = "".join(page_table(t, e(ld), ls, i, total, cr) for i, (t, ld, ls, cr) in enumerate(pages_t, 3))
    n = 3 + len(pages_t)
    corps += (f'<section class="slide">{top(n, total, "5 dimensions")}<div class="body">'
              f'<div class="eyebrow bleu">Observer son environnement</div><h1 class="h">Les 5 dimensions qui pèsent sur notre projet</h1>'
              f'<p class="lead s"><b>{e(D["dimensions_choix"])}</b></p>'
              f'<table class="veille dim mt12"><thead><tr><th style="width:13%">Dimension</th><th style="width:21%">Évolution à surveiller</th>'
              f'<th style="width:38%">Exemple concret (sources de la grille)</th><th style="width:28%">Impact pour le projet</th></tr></thead><tbody>'
              + "".join(f'<tr><td><b>{e(x["dimension"])}</b></td><td class="info-s">{e(x["evolution"])}</td>'
                        f'<td>{e(x["exemple"])}<br><span class="small">{e(" · ".join(x["sources"]))}</span></td>'
                        f'<td class="c-imp">{e(x["impact"])}</td></tr>' for x in D["dimensions"])
              + f'</tbody></table></div>{FOOT}</section>')
    corps += (f'<section class="slide">{top(n + 1, total, "Regard MARKET")}<div class="body">'
              f'<div class="eyebrow bleu">Regard marché et stratégie</div><h1 class="h">Nos réponses aux 5 questions MARKET</h1>'
              f'<p class="lead s">Ce que la veille nous apprend sur la cible, la concurrence et l\'attractivité des magasins compacts.</p>'
              f'<div class="mk mt16">'
              + "".join(f'<div><span class="n">0{i}</span><h3>{e(x["question"])}</h3><p>{e(x["reponse"])}</p>'
                        f'<p class="small mt8">{e(" · ".join(x["sources"]))}</p></div>' for i, x in enumerate(D["regard_market"], 1))
              + f'</div></div>{FOOT}</section>')
    corps += (f'<section class="slide">{top(n + 2, total, "Veille continue")}<div class="body">'
              f'<div class="eyebrow bleu">Organisée · continue · décisionnelle</div><h1 class="h">Ce qu\'on continue de surveiller, et pour quelle décision</h1>'
              f'<p class="lead s">Une information n\'a de valeur que si elle éclaire une décision : chaque question de veille est reliée à un choix du dossier.</p>'
              f'<table class="veille plan mt12"><thead><tr><th style="width:22%">Question de veille</th><th style="width:24%">Ce qu\'on surveille</th>'
              f'<th style="width:18%">Sources à suivre</th><th style="width:12%">Fréquence</th><th style="width:24%">Décision éclairée</th></tr></thead><tbody>'
              + "".join(f'<tr><td class="info-s">{e(x["question"])}</td><td>{e(x["surveiller"])}</td><td>{e(x["sources"])}</td>'
                        f'<td>{e(x["frequence"])}</td><td class="c-imp">{e(x["decision"])}</td></tr>' for x in D["plan_veille"])
              + f'</tbody></table><p class="small mt12"><b>Prompt de veille à réutiliser :</b> « {e(D["prompt_veille"])} »</p></div>{FOOT}</section>')
    fin = (f'<section class="slide">{top(total, total, "À creuser")}<div class="body">'
           f'<div class="eyebrow bleu">Prochaines recherches</div><h1 class="h">Ce qu\'il nous reste à vérifier</h1>'
           f'<p class="lead s">Questions ouvertes pour la session 2 (qualifier les tendances et construire la synthèse décisionnelle).</p>'
           f'<div style="display:grid;grid-template-columns:1.5fr 1fr;gap:40px" class="mt20"><ol class="q">'
           + "".join(f"<li>{e(q)}</li>" for q in D["a_creuser"])
           + '</ol><div class="box jaune" style="align-self:start"><h3>À retenir pour la suite</h3><p class="mt8">Le magasin compact répond à de vraies tendances '
             '(déménagements fréquents, occasion, omnicanal), mais les concurrents vont aussi vers les petits formats. '
             'La différence se fera sur la <b>brique digitale</b> et sur l\'<b>accès sans voiture</b> : ce sont les deux sujets à creuser en priorité.</p>'
             f'<p class="small mt12">Grille complète avec liens et extraits exacts : {e(NOM)}.xlsx</p></div></div></div>{FOOT}</section>')
    return ('<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Veille stratégique · Magasins IKEA compacts</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="style.css"><style>{CSS}</style></head><body>{cover}{methode}{corps}{fin}</body></html>')


def pdf(src, out=None):
    candidats = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                 "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                 "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
                 "/usr/bin/google-chrome"]
    chrome = next(c for c in candidats if Path(c).exists())
    out = out or ICI / f"{NOM}.pdf"
    subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={out}", src.as_uri()], check=True, capture_output=True)
    return out


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    print("Excel :", excel().name)
    print("Grille:", grille_cours().name)
    h = ICI / "veille.html"
    h.write_text(html_doc(), encoding="utf-8")
    print("HTML  :", h.name)
    print("PDF   :", pdf(h).name)
