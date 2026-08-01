"""
Etapa 5 — Analisis cuantitativo e IA aplicada
================================================
1) Correlacion de Pearson: gasto en IA (% market cap) vs rendimiento YTD
   -> valida (o refuta) la narrativa de que "gastar mas en IA = mejor
   rendimiento bursatil" con los 5 datos reales disponibles.
2) KMeans: perfiles de inversion de las 7 Magnificent Seven.
3) Momentum Score: ranking compuesto (YTD + variacion diaria + eficiencia
   de capex) para las 7 empresas principales.
"""
import pandas as pd
import numpy as np
import json
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

PROC = "/home/claude/bigtech_portfolio/data/processed/"
m7 = pd.read_csv(PROC + "magnificent7.csv")

# ============================================================
# 1) CORRELACION: capex/mcap vs YTD (n=5, las que reportan capex)
# ============================================================
print("[1/3] Correlacion capex vs rendimiento...")
capex_df = m7.dropna(subset=["capex_sobre_mcap_pct"])
r, p_value = stats.pearsonr(capex_df["capex_sobre_mcap_pct"], capex_df["ytd_pct"])
print(f"  Pearson r = {r:.3f} (p={p_value:.3f}, n={len(capex_df)})")
print("  Nota: muestra muy pequeña (n=5) -- se reporta como observacion")
print("  descriptiva, no como resultado estadisticamente robusto.")

# ============================================================
# 2) KMEANS — perfiles de inversion (Magnificent 7)
# ============================================================
print("\n[2/3] Clustering de perfiles...")
FEATURES = ["ytd_pct", "var_1d_pct", "market_cap_t"]
scaler = StandardScaler()
X = scaler.fit_transform(m7[FEATURES])

k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
m7["cluster"] = kmeans.fit_predict(X)

profiles = m7.groupby("cluster")[["ytd_pct", "var_1d_pct", "market_cap_t"]].mean().round(2)
ranked = profiles.sort_values("ytd_pct", ascending=False)
tier_names = ["Momentum positivo", "Zona neutral", "Bajo presion"][:len(ranked)]
cluster_names = {int(c): tier_names[i] for i, c in enumerate(ranked.index)}
m7["cluster_name"] = m7["cluster"].map(cluster_names)
print(profiles)

pca = PCA(n_components=2, random_state=42)
coords = pca.fit_transform(X)
m7["pca_x"] = coords[:, 0].round(3)
m7["pca_y"] = coords[:, 1].round(3)

# ============================================================
# 3) MOMENTUM SCORE — ranking compuesto
# ============================================================
print("\n[3/3] Momentum Score...")
def norm(s):
    return (s - s.min()) / (s.max() - s.min() + 1e-9)

m7["score_ytd"] = norm(m7["ytd_pct"])
m7["score_1d"] = norm(m7["var_1d_pct"])
m7["score_mcap"] = norm(m7["market_cap_t"])
# eficiencia de capex: menor gasto relativo + mejor resultado = mejor score
# (empresas sin dato de capex reciben score neutral de 0.5)
m7["score_eficiencia_capex"] = m7["capex_sobre_mcap_pct"].apply(
    lambda x: 1 - (x / m7["capex_sobre_mcap_pct"].max()) if pd.notna(x) else 0.5)

m7["momentum_score"] = (
    m7["score_ytd"] * 0.45 +
    m7["score_1d"] * 0.15 +
    m7["score_mcap"] * 0.15 +
    m7["score_eficiencia_capex"] * 0.25
) * 100

m7 = m7.sort_values("momentum_score", ascending=False).reset_index(drop=True)
m7["momentum_rank"] = m7.index + 1

print(m7[["momentum_rank", "nombre", "ytd_pct", "momentum_score", "cluster_name"]].round(1).to_string(index=False))

m7.to_csv(PROC + "magnificent7.csv", index=False)
m7.to_json(PROC + "magnificent7_ml.json", orient="records", force_ascii=False)

metrics = {
    "correlacion_capex_ytd_r": round(float(r), 3),
    "correlacion_capex_ytd_p": round(float(p_value), 3),
    "correlacion_n": int(len(capex_df)),
    "n_clusters": k,
    "cluster_profiles": {cluster_names[int(c)]: row.to_dict() for c, row in profiles.iterrows()},
    "pca_variance_explained": round(float(pca.explained_variance_ratio_.sum()), 3),
}
with open(PROC + "ml_metrics.json", "w", encoding="utf-8") as f:
    json.dump(metrics, f, indent=2, ensure_ascii=False)
print("\nGuardado: magnificent7_ml.json, ml_metrics.json")
