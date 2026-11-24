"""Présentation orale de la veille Session 1 (une idée par slide), à partir de veille.json.
Produit presentation.html puis « Présentation veille Session 1.pdf » (DA de groupe, 16:9).
Usage : python presentation.py"""
import html
import json
import sys
from pathlib import Path

from build import pdf as imprimer

ICI = Path(__file__).resolve().parent
D = json.loads((ICI / "veille.json").read_text(encoding="utf-8"))
NOM = "Présentation veille Session 1"
e = lambda s: html.escape(s, quote=True)
LIGNES = D["lignes"]
NB_SRC = len({l["source"]["url"] for l in LIGNES}) + 1
SLIDES = []


def src(*idx):
    """Sources des lignes de veille.json (index), au format court « organisme, date »."""
    return " · ".join(f'{LIGNES[i]["source"]["organisme"]}, {LIGNES[i]["source"]["date"]}' for i in idx)


def slide(crumb, corps, sources="", classe=""):
    SLIDES.append((crumb, corps, sources, classe))


def chiffre(valeur, unite, texte, couleur="bleu"):
    return (f'<div class="kpi {couleur}"><div class="val">{valeur}<sup>{unite}</sup></div>'
            f'<p>{texte}</p></div>')


# 1. Couverture
slide("Session 1", f'''
<div class="cover-grid"><div>
<span class="badge bleu">Veille stratégique · Session 1</span>
<h1 class="xl mt16">Ce qui peut changer la donne.</h1>
<p class="lead">Les magasins IKEA compacts face aux jeunes adultes (18-29 ans), en France, à horizon 2030. Regard <b>MARKET</b>.</p>
<p class="small mt24">Équipe IKÉASTRE · Loris, Tobias, Eliott · B3CPD · {e(D["date"])}</p>
</div>
<div class="box jaune big"><div class="val">10</div><p><b>magasins compacts supplémentaires</b> visés par IKEA en France d'ici 2030.</p>
<p class="small mt8">IKEA France, communiqué ChooseFrance, 01/06/2026</p></div></div>''', classe="cover")

# 2. Point de départ
slide("Point de départ", f'''
<div class="eyebrow bleu">Point de départ</div>
<h1 class="h2">Un format annoncé, une expérience à inventer.</h1>
<div class="trio mt32">
<div><span class="n">01</span><h3>Le format existe</h3><p>Premier magasin compact à Limoges le 27 mai 2026, un autre en préparation au Mans.</p></div>
<div><span class="n">02</span><h3>La cible est là</h3><p>Les 18-29 ans s'équipent à chaque déménagement, avec un budget serré et souvent sans voiture.</p></div>
<div><span class="n">03</span><h3>La question</h3><p><b>Est-ce que ce format tient la route pour eux en 2030, et quelle expérience digitale l'accompagne ?</b></p></div>
</div>''', f'{D["contexte"]["source"]["organisme"]}, {D["contexte"]["source"]["date"]}')

# 3. Méthode
slide("Méthode", f'''
<div class="eyebrow bleu">Notre méthode</div>
<h1 class="h2">Observer large, ne garder que le vérifiable.</h1>
<div class="row mt32" style="gap:56px">
{chiffre("8", "/8", "champs de veille traités, comme demandé par le cours")}
{chiffre(str(len(LIGNES)), "", "informations retenues, chacune reliée au projet")}
{chiffre(str(NB_SRC), "", "sources datées, avec lien et extrait exact")}
</div>
<div class="crit5 mt32">
<div><b>Auteur</b><p>Qui produit l'information</p></div><div><b>Date</b><p>Encore d'actualité ?</p></div>
<div><b>Périmètre</b><p>Quel marché, quel public</p></div><div><b>Méthode</b><p>Enquête, estimation, déclaration</p></div>
<div><b>Corroboration</b><p>Extrait retrouvé mot pour mot</p></div></div>''')

# 4. Tendances lourdes
slide("Tendances lourdes", f'''
<div class="eyebrow bleu">Tendances lourdes</div>
<h1 class="h2">Un marché qui bouge sous nos pieds.</h1>
<div class="kpis4 mt32">
{chiffre("79", "%", "des ménages de moins de 30 ans vivent dans leur logement depuis moins de 4 ans.")}
{chiffre("-1,8", "%", "pour le meuble neuf en 2025 (13,6 Md€), après -5,1 % en 2024.", "noir")}
{chiffre("1/4", "", "des meubles vendus en France serait d'occasion (estimation à corroborer).", "noir")}
{chiffre("+7", "%", "pour le commerce en ligne en 2025 : 196,4 Md€.")}
</div>
<div class="box bleu mt32"><p><b>Ce que ça change :</b> le besoin revient à chaque déménagement, mais le neuf recule face à l'occasion et au digital. Le magasin compact doit se justifier par la proximité et le coût complet, et travailler avec le site.</p></div>''',
      src(0, 1, 2, 3))

# 5. La cible
slide("Notre cible", f'''
<div class="eyebrow bleu">Évolutions des usages · Inclusion</div>
<h1 class="h2">Une cible mobile, connectée, souvent sans voiture.</h1>
<div class="kpis3 mt32">
{chiffre("1/3", "", "des ménages de moins de 30 ans n'a pas de voiture.", "noir")}
{chiffre("76", "%", "des 16-25 ans utilisent Instagram, 63 % Snapchat, 60 % TikTok.")}
{chiffre("31", "%", "des cyberacheteurs utilisent déjà l'IA générative pour leurs achats.")}
</div>
<div class="box bleu mt32"><p><b>Ce que ça change :</b> un magasin compact en zone commerciale reste difficile d'accès. Transports, retrait et livraison comptent autant que le magasin ; la découverte passe par les réseaux et par l'IA.</p></div>''',
      src(10, 12, 11))

# 6. Concurrence
conc = {x["ref"].split("ligne ")[1]: x for x in D["sources_concurrence"]}
slide("Concurrence", f'''
<div class="eyebrow bleu">Dimension concurrentielle · la plus stratégique</div>
<h1 class="h2">Tout le monde se rapproche du client.</h1>
<table class="conc mt24"><thead><tr><th style="width:18%">Enseigne</th><th>Ce qu'elle fait</th><th style="width:34%">Ce que ça veut dire pour IKEA</th></tr></thead><tbody>
<tr><td><b>But</b></td><td>Magasins de 1 200 à 1 500 m², dans des villes dès 7 000 habitants, mais en périphérie.</td><td>Le petit format n'est pas une différence en soi.</td></tr>
<tr><td><b>Action</b></td><td>900 magasins en France, un magasin au centre de Paris, 554 K abonnés TikTok (IKEA France : 104 K).</td><td>La proximité et la visibilité auprès des jeunes sont déjà prises.</td></tr>
<tr><td><b>Leboncoin</b></td><td>2e site e-commerce français ; Livraison XL des meubles entre particuliers dès 19,49 €.</td><td>Le vrai concurrent du neuf pour un jeune, c'est l'occasion.</td></tr>
</tbody></table>
<div class="box jaune mt24"><p><b>Il faut une raison de venir chez IKEA plutôt qu'ailleurs.</b></p></div>''',
      f'{src(4)} · Action, 15/12/2025 · Le Bonbon, 02/09/2025 · TikTok, relevé du 05/11/2026 · Ecommerce Nation, 24/03/2026 et 05/05/2025')

# 7. Réglementation
slide("Ce que la loi impose", f'''
<div class="eyebrow rouge">Accessibilité · Réglementation · Durabilité</div>
<h1 class="h2">Trois règles à poser dès la conception.</h1>
<div class="trio mt32">
<div><span class="tag excl">Obligation légale · 28/06/2025</span><h3 class="mt8">Accessibilité</h3><p>La directive européenne impose un commerce en ligne accessible aux personnes handicapées (entre 5,7 et 18,2 millions de personnes en France selon la définition).</p></div>
<div><span class="tag excl">Obligation légale · 02/08/2026</span><h3 class="mt8">Transparence de l'IA</h3><p>L'AI Act oblige à prévenir l'utilisateur quand il parle à une IA (chatbot, agent, avatar). Le RGPD s'ajoute si on utilise la localisation.</p></div>
<div><span class="tag prio">Tendance documentée</span><h3 class="mt8">Sobriété numérique</h3><p>La fabrication des appareils pèse le plus dans l'empreinte du numérique : mieux vaut s'appuyer sur le smartphone du client que sur des bornes neuves.</p></div>
</div>
<div class="box bleu mt32"><p><b>Ce que ça change :</b> la conformité est une ligne du budget dès le scénario minimal viable, pas une option.</p></div>''',
      src(8, 9, 13, 6))

# 8. Signaux faibles
slide("Signaux faibles", f'''
<div class="eyebrow orange">Signaux faibles</div>
<h1 class="h2">Trois indices à surveiller, pas à prendre pour acquis.</h1>
<div class="trio mt32">
<div><span class="tag conq">31/03/2025</span><h3 class="mt8">Le social commerce</h3><p>TikTok Shop permet d'acheter sans quitter l'appli en France.</p><p class="mt8"><b>Pour nous :</b> le magasin compact comme lieu de retrait ou d'essai de ce qu'on a vu en vidéo.</p></div>
<div><span class="tag conq">5 % → 25 % ?</span><h3 class="mt8">Les agents d'achat IA</h3><p>Pas encore disponibles en France ; moins de 5 % du trafic marchand aujourd'hui, près de 25 % possible d'ici 2030.</p><p class="mt8"><b>Pour nous :</b> stock et prix lisibles par ces agents.</p></div>
<div><span class="tag conq">Oslo, Madrid</span><h3 class="mt8">IKEA Preowned</h3><p>Place de marché d'occasion entre particuliers, étendue à la Norvège et à l'Espagne.</p><p class="mt8"><b>Pour nous :</b> le compact comme point de remise entre particuliers.</p></div>
</div>''', src(14, 15, 16))

# 9. Opportunité
slide("Notre opportunité", f'''
<div class="eyebrow bleu">Opportunité de différenciation</div>
<h1 class="h2">Réunir dans un lieu proche ce que les autres font séparément.</h1>
<div class="trio mt32">
<div class="box"><h3>Seconde vie</h3><p class="mt8">IKEA reprend déjà ses meubles usagés contre un bon d'achat et les revend en magasin.</p></div>
<div class="box"><h3>Visualiser chez soi</h3><p class="mt8">IKEA Kreativ permet de scanner sa pièce et d'y tester des meubles : le compact expose peu, la gamme se voit chez soi.</p></div>
<div class="box"><h3>Retrait bon marché</h3><p class="mt8">Point relais à 2 € pour IKEA Family, 7 € sinon (relevé du 05/11/2026).</p></div>
</div>
<div class="box jaune mt32"><p><b>La différence se fera sur la brique digitale et sur l'accès sans voiture.</b> Les attentes de la cible restent à confirmer sur le terrain.</p></div>''',
      f'{src(7, 5)} · IKEA France, page livraison, relevé du 05/11/2026')

# 10. Veille continue
lignes_plan = "".join(f'<tr><td><b>{e(x["question"])}</b></td><td>{e(x["frequence"])}</td><td class="imp">{e(x["decision"])}</td></tr>'
                      for x in D["plan_veille"])
slide("Veille continue", f'''
<div class="eyebrow bleu">Organisée · continue · décisionnelle</div>
<h1 class="h2">Ce qu'on continue de surveiller.</h1>
<table class="conc dense mt24"><thead><tr><th style="width:42%">Question de veille</th><th style="width:20%">Fréquence</th><th>Décision éclairée</th></tr></thead>
<tbody>{lignes_plan}</tbody></table>''')

# 11. Suite
slide("Et maintenant", f'''
<div class="eyebrow bleu">Prochaine étape</div>
<h1 class="h2">Choisir la brique digitale du magasin compact.</h1>
<div class="kpis4 mt32">
<div class="pistes"><span class="n">A</span><h3>Scanner sa pièce</h3><p>IKEA Kreativ</p></div>
<div class="pistes"><span class="n">B</span><h3>Retrait de commandes</h3><p>Le compact comme point de retrait</p></div>
<div class="pistes"><span class="n">C</span><h3>Reprise des meubles</h3><p>Seconde vie de quartier</p></div>
<div class="pistes"><span class="n">D</span><h3>Assistant IA</h3><p>Préparer sa visite, annoncé comme IA</p></div>
</div>
<h3 class="mt32">Encore à vérifier pour la Session 2</h3>
<ul class="q mt8">{"".join(f"<li>{e(q)}</li>" for q in D["a_creuser"][1:5])}</ul>''')

CSS = """
.slide .body { padding-top: 0; padding-bottom: 24px; justify-content: center; }
h1.h2 { font-size: 46px; letter-spacing: -.8px; max-width: 1100px; }
.cover .body { justify-content: center; }
.cover .lead { font-size: 19px; }
.cover-grid { display: grid; grid-template-columns: 1.45fr 1fr; gap: 56px; align-items: center; }
.box.big { padding: 32px; }
.box.big .val { font-size: 120px; font-weight: 800; letter-spacing: -4px; line-height: 1; color: var(--bleu); }
.box.big p { font-size: 18px; }
.kpi .val { font-size: 76px; font-weight: 800; letter-spacing: -2px; line-height: 1; display: inline-flex; align-items: flex-start; }
.kpi .val sup { font-size: 26px; margin: 6px 0 0 3px; letter-spacing: 0; }
.kpi.bleu .val { color: var(--bleu); } .kpi.noir .val { color: var(--noir); }
.kpi p { font-size: 16.5px; margin-top: 10px; max-width: 300px; }
.kpis4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 32px; }
.kpis3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
.kpis4 > div, .kpis3 > div { border-top: 4px solid var(--jaune); padding-top: 14px; }
.trio { display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }
.trio > div:not(.box) { border-top: 4px solid var(--noir); padding-top: 12px; }
.trio .n, .pistes .n { font-size: 12px; font-weight: 700; color: var(--gris-doux); }
.trio h3 { font-size: 20px; margin: 2px 0 6px; }
.trio p { font-size: 16px; }
.trio .tag { font-size: 14px; }
.box p { font-size: 17px; }
.box { padding: 20px 22px; }
.crit5 { display: grid; grid-template-columns: repeat(5, 1fr); gap: 18px; }
.crit5 div { background: var(--fond-gris); padding: 14px; }
.crit5 b { font-size: 17px; }
.crit5 p { font-size: 14.5px; }
table.conc td { font-size: 16px; padding: 13px 12px; line-height: 1.4; }
table.conc th { font-size: 14px; }
table.conc.dense td { font-size: 14.5px; padding: 9px 12px; }
table.conc td.imp { color: var(--noir); background: #fffbe0; }
.pistes h3 { font-size: 20px; margin: 2px 0 4px; }
.pistes p { font-size: 16px; }
ul.q { padding-left: 20px; }
ul.q li { font-size: 16px; margin-bottom: 6px; }
.foot { height: auto; min-height: 34px; padding: 8px 0; }
.foot .src { line-height: 1.4; }
"""


def rendre():
    total = len(SLIDES)
    out = []
    for i, (crumb, corps, sources, classe) in enumerate(SLIDES, 1):
        top = (f'<div class="topbar"><span><b>Projet IKÉASTRE</b> · B3CPD</span>'
               f'<span class="ctr">Session 1 · Veille stratégique</span><span>Présentation</span></div>'
               f'<div class="nav"><img src="ikea-logo.png" alt="Logo IKEA"><div class="crumbs"><span>Magasins compacts</span>'
               f'<span>Veille</span><span>{e(crumb)}</span></div><span class="num">{i:02d} / {total:02d}</span></div>')
        pied = f'Sources : {e(sources)}' if sources else "Concept académique indépendant, non affilié à IKEA. Veille préparée avec l'aide de l'IA, relue par l'équipe."
        out.append(f'<section class="slide {classe}">{top}<div class="body">{corps}</div>'
                   f'<div class="foot"><span class="src">{pied}</span></div></section>')
    return ('<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Veille stratégique · Présentation</title>'
            '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">'
            f'<link rel="stylesheet" href="style.css"><style>{CSS}</style></head><body>{"".join(out)}</body></html>')


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    h = ICI / "presentation.html"
    h.write_text(rendre(), encoding="utf-8")
    print("PDF :", imprimer(h, ICI / f"{NOM}.pdf").name)
