"""
LinkedIn card v2 — inspirado en estructura de infografia tipo "scorecard"
(sin logos ni fotos reales, sin personas reales identificables).

Estructura tomada de la referencia:
1. Header con titulo grande + subtitulo + badges de stats
2. Tabla "scorecard" (equivalente al Indice AXIO) con las 7 Magnificent Seven
3. Badge de diagnostico grande (equivalente a "SALUD GLOBAL")
4. Grid de 4 columnas al pie (equivalente a ecosistema/servicios/etc)
5. Tagline final
"""
import cairosvg
import json
import os
import textwrap
from xml.sax.saxutils import escape as xml_escape

PROC = "/home/claude/bigtech_portfolio/data/processed/"
OUT = "/home/claude/bigtech_portfolio/assets_linkedin"
os.makedirs(OUT, exist_ok=True)

# paleta oscura, colores de sistema de Apple (modo oscuro)
P = {
    "bg": "#0A0A0C", "card": "#18181B", "card2": "#1F1F23", "border": "#2C2C30",
    "text": "#F5F5F7", "text2": "#9A9AA0", "text3": "#6E6E73",
    "blue": "#0A84FF", "green": "#30D158", "red": "#FF453A", "amber": "#FF9F0A",
}

m7 = json.load(open(PROC + "magnificent7_ml.json", encoding="utf-8"))
m7_en = json.load(open(PROC + "magnificent7_ml_en.json", encoding="utf-8"))
metrics = json.load(open(PROC + "ml_metrics.json", encoding="utf-8"))

def status_color(cluster_name):
    if "positivo" in cluster_name.lower() or "positive" in cluster_name.lower():
        return P["green"]
    if "neutral" in cluster_name.lower():
        return P["amber"]
    return P["red"]

def wrap_tspans(text, x, width, font_size, dy_mult=1.35, anchor=None):
    wrapped = textwrap.wrap(xml_escape(text), width=width)
    attrs = f' text-anchor="{anchor}"' if anchor else ''
    lines = "".join(f'<tspan x="{x}" dy="{0 if i==0 else font_size*dy_mult}"{attrs}>{ln}</tspan>' for i, ln in enumerate(wrapped))
    return lines, len(wrapped)

def build_svg(lang):
    data = m7 if lang == "es" else m7_en
    if lang == "es":
        eyebrow = "PORTAFOLIO DE DATA SCIENCE · MERCADOS"
        title = "BIG TECH PULSE"
        subtitle = "El Magnificent 7 bajo la lupa: SQL, Python y Machine Learning aplicados a las siete empresas más valiosas del mundo."
        stat_labels = ["17 empresas analizadas", "$22.4T market cap combinado", "$709B capex en IA 2026", "Snapshot: 1 ago 2026"]
        table_title = "BIG TECH SCORECARD — DIAGNÓSTICO 2026"
        col_headers = ["#", "EMPRESA", "MARKET CAP", "YTD", "MOMENTUM", "ESTADO"]
        badge_eyebrow = "EL HALLAZGO CENTRAL"
        badge_big = "r = −0.94"
        badge_label = "Correlación entre gasto en IA (% del market cap) y rendimiento YTD"
        badge_desc = "Apple gasta menos en IA (0.3% de su valor) y es la única con alza fuerte (+23.9%). Meta gasta más (8.9%) y tiene el peor año (−19.5%)."
        col1_title, col1_items = "METODOLOGÍA", ["Extracción cruzada de 8+ fuentes", "Limpieza y feature engineering", "SQL: esquema + 6 queries EDA", "Machine Learning: KMeans, PCA"]
        col2_title, col2_items = "PANORAMA GLOBAL", ["17 empresas · 4 países", "10 sectores tecnológicos", "No es solo una historia de EE.UU.", "Broadcom, TSMC, Samsung, ASML..."]
        col3_title = "LO QUE MUESTRA ESTE PROYECTO"
        col3_items = ["SQL real con agregaciones y rankings", "Correlación validada con SciPy (p<0.05)", "Cross-filtering interactivo real", "Diseño minimalista tipo Apple"]
        cta_title = "DEMO INTERACTIVO"
        cta_sub = "Explora el cross-filtering en vivo"
        cta_link = "link en el post · ES / EN"
        tagline = "LOS DATOS NO MIENTEN — PERO HAY QUE SABER PREGUNTARLES."
        footer_note = "Snapshot del 28 jul – 1 ago 2026 · no es un feed en vivo"
    else:
        eyebrow = "DATA SCIENCE PORTFOLIO · MARKETS"
        title = "BIG TECH PULSE"
        subtitle = "The Magnificent 7 under the microscope: SQL, Python and Machine Learning applied to the world's seven most valuable companies."
        stat_labels = ["17 companies analyzed", "$22.4T combined market cap", "$709B 2026 AI capex", "Snapshot: Aug 1, 2026"]
        table_title = "BIG TECH SCORECARD — 2026 DIAGNOSIS"
        col_headers = ["#", "COMPANY", "MARKET CAP", "YTD", "MOMENTUM", "STATUS"]
        badge_eyebrow = "THE CORE FINDING"
        badge_big = "r = −0.94"
        badge_label = "Correlation between AI spend (% of market cap) and YTD return"
        badge_desc = "Apple spends the least on AI (0.3% of its value) and is the only one with a strong gain (+23.9%). Meta spends the most (8.9%) and has the worst year (−19.5%)."
        col1_title, col1_items = "METHODOLOGY", ["Cross-checked across 8+ sources", "Cleaning and feature engineering", "SQL: schema + 6 EDA queries", "Machine Learning: KMeans, PCA"]
        col2_title, col2_items = "GLOBAL LANDSCAPE", ["17 companies · 4 countries", "10 tech sectors", "Not just a U.S. story", "Broadcom, TSMC, Samsung, ASML..."]
        col3_title = "WHAT THIS PROJECT SHOWS"
        col3_items = ["Real SQL with aggregations and rankings", "Correlation validated with SciPy (p<0.05)", "Real interactive cross-filtering", "Apple-style minimalist design"]
        cta_title = "INTERACTIVE DEMO"
        cta_sub = "Explore the live cross-filtering"
        cta_link = "link in the post · ES / EN"
        tagline = "THE DATA DOESN'T LIE — BUT YOU HAVE TO KNOW HOW TO ASK IT."
        footer_note = "Snapshot from Jul 28 – Aug 1, 2026 · not a live feed"

    W = 1200
    # escapar variables que se insertan directamente (sin pasar por wrap_tspans)
    eyebrow, title, table_title = xml_escape(eyebrow), xml_escape(title), xml_escape(table_title)
    col_headers = [xml_escape(h) for h in col_headers]
    badge_eyebrow, badge_big, badge_label = xml_escape(badge_eyebrow), xml_escape(badge_big), xml_escape(badge_label)
    col1_title, col2_title, col3_title = xml_escape(col1_title), xml_escape(col2_title), xml_escape(col3_title)
    cta_title, cta_sub, cta_link = xml_escape(cta_title), xml_escape(cta_sub), xml_escape(cta_link)

    svg_parts = []
    svg_parts.append(f'<rect width="{W}" height="__H__" fill="{P["bg"]}"/>')

    y = 64
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="15" font-weight="bold" letter-spacing="2" fill="{P["blue"]}">{eyebrow}</text>')
    y += 62
    svg_parts.append(f'<text x="66" y="{y}" font-family="DejaVu Sans" font-size="58" font-weight="bold" letter-spacing="-1" fill="{P["text"]}">{title}</text>')
    y += 42
    sub_lines, n = wrap_tspans(subtitle, 70, 78, 19)
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="19" fill="{P["text2"]}">{sub_lines}</text>')
    y += n * 19 * 1.35 + 30

    # fila de 4 stat badges
    badge_w = (W - 140 - 3*14) / 4
    for i, label in enumerate(stat_labels):
        bx = 70 + i*(badge_w+14)
        svg_parts.append(f'<rect x="{bx}" y="{y}" width="{badge_w}" height="52" rx="10" fill="{P["card"]}" stroke="{P["border"]}"/>')
        lines, _ = wrap_tspans(label, bx+14, 22, 12.5)
        svg_parts.append(f'<text x="{bx+14}" y="{y+21}" font-family="DejaVu Sans" font-size="12.5" font-weight="bold" fill="{P["text"]}">{lines}</text>')
    y += 52 + 46

    # ============ SCORECARD TABLE ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="16" font-weight="bold" letter-spacing="1.5" fill="{P["blue"]}">{table_title}</text>')
    y += 26
    table_x, table_w = 70, W - 140
    col_x = [table_x, table_x+40, table_x+300, table_x+520, table_x+650, table_x+820]
    row_h = 50
    header_y = y
    svg_parts.append(f'<rect x="{table_x}" y="{header_y}" width="{table_w}" height="34" fill="{P["card"]}"/>')
    for cx, htext in zip(col_x, col_headers):
        svg_parts.append(f'<text x="{cx+10}" y="{header_y+22}" font-family="DejaVu Sans Mono" font-size="11.5" font-weight="bold" letter-spacing="0.5" fill="{P["text2"]}">{htext}</text>')
    y = header_y + 34

    sorted_companies = sorted(data, key=lambda c: -c["momentum_score"])
    for i, c in enumerate(sorted_companies):
        ry = y + i*row_h
        bg = P["card"] if i % 2 == 0 else P["bg"]
        svg_parts.append(f'<rect x="{table_x}" y="{ry}" width="{table_w}" height="{row_h}" fill="{bg}"/>')
        svg_parts.append(f'<text x="{col_x[0]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["text3"]}">{i+1}</text>')
        svg_parts.append(f'<text x="{col_x[1]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans" font-size="15" font-weight="bold" fill="{P["text"]}">{xml_escape(c["nombre"])}</text>')
        svg_parts.append(f'<text x="{col_x[2]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["text2"]}">${c["market_cap_t"]:.2f}T</text>')
        ytd_color = P["green"] if c["ytd_pct"] >= 0 else P["red"]
        ytd_str = f'{"+" if c["ytd_pct"]>=0 else ""}{c["ytd_pct"]:.1f}%'
        svg_parts.append(f'<text x="{col_x[3]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans Mono" font-size="14" font-weight="bold" fill="{ytd_color}">{ytd_str}</text>')
        svg_parts.append(f'<text x="{col_x[4]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["text"]}">{c["momentum_score"]:.0f}</text>')
        dotc = status_color(c["cluster_name"])
        svg_parts.append(f'<circle cx="{col_x[5]+22}" cy="{ry+row_h*0.5}" r="7" fill="{dotc}"/>')
    y += len(sorted_companies) * row_h + 40

    # ============ BADGE DE DIAGNOSTICO GRANDE ============
    badge_h = 200
    svg_parts.append(f'<rect x="70" y="{y}" width="{table_w}" height="{badge_h}" rx="16" fill="{P["card2"]}" stroke="{P["blue"]}" stroke-width="1.5"/>')
    svg_parts.append(f'<text x="102" y="{y+42}" font-family="DejaVu Sans" font-size="14" font-weight="bold" letter-spacing="1.5" fill="{P["blue"]}">{badge_eyebrow}</text>')
    svg_parts.append(f'<text x="102" y="{y+108}" font-family="DejaVu Sans Mono" font-size="56" font-weight="bold" fill="{P["text"]}">{badge_big}</text>')
    svg_parts.append(f'<text x="102" y="{y+138}" font-family="DejaVu Sans" font-size="15" fill="{P["text2"]}">{badge_label}</text>')
    desc_lines, ndesc = wrap_tspans(badge_desc, 102, 92, 15.5)
    svg_parts.append(f'<text x="102" y="{y+168}" font-family="DejaVu Sans" font-size="15.5" fill="{P["text2"]}">{desc_lines}</text>')
    y += badge_h + 44

    # ============ GRID DE 4 COLUMNAS ============
    col_w = (table_w - 3*20) / 4
    columns = [
        (col1_title, col1_items, P["blue"]),
        (col2_title, col2_items, P["green"]),
        (col3_title, col3_items, P["amber"]),
        (cta_title, None, P["blue"]),
    ]
    col_top = y
    max_col_bottom = y
    for i, (ctitle, items, accent) in enumerate(columns):
        cx = 70 + i*(col_w + 20)
        svg_parts.append(f'<rect x="{cx}" y="{col_top}" width="4" height="22" fill="{accent}"/>')
        svg_parts.append(f'<text x="{cx+14}" y="{col_top+17}" font-family="DejaVu Sans" font-size="13" font-weight="bold" letter-spacing="0.5" fill="{P["text"]}">{ctitle}</text>')
        cy = col_top + 46
        if items:
            for item in items:
                lines, n_ = wrap_tspans(item, cx, 26, 12.5)
                svg_parts.append(f'<circle cx="{cx+3}" cy="{cy-4}" r="2.5" fill="{accent}"/>')
                svg_parts.append(f'<text x="{cx+14}" y="{cy}" font-family="DejaVu Sans" font-size="12.5" fill="{P["text2"]}">{lines}</text>')
                cy += n_ * 12.5*1.35 + 12
        else:
            svg_parts.append(f'<text x="{cx}" y="{cy+8}" font-family="DejaVu Sans" font-size="14" font-weight="bold" fill="{P["text"]}">{cta_sub}</text>')
            svg_parts.append(f'<rect x="{cx}" y="{cy+26}" width="{col_w-10}" height="44" rx="10" fill="{P["blue"]}"/>')
            svg_parts.append(f'<text x="{cx+(col_w-10)/2}" y="{cy+53}" font-family="DejaVu Sans Mono" font-size="12" fill="#fff" text-anchor="middle">{cta_link}</text>')
            cy += 26 + 44
        max_col_bottom = max(max_col_bottom, cy)
    y = max_col_bottom + 40

    # ============ TAGLINE FINAL ============
    svg_parts.append(f'<line x1="70" y1="{y}" x2="{W-70}" y2="{y}" stroke="{P["border"]}" stroke-width="1"/>')
    y += 40
    tagline_lines, ntag = wrap_tspans(tagline, W/2, 44, 20, anchor="middle")
    svg_parts.append(f'<text x="{W/2}" y="{y}" font-family="DejaVu Sans" font-size="20" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{tagline_lines}</text>')
    y += ntag*20*1.35 + 20
    svg_parts.append(f'<text x="{W/2}" y="{y}" font-family="DejaVu Sans Mono" font-size="12" fill="{P["text3"]}" text-anchor="middle">{footer_note}</text>')
    y += 50

    H = int(y)
    svg = f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">' + "".join(svg_parts).replace("__H__", str(H)) + '</svg>'
    return svg, W, H

for lang in ["es", "en"]:
    svg_code, W, H = build_svg(lang)
    print(f"{lang}: {W}x{H}")
    svg_path = f"{OUT}/linkedin_scorecard_{lang}.svg"
    png_path = f"{OUT}/linkedin_scorecard_{lang}.png"
    open(svg_path, "w", encoding="utf-8").write(svg_code)
    cairosvg.svg2png(url=svg_path, write_to=png_path, output_width=W, output_height=H)
    print(f"Generado: {png_path}")
