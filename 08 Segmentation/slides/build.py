# Génère index.html (présentation segmentation IKEA x Gen Z) à partir du corpus.
# Les citations sont tirées mot pour mot de corpus/verbatims.json : aucune n'est tapée à la main.
import json, html, pathlib

ICI = pathlib.Path(__file__).parent
CORPUS = ICI.parent / "corpus"
V = {v["id"]: v for v in json.load(open(CORPUS / "verbatims.json", encoding="utf-8"))}
N_V = len(V)
N_SRC = len({v["url"] for v in V.values()})
N_C = len(json.load(open(CORPUS / "chiffres.json", encoding="utf-8")))

def e(s): return html.escape(s, quote=False)

def court(src):
    s = src.split(",")[0].replace("ICI (France Bleu) Occitanie", "ICI Occitanie")
    if s.startswith("jeuxvideo.com"): s = "jeuxvideo.com, forum 18-25"
    return s

def q(vid, cut=None):
    v = V[vid]
    t = v["texte"] if cut is None else cut
    assert t.replace("’", "'") in v["texte"].replace("’", "'"), vid  # garde-fou : extrait exact
    who = v["profil"].split(";")[0].split("(")[0].strip()
    if who.startswith("pseudo"): who = "Pseudo JVC"
    return f'<div class="quote"><q>{e(t)}</q><div class="src"><b>{vid}</b> · {e(who)} · {e(court(v["source"]))}, {v["date"][-4:]}</div></div>'

def head(crumbs, num):
    cr = "".join(f"<span>{c}</span>" for c in crumbs)
    return f'''<div class="topbar"><span><b>Projet IKÉASTRE</b> · B3CPD</span><span class="ctr">Séance 2 · Segmenter et incarner</span><span>Livrable 01 · Analyse de segmentation</span></div>
  <div class="nav"><img src="ikea-logo.png" alt="IKEA"><div class="crumbs">{cr}</div><span class="num">{num:02d} / {{TOTAL}}</span></div>'''

def foot(txt="Concept académique indépendant, non affilié à IKEA. Analyse préparée avec l'aide de l'IA, citations vérifiées mot pour mot."):
    return f'<div class="foot"><span>{txt}</span></div>'

ARROW = '<svg viewBox="0 0 16 16"><path d="M1 8h12M9 4l4 4-4 4" stroke="currentColor" stroke-width="2" fill="none"/></svg>'

# ---------------------------------------------------------------- segments
SEG = [
  dict(k="A", nom="Premier chez-moi", job="« Je m'installe pour de vrai, avec du neuf qui tient, sans me ruiner. »",
       statut="prio", statut_txt="Prioritaire", taille="2,7", unite="M", taille_note="jeunes de 20-29 ans sortis de chez leurs parents et installés depuis moins de 4 ans, hors étudiants du segment B. Ordre de grandeur, calcul p. 15 (C01, C12, C13, C03, C06).",
       attr=5, cap=4,
       crit=[("Socio-démo", "20-29 ans, jeune actif ou alternant, locataire"), ("Comportement", "achète neuf, IKEA par défaut, garde ses meubles"), ("Psycho", "pragmatique, refuse l'occasion (hygiène, galères)"), ("Contexte", "emménagement, souvent sans voiture")],
       jobs=[("Fonctionnel", "Équiper tout l'appart d'un coup, avec un budget fixé (V33)."), ("Émotionnel", "Être sûr que ça ne casse pas au bout de 6 mois (V06)."), ("Social", "Non observé directement : la critique de l'uniformité vient du segment E (V04). À creuser en entretien.")],
       quotes=[("V08", None), ("V07", "emmaus ça me dégoûte j’ai des tocs de propreté du coup voilà je me vois pas acheter des trucs d’occaz"), ("V25", None)],
       freins="Ses freins : la distance (V15), la livraison sans voiture (V25, V26), le samedi (V19), la notice (V03).",
       ids=["V01","V02","V03","V05","V06","V07","V08","V09","V12","V13","V14","V15","V16","V25","V26","V28","V31","V33"],
       persona="Léa, 23 ans", resume="Des jeunes de 20-29 ans qui s'installent pour de vrai et veulent du neuf pas cher qui tienne : IKEA est déjà leur choix, l'accès est leur frein."),
  dict(k="B", nom="Étudiant de passage", job="« Je m'équipe pour l'année, et je ne veux pas m'encombrer quand je repars. »",
       statut="conq", statut_txt="À conquérir", taille="1,3", unite="M", taille_note="étudiants logés dans le parc locatif privé : 3 012 800 inscrits × 44 % (C03, C06). Renouvelé à chaque rentrée.",
       attr=4, cap=3,
       crit=[("Socio-démo", "étudiant, 18-24 ans, parc privé ou Crous"), ("Comportement", "achète pour 8 mois, jette ou récupère"), ("Psycho", "indifférent au design, veut du fonctionnel"), ("Contexte", "rentrée, déménage chaque année, sans voiture")],
       jobs=[("Fonctionnel", "Avoir une chaise et un bureau, vite (V40)."), ("Émotionnel", "Ne pas stresser à l'idée d'abîmer (V40)."), ("Social", "Non observé dans le corpus : à creuser en entretien.")],
       quotes=[("V39", None), ("V17", None), ("V40", "Quand on est étudiant, ce qu’on veut c’est avoir une chaise, on s’en fiche un peu à quoi elle ressemble.")],
       freins="Son vrai concurrent n'est pas une enseigne : c'est le meuble récupéré dans la rue (V18) ou chez les parents (V39).",
       ids=["V17","V18","V19","V30","V32","V37","V39","V40","V44"], persona="Noah, 19 ans", resume="Des étudiants qui s'équipent pour l'année et veulent du pas cher sans s'encombrer : leur concurrent est le meuble récupéré, l'enjeu est de leur faire revendre à IKEA."),
  dict(k="C", nom="Chineur convaincu", job="« Je me meuble sans racheter ce qui existe déjà. »",
       statut="excl", statut_txt="À exclure", taille="n.c.", unite="", taille_note="non chiffrable avec nos sources : l'occasion pèse environ 10 % du marché du meuble en valeur (C24, estimation fragile), sans détail par âge.",
       attr=3, cap=2,
       crit=[("Socio-démo", "étudiant·e, surtout des femmes dans le corpus"), ("Comportement", "Emmaüs, ressourcerie, entraîne ses amis"), ("Psycho", "anti-gaspillage, refuse le neuf par principe"), ("Contexte", "rentrée, petit budget")],
       jobs=[("Fonctionnel", "Se meubler en économisant « au moins 1 000 euros » (V35)."), ("Émotionnel", "Ne pas polluer plus qu'on ne le fait déjà (V38)."), ("Social", "Faire découvrir la seconde main à ses potes (V36).")],
       quotes=[("V38", "Acheter neuf, ce n'est pas quelque chose qui me parle."), ("V41", None), ("V35", None)],
       freins="Ce qui le bloque, c'est le neuf lui-même. IKEA ne le convaincra pas avec une campagne de produits neufs.",
       ids=["V35","V36","V38","V41","V43"], persona="aucun"),
  dict(k="D", nom="Flâneur du samedi", job="« Je viens pour la balade et les boulettes, pas pour un meuble. »",
       statut="oppo", statut_txt="Opportuniste", taille="n.c.", unite="", taille_note="non chiffrable : IKEA France compte 57,7 M de visites (C25), sans part des 18-29 ans ni des visites sans achat.",
       attr=2, cap=5,
       crit=[("Comportement", "visite sans projet, passe au restaurant"), ("Psycho", "plaisir, petit rituel"), ("Contexte", "samedi après-midi, en province")],
       jobs=[("Fonctionnel", "Manger pour « moins de 5 eur » (V22)."), ("Émotionnel", "S'offrir une pause tranquille (V23)."), ("Social", "Non observé dans le corpus.")],
       quotes=[("V23", None), ("V22", None), ("V21", None)],
       freins="Le corpus se contredit : 2 verbatims pour, 3 contre (foule V21, magasin « oppressant » V20, boulettes « dégeu » V24).",
       ids=["V20","V21","V22","V23","V24"], persona="aucun"),
  dict(k="E", nom="Chercheur de pièce unique", job="« Je veux un intérieur qui ne ressemble à celui de personne. »",
       statut="excl", statut_txt="À exclure", taille="n.c.", unite="", taille_note="non chiffrable avec nos sources : aucune donnée sur la part des jeunes qui cherchent des meubles uniques. Corpus mince (4 verbatims).",
       attr=2, cap=1,
       crit=[("Comportement", "cherche du bois massif ou de l'ancien plutôt que du standard"), ("Psycho", "rejette l'uniformité, veut un intérieur qui lui ressemble"), ("Contexte", "quand on monte en gamme après une première installation (V10)")],
       jobs=[("Fonctionnel", "Trouver des meubles solides, en bois massif (V10)."), ("Émotionnel", "Aimer ce qui a du « charme » (V42)."), ("Social", "Ne pas avoir « le même meuble que 99 % de la planète » (V04).")],
       quotes=[("V04", None), ("V27", None), ("V42", None)],
       freins="Ce qu'il fuit, c'est le standard : exactement ce qu'IKEA vend. Corpus mince (4 verbatims) : à confirmer en entretien.",
       ids=["V04","V10","V27","V42"], persona="aucun"),
]
HORS = ["V11", "V29", "V34", "V45"]
assert sorted(sum((s["ids"] for s in SEG), []) + HORS) == sorted(V), "chaque verbatim doit être rangé une seule fois"
TAGCLS = {"prio": "bleu", "conq": "", "oppo": "gris", "excl": "rouge"}

slides = []

# 1 ---------------------------------------------------------------- couverture
cards = "".join(f'''<div class="mini"><span class="tag {s["statut"]}">{s["statut_txt"]}</span><span class="prodname">{s["nom"]}</span>
  <span class="proddesc">Segment {s["k"]} · {len(s["ids"])} verbatims</span>
  <span class="prix s">{s["taille"]}{f'<sup>{s["unite"]}</sup>' if s["unite"] else ''}</span></div>''' for s in SEG)
slides.append(f'''<section class="slide cover">{head(["Projet Gen Z", "Ciblage", "Analyse de segmentation"], 1)}
  <div class="body"><div class="cover-grid">
    <div><span class="badge">Nouveau</span>
      <h1 class="xl mt16">Pour qui,<br>exactement ?</h1>
      <p class="lead">La génération Z n'est pas une cible : c'est une tranche d'âge. À partir de <b>{N_V} verbatims réels</b> et de <b>{N_C} chiffres sourcés</b>, nous la découpons en <b>5 segments</b>, nous les passons aux cinq tests, puis nous choisissons.</p>
      <div class="row mt24" style="align-items:center"><span class="btn">Voir les segments {ARROW}</span><span class="small">Vendredi 6 novembre 2026 · Marie Guinet<br>Loris Demeaux, Tobias Ringot, Eliott Haudiquert</span></div>
    </div>
    <div class="catalogue">{cards}<div class="mini legend"><span class="small">La taille du segment s'affiche comme un prix, son statut comme une étiquette produit.</span></div></div>
  </div></div>
  {foot()}</section>''')

# 2 ---------------------------------------------------------------- méthode
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Méthode"], 2)}
  <div class="body">
    <span class="eyebrow bleu">Méthode data-driven</span>
    <h1>Du corpus aux segments</h1>
    <p class="lead">Aucun segment n'est posé « au feeling » : chacun part de citations réelles, comptées, puis confrontées aux chiffres.</p>
    <div class="steps mt32">
      <div class="step"><span class="n">01</span><h3>Coder</h3><p>Un besoin, un frein et un contexte pour chaque verbatim, avec le prompt du cours.</p></div>
      <div class="step"><span class="n">02</span><h3>Regrouper</h3><p>Des groupes de personnes, pas de thèmes. Au moins deux familles de critères chacun.</p></div>
      <div class="step"><span class="n">03</span><h3>Nommer</h3><p>Un nom qui dit le job, écrit à la première personne.</p></div>
      <div class="step"><span class="n">04</span><h3>Vérifier</h3><p>Compter, citer mot pour mot, garder ce qui contredit, puis les cinq tests.</p></div>
    </div>
    <div class="row mt32">
      <div class="box" style="flex:1"><span class="prix">{N_V}</span><p class="mt8"><b>verbatims réels</b>, recopiés depuis la page</p></div>
      <div class="box" style="flex:1"><span class="prix">{N_SRC}</span><p class="mt8"><b>pages sources</b> : forum 18-25, ICI, France 3</p></div>
      <div class="box" style="flex:1"><span class="prix">{N_C}</span><p class="mt8"><b>chiffres sourcés</b> : Insee, SIES, Dares, IPEA, IKEA</p></div>
      <div class="box bleu" style="flex:1.35"><p><b>Ce qu'on assume</b><br>Toujours 0 entretien. Les verbatims sont publics et la taille des segments est un ordre de grandeur calculé, pas une étude.</p></div>
    </div>
  </div>{foot()}</section>''')

# 3 ---------------------------------------------------------------- le corpus
jvc = sum(1 for v in V.values() if v["source"].startswith("jeuxvideo"))
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Le corpus"], 3)}
  <div class="body">
    <span class="eyebrow bleu">Le corpus</span>
    <h1>{N_V} voix, et leurs limites</h1>
    <div class="cols2 mt20">
      <div>
        <h3>D'où viennent les verbatims</h3>
        <div class="bars mt12">
          <div class="bar"><span class="lab">Forum « Blabla 18-25 ans » (jeuxvideo.com), 12 fils, 2019-2026</span><span class="track"><i style="width:{jvc/N_V*100:.0f}%"></i></span><b>{jvc}</b></div>
          <div class="bar"><span class="lab">Presse régionale avec témoignages (ICI, France 3), 2022-2026</span><span class="track"><i style="width:{(N_V-jvc)/N_V*100:.0f}%" class="o"></i></span><b>{N_V-jvc}</b></div>
        </div>
        <h3 class="mt24">Ce qu'ils couvrent</h3>
        <div class="chips mt12"><span class="chip">IKEA, qualité-prix <i>9</i></span><span class="chip">Accès, transport, montage <i>8</i></span><span class="chip">Seconde main <i>7</i></span><span class="chip">Meuble provisoire <i>6</i></span><span class="chip">Rejet de l'occasion <i>5</i></span><span class="chip">Restaurant, samedi <i>3</i></span><span class="chip">Déco <i>3</i></span><span class="chip">Hard-discount <i>2</i></span></div>
        <p class="small mt8">Comptage issu du codage du prompt du cours (slide 4).</p>
      </div>
      <div class="box">
        <h3>Ce qui fragilise le corpus</h3>
        <ul class="list mt8">
          <li><b>{jvc} verbatims sur {N_V} viennent d'un seul forum</b>, très masculin et provocateur. L'âge y est supposé (nom du forum), jamais vérifié.</li>
          <li><b>{N_V} verbatims, mais pas {N_V} personnes</b> : 6 auteurs parlent deux fois.</li>
          <li><b>Les voix féminines sont presque toutes dans la presse</b>, donc dans le segment C. Ça peut être un effet de source.</li>
          <li><b>V39-V40</b> : cofondateur d'une start-up de location de meubles, avis orienté.</li>
          <li><b>Rien sur TikTok, Pinterest, Temu ou Vinted</b>, et Reddit était inaccessible.</li>
        </ul>
      </div>
    </div>
  </div>{foot()}</section>''')

# 4 ---------------------------------------------------------------- prompt du cours
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Le prompt du cours"], 4)}
  <div class="body">
    <span class="eyebrow bleu">Étape 1 · Coder et regrouper avec l'IA</span>
    <h1>Le prompt du cours, appliqué tel quel</h1>
    <div class="prompt mt16"><span class="k">Prompt envoyé à Claude, avec les {N_V} verbatims numérotés</span>
      Voici {N_V} verbatims numérotés. 1. Attribue à chacun un besoin, un frein et un contexte. 2. Regroupe-les en 3 à 5 groupes. 3. Pour chaque groupe : un nom, le nombre de verbatims, deux citations exactes avec leur numéro. 4. Liste les verbatims qui n'entrent dans aucun groupe. <span class="o">N'invente aucune citation.</span></div>
    <div class="groups mt16">
      <div class="g"><span class="n">9</span><b>Le prix d'abord, IKEA par défaut</b></div>
      <div class="g"><span class="n">7</span><b>La seconde main assumée</b></div>
      <div class="g"><span class="n">5</span><b>Le rejet de l'occasion</b></div>
      <div class="g"><span class="n">8</span><b>Les galères d'accès</b></div>
      <div class="g"><span class="n">6</span><b>Le meuble provisoire</b></div>
      <div class="g hors"><span class="n">10</span><b>Hors groupe</b></div>
    </div>
    <div class="row mt16" style="align-items:stretch">
      <div class="box jaune" style="flex:1"><p><b>Contrôle : 10 citations sur 10 existent mot pour mot</b> dans le corpus (vérification automatique).</p></div>
      <div class="box" style="flex:1.6"><p>L'IA a elle-même signalé ses limites : les auteurs qui parlent deux fois, l'avis orienté de V39-V40, et un effet de source possible entre le forum et la presse.</p></div>
    </div>
  </div>{foot("Réponse complète de l'IA : corpus/reponse_prompt_cours.md. Concept académique indépendant, non affilié à IKEA.")}</section>''')

# 5 ---------------------------------------------------------------- ce qu'on a corrigé
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Vérifier"], 5)}
  <div class="body">
    <span class="eyebrow orange">Étape 2 · Vérifier, contredire</span>
    <h1>Ce que nous avons corrigé dans la réponse de l'IA</h1>
    <p class="lead">L'IA a rangé des <b>thèmes</b>. Un segment, c'est un <b>groupe de personnes</b> qui partage un job. Nous avons donc reconstruit les groupes.</p>
    <table class="mt20">
      <tr><th style="width:30%">Groupe proposé par l'IA</th><th style="width:34%">Problème</th><th>Ce que nous en faisons</th></tr>
      <tr><td><b>Les galères d'accès</b> (8)</td><td>C'est un frein, pas un groupe de personnes.</td><td>Rangés comme <b>freins du segment A</b>, qui achète neuf et doit tout transporter.</td></tr>
      <tr><td><b>Le rejet de l'occasion</b> (5)</td><td>C'est un critère psychographique.</td><td>Il <b>distingue A de C</b> : même âge, même budget, choix opposés.</td></tr>
      <tr><td><b>Le prix d'abord</b> (9) et <b>le meuble provisoire</b> (6)</td><td>Pertinents, mais l'horizon de vie les sépare.</td><td><b>A</b> s'installe pour durer, <b>B</b> s'équipe pour l'année.</td></tr>
      <tr><td><b>Hors groupe</b> (10)</td><td>On y trouve deux vrais comportements.</td><td>Le restaurant et le samedi deviennent <b>D, le flâneur du samedi</b>. Avec V04, V10 et V42, la déco forme <b>E, le chercheur de pièce unique</b>. Il reste 4 verbatims hors segment (V11, V29, V34, V45).</td></tr>
    </table>
    <p class="small mt12">Résultat : 5 segments, et chacun des {N_V} verbatims est rangé une seule fois (vérifié par le script).</p>
  </div>{foot()}</section>''')

# 6 ---------------------------------------------------------------- catalogue
cat = "".join(f'''<div class="pcard"><div class="pvis"><span class="badge {TAGCLS[s["statut"]]}">{s["statut_txt"]}</span><span class="big">{s["k"]}</span></div>
  <span class="tag {s["statut"]} mt8">{s["statut_txt"]}</span><span class="prodname">{s["nom"]}</span><span class="proddesc">{s["job"]}</span>
  <span class="prix s mt8">{s["taille"]}{f'<sup>{s["unite"]}</sup>' if s["unite"] else ''}</span><span class="stars">{"★"*s["attr"]}{"☆"*(5-s["attr"])} <i>({len(s["ids"])})</i></span></div>''' for s in SEG)
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Les 5 segments"], 6)}
  <div class="body">
    <div class="row" style="align-items:flex-end;justify-content:space-between"><div><span class="eyebrow bleu">Étape 3 · Nommer</span><h1>Cinq segments, cinq jobs</h1></div>
    <div class="chips"><span class="chip">Prioritaire <i>1</i></span><span class="chip">À conquérir <i>1</i></span><span class="chip">Opportuniste <i>1</i></span><span class="chip">À exclure <i>2</i></span></div></div>
    <div class="catal mt20">{cat}</div>
    <p class="small mt12">Prix = taille estimée du segment (n.c. = non chiffrable avec nos sources). Étoiles = note d'attractivité sur 5. Entre parenthèses : nombre de verbatims.</p>
  </div>{foot()}</section>''')

# 7-11 ------------------------------------------------------------- fiches
for i, s in enumerate(SEG):
    chips = "".join(f'<span class="chip">{a} <i>{b}</i></span>' for a, b in s["crit"])
    jobs = "".join(f'<div class="job"><span class="k">Job {a.lower()}</span><p>{b}</p></div>' for a, b in s["jobs"])
    quotes = "".join(q(vid, cut) for vid, cut in s["quotes"])
    prix = f'<span class="prix">{s["taille"]}{f"<sup>{s["unite"]}</sup>" if s["unite"] else ""}</span>'
    pers = f'<span class="pill">Persona associé : {s["persona"]}</span>' if s["persona"] != "aucun" else ""
    slides.append(f'''<section class="slide">{head(["Les 5 segments", f'Segment {s["k"]} · {s["nom"]}'], 7 + i)}
  <div class="body"><div class="fiche">
    <div class="visuel"><span class="badge {TAGCLS[s["statut"]]}">{s["statut_txt"]}</span><span class="big">{s["k"]}</span>
      <p class="small mt12">{len(s["ids"])} verbatims sur {N_V} : {", ".join(s["ids"])}</p></div>
    <div class="fcol">
      <span class="tag {s["statut"]}">{s["statut_txt"]}</span>
      <div class="prodname big2">{s["nom"]}</div>
      <div class="proddesc jobline">{s["job"]}</div>
      <div class="row mt12" style="align-items:flex-start;gap:28px">
        <div style="flex:none">{prix}</div>
        <div class="prix-note" style="max-width:420px">{s["taille_note"]}</div>
        <div style="flex:none"><span class="stars">{"★"*s["attr"]}{"☆"*(5-s["attr"])}</span><div class="prix-note">Attractivité {s["attr"]}/5 · Capacité {s["cap"]}/5</div></div>
      </div>
      <div class="chips mt12">{chips}</div>
      <div class="jobs mt12">{jobs}</div>
      <div class="qgrid mt12">{quotes}</div>
      <div class="row mt12" style="align-items:center;gap:12px"><p class="frein">{s["freins"]}</p>{pers}</div>
    </div>
  </div></div>{foot()}</section>''')

# 12 --------------------------------------------------------------- cinq tests
T = {  # Mesurable, Accessible, Substantiel, Différenciable, Actionnable, verdict
 "A": [("ok","≈ 2,7 M (Insee)"),("ok","IKEA Family 12 M (C26), site, réseaux"),("ok","rachète à chaque emménagement (C13)"),("ok","veut du neuf et durable, ≠ B et C"),("ok","relais à 2 € (C28), magasins compacts (C29)"),"Segment exploitable"],
 "B": [("ok","≈ 1,3 M (SIES × OVE)"),("ok","rentrée, campus, Crous"),("mid","volume, mais petit panier"),("ok","horizon de 8 mois, revend ou jette"),("ok","rachat IKEA (C32), relais"),"Exploitable, à investir"],
 "C": [("mid","occasion ≈ 10 % du marché, pas par âge"),("ok","ressourceries, Emmaüs"),("mid","non chiffrable"),("ok","refuse le neuf"),("ko","l'offre IKEA reste du neuf"),"Réel, peu actionnable"],
 "D": [("ko","visites tous âges"),("ok","déjà en magasin"),("ko","pas de projet d'achat"),("mid","un moment plus qu'un profil"),("ok","restaurant, contenus"),"Opportuniste"],
 "E": [("ko","aucune donnée"),("mid","canaux flous : brocantes, artisans"),("mid","4 verbatims seulement"),("ok","fuit le standard"),("ko","l'unique contredit le modèle IKEA"),"Réel, hors de portée d'IKEA"],
}
sym = {"ok": "✓ Oui", "mid": "~ Partiel", "ko": "✕ Non"}
rows = "".join(f'<tr><td><b>{s["k"]} · {s["nom"]}</b></td>' + "".join(f'<td><span class="{c}">{sym[c]}</span><br>{t}</td>' for c, t in T[s["k"]][:5]) + f'<td><b>{T[s["k"]][5]}</b></td></tr>' for s in SEG)
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Les cinq tests"], 12)}
  <div class="body">
    <span class="eyebrow bleu">Étape 4 · D'après Philip Kotler</span>
    <h1>Un segment, ou juste un public ?</h1>
    <table class="mt16 tests"><tr><th>Segment</th><th>Mesurable</th><th>Accessible</th><th>Substantiel</th><th>Différenciable</th><th>Actionnable</th><th>Verdict</th></tr>{rows}</table>
  </div>{foot()}</section>''')

# 13 --------------------------------------------------------------- matrice
def pos(s):
    x = (s["cap"] - 0.5) / 5 * 100
    y = 100 - (s["attr"] - 0.5) / 5 * 100
    return x, y
dots = "".join(f'<div class="dot {s["statut"]}{" left" if s["cap"]>=4 else ""}" style="left:{pos(s)[0]}%;top:{pos(s)[1]}%"><b>{s["k"]}</b><span>{s["nom"]}</span></div>' for s in SEG)
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Prioriser"], 13)}
  <div class="body">
    <span class="eyebrow bleu">Étape 5 · Le ciblage</span>
    <h1>La matrice de priorisation</h1>
    <div class="mx-wrap mt16">
      <div class="mx">
        <div class="q q1"><span>À conquérir</span></div><div class="q q2"><span>Prioritaire</span></div>
        <div class="q q3"><span>À exclure</span></div><div class="q q4"><span>Opportuniste</span></div>
        {dots}
        <div class="ax-y">Attractivité : taille, croissance, valeur ↑</div>
        <div class="ax-x">Capacité à le servir : marque, canaux, ressources →</div>
      </div>
      <div class="mx-side">
        <div class="steplist"><div><span class="n">1</span><p>Chaque segment est noté <b>de 1 à 5 sur les deux axes</b>.</p></div>
        <div><span class="n">2</span><p>Chaque note est <b>justifiée par un verbatim ou un chiffre</b> (slide suivante).</p></div>
        <div><span class="n o">3</span><p>Seuil à 3,5 : au-dessus, l'axe est « haut ». <b>1 prioritaire, 1 à conquérir, 2 exclus.</b></p></div></div>
      </div>
    </div>
  </div>{foot()}</section>''')

# 14 --------------------------------------------------------------- justification
J = {
 "A": ("5", "79 % des ménages de moins de 30 ans habitent leur logement depuis moins de 4 ans, et 80 % sont locataires (C13, C15) : ils emménagent souvent, donc rachètent souvent.", "4", "IKEA est déjà le choix par défaut (V02, V08, V14). Le frein, c'est l'accès (V15, V25), pour lequel IKEA a déjà des relais à 2 € (C28) et des magasins compacts (C29)."),
 "B": ("4", "1,3 M d'étudiants dans le parc privé (C03, C06), renouvelés à chaque rentrée. Mais le budget est serré : 637 € de loyer moyen (C19).", "3", "Le rachat (C32) et les relais existent, mais l'image « jetable » colle (V17, V19) et la récup est gratuite (V18)."),
 "C": ("3", "L'occasion progresse (≈ 1 meuble sur 4, C24, fragile) et ces jeunes la prescrivent à leurs amis (V36).", "2", "Ils refusent le neuf par principe (V38, V41), alors que l'offre IKEA reste du neuf."),
 "D": ("2", "Pas de projet d'achat, et 3 verbatims sur 5 sont négatifs (V20, V21, V24).", "5", "Ils sont déjà dans le magasin : 57,7 M de visites par an chez IKEA France (C25)."),
 "E": ("2", "4 verbatims sur 45 et aucune donnée de taille. Budget plutôt plus élevé (bois massif, V10).", "1", "Le standard est la promesse même d'IKEA : ce segment fuit « le même meuble que 99 % de la planète » (V04)."),
}
rows = "".join(f'<tr><td><span class="tag {s["statut"]}">{s["statut_txt"]}</span><br><b>{s["k"]} · {s["nom"]}</b></td><td class="note">{J[s["k"]][0]}</td><td>{J[s["k"]][1]}</td><td class="note">{J[s["k"]][2]}</td><td>{J[s["k"]][3]}</td></tr>' for s in SEG)
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Justifier les notes"], 14)}
  <div class="body">
    <span class="eyebrow bleu">Chaque note a sa preuve</span>
    <h1>Pourquoi ces notes</h1>
    <table class="mt16 just"><tr><th style="width:15%">Segment</th><th style="width:5%">Attr.</th><th style="width:37%">Justification</th><th style="width:5%">Cap.</th><th>Justification</th></tr>{rows}</table>
  </div>{foot("V = verbatim, C = chiffre (corpus/chiffres.json). Non affilié à IKEA.")}</section>''')

# 15 --------------------------------------------------------------- calcul de taille
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Mesurer"], 15)}
  <div class="body">
    <span class="eyebrow bleu">Test « Mesurable »</span>
    <h1>Comment nous avons chiffré A et B</h1>
    <div class="cols2 mt20">
      <div>
        <div class="calc"><span class="k">A · Premier chez-moi</span>
          <div class="ln"><span>20-24 ans hors foyer parental</span><span>3 935 000 × 47 %</span><b>1 849 450</b></div>
          <div class="ln"><span>25-29 ans hors foyer parental</span><span>3 996 000 × 81,5 %</span><b>3 256 740</b></div>
          <div class="ln"><span>installés depuis moins de 4 ans</span><span>5 106 190 × 79 %</span><b>4 033 890</b></div>
          <div class="ln"><span>moins les étudiants du segment B</span><span>− 1 325 632</span><b>≈ 2,7 M</b></div>
        </div>
        <div class="calc mt16"><span class="k">B · Étudiant de passage</span>
          <div class="ln"><span>inscrits dans le supérieur 2024-25</span><span>3 012 800 × 44 %</span><b>≈ 1,3 M</b></div>
        </div>
      </div>
      <div class="box">
        <h3>Sources et limites du calcul</h3>
        <ul class="list mt8">
          <li><b>C01</b> Insee, population au 1/1/2026 (provisoire).</li>
          <li><b>C12</b> Insee, part vivant chez les parents (2018) : 18-24 ans 58 % H, 48 % F, soit 53 % en moyenne ; 25-29 ans 24 % H, 13 % F, soit 18,5 %. Le taux des 18-24 est appliqué aux 20-24 : il surestime un peu le maintien chez les parents.</li>
          <li><b>C13</b> Insee Première n°2090 : un taux de <b>ménages</b>, appliqué à des <b>personnes</b>.</li>
          <li><b>C03, C06</b> SIES et OVE (2023) : 44 % des étudiants dans le parc locatif privé.</li>
          <li>Résultat : <b>un ordre de grandeur</b> pour comparer les segments, pas une taille de marché.</li>
        </ul>
      </div>
    </div>
  </div>{foot()}</section>''')

# 16 --------------------------------------------------------------- décision
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Décision"], 16)}
  <div class="body">
    <span class="eyebrow bleu">Ce que nous retenons, ce à quoi nous renonçons</span>
    <h1>Notre choix</h1>
    <div class="dec mt20">
      <div class="box bleu big-dec"><span class="badge jaune">Prioritaire</span><div class="prodname mt12" style="font-size:24px">A · Premier chez-moi</div>
        <p class="mt8">C'est le cœur du brief : <b>« devenir le réflexe de la Gen Z à chaque emménagement »</b>. IKEA est déjà son choix, il faut lever l'accès : relais, livraison, magasins compacts.</p>
        <p class="mt8"><b>Persona : Léa, 23 ans.</b></p></div>
      <div class="box orange"><span class="badge gris">À conquérir</span><div class="prodname mt12" style="font-size:18px">B · Étudiant de passage</div>
        <p class="mt8">Seconde cible, à condition d'investir : une offre « rentrée » pensée pour être <b>revendue à IKEA</b> en fin d'année (rachat existant). <b>Persona : Noah, 19 ans.</b></p></div>
      <div class="box"><span class="tag oppo">Opportuniste</span><div class="prodname mt8" style="font-size:16px">D · Flâneur du samedi</div>
        <p class="mt8">Aucun budget dédié. On le capte là où il est déjà : le restaurant et les contenus drôles.</p></div>
      <div class="box"><span class="tag excl">À exclure</span><div class="prodname mt8" style="font-size:16px">C · Chineur convaincu</div>
        <p class="mt8">Une campagne de produits neufs ne le convaincra pas. On ne le vise pas, sans le contredire : l'espace seconde vie reste là.</p></div>
      <div class="box"><span class="tag excl">À exclure</span><div class="prodname mt8" style="font-size:16px">E · Chercheur de pièce unique</div>
        <p class="mt8">Vendre du standard à quelqu'un qui fuit le standard est perdu d'avance. On assume de ne pas le viser.</p></div>
    </div>
  </div>{foot()}</section>''')

# 17 --------------------------------------------------------------- suite
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Et maintenant"], 17)}
  <div class="body">
    <span class="eyebrow bleu">Ce que la segmentation change pour le projet</span>
    <h1>Trois conséquences, trois questions</h1>
    <div class="cols2 mt20">
      <div>
        <div class="cons"><span class="n">1</span><div><h3>L'accès compte plus que le prix</h3><p>Le segment prioritaire trouve déjà IKEA bon marché. Ce qui le perd, c'est la route, la livraison et le samedi. La campagne doit parler d'abord d'accès.</p></div></div>
        <div class="cons"><span class="n">2</span><div><h3>L'humour a un terrain : les galères</h3><p>Les notices (V03), la vis en trop, le jingle qu'on a en tête (V34), le samedi en magasin : le corpus donne la matière, à condition de ne jamais se moquer du client.</p></div></div>
        <div class="cons"><span class="n">3</span><div><h3>Nos personas tiennent, avec un correctif</h3><p>Léa incarne A et Noah incarne B. Mais Noah doit devenir un profil « de passage » qui revend, pas un mini-Léa.</p></div></div>
      </div>
      <div class="box">
        <h3>À vérifier en entretien</h3>
        <ul class="list mt8">
          <li>Quel job social pour B ? Le corpus ne dit rien sur le regard des autres.</li>
          <li>Le rejet de l'occasion (V07, V31) concerne-t-il aussi les filles ? Le corpus ne permet pas de le dire.</li>
          <li>Un étudiant revendrait-il ses meubles à IKEA s'il connaissait le rachat ?</li>
        </ul>
        <p class="small mt12">Cible : 8 à 10 entretiens courts (A et B), avec les mêmes questions.</p>
      </div>
    </div>
  </div>{foot()}</section>''')

# 18 --------------------------------------------------------------- sources
srcs = {}
for v in V.values(): srcs.setdefault(v["url"], (v["source"], v["date"], []))[2].append(v["id"])
press = [(s, d, ids) for u, (s, d, ids) in srcs.items() if not s.startswith("jeuxvideo")]
jv = sorted({s.split("topic")[1].strip(" «»") if "topic" in s else s for s, d, ids in srcs.values() if s.startswith("jeuxvideo")})
pl = "".join(f"<li><b>{', '.join(ids)}</b> · {e(s)} ({d})</li>" for s, d, ids in press)
jl = "".join(f"<li>{e(t)}</li>" for t in jv)
slides.append(f'''<section class="slide">{head(["Analyse de segmentation", "Sources"], 18)}
  <div class="body">
    <span class="eyebrow bleu">Annexe</span>
    <h1>Sources</h1>
    <div class="cols3 mt16 srcs">
      <div><h3>Verbatims · presse ({N_V-jvc})</h3><ul>{pl}</ul></div>
      <div><h3>Verbatims · jeuxvideo.com, Blabla 18-25 ({jvc})</h3><ul>{jl}</ul></div>
      <div><h3>Chiffres utilisés</h3><ul>
        <li><b>C01, C12</b> Insee, population 2026 et décohabitation (2022)</li>
        <li><b>C13, C15</b> Insee Première n°2090, janv. 2026</li>
        <li><b>C16</b> Insee, voiture des ménages, 2026</li>
        <li><b>C03</b> SIES, note 25.15, déc. 2025</li>
        <li><b>C06</b> OVE 2023, via ministère du Logement, 2025</li>
        <li><b>C19</b> FAGE, coût de la rentrée 2026</li>
        <li><b>C24</b> Xerfi citant l'IPEA, août 2026 (fragile)</li>
        <li><b>C25, C26, C28</b> IKEA France, bilan FY25, 04/11/2025</li>
        <li><b>C29</b> IKEA France, 01/06/2026</li>
        <li><b>C32</b> ikea.com/fr, rachat, consulté le 06/11/2026</li>
      </ul><p class="small mt8">URL complètes : corpus/verbatims.md et corpus/chiffres.md.</p></div>
    </div>
  </div>{foot()}</section>''')

total = len(slides)
out = open(ICI / "index.html", "w", encoding="utf-8")
out.write(f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Pour qui, exactement ?</title>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="style.css"><link rel="stylesheet" href="deck.css"></head><body>
{"".join(slides).replace("{TOTAL}", f"{total:02d}")}
</body></html>''')
out.close()
print("ok", total, "slides")
