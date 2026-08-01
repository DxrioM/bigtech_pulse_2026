"""
Etapa 3 — Carga a SQLite
"""
import sqlite3
import pandas as pd

DB_PATH = "/home/claude/bigtech_portfolio/data/processed/bigtech.db"
SCHEMA_PATH = "/home/claude/bigtech_portfolio/sql/01_schema.sql"
PROC = "/home/claude/bigtech_portfolio/data/processed/"

universe = pd.read_csv(PROC + "universe.csv")
universe["es_magnificent7"] = universe["es_magnificent7"].astype(int)

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
with open(SCHEMA_PATH) as f:
    cur.executescript(f.read())

universe.to_sql("companies", conn, if_exists="append", index=False)
conn.commit()

n = cur.execute("SELECT COUNT(*) FROM companies").fetchone()[0]
print(f"companies: {n} filas")
conn.close()
print(f"Base de datos creada en: {DB_PATH}")
