"""
Etapa 1 — Datos crudos: Big Tech Pulse 2026
==============================================
Fuentes: Fast Company (28 jul 2026, YTD returns Magnificent 7), MarketCapLens
(31 jul 2026, market cap/precio/var. diaria), Disfold (market cap empresas tech
adicionales), Tom's Hardware / Value Add VC / Yahoo Finance / CNBC (capex IA
2026, earnings Q1 2026 de 5 hyperscalers).

Snapshot: semana del 28 jul - 1 ago 2026. Los mercados cambian constantemente;
esto es una fotografia de un momento especifico, documentada como tal.
"""

# ============================================================
# MAGNIFICENT 7 — dataset principal (todas las metricas)
# ============================================================
# ticker, nombre, precio, market_cap_T (trillones USD), var_1d_pct, ytd_pct,
# sector, pais, capex_ia_2026_B (billones USD, None si no reportado en la
# comparativa de 5 hyperscalers)
MAGNIFICENT_7 = [
    ("NVDA", "NVIDIA Corporation", 197.95, 4.79, 1.47, 5.37, "Semiconductores", "USA", None),
    ("AAPL", "Apple Inc.", 302.98, 4.45, -9.21, 23.93, "Hardware de consumo", "USA", 13.5),
    ("GOOGL", "Alphabet Inc.", 353.23, 4.27, 5.90, 4.33, "Software / Internet", "USA", 180.0),
    ("MSFT", "Microsoft Corporation", 451.28, 3.35, 0.08, -10.03, "Software / Cloud", "USA", 190.0),
    ("AMZN", "Amazon.com, Inc.", 271.10, 2.92, 15.06, 0.25, "E-commerce / Cloud", "USA", 200.0),
    ("META", "Meta Platforms, Inc.", 551.79, 1.40, 2.31, -19.54, "Software / Internet", "USA", 125.0),
    ("TSLA", "Tesla, Inc.", 308.11, 1.22, -0.29, -31.24, "Automotriz / Energia", "USA", None),
]

# ============================================================
# PANORAMA TECH GLOBAL — empresas adicionales (market cap + contexto)
# no se tiene YTD/capex desglosado para este segundo grupo
# ============================================================
# nombre, ticker, market_cap_T, pais, sector
EXTENDED_TECH = [
    ("Broadcom Inc.", "AVGO", 1.648, "USA", "Semiconductores"),
    ("Taiwan Semiconductor Mfg.", "TSM", 1.312, "Taiwan", "Semiconductores"),
    ("Samsung Electronics", "005930.KS", 0.596, "Corea del Sur", "Electronica de consumo"),
    ("Oracle Corporation", "ORCL", 0.562, "USA", "Software / Infraestructura"),
    ("ASML Holding N.V.", "ASML", 0.450, "Paises Bajos", "Equipos de semiconductores"),
    ("Palantir Technologies", "PLTR", 0.400, "USA", "Software / Infraestructura"),
    ("Advanced Micro Devices", "AMD", 0.364, "USA", "Semiconductores"),
    ("Micron Technology", "MU", 0.355, "USA", "Semiconductores"),
    ("Cisco Systems", "CSCO", 0.300, "USA", "Equipos de comunicacion"),
    ("Intel Corporation", "INTC", 0.188, "USA", "Semiconductores"),
]

SNAPSHOT_INFO = {
    "fecha_snapshot": "2026-08-01",
    "fuente_principal": "Fast Company (YTD, 28 jul 2026) + MarketCapLens (market cap, 31 jul 2026)",
    "nota": "Los mercados cambian diariamente; estos valores son una fotografia de finales de julio 2026, no datos en vivo.",
}

if __name__ == "__main__":
    print(f"Magnificent 7: {len(MAGNIFICENT_7)} empresas")
    print(f"Panorama tech extendido: {len(EXTENDED_TECH)} empresas")
    total_mcap_m7 = sum(x[3] for x in MAGNIFICENT_7)
    print(f"Market cap combinado Magnificent 7: ${total_mcap_m7:.2f}T")
    total_capex = sum(x[8] for x in MAGNIFICENT_7 if x[8])
    print(f"Capex IA 2026 combinado (5 empresas reportadas): ${total_capex:.1f}B")
