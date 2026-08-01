"""
Etapa 6 — Construir el dashboard final
"""
import os, shutil

BASE = "/home/claude/bigtech_portfolio"
TEMPLATE = f"{BASE}/lib/dashboard_template.html"
CHARTJS = f"{BASE}/lib/chart.umd.min.js"
PROC = f"{BASE}/data/processed/"
OUT_DIR = f"{BASE}/outputs"
DOCS_DIR = f"{BASE}/docs"

with open(TEMPLATE, encoding="utf-8") as f:
    html = f.read()
with open(CHARTJS, encoding="utf-8") as f:
    chartjs_lib = f.read()

def load(name):
    with open(PROC + name, encoding="utf-8") as f:
        return f.read()

html = html.replace("__CHARTJS_LIB__", chartjs_lib)
html = html.replace("__M7_JSON__", load("magnificent7_ml.json"))
html = html.replace("__UNIVERSE_JSON__", load("universe.json"))
html = html.replace("__EDA_JSON__", load("eda_results.json"))
html = html.replace("__METRICS_JSON__", load("ml_metrics.json"))

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)
out_path = f"{OUT_DIR}/index.html"
with open(out_path, "w", encoding="utf-8") as f:
    f.write(html)

placeholders = ["__CHARTJS_LIB__","__M7_JSON__","__UNIVERSE_JSON__","__EDA_JSON__","__METRICS_JSON__"]
leftover = [p for p in placeholders if p in html]
size_mb = os.path.getsize(out_path) / (1024*1024)
print(f"Dashboard generado: {out_path} ({size_mb:.2f} MB) — sin resolver: {leftover}")

shutil.copy(out_path, f"{DOCS_DIR}/index.html")
print(f"Copiado a: {DOCS_DIR}/index.html")
