"""Lecture de pages web et PDF en texte brut, partagée par l'agent (lire_page.py)
et par le contrôleur (verifier.py) : les deux voient exactement le même texte."""
import hashlib
import html
import io
import json
import os
import re
import unicodedata
from pathlib import Path

import requests

CACHE = Path(__file__).resolve().parent.parent / "travail" / "cache"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.6"}


def _html_to_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg|template)[^>]*>.*?</\1>", " ", raw)
    # garder le contenu utile des balises meta (descriptions, dates)
    metas = re.findall(r'(?is)<meta[^>]+(?:name|property)="(?:description|og:description|article:published_time|article:modified_time|date|dc\.date)"[^>]*content="([^"]*)"', raw)
    raw = re.sub(r"(?i)<br\s*/?>|</(p|div|li|h[1-6]|tr|td|th|section|article)>", "\n", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    text = html.unescape(raw)
    text = "\n".join(metas) + "\n" + text
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def lire(url: str, timeout: int = 25) -> dict:
    """Renvoie {ok, statut_http, texte, type, erreur}. Met en cache sur disque."""
    CACHE.mkdir(parents=True, exist_ok=True)
    key = CACHE / (hashlib.sha1(url.encode()).hexdigest() + ".json")
    if key.exists():
        return json.loads(key.read_text(encoding="utf-8"))
    res = {"ok": False, "statut_http": None, "texte": "", "type": "", "erreur": "", "url": url}
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        res["statut_http"] = r.status_code
        ctype = r.headers.get("content-type", "")
        res["type"] = ctype
        if r.status_code >= 400:
            res["erreur"] = f"HTTP {r.status_code}"
        elif "pdf" in ctype or url.lower().split("?")[0].endswith(".pdf"):
            from pypdf import PdfReader
            pdf = PdfReader(io.BytesIO(r.content))
            res["texte"] = "\n".join((p.extract_text() or "") for p in pdf.pages)
            res["ok"] = True
        else:
            r.encoding = r.apparent_encoding if not r.encoding or r.encoding.lower() == "iso-8859-1" else r.encoding
            res["texte"] = _html_to_text(r.text)
            res["ok"] = len(res["texte"]) > 200
            if not res["ok"]:
                res["erreur"] = "page vide (contenu chargé en JavaScript ?)"
    except Exception as e:  # réseau, SSL, PDF illisible
        res["erreur"] = f"{type(e).__name__}: {e}"[:300]
    if res["ok"]:  # on ne met en cache que les lectures réussies
        key.write_text(json.dumps(res, ensure_ascii=False), encoding="utf-8")
    return res


def normaliser(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("«", '"').replace("»", '"').replace("–", "-").replace("—", "-").replace("−", "-")
    s = s.replace(" ", " ").replace(" ", " ")
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def _mots(s: str):
    return re.findall(r"[\w%€]+", normaliser(s))


def trouver_extrait(extrait: str, texte: str) -> tuple[str, float]:
    """Cherche l'extrait dans le texte. Renvoie (verdict, score) :
    'exact' si présent tel quel, 'proche' si >= 85 % des groupes de 4 mots s'y trouvent,
    sinon 'absent'."""
    e, t = normaliser(extrait), normaliser(texte)
    if e and e in t:
        return "exact", 1.0
    me, mt = _mots(extrait), _mots(texte)
    if len(me) < 4:
        return ("exact", 1.0) if " ".join(me) in " ".join(mt) else ("absent", 0.0)
    grams_t = {tuple(mt[i:i + 4]) for i in range(len(mt) - 3)}
    grams_e = [tuple(me[i:i + 4]) for i in range(len(me) - 3)]
    score = sum(g in grams_t for g in grams_e) / len(grams_e)
    return ("proche" if score >= 0.85 else "absent"), round(score, 2)
