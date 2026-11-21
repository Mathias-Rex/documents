#!/usr/bin/env python3
"""Verseny-kiírás figyelő scraper a 2026/2027-es tanévre.

Lekérdezi a figyelt magyarországi informatikai/programozó versenyek hivatalos
honlapjait, és egyszerű szövegmintázatok (pl. "2026/2027", a szezon kódneve)
alapján megállapítja, hogy megjelent-e már az adott verseny 2026/2027-es
kiírása. Ez heurisztika, nem garantáltan pontos — kétes esetben (lekérési
hiba, vagy a verseny eltűnt a honlapról) "unsure" státuszt ad, és mindig
megőrzi az utoljára kézzel ellenőrzött megjegyzést is referenciaként.

Két kimenetet generál a repó gyökerébe:

  1. competitions-data.js
     Egyetlen JS adatobjektum (`COMPETITION_DATA`), amit a
     versenyek_2026_2027.html (vagy bármely más JS/HTML) egyszerűen
     <script src="competitions-data.js"> taggel importál, illetve Node-ból
     require()-elhető (CommonJS export is történik).

  2. versenyek_2026_2027_statusz.md
     Ember által olvasható összefoglaló táblázat a jelenlegi állapotról,
     plusz egy dátumozott pillanatkép (versenyek_2026_2027_statusz_<ÉÉÉÉ-hón>.md),
     a repóban már meglévő havi archiválási konvenciót követve.

A scraper kizárólag a Python standard libraryt használja (urllib, re, json,
...) — nincs szükség semmilyen pip install-ra.

Használat:
    python3 scripts/scrape_competitions.py [--dry-run] [--timeout 20]

    --dry-run   Nem ír fájlt, csak a konzolra írja ki az eredményt.
    --timeout   Egy-egy HTTP kérés időkorlátja másodpercben (alapértelmezett: 20).
"""
from __future__ import annotations

import argparse
import dataclasses
import datetime
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import List, Optional

ROOT = Path(__file__).resolve().parents[1]
DATA_JS_PATH = ROOT / "competitions-data.js"
STATUS_MD_PATH = ROOT / "versenyek_2026_2027_statusz.md"

USER_AGENT = (
    "Mozilla/5.0 (compatible; VersenyFigyeloBot/1.0; "
    "+https://github.com/Mathias-Rex/documents)"
)

HU_MONTH_ABBR = {
    1: "jan", 2: "feb", 3: "marc", 4: "apr", 5: "maj", 6: "jun",
    7: "jul", 8: "aug", 9: "szept", 10: "okt", 11: "nov", 12: "dec",
}

# A 2026/2027-es tanévre utaló szövegminták, amiket minden oldalon keresünk
# (az egyes versenyeknél megadott `extra_patterns` ezeken felül érvényesül).
DEFAULT_POSITIVE_PATTERNS = [
    r"2026[/\-\u2013]2027",   # "2026/2027", "2026-2027", "2026–2027"
    r"2026\s*/\s*27\b",       # "2026/27"
]

STATUS_LEGEND = {
    "yes": {
        "icon": "\u2705",
        "label": "M\u00e1r megjelent a 2026/2027-es ki\u00edr\u00e1s",
        "shortLabel": "Van ki\u00edr\u00e1s",
        "badgeType": "success",
    },
    "no": {
        "icon": "\u274c",
        "label": "M\u00e9g a 2025/26-os (vagy kor\u00e1bbi) adatok \u00e9rv\u00e9nyesek",
        "shortLabel": "M\u00e9g nincs",
        "badgeType": "error",
    },
    "unsure": {
        "icon": "\u2753",
        "label": "St\u00e1tusz bizonytalan / nem ellen\u0151rizhet\u0151",
        "shortLabel": "Bizonytalan",
        "badgeType": "warning",
    },
}


@dataclasses.dataclass
class Competition:
    """Egy verseny leíró adatai.

    A statikus mezőket (name/fee/focus/age/type/announce/deadline/eventDate)
    kézzel kurált referenciaként tartjuk — ezeket a scraper nem próbálja
    automatikusan kitalálni tetszőleges HTML/PDF-ből. A `status` és a `note`
    viszont minden futtatáskor frissül a friss ellenőrzés alapján.
    """

    id: str
    name: str
    fee: str
    focus: str
    age: str
    type: str
    announce: str
    link: str
    deadline: str
    event_date: str
    fallback_note: str
    check_urls: List[str]
    extra_patterns: List[str] = dataclasses.field(default_factory=list)
    # Ha meg van adva, legalább egy ilyen mintának illeszkednie kell valahol az
    # oldalon ahhoz, hogy a versenyt egyáltalán "élőnek" tekintsük — ha egyik
    # sem található meg, a verseny eltűnt/átalakult honlapra utalhat (unsure).
    presence_patterns: Optional[List[str]] = None

    # Futás közben kitöltött mezők:
    status: str = "unsure"
    note: str = ""
    checked_urls: List[str] = dataclasses.field(default_factory=list)


def build_registry() -> List[Competition]:
    return [
        Competition(
            id="neumann", name="23. Neumann János Programtermék Verseny", fee="",
            focus="Projektmunka (app, játék, grafika, CAD, animáció, hardver)",
            age="Ált. és közép (a döntő kezdetéig, 2027.03.18-ig, 20 év alatt)", type="Egyéni / csapat",
            announce="szeptember–október", deadline="2027. február 14.",
            event_date="Előzsűri értesítés: 2027. febr. 22. / Döntő: 2027. márc. 18–19. (Szekszárd)",
            link="https://neumannverseny.hu",
            # A neumannverseny.hu maga csak egy "FIGYELEM!" jelzéssel az ibela.hu
            # dokumentumtárára mutat — a tényleges kiírás ott jelenik meg először.
            check_urls=["https://ibela.hu/neumann/dokumentumtar", "https://neumannverseny.hu"],
            extra_patterns=[r"23\.\s*Neumann", r"Versenyfelhívás\s*2027", r"\b2027\b"],
            fallback_note=(
                "A 23. Neumann János verseny 2027. évi kiírása megjelent "
                "(ibela.hu/neumann/dokumentumtar): nevezési határidő 2027. február 14., "
                "döntő 2027. március 18–19. (Szekszárd)."
            ),
        ),
        Competition(
            id="boronkay-8", name="Boronkay Informatika Verseny – 8. évfolyam", fee="",
            focus="Alkalmazói informatika (elmélet + szöveg, táblázat)",
            age="8. osztály (alacsonyabb is indulhat)", type="Egyéni",
            announce="október eleje",
            deadline="1. ford.: november közepe / 2. ford.: január eleje",
            event_date="Döntő: január vége (Vác)",
            link="https://boronkay.vac.hu/informatika-verseny",
            check_urls=["https://boronkay.vac.hu/informatika-verseny"],
            fallback_note="A honlap korábban HTTP 503 hibát adott — nem volt élőben ellenőrizhető.",
        ),
        Competition(
            id="boronkay-57", name="Boronkay Informatika Verseny – 5–7. évfolyam", fee="",
            focus="Alkalmazói informatika (elmélet + grafika, szöveg, prezentáció)",
            age="5–7. osztály", type="Egyéni",
            announce="október közepe",
            deadline="1. ford.: január vége / 2. ford.: április eleje",
            event_date="Döntő: április vége (Vác)",
            link="https://boronkay.vac.hu/informatika-verseny",
            check_urls=["https://boronkay.vac.hu/informatika-verseny"],
            fallback_note="A honlap korábban HTTP 503 hibát adott — nem volt élőben ellenőrizhető.",
        ),
        Competition(
            id="prosuli", name="ProSuli Robotika Verseny", fee="\U0001f4b8",
            focus="LEGO robotprogramozás (vonalkövetés, pályafeladatok)",
            age="Ált. és közép (amatőr / profi liga)", type="Csapat",
            announce="október", deadline="2026/27: hamarosan (a kiírás elindult)",
            event_date="Regionális: február / Döntő: március (Törökbálint)",
            link="https://prosuli.hu/prosuli-robotika-verseny/",
            check_urls=["https://prosuli.hu/prosuli-robotika-verseny/"],
            fallback_note="A honlap a 2026/2027 tanévi versenyt hirdette, de a konkrét dátumok még hiányoztak.",
        ),
        Competition(
            id="fll-challenge", name="FIRST LEGO League – Challenge", fee="\U0001f4b8\U0001f4b8",
            focus="LEGO robotika + tudományos kutatási projekt (2026/27: BIOGLOW)",
            age="9–16 év", type="Csapat (3–10 fő)",
            announce="augusztus (szezon-indulás)", deadline="Csapatregisztráció: 2026. nov. 30.",
            event_date="Regionális: 2026. dec.–2027. febr. / Nemzeti döntő: 2027. márc. 7. (Miskolc)",
            link="https://www.firstlegoleague.hu",
            check_urls=["https://www.firstlegoleague.hu"],
            extra_patterns=[r"BIOGLOW"],
            fallback_note="A 2026/2027-es „BIOGLOW” szezon élt, konkrét dátumokkal.",
        ),
        Competition(
            id="fll-explore", name="FIRST LEGO League – Explore & Discover", fee="\U0001f4b8",
            focus="LEGO robotika (játékos, modellépítés, bemutató)",
            age="4–10 év", type="Csapat",
            announce="augusztus", deadline="Iskolai/óvodai regisztráció: 2027. jan. 31.",
            event_date="Kiállítás: február–május",
            link="https://www.firstlegoleague.hu",
            check_urls=["https://www.firstlegoleague.hu"],
            extra_patterns=[r"BIOGLOW"],
            fallback_note="A 2026/2027-es BIOGLOW szezon része, azonos menetrenddel.",
        ),
        Competition(
            id="wro", name="World Robot Olympiad (WRO)", fee="\U0001f4b8\U0001f4b8",
            focus="Robotika (RoboMission, Future Innovators, RoboSports, Future Engineers)",
            age="8–19 év (kategóriánként)", type="Csapat (2–3 fő)",
            announce="december–január", deadline="február–március (reg.wro.hu)",
            event_date="Magyarországi válogató: április–május",
            link="https://wro.hu",
            check_urls=["https://wro.hu"],
            extra_patterns=[r"WRO\s*2027"],
            fallback_note="A honlap még csak a lezajlott „WRO 2026” szezont mutatta.",
        ),
        Competition(
            id="ftc", name="FIRST Tech Challenge (FTC)", fee="\U0001f4b8\U0001f4b8",
            focus="Haladó mérnöki robotépítés + programozás (2026/27: BIOBUZZ)",
            age="12–18 év (9–12. évf.)", type="Csapat (6–12 fő)",
            announce="augusztus–szeptember",
            deadline="2026/27: dátumok még nincsenek meghirdetve",
            event_date="Ligaversenyek/döntő dátuma: még nem ismert",
            link="https://firsttechchallenge.hu",
            check_urls=["https://firsttechchallenge.hu"],
            extra_patterns=[r"BIOBUZZ"],
            fallback_note="Az oldal már a „BIOBUZZ” szezont nevesítette, de fordulódátumok nélkül.",
        ),
        Competition(
            id="ehod", name="e-Hód / Bebras", fee="",
            focus="Algoritmikus gondolkodás (programozás nélkül, online teszt)",
            age="3–12. évfolyam (5 korcsoport)", type="Egyéni",
            announce="október eleje", deadline="Regisztráció: október közepe",
            event_date="Verseny (előzetes): 2026. nov. 9–20.",
            link="http://e-hod.elte.hu",
            check_urls=["http://e-hod.elte.hu"],
            fallback_note="Előzetes dátum volt látható, de a hivatalos kiírás/regisztráció még nem nyílt meg.",
        ),
        Competition(
            id="nemes-online", name="Nemes Tihamér Online Programozási Verseny", fee="",
            focus="Programozás (algoritmusok, C++/Python/Pascal/C#/Java)",
            age="5–12. osztály", type="Egyéni",
            announce="október", deadline="Folyamatos (fordulónként az előző szerdán éjfélig)",
            event_date="5 forduló: nov, dec, jan, febr, ápr / Eredményhirdetés: máj. 7.",
            link="https://tehetseg.inf.elte.hu/nemes-online/nemes-aktualis.html",
            check_urls=["https://tehetseg.inf.elte.hu/nemes-online/nemes-aktualis.html"],
            fallback_note="Még a 2025/2026-os kiírás volt aktuális.",
        ),
        Competition(
            id="zsako", name="Zsakó László Programozási Verseny", fee="",
            focus="Programozás (algoritmusok, analízis, kódolás)",
            age="5–13. osztály", type="Egyéni",
            announce="október", deadline="1. ford. (iskolai): október",
            event_date="Területi: november / Döntő: február (ELTE IK)",
            link="https://tehetseg.inf.elte.hu/nemes/",
            check_urls=["https://tehetseg.inf.elte.hu/nemes/"],
            extra_patterns=[r"felhiv27"],
            fallback_note="A kiírás dokumentumai még a 2025/2026-os tanévre vonatkoztak.",
        ),
        Competition(
            id="kodkupa", name="Kódkupa – IIOT Válogatóverseny", fee="",
            focus="Csapat algoritmikus programozás (C, C++, Python)",
            age="5–12. évf. (profi: 7–12.)", type="Csapat (max. 4 fő)",
            announce="október", deadline="november eleje",
            event_date="4 online selejtező: nov–febr / Döntő: március (Budapest, Fazekas) / Nemzetközi: május–június",
            link="https://kodkupa.hu",
            check_urls=["https://kodkupa.hu"],
            fallback_note="A honlap és a kiírás PDF-je még a 2025/2026-os szezonra vonatkozott.",
        ),
        Competition(
            id="prograce", name="PROGRACE Programozói Verseny", fee="",
            focus="Programozás (egynapos csapatverseny)",
            age="Közép + egyetemisták (24 év alatt)", type="Csapat (3 fő)",
            announce="szeptember–október", deadline="november",
            event_date="december 1. (Pécs, PTE MIK)",
            link="https://prograce.hu",
            check_urls=["https://prograce.hu"],
            fallback_note="A legfrissebb hír még a 2025/26-os fordulóról szólt.",
        ),
        Competition(
            id="codeweek", name="Code Week Hungary", fee="",
            focus="Kódolás, algoritmikus gondolkodás (nem klasszikus verseny, iskolai esemény)",
            age="Minden korosztály", type="Egyéni / csapat",
            announce="szeptember", deadline="Eseményregisztráció folyamatos",
            event_date="2026. október 10–25. (14. Code Week)",
            link="https://www.codeweekhungary.hu",
            check_urls=["https://www.codeweekhungary.hu"],
            extra_patterns=[r"14\.\s*Code\s*Week", r"\b2026\b"],
            fallback_note="A honlap a 2026-os (14.) Code Week-et hirdette.",
        ),
        Competition(
            id="kozma", name="Kozma László Alkalmazói Tanulmányi Verseny", fee="",
            focus="Alkalmazói informatika (grafika, szöveg, prezentáció, táblázat)",
            age="5–10. évfolyam (2 korcsoport)", type="Páros / csapat",
            announce="szeptember–október", deadline="2026. október 16. (XXV. verseny)",
            event_date="2 forduló: iskolai → Döntő: május (Százhalombatta)",
            link="https://isze.hu/kozma-laszlo-orszagos-informatika-alkalmazoi-tanulmanyi-verseny/",
            check_urls=["https://isze.hu/kozma-laszlo-orszagos-informatika-alkalmazoi-tanulmanyi-verseny/"],
            extra_patterns=[r"XXV\."],
            fallback_note="Megjelent a 2026/2027-es kiírás (XXV. verseny), nevezési határidővel.",
        ),
        Competition(
            id="dusza", name="Dusza Árpád Országos Programozói Emlékverseny", fee="",
            focus="Programozás (hagyományos / web / mobilprogramozás)",
            age="9–13. évfolyam (középiskola)", type="Egyéni",
            announce="szeptember–október",
            deadline="október–november (2026/27-es felhívás elérhető)",
            event_date="Regionális: január–február / Döntő: március–április",
            link="https://isze.hu/dusza-arpad-orszagos-programozoi-emlekverseny/",
            check_urls=["https://isze.hu/dusza-arpad-orszagos-programozoi-emlekverseny/"],
            fallback_note="Elérhető volt a „Versenyfelhívás_2026-2027” PDF.",
        ),
        Competition(
            id="radnoti", name="Radnóti Hack&CODE Informatikai Verseny", fee="",
            focus="Programozás + robotika + projekt (AI, webfejlesztés, szabadulószoba, csapatmunka)",
            age="7–8. évfolyam", type="Csapat (2–4 fő)",
            announce="október", deadline="⚠️ nincs nyoma a versenynek az átalakult honlapon",
            event_date="—",
            link="http://www.radnoti-pecs.hu",
            check_urls=["http://www.radnoti-pecs.hu", "http://technikum.radnoti-pecs.hu"],
            presence_patterns=[r"Hack\s*&\s*CODE", r"Hack&CODE"],
            fallback_note="A honlap teljesen átalakult; a versenynek nem volt nyoma — érdemes megerősítést kérni az iskolától.",
        ),
        Competition(
            id="nemes-alkalmazoi", name="Nemes Tihamér Alkalmazói Tanulmányi Verseny", fee="",
            focus="Alkalmazói informatika (irodai szoftverek, weblapkészítés)",
            age="7–10. évfolyam", type="Egyéni",
            announce="november–december", deadline="2026. december 20.",
            event_date="Iskolai forduló: 2027. jan. 6. / Országos: 2027. márc. 20. / Díjátadó: 2027. máj. 6. (ELTE IK)",
            link="https://versenyportal.hu/nemesa/nemesa_aktualis.html",
            check_urls=[
                "https://versenyportal.hu/nemesa/nemesa_aktualis.html",
                "https://tehetseg.inf.elte.hu/nemesa/",
            ],
            fallback_note="A verseny átkerült a versenyportal.hu-ra, ahol élt a 2026/2027-es kiírás.",
        ),
        Competition(
            id="rocs", name="ROCS – Robotprogramozó Csapatverseny", fee="",
            focus="LEGO robotprogramozás (vonalkövetés, akadálypálya)",
            age="5–8. évfolyam (3 korcsoport)", type="Csapat (2–3 fő)",
            announce="november–december", deadline="január–február",
            event_date="Regionális: február–március / Döntő: április (Kecskemét)",
            link="http://robotprog.hu/",
            check_urls=["http://robotprog.hu/HTML/ROCS_aktualis.html", "http://robotprog.hu/"],
            extra_patterns=[r"XVI\."],
            fallback_note="A honlap még a korábbi (2024/25-ös, XV.) kiírást mutatta.",
        ),
        Competition(
            id="kovacs", name="Kovács Mihály Országos Grafikus Programozási Verseny", fee="",
            focus="Grafikus programozás (teknőcgrafika, animáció, rekurzió – Scratch / Logo / Python)",
            age="3–12. évfolyam (4 korcsoport: K1–K4)", type="Egyéni",
            announce="november–december", deadline="2027. február 16.",
            event_date="Iskolai forduló: 2027. febr. 17. / Országos: 2027. ápr. 10. / Eredményhirdetés: 2027 május (ELTE IK)",
            link="https://versenyportal.hu/logo/logo_aktualis.html",
            check_urls=[
                "https://versenyportal.hu/logo/logo_aktualis.html",
                "http://logo.inf.elte.hu/",
            ],
            fallback_note="A verseny átkerült a versenyportal.hu-ra, ahol élt a 2026/2027-es kiírás.",
        ),
    ]


TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")


def strip_tags(html: str) -> str:
    """Nagyon egyszerű HTML -> sima szöveg konverzió mintázatkereséshez."""
    text = TAG_RE.sub(" ", html)
    return WS_RE.sub(" ", text)


def fetch(url: str, timeout: int) -> Optional[str]:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            return raw.decode(charset, errors="replace")
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, ValueError) as exc:
        print(f"  [warn] {url} -> {exc}", file=sys.stderr)
        return None


def check_competition(comp: Competition, timeout: int) -> Competition:
    print(f"- {comp.name} ...")
    patterns = DEFAULT_POSITIVE_PATTERNS + comp.extra_patterns
    fetch_errors: List[str] = []
    presence_found = comp.presence_patterns is None  # ha nincs megadva, nem kell ellenőrizni
    matched_text: Optional[str] = None
    matched_url: Optional[str] = None

    for url in comp.check_urls:
        html = fetch(url, timeout)
        if html is None:
            fetch_errors.append(url)
            continue
        text = strip_tags(html)

        if not presence_found and comp.presence_patterns:
            if any(re.search(p, text, re.IGNORECASE) for p in comp.presence_patterns):
                presence_found = True

        if matched_text is None:
            for pattern in patterns:
                m = re.search(pattern, text, re.IGNORECASE)
                if m:
                    matched_text = m.group(0)
                    matched_url = url
                    break

    comp.checked_urls = comp.check_urls

    if len(fetch_errors) == len(comp.check_urls):
        comp.status = "unsure"
        comp.note = (
            "Automatikus ellenőrzés: egyik figyelt oldal sem volt elérhető "
            f"({', '.join(fetch_errors)}); a korábbi állapot megőrizve. "
            f"Korábbi megjegyzés: {comp.fallback_note}"
        )
        return comp

    if not presence_found:
        comp.status = "unsure"
        comp.note = (
            "Automatikus ellenőrzés: a verseny megnevezése nem található a figyelt "
            "oldal(ak)on — lehet, hogy a honlap átalakult, vagy a verseny megszűnt. "
            f"Korábbi megjegyzés: {comp.fallback_note}"
        )
        return comp

    if matched_text:
        comp.status = "yes"
        comp.note = (
            f"Automatikus ellenőrzés: a(z) {matched_url} oldalon található "
            f"„{matched_text.strip()}” jelzi a 2026/2027-es kiírást."
        )
    else:
        comp.status = "no"
        comp.note = (
            "Automatikus ellenőrzés: nem található 2026/2027-es kiírásra utaló szöveg "
            f"a figyelt oldal(ak)on. Korábbi megjegyzés: {comp.fallback_note}"
        )
    return comp


def render_data_js(competitions: List[Competition], checked_at: str) -> str:
    items = []
    for c in competitions:
        items.append({
            "id": c.id,
            "name": c.name,
            "status": c.status,
            "fee": c.fee,
            "focus": c.focus,
            "age": c.age,
            "type": c.type,
            "announce": c.announce,
            "deadline": c.deadline,
            "eventDate": c.event_date,
            "link": c.link,
            "note": c.note,
        })

    data = {
        "schoolYear": "2026\u20132027",
        "statusCheckedAt": checked_at,
        "statusLegend": STATUS_LEGEND,
        "items": items,
    }

    body = json.dumps(data, ensure_ascii=False, indent=2)
    generated_at = datetime.datetime.now().isoformat(timespec="seconds")

    return (
        "// \u26a0\ufe0f Ezt a f\u00e1jlt a scripts/scrape_competitions.py "
        "gener\u00e1lja automatikusan \u2014 ne szerkeszd k\u00e9zzel!\n"
        f"// Gener\u00e1lva: {generated_at}\n"
        "//\n"
        "// Haszn\u00e1lat HTML-b\u0151l (klasszikus <script>, glob\u00e1l v\u00e1ltoz\u00f3k\u00e9nt):\n"
        '//   <script src="competitions-data.js"></script>\n'
        "//   <script>console.log(COMPETITION_DATA.items.length);</script>\n"
        "//\n"
        "// Haszn\u00e1lat Node/CommonJS-b\u0151l:\n"
        '//   const { COMPETITION_DATA } = require("./competitions-data.js");\n'
        "\n"
        f"var COMPETITION_DATA = {body};\n"
        "\n"
        'if (typeof module !== "undefined" && module.exports) {\n'
        "  module.exports = COMPETITION_DATA;\n"
        "  module.exports.COMPETITION_DATA = COMPETITION_DATA;\n"
        "}\n"
        'if (typeof window !== "undefined") {\n'
        "  window.COMPETITION_DATA = COMPETITION_DATA;\n"
        "}\n"
    )


def render_status_md(competitions: List[Competition], checked_at: str) -> str:
    counts = {"yes": 0, "no": 0, "unsure": 0}
    for c in competitions:
        counts[c.status] += 1

    lines = [
        "# Versenyek státusza – 2026/2027",
        "",
        f"Automatikus ellenőrzés (scripts/scrape_competitions.py) — **{checked_at}**.",
        "",
        f"**{counts['yes']}** versenynél már megjelent/elérhető az új tanévi kiírás, "
        f"**{counts['no']}**-nál még a korábbi adatok érvényesek, "
        f"**{counts['unsure']}** verseny státusza bizonytalan.",
        "",
        "| Verseny | Státusz | Megjegyzés | Honlap |",
        "|---|---|---|---|",
    ]
    for c in competitions:
        legend = STATUS_LEGEND[c.status]
        note = c.note.replace("|", "\\|").replace("\n", " ")
        lines.append(f"| {c.name} | {legend['icon']} {legend['shortLabel']} | {note} | {c.link} |")

    lines += [
        "",
        "---",
        "",
        "*Ez a fájl a `scripts/scrape_competitions.py` scraper legutóbbi futtatásának eredménye. "
        "A heurisztika egyszerű szövegmintázat-keresésen alapul, ezért kétes esetben érdemes "
        "kézzel is ellenőrizni az adott honlapot.*",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dry-run", action="store_true", help="Ne írjon fájlt, csak a konzolra.")
    parser.add_argument("--timeout", type=int, default=20, help="HTTP timeout másodpercben (alapértelmezett: 20).")
    args = parser.parse_args()

    registry = build_registry()
    for comp in registry:
        check_competition(comp, args.timeout)

    now = datetime.datetime.now()
    checked_at = now.strftime("%Y. ") + HU_MONTH_ABBR[now.month] + now.strftime(". %d.")

    data_js = render_data_js(registry, checked_at)
    status_md = render_status_md(registry, checked_at)
    snapshot_name = f"versenyek_2026_2027_statusz_{now.year}-{HU_MONTH_ABBR[now.month]}.md"
    snapshot_path = ROOT / snapshot_name

    counts = {"yes": 0, "no": 0, "unsure": 0}
    for c in registry:
        counts[c.status] += 1
    print()
    print(f"Összegzés: {counts['yes']} van kiírás / {counts['no']} még nincs / {counts['unsure']} bizonytalan")

    if args.dry_run:
        print("\n--dry-run: nem írtam fájlt. Előnézet:\n")
        print(status_md)
        return 0

    DATA_JS_PATH.write_text(data_js, encoding="utf-8")
    STATUS_MD_PATH.write_text(status_md, encoding="utf-8")
    snapshot_path.write_text(status_md, encoding="utf-8")

    print(f"Írva: {DATA_JS_PATH.relative_to(ROOT)}")
    print(f"Írva: {STATUS_MD_PATH.relative_to(ROOT)}")
    print(f"Írva: {snapshot_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
