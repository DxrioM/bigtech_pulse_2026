-- ============================================================
-- Esquema — Big Tech Pulse 2026
-- ============================================================
DROP TABLE IF EXISTS companies;

CREATE TABLE companies (
    ticker              TEXT PRIMARY KEY,
    nombre              TEXT NOT NULL,
    precio              REAL,
    market_cap_t        REAL NOT NULL,
    var_1d_pct          REAL,
    ytd_pct             REAL,
    sector              TEXT NOT NULL,
    pais                TEXT NOT NULL,
    capex_ia_2026_b     REAL,
    capex_sobre_mcap_pct REAL,
    categoria_rendimiento TEXT,
    es_magnificent7     INTEGER NOT NULL,
    ranking_market_cap  INTEGER,
    ranking_ytd         INTEGER
);

CREATE INDEX idx_companies_sector ON companies(sector);
CREATE INDEX idx_companies_pais ON companies(pais);
CREATE INDEX idx_companies_m7 ON companies(es_magnificent7);
