from pathlib import Path
import pandas as pd

SRC_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = SRC_DIR / "data"

RAW_PATH = DATA_DIR / "external" / "majors_2025_manual.csv"
OUTPUT_DIR = DATA_DIR / "processed" / "majors"

def time_to_seconds(t):
    try:
        h, m, s = map(int, str(t).split(":"))
        return h * 3600 + m * 60 + s
    except:
        return None

if __name__ == "__main__":

    print("Cargando dataset manual...")
    df = pd.read_csv(RAW_PATH)

    # 1. Limpiar nombres de columnas
    df.columns = [col.strip().lower() for col in df.columns]

    # 2. Renombrar columnas a un formato más limpio y consistente
    df = df.rename(columns={
        "marathon": "Marathon",
        "city": "City",
        "country": "Country",
        "date": "Date",
        "year": "Year",
        "elite_time_winner_m": "Elite_time_winner_m",
        "elite_time_winner_f": "Elite_time_winner_f",
        "average_men_time": "Average_men_time",
        "average_women_time": "Average_women_time",
        "participants": "Participants",
        "finishers": "Finishers",
        "completion_rate": "Completion_rate",
        "temperature_start_c": "Temperature_start_c",
        "humidity_in_%": "Humidity_pct",
        "wind_speed_kmh": "Wind_speed_kmh",
        "weather_notes": "Weather_notes",
        "elevation_gain_m": "Elevation_gain_m",
        "course_type": "Course_type",
        "applications": "Applications",
        "source": "Source",
        "notes": "Notes"
    })

    # 3. Tipos numéricos
    numeric_cols = [
        "Year",
        "Participants",
        "Finishers",
        "Completion_rate",
        "Temperature_start_c",
        "Humidity_pct",
        "Wind_speed_kmh",
        "Elevation_gain_m",
        "Applications"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 4. Convertir tiempos a segundos
    time_cols = [
        "Elite_time_winner_m",
        "Elite_time_winner_f",
        "Average_men_time",
        "Average_women_time"
    ]

    for col in time_cols:
        if col in df.columns:
            df[f"{col}_seconds"] = df[col].apply(time_to_seconds)

    # 5. Crear variables de pace
    marathon_km = 42.195

    if "Elite_time_winner_m_seconds" in df.columns:
        df["Pace_elite_m"] = (df["Elite_time_winner_m_seconds"] / 60) / marathon_km

    if "Elite_time_winner_f_seconds" in df.columns:
        df["Pace_elite_f"] = (df["Elite_time_winner_f_seconds"] / 60) / marathon_km

    if "Average_men_time_seconds" in df.columns:
        df["Pace_avg_men"] = (df["Average_men_time_seconds"] / 60) / marathon_km

    if "Average_women_time_seconds" in df.columns:
        df["Pace_avg_women"] = (df["Average_women_time_seconds"] / 60) / marathon_km

    # 6. Redondear floats
    float_cols = df.select_dtypes(include=["float64", "float32"]).columns
    df[float_cols] = df[float_cols].round(2)

    # 7. Ordenar columnas
    column_order = [
        "Marathon",
        "City",
        "Country",
        "Date",
        "Year",
        "Elite_time_winner_m",
        "Elite_time_winner_m_seconds",
        "Pace_elite_m",
        "Elite_time_winner_f",
        "Elite_time_winner_f_seconds",
        "Pace_elite_f",
        "Average_men_time",
        "Average_men_time_seconds",
        "Pace_avg_men",
        "Average_women_time",
        "Average_women_time_seconds",
        "Pace_avg_women",
        "Participants",
        "Finishers",
        "Completion_rate",
        "Temperature_start_c",
        "Humidity_pct",
        "Wind_speed_kmh",
        "Elevation_gain_m",
        "Weather_notes",
        "Course_type",
        "Applications",
        "Source",
        "Notes"
    ]

    df = df[[col for col in column_order if col in df.columns]]

    # 8. Ordenar filas
    df = df.sort_values(["Year", "Marathon"]).reset_index(drop=True)

    # 9. Guardar
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "majors_cleaned.csv"
    df.to_csv(output_path, index=False)

    print("\nDataset MAJORS limpio generado")
    print(df.head())
    print(f"\nColumnas: {df.columns.tolist()}")
    print(f"Guardado en: {output_path}")