// ============================================================================
// VersenyekUtils — újrafelhasználható segédfüggvények.
//
// Szándékosan nem építenek DOM-ot (nem hívnak sem DOMElemJS.createDOMElem-et,
// sem CreateDOMBlocks.*-ot) — csak dátumszámítást, rendezést és localStorage
// olvasást/írást végeznek. Az app.js ezeket a window.VersenyekUtils névtéren
// keresztül éri el, ezért ennek a fájlnak app.js ELŐTT kell betöltődnie.
// ============================================================================
(function () {
  "use strict";

  // --- világos / sötét mód kezelése ---
  var THEME_KEY = "versenyek-theme";

  function getStoredTheme() {
    try { return localStorage.getItem(THEME_KEY); } catch (e) { return null; }
  }
  function setStoredTheme(theme) {
    try {
      if (theme) { localStorage.setItem(THEME_KEY, theme); }
      else { localStorage.removeItem(THEME_KEY); }
    } catch (e) { /* localStorage nem elérhető */ }
  }
  function getEffectiveTheme() {
    var stored = getStoredTheme();
    if (stored === "light" || stored === "dark") { return stored; }
    return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  }
  function applyTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
  }
  function themeButtonLabel(theme) {
    return theme === "dark" ? "☀️ Világos mód" : "🌙 Sötét mód";
  }

  // --- szűrő / kapcsoló állapot megjegyzése ---
  var FILTER_STATE_KEY = "versenyek-filter-state";

  function getStoredFilterState() {
    try {
      var raw = localStorage.getItem(FILTER_STATE_KEY);
      if (!raw) { return null; }
      var parsed = JSON.parse(raw);
      return parsed && typeof parsed === "object" ? parsed : null;
    } catch (e) { return null; }
  }
  function setStoredFilterState(state) {
    try { localStorage.setItem(FILTER_STATE_KEY, JSON.stringify(state)); }
    catch (e) { /* localStorage nem elérhető */ }
  }

  // --- határidő-számítás és rendezés a mai dátumhoz képest ---
  function daysUntilDeadline(deadlineDate) {
    if (!deadlineDate) { return null; }
    var today = new Date();
    today.setHours(0, 0, 0, 0);
    var parts = deadlineDate.split("-").map(Number);
    var deadline = new Date(parts[0], parts[1] - 1, parts[2]);
    return Math.round((deadline - today) / 86400000);
  }

  function countdownText(days) {
    if (days === null) { return null; }
    if (days === 0) { return "⏰ Ma jár le a nevezési határidő!"; }
    if (days > 0) { return "⏳ " + days + " nap múlva jár le a nevezési határidő"; }
    return "✖️ " + Math.abs(days) + " napja lejárt a nevezési határidő";
  }

  // A versenyeket a nevezési határidő szerint rendezi: a legközelebb lejáró
  // (de még nem lejárt) határidejűek elöl, utánuk az ismeretlen/folyamatos
  // határidejűek, végül a már lejártak — azok közül is a régebben lejártak
  // kerülnek leghátrébb.
  function sortItemsByDeadline(items) {
    var withDays = items.map(function (item) {
      return { item: item, days: daysUntilDeadline(item.deadlineDate) };
    });
    var upcoming = withDays.filter(function (x) { return x.days !== null && x.days >= 0; });
    var unknown = withDays.filter(function (x) { return x.days === null; });
    var expired = withDays.filter(function (x) { return x.days !== null && x.days < 0; });

    upcoming.sort(function (a, b) { return a.days - b.days; });
    expired.sort(function (a, b) { return b.days - a.days; });

    return upcoming.concat(unknown, expired).map(function (x) { return x.item; });
  }

  // --- magyar dátumformázás az idővonalhoz ---
  var HU_MONTHS_SHORT = ["jan", "febr", "márc", "ápr", "máj", "jún", "júl", "aug", "szept", "okt", "nov", "dec"];

  function todayIsoDate() {
    var d = new Date();
    var mm = String(d.getMonth() + 1).padStart(2, "0");
    var dd = String(d.getDate()).padStart(2, "0");
    return d.getFullYear() + "-" + mm + "-" + dd;
  }

  function formatIsoDateHu(iso) {
    var parts = iso.split("-").map(Number);
    return parts[0] + ". " + HU_MONTHS_SHORT[parts[1] - 1] + ". " + parts[2] + ".";
  }

  window.VersenyekUtils = {
    getStoredTheme: getStoredTheme,
    setStoredTheme: setStoredTheme,
    getEffectiveTheme: getEffectiveTheme,
    applyTheme: applyTheme,
    themeButtonLabel: themeButtonLabel,
    getStoredFilterState: getStoredFilterState,
    setStoredFilterState: setStoredFilterState,
    daysUntilDeadline: daysUntilDeadline,
    countdownText: countdownText,
    sortItemsByDeadline: sortItemsByDeadline,
    todayIsoDate: todayIsoDate,
    formatIsoDateHu: formatIsoDateHu
  };
})();
