// Mentett téma visszaállítása minél korábban, hogy ne villanjon fel a rossz téma.
// Szándékosan külön, kicsi fájl: ennek már a <head>-ben, a styles.css betöltése
// ELŐTT le kell futnia (blokkoló classic <script>, nem type="module"), hogy a
// data-theme attribútum a CSS kiértékelése előtt beálljon.
(function () {
  try {
    const saved = localStorage.getItem("versenyek-theme");
    if (saved === "light" || saved === "dark") {
      document.documentElement.setAttribute("data-theme", saved);
    }
  } catch (e) { /* localStorage nem elérhető (pl. privát böngészés) */ }
})();
