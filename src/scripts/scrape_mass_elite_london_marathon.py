from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup

import re

def scrape_london_results_page(url, year, category="mass"):
    response = requests.get(url, timeout=20)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Sacamos todas las líneas limpias
    lines = [line.strip() for line in soup.get_text("\n").split("\n")]
    lines = [line for line in lines if line]

    rows_data = []

    i = 0
    while i < len(lines):
        line = lines[i]

        # Detectamos una línea de nombre: suele llevar coma y país entre paréntesis
        # Ejemplo: "Abdisa, Arien Ginanjar (INA)"
        if "," in line and "(" in line and ")" in line:
            try:
                name = line

                # Las 3 líneas anteriores suelen ser:
                # place_overall, place_gender, place_category
                place_overall = lines[i - 3] if i >= 3 else None
                place_gender = lines[i - 2] if i >= 2 else None
                place_category = lines[i - 1] if i >= 1 else None

                # Luego buscamos los campos siguientes
                club = None
                runner_number = None
                runner_category = None
                event = None
                half = None
                finish = None

                j = i + 1
                limit = min(i + 20, len(lines))  # miramos unas líneas después del nombre

                while j < limit:
                    if lines[j] == "Club" and j + 1 < len(lines):
                        club = lines[j + 1]
                    elif lines[j] == "Runner Number" and j + 1 < len(lines):
                        runner_number = lines[j + 1]
                    elif lines[j] == "Category" and j + 1 < len(lines):
                        runner_category = lines[j + 1]
                    elif lines[j] == "Event" and j + 1 < len(lines):
                        event = lines[j + 1]
                    elif lines[j] == "Half" and j + 1 < len(lines):
                        half = lines[j + 1]
                    elif lines[j] == "Finish" and j + 1 < len(lines):
                        finish = lines[j + 1]

                    # Cuando ya tenemos dorsal y finish, ese bloque casi seguro está completo
                    if runner_number is not None and finish is not None:
                        break

                    j += 1

                rows_data.append({
                    "place_overall": place_overall,
                    "place_gender": place_gender,
                    "place_category": place_category,
                    "name": name,
                    "club": club,
                    "runner_number": runner_number,
                    "category_runner": runner_category,
                    "event": event,
                    "half": half,
                    "finish": finish,
                    "year": year,
                    "category": category
                })

            except Exception as e:
                print(f"Error procesando bloque cerca de '{line}': {e}")

        i += 1

    df = pd.DataFrame(rows_data)

    # Quitamos filas basura: por ejemplo, encabezados o líneas raras
    if not df.empty:
        df = df[df["runner_number"].notna()]
        df = df[df["event"].isin(["Mass", "MAS", "mass"]) | df["event"].notna()]

    print(f"Filas útiles extraídas: {len(df)}")
    return df

def save_page_csv(df, year, page_num, category="mass"):
    folder = Path(f"src/data/raw/london/{year}/{category}_pages")
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"london_{year}_{category}_page_{page_num}.csv"
    df.to_csv(file_path, index=False)

def clean_mass_df(df):
    df = df.copy()
    df = df.dropna(how="all")

    if "runner_number" in df.columns:
        df = df.drop_duplicates(subset="runner_number")
        df = df[df["runner_number"].astype(str).str.isdigit()]

    return df

def save_combined_raw(df, year, category="mass"):
    file_path = f"src/data/raw/london/{year}/london_{year}_{category}_combined.csv"
    df.to_csv(file_path, index=False)

def sample_mass_runners(df, n=100, random_state=42):
    if len(df) < n:
        print(f"Solo hay {len(df)} filas, se devuelve todo.")
        return df.copy()

    return df.sample(n=n, random_state=random_state)

def save_processed_sample(df, year, category="mass"):
    folder = Path("src/data/processed/london")
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"london_{year}_{category}_sample.csv"
    df.to_csv(file_path, index=False)

def scrape_multiple_mass_pages(urls, year):
    dfs = []

    for i, url in enumerate(urls, start=1):
        try:
            print(f"Scrapeando página {i}")
            df_page = scrape_london_results_page(url, year, category="mass")
            save_page_csv(df_page, year, i, category="mass")
            dfs.append(df_page)
        except Exception as e:
            print(f"Error en página {i}: {e}")

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)

if __name__ == "__main__":

    urls_mass_by_year = {
        2025: [
            "https://results.tcslondonmarathon.com/2025/?page=3&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2025/?page=1983&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2025/?page=255&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2025/?page=1033&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2025/?page=660&event=MAS&pid=search&pidp=start"
        ],
        2024: [
            "https://results.tcslondonmarathon.com/2024/?page=5&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2024/?page=58&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2024/?page=333&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2024/?page=957&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2024/?page=1788&event=MAS&pid=search&pidp=start",
        ],
        2023: [
            "https://results.tcslondonmarathon.com/2023/?page=13&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2023/?page=88&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2023/?page=500&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2023/?page=711&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2023/?page=1299&event=MAS&pid=search&pidp=start",
        ],
        2022: [
            "https://results.tcslondonmarathon.com/2022/?page=12&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2022/?page=25&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2022/?page=188&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2022/?page=442&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2022/?page=1543&event=MAS&pid=search&pidp=start",
        ],
        2021: [
            "https://results.tcslondonmarathon.com/2021/?page=481&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2021/?page=9&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2021/?page=14&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2021/?page=77&event=MAS&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2021/?page=759&event=MAS&pid=search&pidp=start",
        ],
    }

    urls_elite_by_year = {
        2025: [
            "https://results.tcslondonmarathon.com/2025/?pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2025/?page=2&event=ELIT&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2025/?page=3&event=ELIT&pid=search&pidp=start",
        ],
        2024: [
            "https://results.tcslondonmarathon.com/2024/?pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2024/?page=2&event=ELIT&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2024/?page=3&event=ELIT&pid=search&pidp=start",
        ],
        2023: [
            "https://results.tcslondonmarathon.com/2023/?pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2023/?page=2&event=ELIT&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2023/?page=3&event=ELIT&pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2023/?page=4&event=ELIT&pid=search&pidp=start",
        ],
        2022: [
            "https://results.tcslondonmarathon.com/2022/?pid=search&pidp=start",
            "https://results.tcslondonmarathon.com/2022/?page=2&event=ELIT&pid=search&pidp=start",
        ],
        2021: [
            "https://results.tcslondonmarathon.com/2021/?pid=search",
            "https://results.tcslondonmarathon.com/2021/?page=2&event=ELIT&pid=search",
        ],

    }

    # MASS
    for year, urls in urls_mass_by_year.items():

        if not all(url.startswith("http") for url in urls):
            print(f"⚠️ MASS {year}: URLs pendientes, se salta")
            continue

        print(f"\n===== PROCESANDO MASS {year} =====")

        df_mass = scrape_multiple_mass_pages(urls, year)
        df_mass = clean_mass_df(df_mass)

        save_combined_raw(df_mass, year, category="mass")

        df_mass_sample = sample_mass_runners(df_mass, n=100)
        save_processed_sample(df_mass_sample, year, category="mass")

    # ELITE
    for year, urls in urls_elite_by_year.items():

        if not all(url.startswith("http") for url in urls):
            print(f"⚠️ ELITE {year}: URLs pendientes, se salta")
            continue

        print(f"\n===== PROCESANDO ELITE {year} =====")

        df_elite = scrape_multiple_mass_pages(urls, year)
        df_elite = clean_mass_df(df_elite)

        save_combined_raw(df_elite, year, category="elite")
        save_processed_sample(df_elite, year, category="elite")

    print("\n🔥 TODO COMPLETADO 🔥")