from pathlib import Path
import pandas as pd

# 📁 Rutas
SRC_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = SRC_DIR / "data"

RACES_PATH = DATA_DIR / "processed" / "london" / "london_all_years_combined.csv"
WEATHER_PATH = DATA_DIR / "processed" / "weather" / "london_weather_summary_2021_2025.csv"
OUTPUT_DIR = DATA_DIR / "processed" / "final"

# 🧠 Función para convertir tiempo
def time_to_seconds(t):
    try:
        h, m, s = map(int, str(t).split(":"))
        return h * 3600 + m * 60 + s
    except:
        return None

if __name__ == "__main__":

    print("Cargando datasets...")

    df = pd.read_csv(RACES_PATH)
    df_weather = pd.read_csv(WEATHER_PATH)

    # 🔧 1. Arreglar category
    print("Corrigiendo category...")
    df["category"] = (
        df["event"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # 🔧 2. Convertir tiempos
    print("Convirtiendo tiempos...")
    df["finish_seconds"] = df["finish"].apply(time_to_seconds)

    # 🔧 3. Crear ritmo
    print("Calculando pace...")
    df["pace_min_km"] = (df["finish_seconds"] / 60) / 42.195

    # 🔧 4. Merge con clima
    print("Uniendo con clima...")
    df_final = df.merge(df_weather, on="year", how="left")

    # 🧼 LIMPIEZA FINAL
    print("Limpieza final...")

    # Renombrar columnas
    df_final = df_final.rename(columns={
        "year": "Year",
        "category": "Category",
        "name": "Name",
        "runner_number": "Runner_number",
        "finish": "Finish",
        "finish_seconds": "Finish_seconds",
        "pace_min_km": "Pace_min_km",
        "category_runner": "Age_group",
        "temp_mean": "Temp_mean",
        "temp_min": "Temp_min",
        "temp_max": "Temp_max",
        "apparent_temp_mean": "Apparent_temp_mean",
        "humidity_mean": "Humidity_mean",
        "precipitation_sum": "Precipitation_sum",
        "wind_speed_mean": "Wind_speed_mean",
        "wind_speed_max": "Wind_speed_max"
    })

    # Limpiar Category
    if "Category" in df_final.columns:
        df_final["Category"] = df_final["Category"].replace({
            "mass": "Mass",
            "elite": "Elite"
        })

    # Limpiar Age_group
    if "Age_group" in df_final.columns:
        df_final["Age_group"] = df_final["Age_group"].astype(str).str.strip()
        df_final["Age_group"] = df_final["Age_group"].replace("–", pd.NA)
        df_final["Age_group"] = df_final["Age_group"].replace("-", pd.NA)
        df_final["Age_group"] = df_final["Age_group"].replace("nan", pd.NA)

        age_order = [
            "18-39",
            "40-44",
            "45-49",
            "50-54",
            "55-59",
            "60-64",
            "65-69",
            "70-74",
            "75-79"
        ]

        # Primero dejar fuera los valores no válidos
        valid_age_mask = df_final["Age_group"].isin(age_order) | df_final["Age_group"].isna()
        df_final.loc[~valid_age_mask, "Age_group"] = pd.NA

        df_final["Age_group"] = pd.Categorical(
            df_final["Age_group"],
            categories=age_order,
            ordered=True
        )

    # Quitar filas sin tiempo
    if "Finish_seconds" in df_final.columns:
        df_final = df_final.dropna(subset=["Finish_seconds"])

    # Ranking
    if {"Year", "Category", "Finish_seconds"}.issubset(df_final.columns):
        df_final["Rank_year_category"] = (
            df_final.groupby(["Year", "Category"])["Finish_seconds"]
            .rank(method="first")
            .astype("Int64")
        )

    # Redondear floats
    float_cols = df_final.select_dtypes(include=["float64", "float32"]).columns
    df_final[float_cols] = df_final[float_cols].round(2)

    # Reordenar columnas
    column_order = [
        "Year",
        "Category",
        "Rank_year_category",
        "Name",
        "Runner_number",
        "Age_group",
        "Finish",
        "Finish_seconds",
        "Pace_min_km",
        "Temp_mean",
        "Temp_min",
        "Temp_max",
        "Apparent_temp_mean",
        "Humidity_mean",
        "Precipitation_sum",
        "Wind_speed_mean",
        "Wind_speed_max"
    ]

    df_final = df_final[[col for col in column_order if col in df_final.columns]]

    # Ordenar filas
    sort_cols = [col for col in ["Year", "Category", "Finish_seconds"] if col in df_final.columns]
    if sort_cols:
        df_final = df_final.sort_values(sort_cols).reset_index(drop=True)

    # 📁 Guardar
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = OUTPUT_DIR / "london_marathon_final_dataset.csv"
    df_final.to_csv(output_path, index=False)

    print("\n🔥 DATASET FINAL GENERADO 🔥")
    print(df_final.head())
    print(f"\nFilas: {len(df_final)}")
    print(f"Guardado en: {output_path}")