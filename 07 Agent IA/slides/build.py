"""Génère le deck « Fika » (HTML 16:9 -> PDF) à partir des vrais résultats de l'agent.
Usage : python build.py   (lit ../livrables/*.json et ../agent/journal/bilan-mission-*.json)"""
import html
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
ICI = Path(__file__).resolve().parent
RACINE = ICI.parent
LIV = RACINE / "livrables"


def charger(nom):
    p = LIV / nom
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def bilan(n):
    p = RACINE / "agent" / "journal" / f"bilan-mission-{n}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


M1, M2 = charger("mission-1-verification.json"), charger("mission-2-veille.json")
def ctrl(nom):
    p = RACINE / "agent" / "travail" / nom
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


C1, C2 = ctrl("mission-1-verification.controle.json"), ctrl("mission-2-veille.controle.json")
B1, B2 = bilan(1), bilan(2)
e = lambda s: html.escape(str(s or ""))
DATE = M1.get("date_execution") or M2.get("date_execution") or ""
DATE_FR = "/".join(reversed(DATE.split("-"))) if DATE else ""


def stat(b, cle):
    return (b.get("outils") or {}).get(cle, 0)


def statuts(m):
    d = {}
    for l in m.get("lignes", []):
        d[l.get("statut")] = d.get(l.get("statut"), 0) + 1
    return d


CHIP = {"Confirmé": "ok", "Relevé": "ok", "Nuancé": "nu", "Infirmé": "ko", "Non trouvé": "nt"}


def chip(s):
    return f'<span class="chip {CHIP.get(s, "nt")}">{e(s)}</span>'


def court(s, n):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[: n - 1].rsplit(" ", 1)[0] + "…"


SOURCES = "Concept académique indépendant, non affilié à IKEA · B3CPD Ynov · équipe Loris Demeaux, Tobias Ringot, Eliott Haudiquert · agent, analyse et slides réalisés avec l’aide de l’IA."
slides = []


def slide(contenu, n, classe="", source=""):
    pied = f'<div class="pied"><small>{source + "<br>" if source else ""}{SOURCES}</small><span class="num">{n:02d}</span></div>'
    slides.append(f'<section class="slide {classe}">{contenu}{pied if "couv" not in classe else ""}</section>')


def entete(sur, titre):
    return f'<div class="sur">{e(sur)}</div><div class="trait"></div><h1>{titre}</h1><img class="logo" src="ikea-logo.png" alt="IKEA">'


# 1 · couverture
slides.append(f'''<section class="slide couv">
  <div class="couv-g">
    <div class="sur clair">IKÉASTRE · Module IA · {e(DATE_FR)}</div>
    <div class="fika">Fika</div>
    <div class="trait large"></div>
    <p class="couv-p">L’agent IA qui <b>vérifie nos hypothèses</b> et <b>surveille la concurrence</b>, et rend un tableau sourcé et daté.</p>
  </div>
  <div class="couv-d">
    <div class="mini"><span>Mission 1</span>Vérifier les questions de l’atelier « le brief déconstruit »</div>
    <div class="mini"><span>Mission 2</span>Comparer IKEA à 5 concurrents sur 6 critères Gen Z</div>
    <div class="mini"><span>Pourquoi « Fika »</span>La pause café suédoise : le temps qu’on boive un café, il a fait la recherche.</div>
  </div>
  <small class="couv-pied">{SOURCES}</small>
</section>''')

# 2 · pourquoi
slide(entete("Le problème", "Pourquoi un agent ?") + '''
<div class="g2">
  <div class="carte"><div class="num-c">CE QU’ON AVAIT</div><h2>Des chiffres fragiles</h2>
    <ul>
      <li><b>« 1 jeune sur 4 déménage chaque année »</b> : une étude régionale (La Réunion, 2022).</li>
      <li><b>« 1 meuble sur 4 vendu d’occasion »</b> : source tronquée à l’écran.</li>
      <li><b>« 150 millions de membres IKEA Family »</b> : un chiffre de 2020.</li>
      <li><b>0 entretien, 0 questionnaire</b> : nos personas restent des hypothèses.</li>
    </ul></div>
  <div class="carte forte"><div class="num-c">CE QU’IL NOUS FALLAIT</div><h2>Vérifier vite, sans tricher</h2>
    <ul>
      <li>Répondre aux <b>5 questions à creuser</b> de l’atelier de ce matin.</li>
      <li>Savoir où se situent <b>les concurrents</b> sur nos 3 leviers : proximité, prix, codes Gen Z.</li>
      <li>Un <b>tableau sourcé et daté</b>, réutilisable dans le dossier et à l’oral.</li>
      <li>Une méthode qu’on peut <b>relancer</b> quand les chiffres changent.</li>
    </ul></div>
</div>''', 2, source="Sources : kit de pilotage agile IKÉASTRE, onglet Données IKEA (limites d’usage des chiffres).")

# 3 · la boucle
slide(entete("Théorie appliquée", "La boucle de Fika") + '''
<div class="boucle">
  <svg viewBox="0 0 1136 480" class="fleches">
    <defs>
      <marker id="b" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#0058A3"/></marker>
      <marker id="r" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#D9472B"/></marker>
      <marker id="v" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#1F7A4D"/></marker>
      <marker id="n" markerWidth="8" markerHeight="8" refX="5" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8z" fill="#111418"/></marker>
    </defs>
    <path d="M200,40 H438" stroke="#111418" stroke-width="3" fill="none" marker-end="url(#n)"/>
    <path d="M688,56 H820 V180" stroke="#0058A3" stroke-width="4" fill="none" marker-end="url(#b)"/>
    <path d="M820,282 V416 H698" stroke="#0058A3" stroke-width="4" fill="none" marker-end="url(#b)"/>
    <path d="M448,416 H316 V292" stroke="#0058A3" stroke-width="4" fill="none" marker-end="url(#b)"/>
    <path d="M316,190 V80 H438" stroke="#D9472B" stroke-width="3" stroke-dasharray="9 7" fill="none" marker-end="url(#r)"/>
    <path d="M196,236 H110 V366" stroke="#1F7A4D" stroke-width="4" fill="none" marker-end="url(#v)"/>
    <path d="M940,236 H962" stroke="#8a8d93" stroke-width="3" stroke-dasharray="5 5" fill="none"/>
  </svg>
  <div class="bx mission" style="left:0;top:0"><b>Mission</b><span>rôle, sources, format, règles</span></div>
  <div class="bx" style="left:448px;top:10px"><i>1</i><b>Planifier</b><span>écrit son plan, question par question</span></div>
  <div class="bx" style="left:700px;top:190px"><i>2</i><b>Agir</b><span>appelle un outil</span></div>
  <div class="bx" style="left:448px;top:370px"><i>3</i><b>Observer</b><span>lit la page : URL, date, extrait</span></div>
  <div class="bx verif" style="left:196px;top:190px"><i>4</i><b>Vérifier</b><span>se relit, puis le contrôleur ouvre chaque source</span></div>
  <div class="rond"><b>Modèle</b><span>Claude raisonne</span></div>
  <div class="bx outils" style="left:966px;top:150px"><b>Outils</b><span>recherche web<br>lecture de pages<br>texte exact<br>calcul<br>fichiers, tableur</span></div>
  <div class="bx livr" style="left:0;top:376px"><b>Livrable</b><span>oui : tableau Excel sourcé et daté</span></div>
  <div class="tag-r">non : on reboucle<br><small>3 tours maximum</small></div>
  <div class="tag-v">oui</div>
</div>''', 3, source="Schéma : « La boucle de l’agent », cours IA, appliqué à notre agent.")

# 4 · la fiche mission
slide(entete("Étape 0", "Une fiche mission, pas un vœu") + '''
<div class="g2 g-45">
  <div class="carte sombre">
    <div class="ligne-m"><b>Rôle</b><span>analyste data (mission 1), veilleur (mission 2) de l’équipe IKÉASTRE</span></div>
    <div class="ligne-m"><b>Sources</b><span>statistique publique &gt; site officiel &gt; institut &gt; presse éco &gt; le reste</span></div>
    <div class="ligne-m"><b>Format</b><span>JSON imposé : 16 champs par ligne, dont source, date, extrait exact, limite</span></div>
    <div class="ligne-m"><b>Règles</b><span>zéro invention, extrait mot pour mot, calculs à l’outil, « Non trouvé » plutôt qu’un chiffre faux</span></div>
  </div>
  <div class="col">
    <div class="carte"><div class="num-c">MISSION 1 · VÉRIFIER</div><h3>14 questions en 5 blocs</h3>
      <p>Q1 accès sans voiture · Q2 prix ou livraison · Q3 humour et achat · Q4 budgets de 700 € et 350 € · Q5 nos chiffres à revérifier.</p></div>
    <div class="carte"><div class="num-c">MISSION 2 · VEILLE</div><h3>6 enseignes × 6 critères = 36 cases</h3>
      <p>IKEA, Maisons du Monde, Conforama, But, Action, Leboncoin · réseau, petits formats, livraison, offre jeunes, fidélité et seconde main, TikTok.</p></div>
  </div>
</div>''', 4, source="Fichiers : agent/SYSTEME.md (règles), agent/missions/1-verification.md et 2-veille.md.")

# 5 · outils
OUT = [("Recherche web", "WebSearch", "trouve les sources candidates"),
       ("Lecture de pages", "WebFetch", "lit et résume une page"),
       ("Texte exact", "lire_page.py", "renvoie le passage mot pour mot, HTML ou PDF"),
       ("Calcul", "calcul.py", "additionne les prix, compare aux budgets : jamais de tête"),
       ("Fichiers", "Read / Write", "plan, notes, livrable JSON"),
       ("Contrôle", "verifier.py", "il peut se faire relire avant de rendre")]
cartes = "".join(f'<div class="carte outil"><div class="num-c">{e(c)}</div><h3>{e(t)}</h3><p>{e(d)}</p></div>' for t, c, d in OUT)
slide(entete("Étape 2 · Agir", "Ses outils, et ses interdits") + f'''
<div class="g3">{cartes}</div>
<div class="bandeau">Interdit : se connecter à un compte, remplir un formulaire, lancer une autre commande que ses 3 scripts. En mode « ne demande pas », tout le reste est refusé d’office.</div>''',
      5, source="Fichiers : agent/lancer.py (liste des outils autorisés), agent/outils/.")

# 6 · vérifier
def exemple_refus():
    """Test réel du garde-fou : journal agent/journal/*_test-boucle.md."""
    js = sorted((RACINE / "agent" / "journal").glob("*_test-boucle.md"))
    if not js:
        return ""
    txt = js[-1].read_text(encoding="utf-8")
    erreurs = re.findall(r"\*\*  erreur\*\* · ([^\n]+)", txt)[:2]
    ok = re.search(r"\*\*4 · Vérifier\*\* · (oui[^\n]*)", txt)
    corps = "\n".join("✗ " + court(x, 95) for x in erreurs)
    fin = f"→ l’agent rouvre les sources, corrige, et le contrôleur dit {ok.group(1)} au tour 2." if ok else ""
    return (f'<div class="exemple"><div class="num-c">TEST RÉEL · ON A GLISSÉ UN FAUX CHIFFRE (250 M AU LIEU DE 200 M) ET UNE DATE DANS LE FUTUR</div>'
            f'<code>{e(corps)}</code><p class="fin-ex">{e(fin)}</p></div>')


slide(entete("Étape 4 · Vérifier", "Le contrôleur ne le croit pas sur parole") + f'''
<div class="g4">
  <div class="carte"><div class="num-c">CONTRÔLE 1</div><h3>Structure</h3><p>16 champs par ligne, statut et confiance dans les listes autorisées.</p></div>
  <div class="carte"><div class="num-c">CONTRÔLE 2</div><h3>Couverture</h3><p>Chaque question ou case attendue a au moins une ligne.</p></div>
  <div class="carte"><div class="num-c">CONTRÔLE 3</div><h3>Dates</h3><p>Date de la source et date de consultation valides, jamais dans le futur.</p></div>
  <div class="carte forte"><div class="num-c">CONTRÔLE 4</div><h3>L’extrait existe</h3><p>Le code ouvre chaque lien et cherche l’extrait dans la page. Pas trouvé : ligne refusée.</p></div>
</div>
<div class="flux">
  <div class="etape ko"><b>non</b> : la liste des erreurs repart à l’agent, qui replanifie ces lignes</div>
  <div class="etape ok"><b>oui</b> : le tableur Excel est généré, avec une colonne « Contrôle de l’extrait »</div>
</div>
{exemple_refus()}
<p class="note">Les réseaux sociaux bloquent les robots : ces lignes sortent en « à contrôler à la main », jamais en « vérifié ».</p>''',
      6, source="Fichier : agent/outils/verifier.py · exemple tiré du journal de l’agent (agent/journal).")

# 7 · run réel
def bloc_run(nom, b, c, m):
    st = statuts(m)
    st_txt = " · ".join(f"{v} {k.lower()}" for k, v in st.items()) or "—"
    return f'''<div class="carte run"><div class="num-c">{e(nom)}</div>
      <div class="kpis">
        <div><b>{str(b.get("duree_min", "—")).replace(".", ",")}</b><span>minutes</span></div>
        <div><b>{(b.get("compteurs") or {}).get("agir", "—")}</b><span>actions</span></div>
        <div><b>{stat(b, "WebSearch")}</b><span>recherches</span></div>
        <div><b>{stat(b, "WebFetch") + stat(b, "Bash")}</b><span>lectures et calculs</span></div>
        <div><b>{b.get("boucles", "—")}</b><span>tour(s) de contrôle</span></div>
      </div>
      <p><b>{c.get("lignes_valides", "—")}/{c.get("nb_lignes", "—")}</b> lignes validées par le contrôleur · {e(st_txt)}</p>
      <p class="petit">{len(c.get("alertes", []))} point{"s" if len(c.get("alertes", [])) > 1 else ""} signalé{"s" if len(c.get("alertes", [])) > 1 else ""} « à contrôler à la main » (date absente, page TikTok).</p>
      <div class="outils-run">{" · ".join(f"{ {'Bash': 'scripts (texte exact, calcul, contrôle)'}.get(k, k)} {v}" for k, v in sorted((b.get("outils") or {}).items(), key=lambda x: -x[1]) if k not in ("ToolSearch", "Grep", "Read"))}</div></div>'''


slide(entete("Le vrai lancement", f"Ce qu’il a fait le {DATE_FR}") + f'''
<div class="g2">{bloc_run("MISSION 1 · VÉRIFICATION", B1, C1, M1)}{bloc_run("MISSION 2 · VEILLE", B2, C2, M2)}</div>
<div class="exemple vert"><div class="num-c">ET LE REBOUCLAGE ?</div><p>Les deux missions sont passées au premier contrôle : l’agent s’est relancé lui-même le contrôleur avant de rendre. Pour prouver la boucle, on a saboté une copie (slide 6) : refusée, réparée, acceptée en 0,6 minute.</p></div>''',
      7, source="Sources : agent/journal/bilan-mission-1.json et bilan-mission-2.json.")

# 8-9 · mission 1 résultats
lignes1 = M1.get("lignes", [])


def table_m1(ids):
    par_id = {l.get("id"): l for l in lignes1}
    out = []
    for i in ids:
        l = par_id.get(i)
        if not l:
            continue
        out.append(f'''<tr><td class="id">{e(l.get("id"))}</td><td class="theme">{e(court(l.get("theme"), 30))}</td>
          <td>{e(court(l.get("reponse"), 160))}</td><td>{chip(l.get("statut"))}</td>
          <td class="src">{e(court(l.get("editeur"), 26))}<br><span>{e(l.get("date_source"))}</span></td></tr>''')
    return ("<table class='m1'><tr><th>Id</th><th>Thème</th><th>Ce que dit la source</th><th>Statut</th><th>Source · date</th></tr>"
            + "".join(out) + "</table>")


SEL8 = ["Q1.a-1", "Q1.b-1", "Q1.b-2", "Q1.c-lyon-2", "Q1.c-lille-2", "Q2.a-1", "Q2.b-1", "Q3.a-1", "Q3.a-2", "Q3.b-1"]
SEL9 = ["Q4.a-total", "Q4.a-matelas", "Q4.b-1", "Q5.a-1", "Q5.a-3", "Q5.b", "Q5.c-1", "Q5.d"]
n1 = len(lignes1)
slide(entete("Mission 1 · résultats", "Accès, livraison, humour") + f'<div class="tab">{table_m1(SEL8)}</div>', 8,
      source=f"10 lignes clés sur {n1}. Tableau complet, avec liens et extraits exacts : livrables/IKEA_Agent_Mission1_Verification_{DATE}.xlsx.")
slide(entete("Mission 1 · résultats", "Budgets et chiffres revérifiés") + f'<div class="tab">{table_m1(SEL9)}</div>', 9,
      source="Prix IKEA relevés sur ikea.com/fr le jour indiqué, susceptibles de changer. Kit : lit NEIDEN, sommier LURÖY, matelas ÅGOTNES, LINNMON/ADILS, chaise SANDSBERG, portant MULIG.")

# 10 · mission 2 matrice
ACTEURS = ["IKEA", "Maisons du Monde", "Conforama", "But", "Action", "Leboncoin"]
CRIT = [("V1", "Réseau en France"), ("V2", "Petits formats"), ("V3", "Livraison"), ("V4", "Offre jeunes"),
        ("V5", "Fidélité, occasion"), ("V6", "TikTok")]
idx = {}
for l in M2.get("lignes", []):
    m = re.match(r"(V\d)\.(.+?)(?:[-_]\d+)?$", l.get("id", ""))
    if m:
        idx.setdefault((m.group(1), m.group(2).strip().lower()), l)


# version courte pour la slide, reprise des lignes sourcées (le détail est dans l'Excel)
COURT = {
    ("V2", "ikea"): "Oui : 1er compact à Limoges (27/05/2026), 10 villes d’ici 2030",
    ("V2", "maisons du monde"): "Oui : centre-ville, zone commerciale et centres commerciaux",
    ("V2", "conforama"): "En partie : format plus petit, mais en périphérie",
    ("V2", "but"): "Petit format (1 200 à 1 500 m²), pas de centre-ville",
    ("V2", "action"): "Oui : 1er magasin du centre de Paris (Bastille, 2025)",
    ("V3", "ikea"): "Point relais 2 € (Family) ou 7 €",
    ("V3", "maisons du monde"): "Retrait gratuit ; livraison offerte dès 1 000 € (source tierce)",
    ("V3", "conforama"): "Devant chez soi 35 € (commande < 200 €)",
    ("V3", "but"): "Retrait gratuit en 2 h ; tarif domicile non trouvé",
    ("V3", "action"): "Pas de vente en ligne en France",
    ("V3", "leboncoin"): "Livraison XL meubles dès 19,49 €",
    ("V4", "ikea"): "Rentrée 2025 : −10 % dès 150 € (saisonnier)",
    ("V4", "maisons du monde"): "−10 % étudiants toute l’année (Student Beans)",
    ("V4", "conforama"): "Été 2026 : 50 € offerts dès 250 € (terminé)",
    ("V4", "but"): "Rentrée 2025 : bon de 30 € (saisonnier)",
    ("V5", "ikea"): "IKEA Family + rachat « seconde vie »",
    ("V5", "maisons du monde"): "Programme « Ma Maison du Monde » (2024)",
    ("V5", "conforama"): "Carte Confo+ ; reprise via l’appli Geev",
    ("V5", "but"): "Fidélité oui ; pas de seconde main trouvée",
    ("V5", "action"): "Carte digitale ; pas de seconde main",
    ("V5", "leboncoin"): "La seconde main est le modèle ; pas de fidélité",
}


def insec(s):
    return re.sub(r"(\d) (€|%|K|M)", r"\1&nbsp;\2", s).replace("« ", "«&nbsp;").replace(" »", "&nbsp;»")


def cellule(c, a):
    l = idx.get((c, a.lower()))
    if l and l.get("statut") != "Non trouvé" and (c, a.lower()) in COURT:
        return '<td>' + insec(e(COURT[(c, a.lower())])) + '</td>'
    if not l:
        return '<td class="vide">—</td>'
    txt = l.get("chiffre") if c in ("V1", "V6") and l.get("chiffre") else l.get("reponse")
    if c == "V6" and l.get("chiffre"):
        txt = l["chiffre"].replace(".", ",").replace("K", " K abonnés")
    txt = re.sub(r"^(Oui|Non|En partie)\s*[.,:]?\s*", lambda m: m.group(1) + " : ", txt or "")
    cls = "nt" if l.get("statut") == "Non trouvé" else ""
    return f'<td class="{cls}">{e(court(txt if l.get("statut") != "Non trouvé" else "Non trouvé", 74))}</td>'


mat = "<table class='mat'><tr><th></th>" + "".join(f"<th>{e(a)}</th>" for a in ACTEURS) + "</tr>"
for c, nom in CRIT:
    mat += f"<tr><th class='crit'>{e(nom)}</th>" + "".join(cellule(c, a) for a in ACTEURS) + "</tr>"
mat += "</table>"
slide(entete("Mission 2 · veille", "IKEA face à 5 concurrents") + f'<div class="tab">{mat}</div>', 10,
      source=f"36 cases sourcées et datées (relevés du {DATE_FR}) : livrables/IKEA_Agent_Mission2_Veille.xlsx.")

# 11 · ce que ça change (chaque phrase reprend des lignes sourcées, citées par leur id)
LECONS = [
    ("« Près de toi » = sans voiture", "Un tiers des 18-24 ans n’a pas le permis (Q1.b-1), et seulement 41 % dans l’agglomération parisienne (Q1.b-2). La promesse doit parler du transport des meubles, pas seulement de l’adresse."),
    ("La livraison pèse plus que le prix", "Le kit premier logement le moins cher coûte 190,94 € (Q4.a-total), mais la livraison devant chez soi part de 40 € (Q2.a-1). 76,3 % des e-acheteurs disent abandonner si les frais sont trop élevés (Q2.b-1)."),
    ("Les budgets tiennent", "Kit livré : 230,94 €. Ça rentre dans les 700 € de Léa et les 350 € de Noah (Q4.a-total), en premiers prix. Message possible : « ton studio meublé pour moins de 250 € livré »."),
    ("L’humour fait préférer, pas acheter", "94 % des Gen Z interrogés préfèrent les marques drôles (Q3.a-1), à condition que l’humour soit relié à la marque (Q3.a-2). Donc chaque « raison » montre un vrai produit et son prix."),
    ("TikTok : le terrain est libre", "TikTok est la 1re source d’info produit pour 66 % des jeunes interrogés (Q3.b-1). IKEA France : 104,4 K abonnés, derrière Maisons du Monde (132,6 K) et @actionfrance (554,3 K) (V6)."),
    ("À corriger dans le dossier", "IKEA Family : 200 millions de membres, et non plus 150 (Q5.c-1). Mobilité : l’Insee national remplace l’étude Réunion (Q5.a-1). Le 79 % est confirmé mot pour mot (Q5.d)."),
]
cartes11 = "".join(f'<div class="carte{" forte" if i == 5 else ""}"><div class="num-c">{i + 1:02d}</div><h3>{e(t)}</h3><p>{e(p)}</p></div>'
                   for i, (t, p) in enumerate(LECONS))
slide(entete("Ce que ça change", "6 enseignements pour la campagne") + f'<div class="g3 lecons">{cartes11}</div>', 11,
      source="Chaque phrase reprend des lignes du tableau (id entre parenthèses). Les synthèses complètes de l’agent sont dans l’onglet « Synthèse » des Excel.")

# 12 · limites
slide(entete("Esprit critique", "Ses limites, et nos garde-fous") + '''
<div class="g3">
  <div class="carte"><div class="num-c">LIMITE</div><h3>Il peut mal lire</h3><p>Un modèle peut se tromper de chiffre ou de périmètre. Garde-fou : l’extrait exact est retrouvé dans la page par du code.</p></div>
  <div class="carte"><div class="num-c">LIMITE</div><h3>Le web n’est pas le terrain</h3><p>Il ne remplace pas nos 12 entretiens ni le questionnaire. Garde-fou : la colonne « À creuser » liste ce qu’il reste à demander aux jeunes.</p></div>
  <div class="carte"><div class="num-c">LIMITE</div><h3>Les chiffres vieillissent</h3><p>Prix et abonnés changent. Garde-fou : chaque ligne est datée ; on relance l’agent en double-clic.</p></div>
  <div class="carte"><div class="num-c">LIMITE</div><h3>Sites fermés aux robots</h3><p>TikTok et Instagram bloquent la lecture automatique. Garde-fou : signalé « à contrôler à la main ».</p></div>
  <div class="carte"><div class="num-c">ÉTHIQUE</div><h3>Aucune donnée personnelle</h3><p>Pas de compte, pas de formulaire, pas de profil individuel : seulement des pages publiques.</p></div>
  <div class="carte forte"><div class="num-c">TRANSPARENCE</div><h3>Mention IA partout</h3><p>Chaque livrable dit qu’il a été produit par un agent IA, contrôlé automatiquement puis relu par l’équipe.</p></div>
</div>''', 12, source="Charte d’usage de l’IA du module (mention de l’usage de l’IA dans chaque livrable).")

# 13 · mode d'emploi
slide(entete("Mode d’emploi", "Le relancer en 3 clics") + '''
<div class="g3 etapes">
  <div class="carte"><div class="gros">1</div><h3>Double-clic</h3><p>« Lancer l’agent Fika.cmd » dans le dossier 07 Agent IA.</p></div>
  <div class="carte"><div class="gros">2</div><h3>Choisir</h3><p>1 vérification, 2 veille, 3 les deux. Il travaille seul pendant 15 à 30 minutes et affiche chaque étape.</p></div>
  <div class="carte"><div class="gros">3</div><h3>Ouvrir le tableau</h3><p>Le dossier « livrables » s’ouvre : Excel sourcé et daté, CSV, résumé Markdown.</p></div>
</div>
<div class="g2 bas">
  <div class="carte"><div class="num-c">SANS RIEN INSTALLER</div><p>« Prompt à coller (ChatGPT ou Claude).md » : la même mission, en version copier-coller. Sans contrôleur : la vérification se fait à la main.</p></div>
  <div class="carte"><div class="num-c">CE QU’IL FAUT</div><p>Python et Claude Code connecté à un compte Claude. Le journal de chaque lancement est gardé dans agent/journal.</p></div>
</div>''', 13, source="Dossier : IKEA/07 Agent IA.")

# 14 · fin
slides.append(f'''<section class="slide couv fin">
  <div class="fin-t">Zéro chiffre<br><span>sans source.</span></div>
  <div class="trait large"></div>
  <p class="couv-p">Fika · l’agent de recherche IKÉASTRE</p>
  <small class="couv-pied">{SOURCES}</small>
</section>''')

CSS = (ICI / "style.css").read_text(encoding="utf-8")
doc = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Fika, l’agent IA IKÉASTRE</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;500;700;800;900&family=Noto+Sans+Mono:wght@500;700&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body>{"".join(slides)}</body></html>'''
(ICI / "Fika - Présentation.html").write_text(doc, encoding="utf-8")
print(f"{len(slides)} slides écrites")
