from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, WebDriverException
import time
import random
import logging

# Configurare logging
logging.basicConfig(filename='scraper.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Configurare ChromeDriver (declarare globală)
service = Service(executable_path="C:/chromedriver/chromedriver.exe")
driver = None

# Inițializare driver
def init_driver():
    global driver
    driver = webdriver.Chrome(service=service)
    return driver

# Deschide pagina OLX (ex. județul Bihor)
driver = init_driver()
url = "https://www.olx.ro/bihor-judet/"
logging.info(f"Navigare la URL: {url}")
print(f"Navigare la URL: {url}")
driver.get(url)

# Acceptă cookie-urile
try:
    accept_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
    )
    accept_button.click()
    logging.info("Cookie-urile au fost acceptate.")
    print("Cookie-urile au fost acceptate.")
    time.sleep(random.uniform(3, 5))
except:
    logging.warning("Bannerul de cookie-uri nu a fost găsit.")
    print("Bannerul de cookie-uri nu a fost găsit.")

# Numărul maxim de numere de telefon unice de extras (setat la 3 pentru test)
limita_numere = 50

# Set pentru URL-urile procesate și numerele extrase
processed_urls = set()
extracted_numbers = set()

# Funcție pentru derularea paginii până la capăt
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(2, 4))
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    logging.info("Derulare completă.")
    print("Derulare completă.")

# Funcție pentru extragerea numerelor de telefon
def extrage_numere():
    global driver
    try:
        # Derulează pagina pentru a încărca toate anunțurile
        scroll_to_bottom()

        # Execută JavaScript pentru a extrage doar URL-urile de anunțuri (/d/oferta/)
        logging.info("Execut JavaScript pentru a extrage URL-uri...")
        print("Execut JavaScript pentru a extrage URL-uri...")
        script = """
            var links = document.getElementsByTagName('a');
            var urls = [];
            for (var i = 0; i < links.length; i++) {
                if (links[i].href && links[i].href.includes('olx.ro') && links[i].href.includes('/d/oferta/')) {
                    urls.push(links[i].href);
                }
            }
            return urls;
        """
        url_list = driver.execute_script(script)
        logging.info(f"URL-uri găsite cu JavaScript: {len(url_list)}")
        print(f"URL-uri găsite cu JavaScript: {len(url_list)}")

        # Filtrează duplicatele și creează o listă de tuple (URL, None)
        url_list_unique = list(dict.fromkeys(url_list))
        url_list_processed = [(url, None) for url in url_list_unique]
        logging.info(f"URL-uri unice găsite: {len(url_list_processed)}")
        print(f"URL-uri unice găsite: {len(url_list_processed)}")

        if not url_list_processed:
            logging.error("Nu există anunțuri de procesat (lista URL-urilor este goală).")
            print("Nu există anunțuri de procesat (lista URL-urilor este goală).")
            return False

        # Salvează handle-ul tab-ului original
        original_window = driver.current_window_handle

        # Parcurge lista de URL-uri
        for i, (anunt_url, _) in enumerate(url_list_processed):
            logging.info(f"Procesez URL-ul {i + 1}/{len(url_list_processed)}: {anunt_url}")
            print(f"Procesez URL-ul {i + 1}/{len(url_list_processed)}: {anunt_url}")

            # Verifică dacă sesiunea este validă
            try:
                driver.title
            except WebDriverException:
                logging.error("Sesiune invalidă. Reconectare...")
                print("Sesiune invalidă. Reconectare...")
                driver.quit()
                driver = init_driver()
                driver.get(url)
                time.sleep(random.uniform(3, 5))
                return extrage_numere()

            # Verifică dacă URL-ul a fost deja procesat
            if anunt_url in processed_urls:
                logging.info(f"Anunțul {anunt_url} a fost deja procesat. Sari peste.")
                print(f"Anunțul {anunt_url} a fost deja procesat. Sari peste.")
                continue

            # Navighează direct la URL-ul anunțului
            driver.get(anunt_url)
            time.sleep(random.uniform(3, 5))

            # Verifică URL-ul curent pentru anunțuri externe
            current_url = driver.current_url
            if "olx.ro" not in current_url:
                logging.info("Anunț extern detectat. Revenire la lista de anunțuri.")
                print("Anunț extern detectat. Revenire la lista de anunțuri.")
                driver.get(url)
                time.sleep(random.uniform(3, 5))
                continue

            # Adaugă URL-ul în setul de procesate
            processed_urls.add(anunt_url)

            try:
                # Așteaptă și apasă butonul „Sună vânzătorul”
                buton_telefon = WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "css-10t2p5d"))
                )
                buton_telefon.click()
                logging.info("Butonul 'Sună vânzătorul' a fost apăsat.")
                print("Butonul 'Sună vânzătorul' a fost apăsat.")

                # Extrage numărul de telefon
                numar = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.XPATH, "//a[contains(@href, 'tel:')]"))
                )
                numar_telefon = numar.get_attribute("href").replace("tel:", "")
                logging.info(f"Număr extras: {numar_telefon}")
                print(f"Număr extras: {numar_telefon}")

                # Verifică dacă a fost atinsă limita de numere
                if len(extracted_numbers) >= limita_numere:
                    logging.info("Limita de numere unice atinsă. Oprire procesare.")
                    print("Limita de numere unice atinsă. Oprire procesare.")
                    return True

                # Verifică dacă numărul a fost deja extras
                if numar_telefon not in extracted_numbers:
                    extracted_numbers.add(numar_telefon)
                    with open("numere_telefon.txt", "a") as file:
                        file.write(numar_telefon + "\n")
                else:
                    logging.info(f"Numărul {numar_telefon} a fost deja extras.")
                    print(f"Numărul {numar_telefon} a fost deja extras.")

            except Exception as e:
                logging.warning("Eroare: Număr nu găsit.")
                print("Eroare: Număr nu găsit.")

            # Revenire la pagina inițială
            driver.get(url)
            time.sleep(random.uniform(3, 5))
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "css-qo0cxu"))
            )

        return True  # Continuă la următoarea pagină

    except Exception as e:
        logging.error(f"Eroare: {str(e)}")
        print(f"Eroare: {str(e)}")
        return False

# Procesează paginile până la limită
while len(extracted_numbers) < limita_numere:
    if not extrage_numere():
        break

    if len(extracted_numbers) >= limita_numere:
        logging.info("Limita de numere unice a fost atinsă.")
        print("Limita de numere unice a fost atinsă.")
        break

    try:
        # Găsește butonul „Următoarea pagină”
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "css-6tfxml"))
        )
        next_button.click()
        time.sleep(random.uniform(5, 10))
    except Exception as e:
        logging.info(f"Eroare: Nu mai sunt pagini disponibile.")
        print(f"Eroare: Nu mai sunt pagini disponibile.")
        break

# Închide browser-ul
logging.info("Închid browser-ul.")
print("Închid browser-ul.")
driver.quit()