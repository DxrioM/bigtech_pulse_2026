# 📈 Big Tech Pulse — Portafolio de Data Science de Mercados

Análisis del "Magnificent 7" (Apple, Microsoft, Alphabet, Amazon, Nvidia, Meta, Tesla) con SQL, Python y Machine Learning — precio, market cap, gasto en IA, y un dashboard interactivo con cross-filtering real, en un diseño minimalista inspirado en Apple.

**🔴 Demo:** [Español](https://dxriom.github.io/bigtech_pulse_2026/) · [English](https://dxriom.github.io/bigtech_pulse_2026/dashboard_en.html)

**📁 Repositorio:** [github.com/DxrioM/bigtech_pulse_2026](https://github.com/DxrioM/bigtech_pulse_2026)

---

## El hallazgo central

¿Gastar más en IA garantiza mejor rendimiento en bolsa? Con los datos disponibles, la respuesta es **no** — y es casi lo contrario. Comparando el gasto en infraestructura de IA (como % del market cap) contra el rendimiento YTD 2026 de las 5 empresas que reportan esa cifra:

| Empresa | Capex IA / Market Cap | Rendimiento YTD |
|---|---|---|
| Apple | 0.3% | **+23.9%** |
| Alphabet | 4.2% | +4.3% |
| Microsoft | 5.7% | -10.0% |
| Amazon | 6.9% | +0.3% |
| Meta | 8.9% | **-19.5%** |

Correlación de Pearson: **r = -0.94** (p = 0.019). Apple, la que menos apuesta relativamente, es la única con un alza fuerte; Meta, la que más apuesta, tiene el peor año. Con solo 5 puntos de datos esto es una observación, no una ley — pero es el tipo de patrón que vale la pena señalar, no ocultar.

## Por qué este proyecto es distinto a los anteriores

A diferencia del Mundial (una fuente rica y ya cerrada) o Spotify (un dataset ya empaquetado), aquí **no existe una fuente única** — los datos de mercado cambian constantemente. Cada cifra se recopiló y cruzó contra múltiples fuentes (Fast Company, MarketCapLens, Disfold, Tom's Hardware, Yahoo Finance, CNBC) y se documentó como **una fotografía de un momento específico** (28 jul – 1 ago 2026), no como un feed en vivo. Esa distinción — snapshot vs. tiempo real — es una decisión de diseño de datos real, y se comunica explícitamente en el dashboard.

## El diseño: minimalismo tipo Apple + cross-filtering real

- **Paleta y tipografía**: los colores de sistema reales de Apple (`#1D1D1F`, `#F5F5F7`, `#0071E3`, `#34C759`/`#FF3B30` adaptados), tipografía `-apple-system` con `Inter` como respaldo web
- **Una sola sección oscura de alto impacto** (el hallazgo de correlación) — el resto del sitio se mantiene deliberadamente contenido, sin decoración de sobra
- **Cross-filtering real**: seleccionar una empresa (desde la grilla, el gráfico de barras, el scatter, o el ranking) actualiza *todas* las demás vistas a la vez — no son filtros aislados, son vistas enlazadas. Validado con pruebas automatizadas simulando clics reales.

## Estructura del proyecto

```
bigtech_portfolio/
├── data/
│   ├── raw/bigtech_2026_data.py     # datos crudos verificados (17 empresas)
│   └── processed/                    # CSV/JSON limpios + base SQLite
├── sql/
│   ├── 01_schema.sql
│   └── 02_eda_queries.sql            # 6 queries de análisis exploratorio
├── scripts/
│   ├── 01_clean_transform.py         # limpieza + feature engineering
│   ├── 02_load_db.py                 # carga a SQLite
│   ├── 03_run_eda.py                 # ejecuta las queries SQL → JSON
│   ├── 04_ml_analysis.py             # correlación, KMeans, Momentum Score
│   ├── 07_translate_exports.py       # genera las etiquetas categóricas en inglés
│   └── 08_build_dashboards.py        # inyecta datos + Chart.js en las plantillas ES/EN
├── lib/
│   ├── chart.umd.min.js
│   └── dashboard_template_i18n.html  # plantilla bilingüe (i18n vía data-i18n)
├── docs/
│   ├── index.html                    # ⭐ producto final en Español
│   └── dashboard_en.html             # ⭐ producto final en Inglés
└── README.md
```

## Cómo reproducirlo

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

## Metodología del Momentum Score

Score compuesto (0-100) para el ranking del Magnificent 7:
- **45%** rendimiento YTD
- **15%** variación del último día
- **15%** tamaño (market cap)
- **25%** eficiencia de capex (menor gasto relativo a su tamaño = mejor score; empresas sin dato reportado reciben score neutral)

## Stack técnico

`Python` · `pandas` · `scikit-learn` (KMeans, PCA) · `SciPy` (correlación de Pearson) · `SQL` · `SQLite` · `HTML/CSS/JS` · `Chart.js`

---

*Datos recopilados y verificados de fuentes públicas durante la semana del 28 jul – 1 ago 2026. Los mercados cambian constantemente — estos valores son una fotografía, no datos en vivo.*
