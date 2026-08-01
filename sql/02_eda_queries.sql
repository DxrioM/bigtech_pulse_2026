-- ============================================================
-- Análisis Exploratorio — Big Tech Pulse 2026
-- ============================================================

-- 1. Market cap total y promedio por sector
SELECT sector,
       COUNT(*) AS num_empresas,
       ROUND(SUM(market_cap_t), 2) AS market_cap_total_t,
       ROUND(AVG(market_cap_t), 2) AS market_cap_promedio_t
FROM companies
GROUP BY sector
ORDER BY market_cap_total_t DESC;

-- 2. Market cap total por país (panorama global, no solo USA)
SELECT pais,
       COUNT(*) AS num_empresas,
       ROUND(SUM(market_cap_t), 2) AS market_cap_total_t
FROM companies
GROUP BY pais
ORDER BY market_cap_total_t DESC;

-- 3. Ranking YTD del Magnificent 7 (de mejor a peor)
SELECT ranking_ytd, nombre, ticker, ytd_pct, var_1d_pct, categoria_rendimiento
FROM companies
WHERE es_magnificent7 = 1
ORDER BY ytd_pct DESC;

-- 4. Capex en IA vs Market Cap vs Rendimiento (las 5 empresas con dato de capex)
SELECT nombre, capex_ia_2026_b, capex_sobre_mcap_pct, ytd_pct
FROM companies
WHERE capex_ia_2026_b IS NOT NULL
ORDER BY capex_sobre_mcap_pct DESC;

-- 5. Distribución de categorías de rendimiento (Magnificent 7)
SELECT categoria_rendimiento, COUNT(*) AS num_empresas
FROM companies
WHERE es_magnificent7 = 1
GROUP BY categoria_rendimiento;

-- 6. Top 10 empresas por market cap (panorama completo)
SELECT ranking_market_cap, nombre, ticker, market_cap_t, pais, sector
FROM companies
ORDER BY market_cap_t DESC
LIMIT 10;
