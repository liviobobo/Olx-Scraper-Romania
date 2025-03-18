Proiect: OLX Scraper - Extragere Numere de Telefon
Descriere:

Acesta este un script Python care utilizează Selenium pentru a scapa și extrage numerele de telefon din anunțurile disponibile pe site-ul OLX (olx.ro). Scriptul este conceput pentru a naviga prin paginile de anunțuri, a derula conținutul pentru a încărca toate listările, a extrage URL-urile unice ale anunțurilor și a obține numerele de telefon asociate. Este optimizat pentru a evita duplicatele și respectă o limită configurabilă de numere extrase, ideal pentru testare sau utilizare controlată.

Caracteristici:

Derulare automată: Scriptul derulează pagina pentru a încărca toate anunțurile, gestionând încărcarea dinamică.
Extragere URL-uri cu JavaScript: Folosește un script JavaScript pentru a identifica și extrage doar URL-urile relevante ale anunțurilor (ce conțin /d/oferta/).
Limită de numere: Permite setarea unei limite maxime de numere unice extrase (implicit 3 pentru testare).
Evitare duplicate: Verifică și procesează doar URL-urile unice, prevenind accesarea repetată a aceluiași anunț.
Logging detaliat: Generează un fișier scraper.log pentru a înregistra toate acțiunile și erorile, facilitând depanarea.
Mesaje scurte de eroare: Înlocuiește stivele de erori lungi cu mesaje concise și informative.
Reinițializare sesiune: Detectează și gestionează pierderea sesiunii, reinitializând browserul dacă este necesar.
Tehnologii utilizate:

Python: Limbajul principal de programare.
Selenium: Pentru automatizarea browserului și interacțiunea cu paginile OLX.
ChromeDriver: Pentru controlul browserului Chrome.
Cerințe:

Python 3.x
Biblioteca Selenium (pip install selenium)
ChromeDriver compatibil cu versiunea Chrome instalată (descărcabil de pe chromedriver.chromium.org)
Instalare și utilizare:

Instalează dependințele Python necesare.
Descarcă și configurează ChromeDriver, actualizând calea din cod (executable_path="C:/chromedriver/chromedriver.exe") dacă este necesar.
Rulează scriptul:
bash

Collapse

Wrap

Copy
python olx_scraper.py
Verifică fișierul scraper.log și numere_telefon.txt pentru rezultate.
Autor:

Acest script a fost creat de Grok, o IA dezvoltată de xAI, cu contribuția esențială a lui Liviu. Mulțumim lui Liviu pentru feedback-ul, testarea și colaborarea strânsă care au dus la optimizarea și finalizarea acestui proiect.

Licență:

MIT License

Note:

Scriptul este personalizat pentru olx.ro. Poate necesita ajustări pentru alte versiuni OLX.
Respectă termenii de utilizare ai OLX și reglementările privind protecția datelor (ex. GDPR) atunci când folosești acest script.
Folosește-l responsabil și doar în scopuri legale.
Versiune: 5

Data: 17 Martie 2025
