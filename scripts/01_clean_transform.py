"""
Etapa 2 — Limpieza y transformacion
======================================
Unifica Magnificent 7 (dataset principal, con todas las metricas) y el
panorama tech extendido (solo market cap/pais/sector) en tablas limpias,
mas feature engineering: ratio capex/market cap, categoria de rendimiento,
ranking.
"""
import sys, os
sys.path.insert(0, "/home/claude/bigtech_portfolio/data/raw")
import bigtech_2026_data as raw
import pandas as pd

OUT_DIR = "/home/claude/bigtech_portfolio/data/processed"
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# TABLA PRINCIPAL: Magnificent 7 con todas las metricas
# ============================================================
m7 = pd.DataFrame(raw.MAGNIFICENT_7, columns=[
    "ticker", "nombre", "precio", "market_cap_t", "var_1d_pct", "ytd_pct",
    "sector", "pais", "capex_ia_2026_b"
])
m7["es_magnificent7"] = True

# ratio capex / market cap (en %): cuanto "apuestan" relativo a su tamaño
m7["capex_sobre_mcap_pct"] = (m7["capex_ia_2026_b"] / (m7["market_cap_t"] * 1000) * 100).round(2)

# categoria de rendimiento
def categoria(ytd):
    if ytd >= 15: return "Fuerte alza"
    if ytd >= 0: return "Alza moderada"
    if ytd >= -15: return "Baja moderada"
    return "Fuerte baja"
m7["categoria_rendimiento"] = m7["ytd_pct"].apply(categoria)

m7["ranking_market_cap"] = m7["market_cap_t"].rank(ascending=False).astype(int)
m7["ranking_ytd"] = m7["ytd_pct"].rank(ascending=False).astype(int)

# ============================================================
# TABLA EXTENDIDA: panorama tech global (10 empresas adicionales)
# ============================================================
ext = pd.DataFrame(raw.EXTENDED_TECH, columns=["nombre", "ticker", "market_cap_t", "pais", "sector"])
ext["es_magnificent7"] = False
for col in ["precio", "var_1d_pct", "ytd_pct", "capex_ia_2026_b", "capex_sobre_mcap_pct",
            "categoria_rendimiento", "ranking_ytd"]:
    ext[col] = None
ext["ranking_market_cap"] = None  # se recalcula abajo sobre el universo completo

# ============================================================
# UNIVERSO COMPLETO (17 empresas) — para vistas de "panorama global"
# ============================================================
cols_order = ["ticker", "nombre", "precio", "market_cap_t", "var_1d_pct", "ytd_pct",
              "sector", "pais", "capex_ia_2026_b", "capex_sobre_mcap_pct",
              "categoria_rendimiento", "es_magnificent7", "ranking_market_cap", "ranking_ytd"]
universe = pd.concat([m7[cols_order], ext[cols_order]], ignore_index=True)
universe["ranking_market_cap"] = universe["market_cap_t"].rank(ascending=False).astype(int)
universe = universe.sort_values("market_cap_t", ascending=False).reset_index(drop=True)

# guardar
m7.to_csv(f"{OUT_DIR}/magnificent7.csv", index=False)
universe.to_csv(f"{OUT_DIR}/universe.csv", index=False)
universe.to_json(f"{OUT_DIR}/universe.json", orient="records", force_ascii=False)

print(f"Magnificent 7: {len(m7)} filas")
print(f"Universo completo: {len(universe)} filas")
print("\nRanking de market cap (universo completo):")
print(universe[["ranking_market_cap", "nombre", "market_cap_t", "pais"]].head(10).to_string(index=False))
print("\nCapex vs Market Cap (Magnificent 7 con dato de capex):")
print(m7.dropna(subset=["capex_ia_2026_b"])[["nombre", "capex_ia_2026_b", "capex_sobre_mcap_pct", "ytd_pct"]].to_string(index=False))
