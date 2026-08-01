"""
Etapa 7 — Generar variantes en ingles de los JSON exportados
================================================================
Traduce solo las etiquetas categoricas propias (sector, pais, categoria
de rendimiento, nombre de cluster). Nombres de empresas/tickers no se
tocan (son datos, no UI).
"""
import json

PROC = "/home/claude/bigtech_portfolio/data/processed/"

SECTOR_ES_EN = {
    "Semiconductores": "Semiconductors",
    "Hardware de consumo": "Consumer hardware",
    "Software / Internet": "Software / Internet",
    "Software / Cloud": "Software / Cloud",
    "E-commerce / Cloud": "E-commerce / Cloud",
    "Automotriz / Energia": "Automotive / Energy",
    "Electronica de consumo": "Consumer electronics",
    "Software / Infraestructura": "Software / Infrastructure",
    "Equipos de semiconductores": "Semiconductor equipment",
    "Equipos de comunicacion": "Communication equipment",
}
PAIS_ES_EN = {
    "USA": "USA",
    "Taiwan": "Taiwan",
    "Corea del Sur": "South Korea",
    "Paises Bajos": "Netherlands",
}
CATEGORIA_ES_EN = {
    "Fuerte alza": "Strong gain",
    "Alza moderada": "Moderate gain",
    "Baja moderada": "Moderate loss",
    "Fuerte baja": "Strong loss",
}
CLUSTER_ES_EN = {
    "Momentum positivo": "Positive momentum",
    "Zona neutral": "Neutral zone",
    "Bajo presion": "Under pressure",
}

def tr(d, v):
    return d.get(v, v) if v else v

# ---------- magnificent7_ml.json ----------
m7 = json.load(open(PROC + "magnificent7_ml.json", encoding="utf-8"))
for row in m7:
    row["sector"] = tr(SECTOR_ES_EN, row["sector"])
    row["pais"] = tr(PAIS_ES_EN, row["pais"])
    row["categoria_rendimiento"] = tr(CATEGORIA_ES_EN, row["categoria_rendimiento"])
    row["cluster_name"] = tr(CLUSTER_ES_EN, row["cluster_name"])
json.dump(m7, open(PROC + "magnificent7_ml_en.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- universe.json ----------
universe = json.load(open(PROC + "universe.json", encoding="utf-8"))
for row in universe:
    row["sector"] = tr(SECTOR_ES_EN, row["sector"])
    row["pais"] = tr(PAIS_ES_EN, row["pais"])
    row["categoria_rendimiento"] = tr(CATEGORIA_ES_EN, row.get("categoria_rendimiento"))
json.dump(universe, open(PROC + "universe_en.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- eda_results.json ----------
eda = json.load(open(PROC + "eda_results.json", encoding="utf-8"))
eda_en = json.loads(json.dumps(eda))
for row in eda_en["mcap_por_sector"]:
    row["sector"] = tr(SECTOR_ES_EN, row["sector"])
for row in eda_en["mcap_por_pais"]:
    row["pais"] = tr(PAIS_ES_EN, row["pais"])
for row in eda_en["ranking_ytd_m7"]:
    row["categoria_rendimiento"] = tr(CATEGORIA_ES_EN, row["categoria_rendimiento"])
for row in eda_en["capex_vs_rendimiento"]:
    pass  # solo nombres/numeros, sin traducir
for row in eda_en["distribucion_categorias"]:
    row["categoria_rendimiento"] = tr(CATEGORIA_ES_EN, row["categoria_rendimiento"])
for row in eda_en["top10_mcap"]:
    row["sector"] = tr(SECTOR_ES_EN, row["sector"])
    row["pais"] = tr(PAIS_ES_EN, row["pais"])
json.dump(eda_en, open(PROC + "eda_results_en.json", "w", encoding="utf-8"), ensure_ascii=False)

# ---------- ml_metrics.json ----------
metrics = json.load(open(PROC + "ml_metrics.json", encoding="utf-8"))
metrics["cluster_profiles"] = {tr(CLUSTER_ES_EN, k): v for k, v in metrics["cluster_profiles"].items()}
json.dump(metrics, open(PROC + "ml_metrics_en.json", "w", encoding="utf-8"), ensure_ascii=False)

print("Variantes en ingles generadas:")
import os
for f in ["magnificent7_ml_en.json", "universe_en.json", "eda_results_en.json", "ml_metrics_en.json"]:
    print(" ", f, os.path.getsize(PROC+f), "bytes")
