from pathlib import Path
import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = SRC_DIR / "data"

RACES_DIR = DATA_DIR / "processed" / "Races"
OUTPUT_DIR = DATA_DIR / "processed" / "london"

FILES = [
    "london_2021_elite_sample.csv",
    "london_2021_mass_sample.csv",
    "london_2022_elite_sample.csv",
    "london_2022_mass_sample.csv",
    "london_2023_elite_sample.csv",
    "london_2023_mass_sample.csv",
    "london_2024_elite_sample.csv",
    "london_2024_mass_sample.csv",
    "london_2025_elite_sample.csv",
    "london_2025_mass_sample.csv",
]

def load_race_samples():
    dfs = []

    for filename in FILES:
        file_path = RACES_DIR / filename

        if not file_path.exists():
            print(f"No existe: {file_path}")
            continue

        print(f"Cargando {filename}")
        df = pd.read_csv(file_path)

        # Normalizar columnas
        df.columns = [col.strip().lower() for col in df.columns]

        # Asegurar year
        if "year" not in df.columns:
            year = int(filename.split("_")[1])
            df["year"] = year

        # Asegurar category
        if "category" not in df.columns:
            if "mass" in filename.lower():
                df["category"] = "mass"
            elif "elite" in filename.lower():
                df["category"] = "elite"

        dfs.append(df)

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)

def clean_races_dataset(df):
    df = df.copy()

    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")
        df = df.dropna(subset=["year"])
        df["year"] = df["year"].astype(int)

    text_cols = ["name", "club", "category", "category_runner", "event"]
    for col in text_cols:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    if "runner_number" in df.columns:
        df["runner_number"] = df["runner_number"].astype(str).str.strip()

    if {"year", "category", "runner_number"}.issubset(df.columns):
        df = df.drop_duplicates(subset=["year", "category", "runner_number"])
    else:
        df = df.drop_duplicates()

    return df

if __name__ == "__main__":
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df_races = load_race_samples()
    df_races = clean_races_dataset(df_races)

    output_path = OUTPUT_DIR / "london_all_years_combined.csv"
    df_races.to_csv(output_path, index=False)

    print("\nDataset de carreras generado.")
    print(df_races.head())
    print(f"\nFilas totales: {len(df_races)}")
    print(f"Guardado en: {output_path}")