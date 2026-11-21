# Perplexity ellenőrző prompt — 2026/2027-es verseny-kiírások

Ezt a promptot másold be a Perplexitybe (vagy bármely más, élő webkereséssel
rendelkező AI-ba), hogy keresztellenőriztesd vele a `competitions-data.js`-ben
nyilvántartott magyarországi informatikai/programozó versenyek 2026/2027-es
kiírás-státuszát. A válasz JSON-struktúráját szándékosan úgy adtam meg, hogy
az eredményt közvetlenül vissza tudjam illeszteni a scraper regisztrumába
(`scripts/scrape_competitions.py`) — csak másold be nekem a kapott JSON-t.

---

## A prompt (másold innentől a záró kódblokkig)

```
Egy magyarországi, általános és középiskolásoknak szóló informatikai/programozó
versenyeket nyilvántartó listát ellenőrzök. Minden versenynél tudnom kell, hogy
a 2026/2027-es TANÉVRE (azaz a 2026 őszén induló, 2027 tavaszán/nyarán záruló
tanévre) megjelent-e már a hivatalos versenykiírás, és ha igen, mik a pontos
dátumok.

Az alábbi JSON tömb az eddig általam ismert (lehet, hogy elavult) állapotot
tartalmazza versenyenként: id, name (verseny neve), link (eddig ismert
hivatalos oldal), status ("yes" = már van 2026/27-es kiírás, "no" = még
nincs/a régi érvényes, "unsure" = bizonytalan), deadline (nevezési határidő)
és eventDate (fordulók/döntő időpontjai).

[
  {
    "id": "neumann",
    "name": "23. Neumann János Programtermék Verseny",
    "link": "https://neumannverseny.hu",
    "status": "yes",
    "deadline": "2027. február 14.",
    "eventDate": "Előzsűri értesítés: 2027. febr. 22. / Döntő: 2027. márc. 18–19. (Szekszárd)"
  },
  {
    "id": "boronkay-8",
    "name": "Boronkay Informatika Verseny – 8. évfolyam",
    "link": "https://boronkay.vac.hu/informatika-verseny",
    "status": "unsure",
    "deadline": "1. ford.: november közepe / 2. ford.: január eleje",
    "eventDate": "Döntő: január vége (Vác)"
  },
  {
    "id": "boronkay-57",
    "name": "Boronkay Informatika Verseny – 5–7. évfolyam",
    "link": "https://boronkay.vac.hu/informatika-verseny",
    "status": "unsure",
    "deadline": "1. ford.: január vége / 2. ford.: április eleje",
    "eventDate": "Döntő: április vége (Vác)"
  },
  {
    "id": "prosuli",
    "name": "ProSuli Robotika Verseny",
    "link": "https://prosuli.hu/prosuli-robotika-verseny/",
    "status": "no",
    "deadline": "2026/27: hamarosan (a kiírás elindult)",
    "eventDate": "Regionális: február / Döntő: március (Törökbálint)"
  },
  {
    "id": "fll-challenge",
    "name": "FIRST LEGO League – Challenge",
    "link": "https://www.firstlegoleague.hu",
    "status": "yes",
    "deadline": "Csapatregisztráció: 2026. nov. 30.",
    "eventDate": "Regionális: 2026. dec.–2027. febr. / Nemzeti döntő: 2027. márc. 7. (Miskolc)"
  },
  {
    "id": "fll-explore",
    "name": "FIRST LEGO League – Explore & Discover",
    "link": "https://www.firstlegoleague.hu",
    "status": "yes",
    "deadline": "Iskolai/óvodai regisztráció: 2027. jan. 31.",
    "eventDate": "Kiállítás: február–május"
  },
  {
    "id": "wro",
    "name": "World Robot Olympiad (WRO)",
    "link": "https://wro.hu",
    "status": "no",
    "deadline": "február–március (reg.wro.hu)",
    "eventDate": "Magyarországi válogató: április–május"
  },
  {
    "id": "ftc",
    "name": "FIRST Tech Challenge (FTC)",
    "link": "https://firsttechchallenge.hu",
    "status": "yes",
    "deadline": "2026/27: dátumok még nincsenek meghirdetve",
    "eventDate": "Ligaversenyek/döntő dátuma: még nem ismert"
  },
  {
    "id": "ehod",
    "name": "e-Hód / Bebras",
    "link": "http://e-hod.elte.hu",
    "status": "no",
    "deadline": "Regisztráció: október közepe",
    "eventDate": "Verseny (előzetes): 2026. nov. 9–20."
  },
  {
    "id": "nemes-online",
    "name": "Nemes Tihamér Online Programozási Verseny",
    "link": "https://tehetseg.inf.elte.hu/nemes-online/nemes-aktualis.html",
    "status": "yes",
    "deadline": "Folyamatos (fordulónként az előző szerdán éjfélig)",
    "eventDate": "5 forduló: nov, dec, jan, febr, ápr / Eredményhirdetés: máj. 7."
  },
  {
    "id": "zsako",
    "name": "Zsakó László Programozási Verseny",
    "link": "https://tehetseg.inf.elte.hu/nemes/",
    "status": "unsure",
    "deadline": "1. ford. (iskolai): október",
    "eventDate": "Területi: november / Döntő: február (ELTE IK)"
  },
  {
    "id": "kodkupa",
    "name": "Kódkupa – IIOT Válogatóverseny",
    "link": "https://kodkupa.hu",
    "status": "no",
    "deadline": "november eleje",
    "eventDate": "4 online selejtező: nov–febr / Döntő: március (Budapest, Fazekas) / Nemzetközi: május–június"
  },
  {
    "id": "prograce",
    "name": "PROGRACE Programozói Verseny",
    "link": "https://prograce.hu",
    "status": "no",
    "deadline": "november",
    "eventDate": "december 1. (Pécs, PTE MIK)"
  },
  {
    "id": "codeweek",
    "name": "Code Week Hungary",
    "link": "https://www.codeweekhungary.hu",
    "status": "yes",
    "deadline": "Eseményregisztráció folyamatos",
    "eventDate": "2026. október 10–25. (14. Code Week)"
  },
  {
    "id": "kozma",
    "name": "Kozma László Alkalmazói Tanulmányi Verseny",
    "link": "https://isze.hu/kozma-laszlo-orszagos-informatika-alkalmazoi-tanulmanyi-verseny/",
    "status": "yes",
    "deadline": "2026. október 16. (XXV. verseny)",
    "eventDate": "2 forduló: iskolai → Döntő: május (Százhalombatta)"
  },
  {
    "id": "dusza",
    "name": "Dusza Árpád Országos Programozói Emlékverseny",
    "link": "https://isze.hu/dusza-arpad-orszagos-programozoi-emlekverseny/",
    "status": "yes",
    "deadline": "október–november (2026/27-es felhívás elérhető)",
    "eventDate": "Regionális: január–február / Döntő: március–április"
  },
  {
    "id": "radnoti",
    "name": "Radnóti HACK & CODE Informatikai Verseny",
    "link": "http://www.radnoti-pecs.hu",
    "status": "yes",
    "deadline": "2026. november 6.",
    "eventDate": "I. forduló (online): 2026. nov. 16. – dec. 11. / II. forduló (Pécs, személyes): 2027. jan. 8. / III. forduló (döntő): 2027. febr. 5."
  },
  {
    "id": "nemes-alkalmazoi",
    "name": "Nemes Tihamér Alkalmazói Tanulmányi Verseny",
    "link": "https://versenyportal.hu/nemesa/nemesa_aktualis.html",
    "status": "yes",
    "deadline": "2026. december 20.",
    "eventDate": "Iskolai forduló: 2027. jan. 6. / Országos: 2027. márc. 20. / Díjátadó: 2027. máj. 6. (ELTE IK)"
  },
  {
    "id": "rocs",
    "name": "ROCS – Robotprogramozó Csapatverseny",
    "link": "http://robotprog.hu/",
    "status": "no",
    "deadline": "január–február",
    "eventDate": "Regionális: február–március / Döntő: április (Kecskemét)"
  },
  {
    "id": "kovacs",
    "name": "Kovács Mihály Országos Grafikus Programozási Verseny",
    "link": "https://versenyportal.hu/logo/logo_aktualis.html",
    "status": "yes",
    "deadline": "2027. február 16.",
    "eventDate": "Iskolai forduló: 2027. febr. 17. / Országos: 2027. ápr. 10. / Eredményhirdetés: 2027 május (ELTE IK)"
  },
  {
    "id": "arpad-kupa",
    "name": "Árpád-kupa (Pécsi Árpád Fejedelem Gimnázium)",
    "link": "https://www.arpad-pecs.hu",
    "status": "yes",
    "deadline": "2026. november 20. (éjfél)",
    "eventDate": "1. forduló beadandó: 2026. dec. 19. / 2. forduló beadandó: 2027. febr. 19. / Döntő: 2027. ápr. 6., 14:00 (Pécs)"
  }
]

FELADAT:
Minden egyes versenynél, a `link` mezőben megadott (vagy ha az nem a jó
forrás, az általad megtalált hivatalos) oldal és/vagy friss webes keresés
alapján állapítsd meg:
1. Van-e már hivatalosan közzétett 2026/2027-es tanévi kiírás (ne a korábbi,
   2025/2026-os vagy még régebbi adatokat vedd figyelembe).
2. Ha van, mi a pontos nevezési határidő és a fordulók/döntő dátumai.
3. Mi a legfrissebb, ténylegesen működő hivatalos URL (ha a megadott `link`
   elavult, redirectel, vagy 404-et ad, találd meg a jelenlegi helyes linket).

KIMENETI FORMÁTUM — EZ KÖTELEZŐ, NE TÉRJ EL TŐLE:
Kizárólag egy érvényes JSON tömböt adj vissza, semmi mást (ne írj elé/mögé
magyarázó szöveget, ne csomagold markdown kódblokkba sem). A tömb minden
eleme pontosan ezekkel a kulcsokkal rendelkezzen, ugyanabban a sorrendben,
és minden bemenetben szereplő `id`-hoz pontosan egy kimeneti objektum
tartozzon (az `id` mezőt változatlanul vedd át):

[
  {
    "id": "ugyanaz, mint a bemeneti JSON-ban",
    "status": "yes | no | unsure",
    "deadline": "a nevezési határidő magyarul kiírva, pl. '2027. február 14.' — ha nincs friss infó, hagyd meg a bemeneti értéket",
    "eventDate": "a fordulók/döntő dátumai magyarul, pl. 'Döntő: 2027. március 18–19. (Szekszárd)' — ha nincs friss infó, hagyd meg a bemeneti értéket",
    "link": "a legfrissebb, ténylegesen működő hivatalos URL",
    "source_url": "a konkrét oldal/dokumentum URL-je, ahol a 2026/27-es infót találtad (ha más, mint a link)",
    "note": "1-2 mondatos magyar indoklás: mit találtál, milyen dátumot/szöveget láttál, és ha 'unsure', miért",
    "checked_at": "a mai dátum ÉÉÉÉ-HH-NN formátumban"
  }
]

Ha egy versenyről semmilyen friss infót nem találsz, `status: "unsure"`-t adj
vissza, és a `note` mezőben írd le, mit próbáltál (milyen oldalakat néztél
meg), és hagyd meg a bemeneti `deadline`/`eventDate`/`link` értékeket
változatlanul.
```

---

## Használat

1. Másold be a teljes promptot (a fenti kódblokk tartalmát) a Perplexitybe —
   az aktuális (2026.11.21-i) állapot már bele van ágyazva, nincs mit
   kézzel kitölteni.
2. A kapott JSON választ másold vissza ide a beszélgetésbe — abból közvetlenül
   frissítem a `scripts/scrape_competitions.py` registry-t (a már bizonytalan
   vagy eltérő eredményű versenyeknél `manual_status`/`manual_note` mezőkkel,
   ahogy a Radnóti HACK & CODE és az Árpád-kupa esetében is történt).
3. **Ha később újrafuttatod a scrapert** (`python3 scripts/scrape_competitions.py`),
   és frissebb promptot szeretnél, kérd meg Claude-ot, hogy generálja újra ezt
   a fájlt a `competitions-data.js` aktuális tartalmából — a beágyazott JSON-tömb
   gyorsan elavulhat, ahogy a kiírások megjelennek.
