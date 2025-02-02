# README - Web Scraping i Analiza Wynagrodzeń dla Java Developerów

## Opis projektu
Projekt polega na pobieraniu ofert pracy dla programistów Java z serwisu NoFluffJobs, analizowaniu wynagrodzeń i prezentowaniu wyników w formie interaktywnego dashboardu.

## Struktura projektu
- `scraper.py` - Skrypt do pobierania danych z NoFluffJobs.
- `nofluffjobs_offers.csv` - Plik CSV zawierający pobrane i przetworzone dane.
- `analysis.py` - Skrypt przeprowadzający analizę danych.
- `dashboard.py` - Aplikacja Streamlit do wizualizacji wyników.

## Instalacja i uruchomienie
1. **Zainstaluj wymagane biblioteki**:
   
   pip install selenium pandas matplotlib streamlit webdriver-manager
  
3. **Uruchom scraper do pobrania danych**:
   
   python scraper.py
   
4. **Uruchom analizę danych**:
  
   python analysis.py
   
5. **Uruchom dashboard Streamlit**:
   
   streamlit run dashboard.py
   

## Szczegóły skryptów
### `scraper.py` (Web Scraping)
Skrypt wykorzystuje Selenium do pobrania ofert pracy. Pobierane są następujące dane:
- Tytuł stanowiska (standaryzowany: `Java Developer`, `Junior Java Developer`, `Mid Java Developer`, `Senior Java Developer`)
- Lokalizacja
- Wynagrodzenie (zakres: `od` - `do` w PLN)

### `analysis.py` (Analiza danych)
Przeprowadzane analizy obejmują:
- Rozkład wynagrodzeń
- Średnie wynagrodzenie w zależności od stanowiska (z poprawioną widocznością nazw na wykresie)
- Średnie wynagrodzenie w zależności od lokalizacji

### `dashboard.py` (Aplikacja Streamlit)
Aplikacja umożliwia:
- Wizualizację rozkładu wynagrodzeń
- Filtrację ofert według lokalizacji
- Analizę średnich wynagrodzeń dla różnych stanowisk (z poprawioną widocznością etykiet na wykresie)

## Źródło danych
Dane pochodzą ze strony [NoFluffJobs](https://nofluffjobs.com/pl/Java).
