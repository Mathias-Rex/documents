# Miért kell verziókövetés?

A szoftverfejlesztés **csapatjáték**. Ha pendrive-on vagy e‑mailben küldözgetjük a fájlokat:

* könnyen lesz **10 különböző változat** ugyanarról a projektről ("final", "final2", "végleges_legutolsó"… 😅),
* nem látjuk, **ki mit** módosított és **miért**,
* ha ketten ugyanazt a fájlt szerkesztik, **összefűzni** őket utólag szinte lehetetlen,
* elég egy elveszett pendrive, és **odavész a munka**.

A **verziókövetés** (Git) erre ad megoldást:

* Minden módosítás **naplózva** van: ki, mikor, mit és miért (rövid üzenettel).
* Többen dolgozhatnak **párhuzamosan**: mindenkinek lehet saját „ág” (branch), a végén **egyesítjük** (merge).
* Ha összeakadtok ugyanazon a soron, a rendszer **szól**, és segít megoldani a **konfliktust**.
* A központi tárhely (**GitHub**) olyan, mint a „**közös mappa a felhőben**”: biztonsági másolat, hozzáférés‑kezelés, visszaállítható korábbi állapot.
* Extra bónusz: egy kattintással lehet **webes demót** publikálni (GitHub Pages), és látszik a diákok **saját hozzájárulása** is (CV‑be kiváló).

> Röviden: a Git (verziókövetés) = **időgép + munkamegosztás + biztonsági másolat**. A GitHub = **közös, felhős munkahely**, ahol ez mind együtt kényelmesen használható.

# 🎓 GitHub – Iskolai szervezet (Tanári – Szervezet Adminisztrátori) és GitHub Desktop (Diákok) útmutató

Ez a dokumentum két részből áll:

* **A. Tanári – Szervezet Adminisztrátori útmutató** – GitHub szervezet (**Mathias‑Rex**) kezelése, meghívások, jogosultságok, repo‑kezelés.
* **B. Diák útmutató** – GitHub Desktop telepítése és használata Windowson és macOS-en.

---

## A) 👩‍🏫 Tanári – Szervezet Adminisztrátori útmutató

### 1) Mi az a GitHub-szervezet és miért hasznos?

* **GitHub-szervezet**: olyan „iskolai mappa”, ahol **több repo** (projekt) és **több felhasználó** dolgozik együtt.
* Előnyök: közös tárhely, hozzáférés-kezelés, láthatóság beállítása (privát/nyilvános), egyszerű megosztás.
* Hol érhető el: [https://github.com/](https://github.com/) (bejelentkezés után a **Mathias‑Rex** szervezet látszik a profilképre kattintva).

### 2) Szerepkörök (jogosultságok) röviden

* **Owner** (Tulajdonos): teljes hozzáférés az egész szervezethez (beállítások, tagok, repo‑k). Javaslat: legyen **min. 1 Owner** (pl. Tanárnő), a többiek **Member**.
* **Member** (Tag): a kiosztott repókban tud dolgozni (írási/olvasási jog attól függően, mit kap).
* **Team** (Csapat – opcionális): pl. „CodeQuartet” csapat; a csapatnak adunk jogot a repókhoz, és a gyerekeket ehhez a csapathoz rendeljük.

### 3) Meghívók küldése a diákoknak és szülőknek

1. Lépjen a szervezet főoldalára (Mathias‑Rex).
2. **People** → **Invite member**.
3. Írja be az e-mail címet / GitHub felhasználónevet.
4. Válassza ki a szerepkört (**Member**), majd **Send invitation**.
5. (Opcionális) **Teams** → válassza ki a **CodeQuartet** csapatot → **Add a member**.

> Tipp: Ha valaki még nem regisztrált GitHubra, a meghívót később is elfogadhatja; a rendszer végig fogja vezetni a regisztráción.

### 3.1) Csapat létrehozása (példa: CodeQuartet)

1. Lépjen a szervezet főoldalára → **Teams** → **New team**.
2. **Team name**: `CodeQuartet` (leírás adható, pl. „Versenycsapat 2025 – platformer játék”).
3. **Team visibility**:

   * **Visible**: a szervezeten belül mindenki látja, könnyebb meghívni és azonosítani.
   * **Secret**: csak a tagok és az ownerek látják (pl. ha a projekt még meglepetés).
4. Kattintson **Create team**.
5. **Tagok hozzáadása**: a csapat oldalán **Members → Add a member** → írja be a diákok GitHub‑nevét/e‑mailjét.
6. **Hozzáférés adása repókhoz**: **Repositories → Add repository** → válassza ki a projektet → **Permission**: javasolt **Write** (írás) a diákoknak. (Tanárnő maradjon **Admin**/**Owner** szinten.)
7. (Opcionális) **Alcsapatok**: nagyobb létszámnál létrehozhatók pl. „Frontend”, „Pályatervezés”, „Tesztelés” alcsapatok.

> **Miért jó a csapat?**
> Ha új diák érkezik, elég a csapatba felvenni – **minden csapathoz rendelt repohoz automatikusan megkapja a jogot**. Ha valaki kilép, elég a csapatból eltávolítani.

**🎯 Példa – CodeQuartet csapat felépítés**

* **Team**: `CodeQuartet`
* **Repositories hozzáadva**: `codequartet-2025-platformer`, `assets-pack`, `docs`
* **Jogosultság**: `Write` a diákoknak, `Admin` a Tanárnőnek
* **Alcsapatok**: `level-design`, `ui-sfx`

**✉️ Meghívó‑szöveg minta (Teams → Add a member)**

> Szia! Meghívtunk a Mathias‑Rex szervezet **CodeQuartet** csapatába. Itt dolgozunk a 2025‑ös versenyjátékunkon. Ha kérdésed van a belépésnél, szólj – segítünk!

### 4) Új repo létrehozása (versenyprojektekhez)

1. Szervezet főoldal: **Repositories** → **New**.
2. **Repository name** példák:

   * `codequartet-2025-platformer` (fő játék)
   * `codequartet-2025-assets` (képek/zenék külön tárolva)
   * `codequartet-2025-docs` (leírások, ötletlista, feladatok)
3. **Visibility**: kezdetben **Private** (később átállítható **Public**‑ra, ha szeretnénk megmutatni a világnak).
4. **Add a README**: pipálja be; így lesz rögtön leírás a projekt gyökérben.
5. **Add .gitignore**: válassza ki pl. `Node`/`JavaScript` sablont (felesleges build fájlok kizárására).
6. **Create repository**.

**📁 Ajánlott mappaszerkezet példa (platformer játék)**

```
root/
├─ src/
│  ├─ scenes/
│  ├─ sprites/
│  ├─ systems/
│  └─ main.js
├─ assets/
│  ├─ images/
│  ├─ audio/
│  └─ fonts/
├─ docs/
│  └─ design-notes.md
├─ .gitignore
├─ package.json
└─ README.md
```

**🧾 Commit‑üzenet példák**

* „Add player jump and gravity”
* „Fix enemy collision on platforms”
* „Setup GitHub Pages deploy script”

### 5) Hozzáférések kiosztása egy repo-hoz

1. Lépjen be a repo-ba → **Settings** → **Collaborators and teams** (Szervezeten belül: **Manage access** / **Teams**).
2. Adja hozzá a **CodeQuartet** csapatot **Write** jogosultsággal.
3. Tanárnő maradhat **Admin** (vagy Owner) jogosultsággal a repo felett.

### 6) Láthatóság: mikor legyen Public?

* **Privát** fejlesztés közben: biztonságosabb (diákok kódja nem publikus).
* **Publikus** kiadásnál: ha szeretnénk linkkel megmutatni (pl. demó oldal). A beállítás a repo **Settings → General → Change repository visibility** alatt módosítható.

### 7) GitHub Pages – webes játék közzététele

1. Repo → **Settings** → **Pages**.
2. **Source**: `Deploy from a branch`, Branch: `main`, Folder: `/root` (statikus projektnél) → **Save**.
3. Pár perc múlva lesz egy URL (pl. `https://mathias-rex.github.io/codequartet-2025-platformer`).

**⚙️ Vite/Phaser projekt publikálása – szemléletes példa**

* Adjunk a `package.json`‑hoz deploy scripteket:

```
{
  "scripts": {
    "build": "vite build",
    "predeploy": "npm run build",
    "deploy": "gh-pages -d dist"
  }
}
```

* Telepítés helyben: `npm i -D gh-pages`
* **Settings → Pages**: `Deploy from a branch` helyett használhatjuk a `gh-pages` brancht; a `gh-pages` csomag push-olja oda a buildet.
* Parancs: `npm run deploy` → a demó a `https://<org>.github.io/<repo>/` címen jelenik meg.

> **Megjegyzés**: ha az oldal üresnek tűnik, nézze meg, hogy a `base` beállítás Vite‑ban egyezik‑e a repo nevével (pl. `base: '/codequartet-2025-platformer/'`).

### 8) Egységes elnevezések és szabályok (javaslat)

* **Branch‑név**: `feature/valami`, `fix/hiba-123`.
* **Commit‑üzenet**: rövid, jelen idő: „Add player jump”, „Fix collision bug”.
* **Mappa‑szerkezet**: `src/`, `assets/`, `docs/`.
* **README.md**: pár sor leírás + futtatási lépések.

### 9) Biztonság és adatvédelem (iskolai környezet)

* Diákok csak az **iskolai projekthez szükséges** adatot osszák meg.
* Magán e‑mail cím: használható, de javasolt külön „iskolai célú” e‑mail.
* **Képek/név**: ha publikus repo lesz, érdemes minimalizálni a személyes azonosítást.
* **Moderálás**: a **Settings → Moderation** alatt beállítható a hozzászólások kezelése (public repóknál hasznos).
* **Branch protection**: a **Settings → Branches → Add rule** alatt megkövetelhető a Pull Request (így nem megy közvetlenül a `main`‑be a hibás kód).

**🔐 Branch protection példa**

* `Branch name pattern`: `main`
* Pipák: „Require a pull request before merging”, „Require approvals: 1”, „Require status checks” (ha van).

### 10) Tipikus tanári feladatok – gyorslista

* [ ] Meghívók küldése (People → Invite member)
* [ ] Csapat létrehozása: **CodeQuartet** (Teams)
* [ ] Repo létrehozása (Private) + README
* [ ] Csapatnak Write jog adása
* [ ] GitHub Pages beállítása (ha publikus demó kell)
* [ ] Repo láthatóság állítása (Public csak a végén)

### 11) Gyakori kérdések (GYIK)

**Kell-e érteni a Git parancsokat?** – Nem. A diákok a **GitHub Desktop** alkalmazással kattintgatva tudnak dolgozni.

**Mi van, ha valaki nem tud/akar regisztrálni?** – Átmenetileg megoldható **egy közös (szülő) fiókon** keresztül is, de a név szerzői megjelenítése ilyenkor nem automatikus.

**Több repo lesz?** – Igen, akár tantárgyanként/évenként. A szervezet hosszú távú „iskolai tárhely”.