## Käyttöohjeet

### Vaatimukset

* Python 3.12 tai uudempi
* Internet-yhteys (Vipunen API:n ja Gemini API:n käyttöä varten)

### 1. Siirry projektihakemistoon

Avaa komentokehote tai PowerShell ja siirry projektin juurihakemistoon:

```bash
cd polku/projektiin
```

Esimerkiksi:

```bash
cd C:\Users\Käyttäjä\Documents\gradia-showcase
```

---

### 2. Luo virtuaaliympäristö

```bash
python -m venv .venv
```

Aktivoi ympäristö:

**Windows**

```bash
.venv\Scripts\activate
```

**Linux / macOS**

```bash
source .venv/bin/activate
```

---

### 3. Asenna riippuvuudet

```bash
pip install -r requirements.txt
```

---

### 4. Määritä Gemini API -avain (Vaihtoehtoinen)

**Ohjelmisto käyttää puuttuvan tai virheellisen API -avaimen tapauksessa tallenettua vastausta, joten avaimen määrittäminen ei ole pakollista.** <br>
Geminin API -avain haetaan ympäristömuuttujista nimellä "GENAI_API_KEY". Vaihtoehtoisesti avaimen voi manuaalisesti asettaa gemini.py tiedoston rivillä 37. Gemini API-avaimen voi luoda ilmaiseksi osoitteessa https://aistudio.google.com/. 

---

### 5. Käynnistä sovellus

```bash
uvicorn main:app --reload
```

Sovellus käynnistyy oletuksena osoitteeseen:

```text
http://127.0.0.1:8000
```

Avaa osoite selaimessa.

---

### Sovelluksen toiminta

Käynnistyksen yhteydessä sovellus:

1. Hakee opinnäytetyödatan Vipunen API:sta (myös virheen sattuessa käyttää tallennettua CSV-tiedostoa).
2. Käsittelee datan Pandas-kirjastolla laskemalla vuosittaiset aggregaatit ja osuudet sekä koulu- että koulutuslinjan mukaan.
3. Generoi vuosikohtaiset havainnot Gemini-mallilla.
4. Tarjoaa tulokset FastAPI-rajapinnan kautta käyttöliittymälle.

Ensimmäinen lataus voi kestää hetken riippuen API-vastausajoista ja mahdollisen tekoälyanalyysin suorittamisesta. 
