# 📈 Big Tech Pulse — Markets Data Science Portfolio

**🌐 [Leer esto en Español](README.md)**

An analysis of the "Magnificent 7" (Apple, Microsoft, Alphabet, Amazon, Nvidia, Meta, Tesla) with SQL, Python and Machine Learning — price, market cap, AI spending, and an interactive dashboard with real cross-filtering, in an Apple-inspired minimalist design.

**🔴 Demo:** [Español](https://dxriom.github.io/bigtech_pulse_2026/) · [English](https://dxriom.github.io/bigtech_pulse_2026/dashboard_en.html)

**📁 Repository:** [github.com/DxrioM/bigtech_pulse_2026](https://github.com/DxrioM/bigtech_pulse_2026)

---

## The core finding

Does spending more on AI guarantee better stock returns? Based on the available data, the answer is **no** — if anything, it's close to the opposite. Comparing AI infrastructure spending (as % of market cap) against 2026 YTD return for the 5 companies that report that figure:

| Company | AI Capex / Market Cap | YTD Return |
|---|---|---|
| Apple | 0.3% | **+23.9%** |
| Alphabet | 4.2% | +4.3% |
| Microsoft | 5.7% | -10.0% |
| Amazon | 6.9% | +0.3% |
| Meta | 8.9% | **-19.5%** |

Pearson correlation: **r = -0.94** (p = 0.019). Apple, which is betting the least relative to its size, is the only one with a strong gain; Meta, which is betting the most, has had the worst year. With only 5 data points this is an observation, not a law — but it's the kind of pattern worth pointing out, not hiding.

## Why this project is different from the previous ones

Unlike the World Cup (a rich, already-closed source) or Spotify (an already-packaged dataset), here **there is no single source** — market data changes constantly. Every figure was collected and cross-checked against multiple sources (Fast Company, MarketCapLens, Disfold, Tom's Hardware, Yahoo Finance, CNBC) and documented as **a snapshot of a specific moment** (Jul 28 – Aug 1, 2026), not a live feed. That distinction — snapshot vs. real-time — is a real data-design decision, and it's communicated explicitly in the dashboard.

## The design: Apple-style minimalism + real cross-filtering

- **Palette and typography**: Apple's actual system colors (`#1D1D1F`, `#F5F5F7`, `#0071E3`, adapted `#34C759`/`#FF3B30`), `-apple-system` typography with `Inter` as the web fallback
- **A single high-impact dark section** (the correlation finding) — the rest of the site stays deliberately restrained, with no excess decoration
- **Real cross-filtering**: selecting a company (from the grid, the bar chart, the scatter plot, or the ranking) updates *all* the other views at once — these aren't isolated filters, they're linked views. Validated with automated tests simulating real clicks.

## Project structure

```
bigtech_portfolio/
├── data/
│   ├── raw/bigtech_2026_data.py     # verified raw data (17 companies)
│   └── processed/                    # clean CSV/JSON + SQLite database
├── sql/
│   ├── 01_schema.sql
│   └── 02_eda_queries.sql            # 6 exploratory analysis queries
├── scripts/
│   ├── 01_clean_transform.py         # cleaning + feature engineering
│   ├── 02_load_db.py                 # load into SQLite
│   ├── 03_run_eda.py                 # runs the SQL queries → JSON
│   ├── 04_ml_analysis.py             # correlation, KMeans, Momentum Score
│   ├── 07_translate_exports.py       # generates English category labels
│   └── 08_build_dashboards.py        # injects data + Chart.js into the ES/EN templates
├── lib/
│   ├── chart.umd.min.js
│   └── dashboard_template_i18n.html  # bilingual template (i18n via data-i18n)
├── docs/
│   ├── index.html                    # ⭐ final product in Spanish
│   └── dashboard_en.html             # ⭐ final product in English
├── README.md                         # this file, in Spanish
└── README.en.md                      # this file, in English
```

## How to reproduce it

```bash
pip install pandas numpy scikit-learn scipy
cd scripts
python3 01_clean_transform.py
python3 02_load_db.py
python3 03_run_eda.py
python3 04_ml_analysis.py
python3 07_translate_exports.py
python3 08_build_dashboards.py
cp ../outputs/*.html ../docs/
```

## Momentum Score methodology

Composite score (0-100) for the Magnificent 7 ranking:
- **45%** YTD return
- **15%** latest daily change
- **15%** size (market cap)
- **25%** capex efficiency (lower spend relative to size = better score; companies without a reported figure receive a neutral score)

## Tech stack

`Python` · `pandas` · `scikit-learn` (KMeans, PCA) · `SciPy` (Pearson correlation) · `SQL` · `SQLite` · `HTML/CSS/JS` · `Chart.js`

---

*Data collected and verified from public sources during the week of Jul 28 – Aug 1, 2026. Markets change constantly — these values are a snapshot, not live data.*
