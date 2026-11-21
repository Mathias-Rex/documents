// ============================================================================
// RENDERELÉS — DOMelemJS (DOMElemJS.createDOMElem) + createDOMBlocks
// (CreateDOMBlocks.*) segítségével, kizárólag a competitions-data.js-ből
// importált COMPETITION_DATA objektumból.
//
// Betöltési sorrend (lásd versenyek_2026_2027.html): domelemjs, createdomblocks,
// competitions-data.js, utils.js, majd ez a fájl — ebben a sorrendben kell
// lennie, mert ez a script a globális DOMElemJS, CreateDOMBlocks,
// COMPETITION_DATA és VersenyekUtils változókra támaszkodik.
// ============================================================================
(function () {
  "use strict";
  const createDOMElem = DOMElemJS.createDOMElem;
  const CDB = CreateDOMBlocks;

  // Tisztán számító/localStorage-ot kezelő segédfüggvények a utils.js-ből
  // (lásd ott: window.VersenyekUtils) — ez a fájl csak a tényleges DOM-
  // renderelésért felel.
  const getStoredTheme = VersenyekUtils.getStoredTheme;
  const setStoredTheme = VersenyekUtils.setStoredTheme;
  const getEffectiveTheme = VersenyekUtils.getEffectiveTheme;
  const applyTheme = VersenyekUtils.applyTheme;
  const themeButtonLabel = VersenyekUtils.themeButtonLabel;
  const getStoredFilterState = VersenyekUtils.getStoredFilterState;
  const setStoredFilterState = VersenyekUtils.setStoredFilterState;
  const daysUntilDeadline = VersenyekUtils.daysUntilDeadline;
  const countdownText = VersenyekUtils.countdownText;
  const sortItemsByDeadline = VersenyekUtils.sortItemsByDeadline;
  const todayIsoDate = VersenyekUtils.todayIsoDate;
  const formatIsoDateHu = VersenyekUtils.formatIsoDateHu;

  // Egy átfogó idővonal, ami minden (napra pontos határidejű) versenyt
  // időrendben felsorol, és a megfelelő helyen megjelöli a mai napot is —
  // azokat a versenyeket, amiknek a határideje folyamatos/ismeretlen, nem
  // lehet elhelyezni rajta, ezért kimaradnak (de külön jelezzük a számukat).
  function renderTimeline(parent, items) {
    const section = createDOMElem({ tag: "div", attrs: { class: "timeline-section" }, parent: parent });
    CDB.createTitle({ parent: section, id: "timeline-title", text: "📅 Idővonal — nevezési határidők" }, 3);

    const dated = items.filter(function (i) { return !!i.deadlineDate; });
    const undatedCount = items.length - dated.length;
    dated.sort(function (a, b) {
      return a.deadlineDate < b.deadlineDate ? -1 : (a.deadlineDate > b.deadlineDate ? 1 : 0);
    });

    createDOMElem({
      tag: "p", parent: section, attrs: { class: "timeline-hint" },
      text: "A konkrét (napra pontos) nevezési határidővel rendelkező " + dated.length + " verseny, időrendben." +
        (undatedCount > 0 ? " (" + undatedCount + " versenynek folyamatos/ismeretlen a határideje, ők nem kerülhetnek fel az idővonalra.)" : "")
    });

    const todayIso = todayIsoDate();
    const timelineEl = createDOMElem({ tag: "div", attrs: { class: "timeline" }, parent: section });
    let todayInserted = false;

    function insertTodayMarker() {
      createDOMElem({
        tag: "div", parent: timelineEl, attrs: { class: "timeline-today" },
        text: "📍 MA — " + formatIsoDateHu(todayIso)
      });
      todayInserted = true;
    }

    dated.forEach(function (item) {
      if (!todayInserted && item.deadlineDate >= todayIso) {
        insertTodayMarker();
      }
      const isExpiredEntry = item.deadlineDate < todayIso;
      const registeredMark = item.registered ? (isExpiredEntry ? " ✔️" : " 📝") : "";
      createDOMElem({
        tag: "div", parent: timelineEl,
        attrs: { class: "timeline-item" + (isExpiredEntry ? " is-expired-entry" : ""), "data-status": item.status },
        children: [
          { tag: "span", attrs: { class: "timeline-date" }, text: formatIsoDateHu(item.deadlineDate) },
          { tag: "span", attrs: { class: "timeline-name" }, text: item.name + registeredMark }
        ]
      });
    });
    if (!todayInserted) { insertTodayMarker(); }
  }

  function renderPage(data) {
    const page = CDB.createContainer({ parent: "#app", id: "page", class: "page" });

    const headerBar = createDOMElem({ tag: "div", attrs: { class: "header-bar" }, parent: page });
    const headerText = createDOMElem({ tag: "div", attrs: { class: "header-text" }, parent: headerBar });

    CDB.createTitle({ parent: headerText, id: "page-title", text: "Magyarországi Informatikai és Programozó Versenyek" }, 1);
    CDB.createTitle({ parent: headerText, id: "page-subtitle", text: data.schoolYear + "-es tanév", class: "subtitle" }, 2);
    createDOMElem({
      tag: "p", parent: headerText, attrs: { class: "meta-line" },
      text: "Adatvezérelt áttekintő — egyetlen JavaScript objektumból renderelve, DOMelemJS + createDOMBlocks segítségével."
    });

    const themeBtn = CDB.createButton({
      parent: headerBar, id: "theme-toggle",
      text: themeButtonLabel(getEffectiveTheme()),
      click: function () {
        const next = getEffectiveTheme() === "dark" ? "light" : "dark";
        applyTheme(next);
        setStoredTheme(next);
        themeBtn.textContent = themeButtonLabel(next);
      }
    });
    // Amíg a felhasználó nem választott explicit témát, kövessük élőben a
    // rendszer világos/sötét beállításának változását is (csak a gomb feliratán).
    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
        if (!getStoredTheme()) { themeBtn.textContent = themeButtonLabel(getEffectiveTheme()); }
      });
    }

    CDB.createAlert({
      parent: page, id: "status-alert", type: "info",
      title: "Utolsó ellenőrzés: " + data.statusCheckedAt,
      message: "A státuszok a versenyek hivatalos honlapjainak automatizált, webes ellenőrzésén alapulnak. Ahol még nincs 2026/27-es kiírás, ott a legutóbb ismert adatok láthatók."
    });

    // --- jelmagyarázat, a statusLegend objektumból felépítve ---
    const legendRow = createDOMElem({ tag: "div", attrs: { class: "legend-row" }, parent: page });
    Object.keys(data.statusLegend).forEach(function (key) {
      const l = data.statusLegend[key];
      createDOMElem({
        tag: "span", parent: legendRow, attrs: { class: "legend-item" },
        children: [
          { tag: "span", text: l.icon },
          { tag: "span", text: l.label }
        ]
      });
    });

    CDB.createDivider({ parent: page, id: "divider-1" });

    renderTimeline(page, data.items);

    CDB.createDivider({ parent: page, id: "divider-timeline" });

    // --- statisztika a data.items alapján kiszámolva (a szűrőgombok feliratain jelenik meg) ---
    const counts = { yes: 0, no: 0, unsure: 0 };
    data.items.forEach(function (item) { counts[item.status]++; });

    // --- szűrő gombsor (a kezdeti állapotot a localStorage-ból töltjük vissza) ---
    const storedFilterState = getStoredFilterState();
    const filterBar = createDOMElem({ tag: "div", attrs: { class: "filter-bar" }, parent: page });
    let currentFilterKey = (storedFilterState && storedFilterState.filterKey) || "all";
    let showExpired = storedFilterState && typeof storedFilterState.showExpired === "boolean"
      ? storedFilterState.showExpired
      : true;

    function persistFilterState() {
      setStoredFilterState({ filterKey: currentFilterKey, showExpired: showExpired });
    }

    function updateVisibility() {
      const cards = document.querySelectorAll("#competition-grid .comp-card");
      cards.forEach(function (card) {
        const matchesFilter = currentFilterKey === "all"
          || (currentFilterKey === "registered"
                ? card.dataset.registered === "true"
                : card.dataset.status === currentFilterKey);
        const matchesExpiredToggle = showExpired || card.dataset.expired !== "true";
        card.classList.toggle("is-hidden", !(matchesFilter && matchesExpiredToggle));
      });
    }

    function applyFilter(key) {
      currentFilterKey = key;
      filterBar.querySelectorAll(".btn").forEach(function (btn) {
        btn.classList.toggle("active", btn.id === "filter-" + key);
      });
      updateVisibility();
      persistFilterState();
    }

    CDB.createButton({
      parent: filterBar, id: "filter-all", text: "Összes (" + data.items.length + ")",
      click: function () { applyFilter("all"); }
    });
    Object.keys(data.statusLegend).forEach(function (key) {
      const l = data.statusLegend[key];
      CDB.createButton({
        parent: filterBar, id: "filter-" + key,
        text: l.icon + " " + l.shortLabel + " (" + counts[key] + ")",
        click: function () { applyFilter(key); }
      });
    });
    const registeredCount = data.items.filter(function (i) { return i.registered; }).length;
    CDB.createButton({
      parent: filterBar, id: "filter-registered",
      text: "📝 Neveztünk (" + registeredCount + ")",
      click: function () { applyFilter("registered"); }
    });
    // Ha a mentett szűrő időközben érvénytelenné vált (pl. régi adat), essünk vissza "all"-ra.
    if (!document.getElementById("filter-" + currentFilterKey)) { currentFilterKey = "all"; }
    filterBar.querySelectorAll(".btn").forEach(function (btn) {
      btn.classList.toggle("active", btn.id === "filter-" + currentFilterKey);
    });

    // --- "lejárt határidejűek mutatása" kapcsoló ---
    const expiredToggleRow = createDOMElem({ tag: "div", attrs: { class: "expired-toggle-row" }, parent: page });
    CDB.createCheckbox({
      parent: expiredToggleRow, id: "show-expired-toggle",
      labelText: "Lejárt határidejű versenyek mutatása (szürkítve)",
      labelfirst: false,
      checked: showExpired,
      onChange: function (e) {
        showExpired = e.target.checked;
        updateVisibility();
        persistFilterState();
      }
    });

    // --- verseny-kártyák rácsa ---
    const grid = CDB.createGrid({ parent: page, id: "competition-grid", class: "competition-grid", columns: 2, gap: "1.25rem" });

    sortItemsByDeadline(data.items).forEach(function (item) {
      renderCard(grid, item, data.statusLegend[item.status]);
    });
    // A mentett szűrő/kapcsoló állapotot csak most tudjuk érvényesíteni, miután
    // a kártyák ténylegesen létrejöttek a DOM-ban.
    updateVisibility();

    CDB.createDivider({ parent: page, id: "divider-2" });

    createDOMElem({
      tag: "footer", parent: page, attrs: { class: "page-footer" },
      children: [
        {
          tag: "p",
          children: [
            { tag: "span", text: "Forrás és teljes ellenőrzési jegyzőkönyv: " },
            { tag: "a", text: "figyelendo_versenyek_2026_2027.md", attrs: { href: "./figyelendo_versenyek_2026_2027.md" } },
            { tag: "span", text: " · " },
            { tag: "a", text: "versenyek_2026_2027_statusz.md", attrs: { href: "./versenyek_2026_2027_statusz.md" } }
          ]
        },
        { tag: "p", text: "Renderelve: DOMelemJS (createDOMElem) + createDOMBlocks (createdomblocks) — a competitions-data.js-ből importált egyetlen JS adatobjektumból. Az adatokat a scripts/scrape_competitions.py scraper generálja." }
      ]
    });
  }

  function renderCard(grid, item, legend) {
    // A kártya belső tartalmát közvetlenül DOMElemJS.createDOMElem-mel építjük fel
    // (append: false — csak a createCard() kapja meg a végén, body-ként).
    const metaWrap = createDOMElem({ tag: "div", attrs: { class: "comp-meta" }, append: false });
    const days = daysUntilDeadline(item.deadlineDate);

    CDB.createBadge({
      parent: metaWrap, id: "badge-" + item.id,
      text: legend.icon + " " + legend.shortLabel,
      type: legend.badgeType
    });
    if (item.registered) {
      // A határidő lejárta választja el a két állapotot: ha már lejárt, a
      // nevezés biztosan megtörtént ("Neveztünk"); ha még nem (vagy a
      // határidő ismeretlen/folyamatos), még csak szándékunkban áll
      // ("Jelentkezünk").
      const hasEntered = days !== null && days < 0;
      CDB.createBadge({
        parent: metaWrap, id: "badge-registered-" + item.id,
        text: hasEntered ? "✔️ Neveztünk" : "📝 Jelentkezünk",
        type: hasEntered ? "success" : "info"
      });
    }

    const fields = [
      { label: "Fókusz", value: item.focus },
      { label: "Korosztály", value: item.age },
      { label: "Típus", value: item.type },
      { label: "Kiírás megjelenése", value: item.announce },
      { label: "Nevezési határidő", value: item.deadline },
      { label: "Verseny időpontja", value: item.eventDate }
    ];

    createDOMElem({
      tag: "dl", parent: metaWrap, attrs: { class: "comp-fields" },
      children: fields.map(function (f) {
        return {
          tag: "div", attrs: { class: "comp-row" },
          children: [
            { tag: "dt", text: f.label },
            { tag: "dd", text: f.value }
          ]
        };
      })
    });

    const countdown = countdownText(days);
    if (countdown) {
      CDB.createParagraph({ parent: metaWrap, id: "countdown-" + item.id, text: countdown, class: "comp-countdown" });
    }

    CDB.createParagraph({ parent: metaWrap, id: "note-" + item.id, text: item.note, class: "comp-note" });
    CDB.createLink({ parent: metaWrap, id: "link-" + item.id, text: "Hivatalos oldal →", href: item.link, target: "_blank" });

    const titleText = (item.fee ? item.fee + " " : "") + item.name;
    const card = CDB.createCard({
      parent: grid, id: "card-" + item.id, class: "comp-card",
      title: titleText,
      body: metaWrap
    });
    card.dataset.status = item.status;
    card.dataset.registered = item.registered ? "true" : "false";
    const isExpired = days !== null && days < 0;
    card.dataset.expired = isExpired ? "true" : "false";
    card.classList.toggle("is-expired", isExpired);
  }

  renderPage(COMPETITION_DATA);
})();
