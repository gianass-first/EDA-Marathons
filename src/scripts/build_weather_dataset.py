from pathlib import Path
import pandas as pd
import re

SRC_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = SRC_DIR / "data"

RAW_WEATHER_DIR = DATA_DIR / "raw" / "Weather"
PROCESSED_WEATHER_DIR = DATA_DIR / "processed" / "weather"

def summarize_weather_file(file_path, year):
    # Saltamos las filas metadata del principio
    df = pd.read_csv(file_path, skiprows=3)

    # Limpiar nombres de columnas
    df.columns = [col.strip() for col in df.columns]

    # Convertir columnas numéricas
    numeric_cols = [
        "temperature_2m (°C)",
        "relative_humidity_2m (%)",
        "precipitation (mm)",
        "apparent_temperature (°C)",
        "wind_speed_10m (km/h)"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    summary = {
        "year": year,
        "marathon_date": df["time"].iloc[0][:10] if "time" in df.columns and not df.empty else None,
        "temp_mean": df["temperature_2m (°C)"].mean() if "temperature_2m (°C)" in df.columns else None,
        "temp_min": df["temperature_2m (°C)"].min() if "temperature_2m (°C)" in df.columns else None,
        "temp_max": df["temperature_2m (°C)"].max() if "temperature_2m (°C)" in df.columns else None,
        "apparent_temp_mean": df["apparent_temperature (°C)"].mean() if "apparent_temperature (°C)" in df.columns else None,
        "humidity_mean": df["relative_humidity_2m (%)"].mean() if "relative_humidity_2m (%)" in df.columns else None,
        "precipitation_sum": df["precipitation (mm)"].sum() if "precipitation (mm)" in df.columns else None,
        "wind_speed_mean": df["wind_speed_10m (km/h)"].mean() if "wind_speed_10m (km/h)" in df.columns else None,
        "wind_speed_max": df["wind_speed_10m (km/h)"].max() if "wind_speed_10m (km/h)" in df.columns else None,
    }

    return pd.DataFrame([summary])

def extract_year_from_filename(filename):
    match = re.search(r"(20\d{2})", filename)
    if match:
        return int(match.group(1))
    return None

def build_weather_summary():
    dfs = []

    for file_path in sorted(RAW_WEATHER_DIR.glob("*.csv")):
        year = extract_year_from_filename(file_path.name)

        if year is None:
            print(f"No se pudo extraer el año de {file_path.name}, se salta")
            continue

        print(f"Procesando clima {year}: {file_path.name}")

        df_summary = summarize_weather_file(file_path, year)
        dfs.append(df_summary)

    if not dfs:
        return pd.DataFrame()

    df_all = pd.concat(dfs, ignore_index=True)
    df_all = df_all.sort_values("year").reset_index(drop=True)

    return df_all

if __name__ == "__main__":
    PROCESSED_WEATHER_DIR.mkdir(parents=True, exist_ok=True)

    df_weather_summary = build_weather_summary()

    output_path = PROCESSED_WEATHER_DIR / "london_weather_summary_2021_2025.csv"
    df_weather_summary.to_csv(output_path, index=False)

    print("\nResumen climático generado:")
    print(df_weather_summary)
    print(f"\nGuardado en: {output_path}")