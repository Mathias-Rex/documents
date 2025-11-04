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

## 👦👧 Diák útmutató – GitHub Desktop telepítés és használat

### 1) Mire való a GitHub Desktop?

* Olyan, mint egy „mentőgomb” a kódhoz: **verziókat** őriz, vissza lehet lépni, és **össze lehet dolgozni** másokkal.
* Letöltés: [https://desktop.github.com/](https://desktop.github.com/)

**🎮 Szemléletes példa**

* Ma hozzáadod a **pontszámlálót** → holnap rájössz, hogy jobb volt a régi. A Desktopban visszakattintasz a tegnapi verzióra: kész.
* Team‑munkánál a Desktop jelzi, ha valaki **ugyanazt a fájlt** módosította – így nem írtok egymásra.

### 2) Telepítés

**Windows**

1. Töltsd le a telepítőt: [https://desktop.github.com/](https://desktop.github.com/)
2. Futtasd (`GitHubDesktopSetup.exe`) → Kövesd a varázslót.
3. Indítsd el: **GitHub Desktop** → **Sign in to GitHub**.

**macOS**

1. Töltsd le a `.dmg` fájlt: [https://desktop.github.com/](https://desktop.github.com/)
2. Nyisd meg, húzd az appot az **Applications** mappába.
3. Indítsd el → **Sign in to GitHub**.

> Tipp: Regisztráció GitHubra: [https://github.com/join](https://github.com/join) (szülői engedéllyel!).

### 3) Első belépés és beállítás

1. **Sign in** a GitHub‑fiókoddal.
2. A **Name** és **Email** mezőben azt állítsd be, amit szeretnél, hogy a commitoknál látszódjon.
3. (Opcionális) **Editor**: válaszd a kedvenc kódszerkesztőd (pl. Visual Studio Code). Letöltés: [https://code.visualstudio.com/](https://code.visualstudio.com/)

**👤 Példa – megjelenő név a commitokban**

* Name: `Kiss Bence`
* Email: `bence.k@example.com`
  A GitHubon így fog látszani: „Kiss Bence committed …”

### 4) Projekt (repo) letöltése a szervezetből

1. GitHub Desktop → **File → Clone repository**.
2. **URL** fülön illeszd be a repo linkjét (pl. `https://github.com/Mathias-Rex/codequartet-2025-platformer`).
3. Válassz helyi mappát → **Clone**.
4. **Open in Visual Studio Code** gombbal nyisd meg a kódot.

### 5) Napi munka – a 3 lépés

1. **Fetch/Pull** – először töltsd le a többiek frissítéseit: **Fetch origin** majd **Pull** (ha van).
2. **Commit** – dolgozz a kódban → GitHub Desktopban add meg a **Summary** mezőt (pl. „Add enemy movement”) → **Commit to main** (vagy saját brancheden).
3. **Push** – küldd fel: **Push origin**.

**🧠 Emlékeztető példa**

* *Reggel*: `Fetch/Pull` (hozd le, amit a többiek tegnap csináltak)
* *Nap közben*: kicsi, gyakori `Commit`‑ok beszédes üzenettel
* *Nap végén*: `Push` (küldd fel, hogy a többiek lássák)

### 6) Branch használata (haladóbb, de hasznos)

1. **Current branch** menü → **New branch** → pl. `feature/jump-logic` → **Create branch**.
2. Dolgozz ezen a branchen, commitolj, majd **Push**.
3. Ha kész, nyisd meg a GitHub weben a repo‑t → **Compare & pull request** → küldd be felülvizsgálatra.

**🌿 Példa – saját feature‑branch**

* `feature/score-hud` – pontszám kijelző
* `fix/mobile-controls` – mobil irányítás javítása
* `chore/assets-optimize` – képek tömörítése

### 7) Konfliktus? (amikor ketten ugyanazt a sort módosítják)

* GitHub Desktop jelzi: **conflict**.
* Kattints **Open in editor** → oldd meg kézzel (döntsd el, melyik változat maradjon).
* **Mark as resolved** → **Commit merge** → **Push**.

**🔧 Példa – tipikus konfliktus**

* `src/scenes/Level1.js` ugyanazt a sort változtattátok.
* A szerkesztő így jelöli:

```
<<<<<<< HEAD
player.speed = 200
=======
player.speed = 220
>>>>>>> feature/speed-tuning
```

* Döntsd el, melyik maradjon (pl. `220`), töröld a jelölő sorokat, mentsd el → jelöld `resolved`‑nak.

### 8) GitHub Pages – demó oldal frissítése

* Ha a tanárnő bekapcsolta a Pages-t, elég **Push‑olni a main brancre**: a változások pár perc után megjelennek a project URL‑en.

### 9) Jó szokások (pro tipp)

* **Kicsi, gyakori commitok** (könnyebb visszavonni).
* **Beszédes üzenetek**: „Add score HUD”, „Improve collision”.
* **Pull mielőtt dolgozol**, és **Push amikor végeztél**.
* **Ne tegyél fel jelszót, privát kulcsot, személyes adatot** a repo‑ba.
* **README frissítése**: ha valamit telepíteni kell (`npm i`), írd bele a lépéseket.

**✅ Mintafolyamat – első indítás Vite/Phaser projektnél**

1. `npm i` (függőségek)
2. `npm run dev` (fejlesztői szerver)
3. Kódolj → `Commit` → `Push`

### 10) Gyors hibaelhárítás

* **Nem tudok Push‑olni**: előbb **Pull**, lehet, hogy közben más is változtatott.
* **`gh-pages` után nincs frissülés**: várj 2‑3 percet; ellenőrizd a Vite `base` beállítást.
* **„Permission denied”**: kérj meghívót a szervezetbe / repohoz; ellenőrizd, nem csak „Read” jogod van‑e.
* **Nem látom a repót klónozásnál**: kapj meghívót, vagy **URL** fülön illeszd be a linket.
* **Minden piros a Desktopban**: lehet, hogy a fájlok még nincsenek „staged”; jelöld ki és add hozzá a commit‑hoz.

---

## C) 🌱 Pályaorientációs megjegyzés (röviden)

* Aki a jövőben **technológiai pályán** gondolkodik, annak a **GitHub‑jelenlét** szinte elkerülhetetlen.
* A CV‑ben jól mutat: *„már általános iskolában, a Mathias‑Rex szervezetben dolgoztam az első játékomon”*.

---

## D) 📎 Hasznos linkek (sima URL‑ek)

* GitHub főoldal: [https://github.com/](https://github.com/)
* Regisztráció: [https://github.com/join](https://github.com/join)
* GitHub Desktop: [https://desktop.github.com/](https://desktop.github.com/)
* Visual Studio Code: [https://code.visualstudio.com/](https://code.visualstudio.com/)
* GitHub Pages útmutató (általános): [https://docs.github.com/pages](https://docs.github.com/pages)

---

**Megjegyzés:** Ha bármiben elakadás van, **nyugodtan keressenek** – távoli segítség/mini‑betanítás szívesen. Ha a családi szabályzat nem enged regisztrációt, **átmenetileg megoldható egyetlen (szülői) GitHub‑hozzáférésen** keresztül is; működőképes, csak kicsit körülményesebb.
