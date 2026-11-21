// ⚠️ Ezt a fájlt a scripts/scrape_competitions.py generálja automatikusan — ne szerkeszd kézzel!
// Generálva: 2026-11-21T20:14:26
//
// Használat HTML-ből (klasszikus <script>, globál változóként):
//   <script src="competitions-data.js"></script>
//   <script>console.log(COMPETITION_DATA.items.length);</script>
//
// Használat Node/CommonJS-ből:
//   const { COMPETITION_DATA } = require("./competitions-data.js");

var COMPETITION_DATA = {
  "schoolYear": "2026–2027",
  "statusCheckedAt": "2026. nov. 21.",
  "statusLegend": {
    "yes": {
      "icon": "✅",
      "label": "Már megjelent a 2026/2027-es kiírás",
      "shortLabel": "Van kiírás",
      "badgeType": "success"
    },
    "no": {
      "icon": "❌",
      "label": "Még a 2025/26-os (vagy korábbi) adatok érvényesek",
      "shortLabel": "Még nincs",
      "badgeType": "error"
    },
    "unsure": {
      "icon": "❓",
      "label": "Státusz bizonytalan / nem ellenőrizhető",
      "shortLabel": "Bizonytalan",
      "badgeType": "warning"
    }
  },
  "items": [
    {
      "id": "neumann",
      "name": "23. Neumann János Programtermék Verseny",
      "status": "yes",
      "fee": "",
      "focus": "Projektmunka (app, játék, grafika, CAD, animáció, hardver)",
      "age": "Ált. és közép (a döntő kezdetéig, 2027.03.18-ig, 20 év alatt)",
      "type": "Egyéni / csapat",
      "announce": "szeptember–október",
      "deadline": "2027. február 14.",
      "eventDate": "Előzsűri értesítés: 2027. febr. 22. / Döntő: 2027. márc. 18–19. (Szekszárd)",
      "link": "https://neumannverseny.hu",
      "note": "Automatikus ellenőrzés: a(z) https://ibela.hu/neumann/dokumentumtar oldalon található „23. Neumann” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "boronkay-8",
      "name": "Boronkay Informatika Verseny – 8. évfolyam",
      "status": "unsure",
      "fee": "",
      "focus": "Alkalmazói informatika (elmélet + szöveg, táblázat)",
      "age": "8. osztály (alacsonyabb is indulhat)",
      "type": "Egyéni",
      "announce": "október eleje",
      "deadline": "1. ford.: november közepe / 2. ford.: január eleje",
      "eventDate": "Döntő: január vége (Vác)",
      "link": "https://boronkay.vac.hu/informatika-verseny",
      "note": "Automatikus ellenőrzés: egyik figyelt oldal sem volt elérhető (https://boronkay.vac.hu/informatika-verseny); a korábbi állapot megőrizve. Korábbi megjegyzés: A honlap korábban HTTP 503 hibát adott — nem volt élőben ellenőrizhető."
    },
    {
      "id": "boronkay-57",
      "name": "Boronkay Informatika Verseny – 5–7. évfolyam",
      "status": "unsure",
      "fee": "",
      "focus": "Alkalmazói informatika (elmélet + grafika, szöveg, prezentáció)",
      "age": "5–7. osztály",
      "type": "Egyéni",
      "announce": "október közepe",
      "deadline": "1. ford.: január vége / 2. ford.: április eleje",
      "eventDate": "Döntő: április vége (Vác)",
      "link": "https://boronkay.vac.hu/informatika-verseny",
      "note": "Automatikus ellenőrzés: egyik figyelt oldal sem volt elérhető (https://boronkay.vac.hu/informatika-verseny); a korábbi állapot megőrizve. Korábbi megjegyzés: A honlap korábban HTTP 503 hibát adott — nem volt élőben ellenőrizhető."
    },
    {
      "id": "prosuli",
      "name": "ProSuli Robotika Verseny",
      "status": "no",
      "fee": "💸",
      "focus": "LEGO robotprogramozás (vonalkövetés, pályafeladatok)",
      "age": "Ált. és közép (amatőr / profi liga)",
      "type": "Csapat",
      "announce": "október",
      "deadline": "2026/27: hamarosan (a kiírás elindult)",
      "eventDate": "Regionális: február / Döntő: március (Törökbálint)",
      "link": "https://prosuli.hu/prosuli-robotika-verseny/",
      "note": "Automatikus ellenőrzés: nem található 2026/2027-es kiírásra utaló szöveg a figyelt oldal(ak)on. Korábbi megjegyzés: A honlap a 2026/2027 tanévi versenyt hirdette, de a konkrét dátumok még hiányoztak."
    },
    {
      "id": "fll-challenge",
      "name": "FIRST LEGO League – Challenge",
      "status": "yes",
      "fee": "💸💸",
      "focus": "LEGO robotika + tudományos kutatási projekt (2026/27: BIOGLOW)",
      "age": "9–16 év",
      "type": "Csapat (3–10 fő)",
      "announce": "augusztus (szezon-indulás)",
      "deadline": "Csapatregisztráció: 2026. nov. 30.",
      "eventDate": "Regionális: 2026. dec.–2027. febr. / Nemzeti döntő: 2027. márc. 7. (Miskolc)",
      "link": "https://www.firstlegoleague.hu",
      "note": "Automatikus ellenőrzés: a(z) https://www.firstlegoleague.hu oldalon található „2026–2027” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "fll-explore",
      "name": "FIRST LEGO League – Explore & Discover",
      "status": "yes",
      "fee": "💸",
      "focus": "LEGO robotika (játékos, modellépítés, bemutató)",
      "age": "4–10 év",
      "type": "Csapat",
      "announce": "augusztus",
      "deadline": "Iskolai/óvodai regisztráció: 2027. jan. 31.",
      "eventDate": "Kiállítás: február–május",
      "link": "https://www.firstlegoleague.hu",
      "note": "Automatikus ellenőrzés: a(z) https://www.firstlegoleague.hu oldalon található „2026–2027” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "wro",
      "name": "World Robot Olympiad (WRO)",
      "status": "no",
      "fee": "💸💸",
      "focus": "Robotika (RoboMission, Future Innovators, RoboSports, Future Engineers)",
      "age": "8–19 év (kategóriánként)",
      "type": "Csapat (2–3 fő)",
      "announce": "december–január",
      "deadline": "február–március (reg.wro.hu)",
      "eventDate": "Magyarországi válogató: április–május",
      "link": "https://wro.hu",
      "note": "Automatikus ellenőrzés: nem található 2026/2027-es kiírásra utaló szöveg a figyelt oldal(ak)on. Korábbi megjegyzés: A honlap még csak a lezajlott „WRO 2026” szezont mutatta."
    },
    {
      "id": "ftc",
      "name": "FIRST Tech Challenge (FTC)",
      "status": "yes",
      "fee": "💸💸",
      "focus": "Haladó mérnöki robotépítés + programozás (2026/27: BIOBUZZ)",
      "age": "12–18 év (9–12. évf.)",
      "type": "Csapat (6–12 fő)",
      "announce": "augusztus–szeptember",
      "deadline": "2026/27: dátumok még nincsenek meghirdetve",
      "eventDate": "Ligaversenyek/döntő dátuma: még nem ismert",
      "link": "https://firsttechchallenge.hu",
      "note": "Automatikus ellenőrzés: a(z) https://firsttechchallenge.hu oldalon található „2026/2027” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "ehod",
      "name": "e-Hód / Bebras",
      "status": "no",
      "fee": "",
      "focus": "Algoritmikus gondolkodás (programozás nélkül, online teszt)",
      "age": "3–12. évfolyam (5 korcsoport)",
      "type": "Egyéni",
      "announce": "október eleje",
      "deadline": "Regisztráció: október közepe",
      "eventDate": "Verseny (előzetes): 2026. nov. 9–20.",
      "link": "http://e-hod.elte.hu",
      "note": "Automatikus ellenőrzés: nem található 2026/2027-es kiírásra utaló szöveg a figyelt oldal(ak)on. Korábbi megjegyzés: Előzetes dátum volt látható, de a hivatalos kiírás/regisztráció még nem nyílt meg."
    },
    {
      "id": "nemes-online",
      "name": "Nemes Tihamér Online Programozási Verseny",
      "status": "yes",
      "fee": "",
      "focus": "Programozás (algoritmusok, C++/Python/Pascal/C#/Java)",
      "age": "5–12. osztály",
      "type": "Egyéni",
      "announce": "október",
      "deadline": "Folyamatos (fordulónként az előző szerdán éjfélig)",
      "eventDate": "5 forduló: nov, dec, jan, febr, ápr / Eredményhirdetés: máj. 7.",
      "link": "https://tehetseg.inf.elte.hu/nemes-online/nemes-aktualis.html",
      "note": "Automatikus ellenőrzés: a(z) https://tehetseg.inf.elte.hu/nemes-online/nemes-aktualis.html oldalon található „2026/2027” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "zsako",
      "name": "Zsakó László Programozási Verseny",
      "status": "unsure",
      "fee": "",
      "focus": "Programozás (algoritmusok, analízis, kódolás)",
      "age": "5–13. osztály",
      "type": "Egyéni",
      "announce": "október",
      "deadline": "1. ford. (iskolai): október",
      "eventDate": "Területi: november / Döntő: február (ELTE IK)",
      "link": "https://tehetseg.inf.elte.hu/nemes/",
      "note": "Automatikus ellenőrzés: egyik figyelt oldal sem volt elérhető (https://tehetseg.inf.elte.hu/nemes/); a korábbi állapot megőrizve. Korábbi megjegyzés: A kiírás dokumentumai még a 2025/2026-os tanévre vonatkoztak."
    },
    {
      "id": "kodkupa",
      "name": "Kódkupa – IIOT Válogatóverseny",
      "status": "no",
      "fee": "",
      "focus": "Csapat algoritmikus programozás (C, C++, Python)",
      "age": "5–12. évf. (profi: 7–12.)",
      "type": "Csapat (max. 4 fő)",
      "announce": "október",
      "deadline": "november eleje",
      "eventDate": "4 online selejtező: nov–febr / Döntő: március (Budapest, Fazekas) / Nemzetközi: május–június",
      "link": "https://kodkupa.hu",
      "note": "Automatikus ellenőrzés: nem található 2026/2027-es kiírásra utaló szöveg a figyelt oldal(ak)on. Korábbi megjegyzés: A honlap és a kiírás PDF-je még a 2025/2026-os szezonra vonatkozott."
    },
    {
      "id": "prograce",
      "name": "PROGRACE Programozói Verseny",
      "status": "no",
      "fee": "",
      "focus": "Programozás (egynapos csapatverseny)",
      "age": "Közép + egyetemisták (24 év alatt)",
      "type": "Csapat (3 fő)",
      "announce": "szeptember–október",
      "deadline": "november",
      "eventDate": "december 1. (Pécs, PTE MIK)",
      "link": "https://prograce.hu",
      "note": "Automatikus ellenőrzés: nem található 2026/2027-es kiírásra utaló szöveg a figyelt oldal(ak)on. Korábbi megjegyzés: A legfrissebb hír még a 2025/26-os fordulóról szólt."
    },
    {
      "id": "codeweek",
      "name": "Code Week Hungary",
      "status": "yes",
      "fee": "",
      "focus": "Kódolás, algoritmikus gondolkodás (nem klasszikus verseny, iskolai esemény)",
      "age": "Minden korosztály",
      "type": "Egyéni / csapat",
      "announce": "szeptember",
      "deadline": "Eseményregisztráció folyamatos",
      "eventDate": "2026. október 10–25. (14. Code Week)",
      "link": "https://www.codeweekhungary.hu",
      "note": "Automatikus ellenőrzés: a(z) https://www.codeweekhungary.hu oldalon található „14. Code Week” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "kozma",
      "name": "Kozma László Alkalmazói Tanulmányi Verseny",
      "status": "yes",
      "fee": "",
      "focus": "Alkalmazói informatika (grafika, szöveg, prezentáció, táblázat)",
      "age": "5–10. évfolyam (2 korcsoport)",
      "type": "Páros / csapat",
      "announce": "szeptember–október",
      "deadline": "2026. október 16. (XXV. verseny)",
      "eventDate": "2 forduló: iskolai → Döntő: május (Százhalombatta)",
      "link": "https://isze.hu/kozma-laszlo-orszagos-informatika-alkalmazoi-tanulmanyi-verseny/",
      "note": "Automatikus ellenőrzés: a(z) https://isze.hu/kozma-laszlo-orszagos-informatika-alkalmazoi-tanulmanyi-verseny/ oldalon található „2026/2027” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "dusza",
      "name": "Dusza Árpád Országos Programozói Emlékverseny",
      "status": "yes",
      "fee": "",
      "focus": "Programozás (hagyományos / web / mobilprogramozás)",
      "age": "9–13. évfolyam (középiskola)",
      "type": "Egyéni",
      "announce": "szeptember–október",
      "deadline": "október–november (2026/27-es felhívás elérhető)",
      "eventDate": "Regionális: január–február / Döntő: március–április",
      "link": "https://isze.hu/dusza-arpad-orszagos-programozoi-emlekverseny/",
      "note": "Automatikus ellenőrzés: a(z) https://isze.hu/dusza-arpad-orszagos-programozoi-emlekverseny/ oldalon található „2026/2027” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "radnoti",
      "name": "Radnóti HACK & CODE Informatikai Verseny",
      "status": "yes",
      "fee": "",
      "focus": "Programozás (Scratch) + logika + projekt (idei téma: „A bolygóért” – globális felmelegedés, szabadulószoba, csapatmunka)",
      "age": "7–8. évfolyam",
      "type": "Csapat (2–4 fő)",
      "announce": "október",
      "deadline": "2026. november 6.",
      "eventDate": "I. forduló (online): 2026. nov. 16. – dec. 11. / II. forduló (Pécs, személyes): 2027. jan. 8. / III. forduló (döntő): 2027. febr. 5.",
      "link": "http://www.radnoti-pecs.hu",
      "note": "Kézzel megerősítve (versenyfelhívás PDF, Pécs, 2026. október 5., pecsiradnoti.verseny@gmail.com): a verseny idén „Radnóti HACK & CODE a bolygóért” néven, a globális felmelegedés témájában fut. Nevezési határidő: 2026. november 6. A honlap keresésből ez nem derült ki, úgyhogy a jövőben is érdemes kézzel ellenőrizni/megerősíteni."
    },
    {
      "id": "nemes-alkalmazoi",
      "name": "Nemes Tihamér Alkalmazói Tanulmányi Verseny",
      "status": "yes",
      "fee": "",
      "focus": "Alkalmazói informatika (irodai szoftverek, weblapkészítés)",
      "age": "7–10. évfolyam",
      "type": "Egyéni",
      "announce": "november–december",
      "deadline": "2026. december 20.",
      "eventDate": "Iskolai forduló: 2027. jan. 6. / Országos: 2027. márc. 20. / Díjátadó: 2027. máj. 6. (ELTE IK)",
      "link": "https://versenyportal.hu/nemesa/nemesa_aktualis.html",
      "note": "Automatikus ellenőrzés: a(z) https://versenyportal.hu/nemesa/nemesa_aktualis.html oldalon található „2026/2027” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "rocs",
      "name": "ROCS – Robotprogramozó Csapatverseny",
      "status": "no",
      "fee": "",
      "focus": "LEGO robotprogramozás (vonalkövetés, akadálypálya)",
      "age": "5–8. évfolyam (3 korcsoport)",
      "type": "Csapat (2–3 fő)",
      "announce": "november–december",
      "deadline": "január–február",
      "eventDate": "Regionális: február–március / Döntő: április (Kecskemét)",
      "link": "http://robotprog.hu/",
      "note": "Automatikus ellenőrzés: nem található 2026/2027-es kiírásra utaló szöveg a figyelt oldal(ak)on. Korábbi megjegyzés: A honlap még a korábbi (2024/25-ös, XV.) kiírást mutatta."
    },
    {
      "id": "kovacs",
      "name": "Kovács Mihály Országos Grafikus Programozási Verseny",
      "status": "yes",
      "fee": "",
      "focus": "Grafikus programozás (teknőcgrafika, animáció, rekurzió – Scratch / Logo / Python)",
      "age": "3–12. évfolyam (4 korcsoport: K1–K4)",
      "type": "Egyéni",
      "announce": "november–december",
      "deadline": "2027. február 16.",
      "eventDate": "Iskolai forduló: 2027. febr. 17. / Országos: 2027. ápr. 10. / Eredményhirdetés: 2027 május (ELTE IK)",
      "link": "https://versenyportal.hu/logo/logo_aktualis.html",
      "note": "Automatikus ellenőrzés: a(z) https://versenyportal.hu/logo/logo_aktualis.html oldalon található „2026/2027” jelzi a 2026/2027-es kiírást."
    },
    {
      "id": "arpad-kupa",
      "name": "Árpád-kupa (Pécsi Árpád Fejedelem Gimnázium)",
      "status": "yes",
      "fee": "",
      "focus": "Digitális kultúra verseny (matematikai/logikai feladatok, grafika, szövegszerkesztés, prezentáció, táblázatkezelés, micro:bit programozás)",
      "age": "7–8. évfolyam",
      "type": "Csapat (2 fő)",
      "announce": "október",
      "deadline": "2026. november 20. (éjfél)",
      "eventDate": "1. forduló beadandó: 2026. dec. 19. / 2. forduló beadandó: 2027. febr. 19. / Döntő: 2027. ápr. 6., 14:00 (Pécs)",
      "link": "https://www.arpad-pecs.hu",
      "note": "Kézzel felvéve (versenyfelhívás PDF, Pécs, 2026. október 20., arpad-kupa@arpad-pecs.hu): a Pécsi Árpád Fejedelem Gimnázium és Általános Iskola digitális kultúra versenye, 7–8. évfolyamos, 2 fős csapatoknak. Regisztráció/1. forduló tesztmegoldás határideje: 2026. november 20. éjfél."
    }
  ]
};

if (typeof module !== "undefined" && module.exports) {
  module.exports = COMPETITION_DATA;
  module.exports.COMPETITION_DATA = COMPETITION_DATA;
}
if (typeof window !== "undefined") {
  window.COMPETITION_DATA = COMPETITION_DATA;
}
