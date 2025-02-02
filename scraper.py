import os
import re
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Funkcja do ładowania wszystkich ofert poprzez klikanie "Pokaż kolejne oferty"
def load_all_pages(driver, max_clicks=200):
    clicks = 0
    last_count = 0
    while clicks < max_clicks:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)

            try:
                load_more_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Pokaż kolejne oferty')]"))
                )
            except:
                print("Nie znaleziono przycisku 'Pokaż kolejne oferty'. Kończę pobieranie.")
                break

            driver.execute_script("arguments[0].scrollIntoView();", load_more_button)
            time.sleep(2)
            driver.execute_script("arguments[0].click();", load_more_button)
            print(f"Kliknięto 'Pokaż kolejne oferty'.")
            time.sleep(1)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            new_count = len(driver.find_elements(By.CLASS_NAME, "posting-list-item"))
            print(f"Załadowano {new_count} ofert.")

            if new_count == last_count:
                print("Nie załadowano nowych ofert, kończę pobieranie...")
                break

            last_count = new_count
            clicks += 1
        except Exception as e:
            print(f"Błąd podczas ładowania ofert: {e}")
            break

# Funkcja do pobierania ofert pracy
def get_job_offers(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    driver.get(url)
    time.sleep(5)
    load_all_pages(driver, max_clicks=200)

    job_offers = []
    offers = driver.find_elements(By.CLASS_NAME, "posting-list-item")

    for offer in offers:
        try:
            title = offer.find_element(By.CLASS_NAME, "posting-title__position").text.replace("NOWA", "").strip()
            location = re.sub(r"\+\d+", "", offer.find_element(By.CLASS_NAME, "posting-info__location").text).strip()

            salary_from, salary_to, currency = "Brak danych", "", ""

            offer_text = offer.text.split('\n')

            for line in offer_text:
                if "PLN" in line:
                    salary_parts = line.split(" – ")
                    salary_from = salary_parts[0].replace("PLN", "").strip()
                    if len(salary_parts) > 1:
                        salary_to = salary_parts[1].replace("PLN", "").strip()
                    currency = "PLN"

            # Standaryzacja nazw stanowisk
            title = title.lower()
            if "junior" in title or "jr." in title or "jr " in title:
                title = "Junior Java Developer"
            elif "mid" in title or "regular" in title:
                title = "Mid Java Developer"
            elif "senior" in title or "sr." in title or "sr " in title:
                title = "Senior Java Developer"
            else:
                title = "Java Developer"

            # Standaryzacja nazw lokalizacji
            location = location.strip().replace(" ", "").replace("Ł", "L").replace("ł", "l").replace("ą", "a") \
                .replace("ć", "c").replace("ę", "e").replace("ń", "n").replace("ó", "o").replace("ś", "s") \
                .replace("ź", "z").replace("ż", "z")
            location = location.replace("Warsaw", "Warszawa").replace("Krakow", "Kraków").replace("Poznan", "Poznań")
            if "," in location:
                continue

            # Dodanie oferty do listy
            if salary_from != "Brak danych" and currency == "PLN":
                job_offers.append({
                    "Tytuł": title,
                    "Lokalizacja": location.capitalize(),
                    f"Wynagrodzenie od ({currency})": salary_from,
                    f"Wynagrodzenie do ({currency})": salary_to
                })
        except Exception as e:
            print("Błąd podczas przetwarzania oferty:", str(e))
            continue

    driver.quit()
    return job_offers

# Usunięcie poprzedniego pliku CSV
csv_filename = "nofluffjobs_offers.csv"
if os.path.exists(csv_filename):
    os.remove(csv_filename)

# Pobranie danych
data = get_job_offers("https://nofluffjobs.com/pl/Java")

df = pd.DataFrame(data)
df.to_csv(csv_filename, index=False)
print("Dane zapisane do", csv_filename)
