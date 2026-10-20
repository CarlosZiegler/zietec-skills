# -*- coding: utf-8 -*-
# Forja · i18n EN · PT · DE construído no próprio build. Todo texto é escrito como T(pt, en, de);
# o build define o idioma corrente (set_lang) e chama os geradores 3 vezes.
# Configure SCREEN_BASE com o idioma-base das telas (mercado-alvo); pitch e doc têm base PT.
# Arquivos do idioma-base não têm sufixo; os outros levam -EN/-PT/-DE (telas) ou Pitch-EN-01 / Doc-DE-01.
import re

LANGS = ["en", "pt", "de"]                 # ordem fixa do seletor
BASE = "pt"                                # idioma-base de pitch e doc
SCREEN_BASE = "en"                         # idioma-base das telas: troque por "de" ou "pt" conforme o mercado
NAMES = {"en": "English", "pt": "Português", "de": "Deutsch"}
HTML_LANG = {"en": "en", "pt": "pt-BR", "de": "de"}
_cur = {"lang": BASE}


def set_lang(l):
    assert l in LANGS, l
    _cur["lang"] = l


def lang():
    return _cur["lang"]


def T(pt, en, de):
    return {"pt": pt, "en": en, "de": de}[_cur["lang"]]


def set_screen_base(l):
    global SCREEN_BASE
    assert l in LANGS, l
    SCREEN_BASE = l


def sfx(l=None):
    l = l or _cur["lang"]
    return "" if l == SCREEN_BASE else "-" + l.upper()


def fname(base, l=None):
    return base.replace(".dc.html", sfx(l) + ".dc.html")


def pitch_file(n, l=None):
    l = l or _cur["lang"]
    return f"Pitch-{n:02d}.dc.html" if l == BASE else f"Pitch-{l.upper()}-{n:02d}.dc.html"


def doc_file(n, l=None):
    l = l or _cur["lang"]
    return f"Doc-{n:02d}.dc.html" if l == BASE else f"Doc-{l.upper()}-{n:02d}.dc.html"


SCREEN_RE = re.compile(r'href="((?:Main|[MD]-[A-Za-z]+)\.dc\.html)"')


def localize_hrefs(html, l=None):
    return SCREEN_RE.sub(lambda m: f'href="{fname(m.group(1), l)}"', html)


# ---------------------------------------------------------------- formatos
def fmt_num(x, dec=0):
    s = f"{x:,.{dec}f}"
    if _cur["lang"] in ("pt", "de"):
        s = s.replace(",", "§").replace(".", ",").replace("§", ".")
    return s


WD = {"de": ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"], "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], "pt": ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]}
WDL = {"de": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"], "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
       "pt": ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]}


def wd(i, long=False):
    return (WDL if long else WD)[_cur["lang"]][i]


def fmt_date(d, m, y=None):
    l = _cur["lang"]
    mon_en = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    if l == "en":
        return f"{mon_en[m-1]} {d}" + (f", {y}" if y else "")
    if l == "de":
        return f"{d:02d}.{m:02d}." + (f"{y}" if y else "")
    return f"{d:02d}/{m:02d}" + (f"/{y}" if y else "")


def eur(x, dec=0):
    v = fmt_num(x, dec)
    return {"en": "€" + v, "pt": v + " €", "de": v + " €"}[_cur["lang"]]


def pct(x, dec=0):
    s = fmt_num(x, dec)
    return s + (" %" if _cur["lang"] == "de" else "%")


def dec(x, d=1):
    return fmt_num(x, d)


def TBD():
    return T("[A DEFINIR]", "[TBD]", "[offen]")


def BETA():
    return T("[medir no beta]", "[measure in beta]", "[im Beta messen]")


def HYP():
    return T("hipótese", "hypothesis", "Hypothese")


def NP():
    return T("não publicado", "not published", "nicht veröffentlicht")
