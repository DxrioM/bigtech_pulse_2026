"""
Etapa 8 — Construir dashboard.html en ES y EN
"""
import os, shutil

BASE = "/home/claude/bigtech_portfolio"
TEMPLATE = f"{BASE}/lib/dashboard_template_i18n.html"
CHARTJS = f"{BASE}/lib/chart.umd.min.js"
PROC = f"{BASE}/data/processed/"
OUT_DIR = f"{BASE}/outputs"
DOCS_DIR = f"{BASE}/docs"

with open(TEMPLATE, encoding="utf-8") as f:
    template = f.read()
with open(CHARTJS, encoding="utf-8") as f:
    chartjs_lib = f.read()

def load(name):
    with open(PROC + name, encoding="utf-8") as f:
        return f.read()

CONFIGS = {
    "es": {
        "html_lang": "es",
        "page_title": "Big Tech Pulse — Agosto 2026",
        "og_desc": "El Magnificent 7 analizado con SQL, Python y Machine Learning: rendimiento, gasto en IA, y una correlación que sorprende.",
        "canonical": "https://dxriom.github.io/bigtech_pulse_2026/",
        "m7": "magnificent7_ml.json", "universe": "universe.json",
        "eda": "eda_results.json", "metrics": "ml_metrics.json",
        "out": "index.html",
        "link_es": "index.html", "link_en": "dashboard_en.html",
        "es_active": "active", "en_active": "",
    },
    "en": {
        "html_lang": "en",
        "page_title": "Big Tech Pulse — August 2026",
        "og_desc": "The Magnificent 7 analyzed with SQL, Python and Machine Learning: performance, AI spending, and a surprising correlation.",
        "canonical": "https://dxriom.github.io/bigtech_pulse_2026/dashboard_en.html",
        "m7": "magnificent7_ml_en.json", "universe": "universe_en.json",
        "eda": "eda_results_en.json", "metrics": "ml_metrics_en.json",
        "out": "dashboard_en.html",
        "link_es": "index.html", "link_en": "dashboard_en.html",
        "es_active": "", "en_active": "active",
    },
}

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

for lang, cfg in CONFIGS.items():
    html = template
    html = html.replace("__CHARTJS_LIB__", chartjs_lib)
    html = html.replace("__HTML_LANG__", cfg["html_lang"])
    html = html.replace("__PAGE_TITLE__", cfg["page_title"])
    html = html.replace("__OG_DESC__", cfg["og_desc"])
    html = html.replace("__CANONICAL_URL__", cfg["canonical"])
    html = html.replace("__LANG__", lang)
    html = html.replace("__LINK_ES__", cfg["link_es"])
    html = html.replace("__LINK_EN__", cfg["link_en"])
    html = html.replace("__ES_ACTIVE__", cfg["es_active"])
    html = html.replace("__EN_ACTIVE__", cfg["en_active"])
    html = html.replace("__M7_JSON__", load(cfg["m7"]))
    html = html.replace("__UNIVERSE_JSON__", load(cfg["universe"]))
    html = html.replace("__EDA_JSON__", load(cfg["eda"]))
    html = html.replace("__METRICS_JSON__", load(cfg["metrics"]))

    out_path = f"{OUT_DIR}/{cfg['out']}"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    placeholders = ["__CHARTJS_LIB__","__HTML_LANG__","__PAGE_TITLE__","__OG_DESC__","__CANONICAL_URL__",
                     "__LANG__","__LINK_ES__","__LINK_EN__","__ES_ACTIVE__","__EN_ACTIVE__",
                     "__M7_JSON__","__UNIVERSE_JSON__","__EDA_JSON__","__METRICS_JSON__"]
    leftover = [p for p in placeholders if p in html]
    size_mb = os.path.getsize(out_path) / (1024*1024)
    print(f"{lang}: {out_path} ({size_mb:.2f} MB) — sin resolver: {leftover}")
    shutil.copy(out_path, f"{DOCS_DIR}/{cfg['out']}")

print("Copiados a docs/")
