"""
LinkedIn card v3 — ajustes de feedback:
1. Cards de KPI mas grandes, digito como protagonista, con mini-graficas reales.
2. Hallazgo principal reorganizado lado a lado (numero + texto), mas compacto.
3. Footer: 3 columnas parejas (ya no 4 desbalanceadas) + banner CTA de ancho
   completo debajo -- corrige el overlap real que tenia el titulo de la
   columna 3 con la columna 4.
"""
import cairosvg
import json
import os
import textwrap
from xml.sax.saxutils import escape as xml_escape

PROC = "/home/claude/bigtech_portfolio/data/processed/"
OUT = "/home/claude/bigtech_portfolio/assets_linkedin"
os.makedirs(OUT, exist_ok=True)

P = {
    "bg": "#0A0A0C", "card": "#18181B", "card2": "#1F1F23", "border": "#2C2C30",
    "text": "#F5F5F7", "text2": "#9A9AA0", "text3": "#6E6E73",
    "blue": "#0A84FF", "green": "#30D158", "red": "#FF453A", "amber": "#FF9F0A",
}

m7 = json.load(open(PROC + "magnificent7_ml.json", encoding="utf-8"))
m7_en = json.load(open(PROC + "magnificent7_ml_en.json", encoding="utf-8"))
universe = json.load(open(PROC + "universe.json", encoding="utf-8"))

def status_color(cluster_name):
    if "positivo" in cluster_name.lower() or "positive" in cluster_name.lower():
        return P["green"]
    if "neutral" in cluster_name.lower():
        return P["amber"]
    return P["red"]

def esc(s):
    return xml_escape(str(s))

def wrap_tspans(text, x, width, font_size, dy_mult=1.35, anchor=None):
    wrapped = textwrap.wrap(esc(text), width=width)
    attrs = f' text-anchor="{anchor}"' if anchor else ''
    lines = "".join(f'<tspan x="{x}" dy="{0 if i==0 else font_size*dy_mult}"{attrs}>{ln}</tspan>' for i, ln in enumerate(wrapped))
    return lines, len(wrapped)

def mini_stacked_bar(x, y, w, h, segments):
    """segments: [(valor, color), ...] -- barra horizontal apilada."""
    total = sum(v for v, _ in segments)
    svg = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h/2}" fill="{P["bg"]}"/>'
    cx = x
    for v, c in segments:
        seg_w = (v/total) * w
        svg += f'<rect x="{cx:.1f}" y="{y}" width="{seg_w:.1f}" height="{h}" fill="{c}"/>'
        cx += seg_w
    return svg

def mini_dual_bar(x, y, w, h, label1, val1, color1, label2, val2, color2, max_abs):
    """Dos barras horizontales cortas, una encima de otra (comparacion simple)."""
    svg = ""
    bw1 = max(4, abs(val1)/max_abs * w)
    bw2 = max(4, abs(val2)/max_abs * w)
    svg += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{P["bg"]}"/>'
    svg += f'<rect x="{x}" y="{y}" width="{bw1:.1f}" height="{h}" rx="3" fill="{color1}"/>'
    svg += f'<rect x="{x}" y="{y+h+6}" width="{w}" height="{h}" rx="3" fill="{P["bg"]}"/>'
    svg += f'<rect x="{x}" y="{y+h+6}" width="{bw2:.1f}" height="{h}" rx="3" fill="{color2}"/>'
    return svg

def build_svg(lang):
    data = m7 if lang == "es" else m7_en
    ext_total = sum(c["market_cap_t"] for c in universe if not c["es_magnificent7"])
    m7_total = sum(c["market_cap_t"] for c in data)

    if lang == "es":
        eyebrow = "PORTAFOLIO DE DATA SCIENCE · MERCADOS"
        title = "BIG TECH PULSE"
        subtitle = "El Magnificent 7 bajo la lupa: SQL, Python y Machine Learning aplicados a las siete empresas más valiosas del mundo."
        kpi1_num, kpi1_lbl, kpi1_sub = "17", "EMPRESAS ANALIZADAS", "7 Magnificent · 10 panorama global"
        kpi2_num, kpi2_lbl, kpi2_sub = "$22.4T", "MARKET CAP MAGNIFICENT 7", f"78% del universo total (${m7_total+ext_total:.1f}T)"
        kpi3_num, kpi3_lbl, kpi3_sub = "$709B", "CAPEX EN IA 2026", "Amazon, Microsoft, Alphabet, Meta, Apple"
        kpi4_num, kpi4_lbl = "+23.9% / −31.2%", "MEJOR VS. PEOR YTD"
        kpi4_sub1, kpi4_sub2 = "AAPL", "TSLA"
        table_title = "BIG TECH SCORECARD — DIAGNÓSTICO 2026"
        col_headers = ["#", "EMPRESA", "MARKET CAP", "YTD", "MOMENTUM", "ESTADO"]
        badge_eyebrow = "EL HALLAZGO CENTRAL"
        badge_big = "r = −0.94"
        badge_label = "Capex en IA vs. rendimiento YTD"
        badge_desc = "Apple gasta menos en IA (0.3% de su valor) y es la única con alza fuerte (+23.9%). Meta gasta más (8.9%) y tiene el peor año (−19.5%). n=5 · p<0.05, muestra pequeña."
        col1_title, col1_items = "METODOLOGÍA", ["Extracción cruzada de 8+ fuentes", "SQL: esquema + 6 queries EDA", "Machine Learning: KMeans, PCA"]
        col2_title, col2_items = "PANORAMA GLOBAL", ["17 empresas · 4 países", "10 sectores tecnológicos", "No es solo una historia de EE.UU."]
        col3_title, col3_items = "DESTACADOS", ["Correlación validada con SciPy", "Cross-filtering interactivo real", "Diseño minimalista tipo Apple"]
        cta_text = "Explora el cross-filtering en vivo — demo interactivo + código completo"
        cta_link = "link en el post · ES / EN"
        tagline = "LOS DATOS NO MIENTEN — PERO HAY QUE SABER PREGUNTARLES."
        footer_note = "Snapshot del 28 jul – 1 ago 2026 · no es un feed en vivo"
    else:
        eyebrow = "DATA SCIENCE PORTFOLIO · MARKETS"
        title = "BIG TECH PULSE"
        subtitle = "The Magnificent 7 under the microscope: SQL, Python and Machine Learning applied to the world's seven most valuable companies."
        kpi1_num, kpi1_lbl, kpi1_sub = "17", "COMPANIES ANALYZED", "7 Magnificent · 10 global landscape"
        kpi2_num, kpi2_lbl, kpi2_sub = "$22.4T", "MAGNIFICENT 7 MARKET CAP", f"78% of the total universe (${m7_total+ext_total:.1f}T)"
        kpi3_num, kpi3_lbl, kpi3_sub = "$709B", "2026 AI CAPEX", "Amazon, Microsoft, Alphabet, Meta, Apple"
        kpi4_num, kpi4_lbl = "+23.9% / −31.2%", "BEST VS. WORST YTD"
        kpi4_sub1, kpi4_sub2 = "AAPL", "TSLA"
        table_title = "BIG TECH SCORECARD — 2026 DIAGNOSIS"
        col_headers = ["#", "COMPANY", "MARKET CAP", "YTD", "MOMENTUM", "STATUS"]
        badge_eyebrow = "THE CORE FINDING"
        badge_big = "r = −0.94"
        badge_label = "AI capex vs. YTD performance"
        badge_desc = "Apple spends the least on AI (0.3% of its value) and is the only one with a strong gain (+23.9%). Meta spends the most (8.9%) and has the worst year (−19.5%). n=5 · p<0.05, small sample."
        col1_title, col1_items = "METHODOLOGY", ["Cross-checked across 8+ sources", "SQL: schema + 6 EDA queries", "Machine Learning: KMeans, PCA"]
        col2_title, col2_items = "GLOBAL LANDSCAPE", ["17 companies · 4 countries", "10 tech sectors", "Not just a U.S. story"]
        col3_title, col3_items = "HIGHLIGHTS", ["Correlation validated with SciPy", "Real interactive cross-filtering", "Apple-style minimalist design"]
        cta_text = "Explore the live cross-filtering — interactive demo + full code"
        cta_link = "link in the post · ES / EN"
        tagline = "THE DATA DOESN'T LIE — BUT YOU HAVE TO KNOW HOW TO ASK IT."
        footer_note = "Snapshot from Jul 28 – Aug 1, 2026 · not a live feed"

    W = 1200
    for name in ["eyebrow","title","table_title","badge_eyebrow","badge_big","badge_label",
                 "col1_title","col2_title","col3_title","kpi1_lbl","kpi2_lbl","kpi3_lbl","kpi4_lbl"]:
        pass
    eyebrow, title, table_title = esc(eyebrow), esc(title), esc(table_title)
    col_headers = [esc(h) for h in col_headers]
    badge_eyebrow, badge_big, badge_label = esc(badge_eyebrow), esc(badge_big), esc(badge_label)
    col1_title, col2_title, col3_title = esc(col1_title), esc(col2_title), esc(col3_title)

    svg_parts = [f'<rect width="{W}" height="__H__" fill="{P["bg"]}"/>']

    # ============ HEADER ============
    y = 64
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="15" font-weight="bold" letter-spacing="2" fill="{P["blue"]}">{eyebrow}</text>')
    y += 62
    svg_parts.append(f'<text x="66" y="{y}" font-family="DejaVu Sans" font-size="58" font-weight="bold" letter-spacing="-1" fill="{P["text"]}">{title}</text>')
    y += 40
    sub_lines, n = wrap_tspans(subtitle, 70, 78, 19)
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="19" fill="{P["text2"]}">{sub_lines}</text>')
    y += n * 19 * 1.35 + 36

    # ============ KPI CARDS (mas grandes, digito protagonista, mini-graficas) ============
    kpi_w = (W - 140 - 3*16) / 4
    kpi_h = 150
    kx = 70

    # Card 1: empresas (mini stacked bar M7 vs extendido)
    svg_parts.append(f'<rect x="{kx}" y="{y}" width="{kpi_w}" height="{kpi_h}" rx="14" fill="{P["card"]}" stroke="{P["border"]}"/>')
    svg_parts.append(f'<text x="{kx+18}" y="{y+56}" font-family="DejaVu Sans Mono" font-size="40" font-weight="bold" fill="{P["text"]}">{kpi1_num}</text>')
    lbl_lines, _ = wrap_tspans(kpi1_lbl, kx+18, 22, 11)
    svg_parts.append(f'<text x="{kx+18}" y="{y+76}" font-family="DejaVu Sans" font-size="11" font-weight="bold" letter-spacing="0.5" fill="{P["text2"]}">{lbl_lines}</text>')
    svg_parts.append(mini_stacked_bar(kx+18, y+100, kpi_w-36, 8, [(7, P["blue"]), (10, P["border"])]))
    sub_lines1, _ = wrap_tspans(kpi1_sub, kx+18, 30, 10.5)
    svg_parts.append(f'<text x="{kx+18}" y="{y+126}" font-family="DejaVu Sans" font-size="10.5" fill="{P["text3"]}">{sub_lines1}</text>')

    # Card 2: market cap M7 (mini stacked bar M7 vs resto)
    kx2 = kx + kpi_w + 16
    svg_parts.append(f'<rect x="{kx2}" y="{y}" width="{kpi_w}" height="{kpi_h}" rx="14" fill="{P["card"]}" stroke="{P["border"]}"/>')
    svg_parts.append(f'<text x="{kx2+18}" y="{y+56}" font-family="DejaVu Sans Mono" font-size="32" font-weight="bold" fill="{P["text"]}">{kpi2_num}</text>')
    lbl_lines2, _ = wrap_tspans(kpi2_lbl, kx2+18, 24, 11)
    svg_parts.append(f'<text x="{kx2+18}" y="{y+76}" font-family="DejaVu Sans" font-size="11" font-weight="bold" letter-spacing="0.5" fill="{P["text2"]}">{lbl_lines2}</text>')
    svg_parts.append(mini_stacked_bar(kx2+18, y+100, kpi_w-36, 8, [(m7_total, P["green"]), (ext_total, P["border"])]))
    sub_lines2, _ = wrap_tspans(kpi2_sub, kx2+18, 30, 10.5)
    svg_parts.append(f'<text x="{kx2+18}" y="{y+126}" font-family="DejaVu Sans" font-size="10.5" fill="{P["text3"]}">{sub_lines2}</text>')

    # Card 3: capex IA (mini stacked bar por empresa)
    kx3 = kx2 + kpi_w + 16
    svg_parts.append(f'<rect x="{kx3}" y="{y}" width="{kpi_w}" height="{kpi_h}" rx="14" fill="{P["card"]}" stroke="{P["border"]}"/>')
    svg_parts.append(f'<text x="{kx3+18}" y="{y+56}" font-family="DejaVu Sans Mono" font-size="32" font-weight="bold" fill="{P["text"]}">{kpi3_num}</text>')
    lbl_lines3, _ = wrap_tspans(kpi3_lbl, kx3+18, 22, 11)
    svg_parts.append(f'<text x="{kx3+18}" y="{y+76}" font-family="DejaVu Sans" font-size="11" font-weight="bold" letter-spacing="0.5" fill="{P["text2"]}">{lbl_lines3}</text>')
    capex_companies = sorted([c for c in data if c.get("capex_ia_2026_b")], key=lambda c: -c["capex_ia_2026_b"])
    capex_colors = [P["blue"], P["green"], P["amber"], P["red"], P["text3"]]
    capex_segments = [(c["capex_ia_2026_b"], capex_colors[i % len(capex_colors)]) for i, c in enumerate(capex_companies)]
    svg_parts.append(mini_stacked_bar(kx3+18, y+100, kpi_w-36, 8, capex_segments))
    sub_lines3, _ = wrap_tspans(kpi3_sub, kx3+18, 30, 10.5)
    svg_parts.append(f'<text x="{kx3+18}" y="{y+126}" font-family="DejaVu Sans" font-size="10.5" fill="{P["text3"]}">{sub_lines3}</text>')

    # Card 4: mejor vs peor YTD (mini dual bar)
    kx4 = kx3 + kpi_w + 16
    svg_parts.append(f'<rect x="{kx4}" y="{y}" width="{kpi_w}" height="{kpi_h}" rx="14" fill="{P["card"]}" stroke="{P["border"]}"/>')
    svg_parts.append(f'<text x="{kx4+18}" y="{y+40}" font-family="DejaVu Sans Mono" font-size="22" font-weight="bold" fill="{P["green"]}">+23.9%</text>')
    svg_parts.append(f'<text x="{kx4+18}" y="{y+66}" font-family="DejaVu Sans Mono" font-size="22" font-weight="bold" fill="{P["red"]}">−31.2%</text>')
    lbl_lines4, _ = wrap_tspans(kpi4_lbl, kx4+18, 22, 11)
    svg_parts.append(f'<text x="{kx4+18}" y="{y+86}" font-family="DejaVu Sans" font-size="11" font-weight="bold" letter-spacing="0.5" fill="{P["text2"]}">{lbl_lines4}</text>')
    svg_parts.append(mini_dual_bar(kx4+18, y+100, kpi_w-70, 8, kpi4_sub1, 23.9, P["green"], kpi4_sub2, 31.2, P["red"], 32))
    svg_parts.append(f'<text x="{kx4+18}" y="{y+96+8}" font-family="DejaVu Sans Mono" font-size="9.5" fill="{P["text3"]}"></text>')
    svg_parts.append(f'<text x="{kx4+kpi_w-52}" y="{y+108}" font-family="DejaVu Sans Mono" font-size="9.5" fill="{P["text3"]}">{kpi4_sub1}</text>')
    svg_parts.append(f'<text x="{kx4+kpi_w-52}" y="{y+122}" font-family="DejaVu Sans Mono" font-size="9.5" fill="{P["text3"]}">{kpi4_sub2}</text>')

    y += kpi_h + 44

    # ============ SCORECARD TABLE ============
    svg_parts.append(f'<text x="70" y="{y}" font-family="DejaVu Sans" font-size="16" font-weight="bold" letter-spacing="1.5" fill="{P["blue"]}">{table_title}</text>')
    y += 26
    table_x, table_w = 70, W - 140
    col_x = [table_x, table_x+40, table_x+300, table_x+520, table_x+650, table_x+820]
    row_h = 50
    header_y = y
    svg_parts.append(f'<rect x="{table_x}" y="{header_y}" width="{table_w}" height="34" fill="{P["card"]}"/>')
    for cx_, htext in zip(col_x, col_headers):
        svg_parts.append(f'<text x="{cx_+10}" y="{header_y+22}" font-family="DejaVu Sans Mono" font-size="11.5" font-weight="bold" letter-spacing="0.5" fill="{P["text2"]}">{htext}</text>')
    y = header_y + 34

    sorted_companies = sorted(data, key=lambda c: -c["momentum_score"])
    for i, c in enumerate(sorted_companies):
        ry = y + i*row_h
        bg = P["card"] if i % 2 == 0 else P["bg"]
        svg_parts.append(f'<rect x="{table_x}" y="{ry}" width="{table_w}" height="{row_h}" fill="{bg}"/>')
        svg_parts.append(f'<text x="{col_x[0]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["text3"]}">{i+1}</text>')
        svg_parts.append(f'<text x="{col_x[1]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans" font-size="15" font-weight="bold" fill="{P["text"]}">{esc(c["nombre"])}</text>')
        svg_parts.append(f'<text x="{col_x[2]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["text2"]}">${c["market_cap_t"]:.2f}T</text>')
        ytd_color = P["green"] if c["ytd_pct"] >= 0 else P["red"]
        ytd_str = f'{"+" if c["ytd_pct"]>=0 else ""}{c["ytd_pct"]:.1f}%'
        svg_parts.append(f'<text x="{col_x[3]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans Mono" font-size="14" font-weight="bold" fill="{ytd_color}">{ytd_str}</text>')
        svg_parts.append(f'<text x="{col_x[4]+10}" y="{ry+row_h*0.62}" font-family="DejaVu Sans Mono" font-size="14" fill="{P["text"]}">{c["momentum_score"]:.0f}</text>')
        dotc = status_color(c["cluster_name"])
        svg_parts.append(f'<circle cx="{col_x[5]+22}" cy="{ry+row_h*0.5}" r="7" fill="{dotc}"/>')
    y += len(sorted_companies) * row_h + 40

    # ============ HALLAZGO PRINCIPAL — compacto, lado a lado ============
    badge_h = 130
    svg_parts.append(f'<rect x="70" y="{y}" width="{table_w}" height="{badge_h}" rx="16" fill="{P["card2"]}" stroke="{P["blue"]}" stroke-width="1.5"/>')
    left_w = 340
    svg_parts.append(f'<text x="102" y="{y+32}" font-family="DejaVu Sans" font-size="12.5" font-weight="bold" letter-spacing="1.2" fill="{P["blue"]}">{badge_eyebrow}</text>')
    svg_parts.append(f'<text x="102" y="{y+90}" font-family="DejaVu Sans Mono" font-size="48" font-weight="bold" fill="{P["text"]}">{badge_big}</text>')
    svg_parts.append(f'<text x="102" y="{y+114}" font-family="DejaVu Sans" font-size="13.5" fill="{P["text2"]}">{badge_label}</text>')
    # divisor vertical
    svg_parts.append(f'<line x1="{70+left_w}" y1="{y+22}" x2="{70+left_w}" y2="{y+badge_h-22}" stroke="{P["border"]}" stroke-width="1"/>')
    # columna derecha: descripcion
    right_x = 70 + left_w + 30
    right_w_chars = int((table_w - left_w - 60) / 6.8)
    desc_lines, ndesc = wrap_tspans(badge_desc, right_x, right_w_chars, 15)
    desc_y = y + badge_h/2 - (ndesc-1)*15*1.35/2 + 5
    svg_parts.append(f'<text x="{right_x}" y="{desc_y}" font-family="DejaVu Sans" font-size="15" fill="{P["text2"]}">{desc_lines}</text>')
    y += badge_h + 40

    # ============ FOOTER: 3 COLUMNAS PAREJAS ============
    col_w = (table_w - 2*24) / 3
    columns = [(col1_title, col1_items, P["blue"]), (col2_title, col2_items, P["green"]), (col3_title, col3_items, P["amber"])]
    col_top = y
    max_col_bottom = y
    for i, (ctitle, items, accent) in enumerate(columns):
        cx_ = 70 + i*(col_w + 24)
        svg_parts.append(f'<rect x="{cx_}" y="{col_top}" width="4" height="20" fill="{accent}"/>')
        title_lines, _ = wrap_tspans(ctitle, cx_+14, 24, 13)
        svg_parts.append(f'<text x="{cx_+14}" y="{col_top+16}" font-family="DejaVu Sans" font-size="13" font-weight="bold" letter-spacing="0.5" fill="{P["text"]}">{title_lines}</text>')
        cy = col_top + 44
        for item in items:
            lines, n_ = wrap_tspans(item, cx_+14, 27, 12.5)
            svg_parts.append(f'<circle cx="{cx_+3}" cy="{cy-4}" r="2.5" fill="{accent}"/>')
            svg_parts.append(f'<text x="{cx_+14}" y="{cy}" font-family="DejaVu Sans" font-size="12.5" fill="{P["text2"]}">{lines}</text>')
            cy += n_ * 12.5*1.35 + 12
        max_col_bottom = max(max_col_bottom, cy)
    y = max_col_bottom + 30

    # ============ CTA BANNER (ancho completo) ============
    cta_h = 70
    svg_parts.append(f'<rect x="70" y="{y}" width="{table_w}" height="{cta_h}" rx="14" fill="{P["blue"]}"/>')
    svg_parts.append(f'<text x="100" y="{y+cta_h/2+6}" font-family="DejaVu Sans" font-size="17" font-weight="bold" fill="#fff">{esc(cta_text)}</text>')
    svg_parts.append(f'<text x="{70+table_w-30}" y="{y+cta_h/2+5}" font-family="DejaVu Sans Mono" font-size="13" fill="#e3f1ff" text-anchor="end">{esc(cta_link)}</text>')
    y += cta_h + 44

    # ============ TAGLINE FINAL ============
    svg_parts.append(f'<line x1="70" y1="{y}" x2="{W-70}" y2="{y}" stroke="{P["border"]}" stroke-width="1"/>')
    y += 40
    tagline_lines, ntag = wrap_tspans(tagline, W/2, 44, 20, anchor="middle")
    svg_parts.append(f'<text x="{W/2}" y="{y}" font-family="DejaVu Sans" font-size="20" font-weight="bold" fill="{P["text"]}" text-anchor="middle">{tagline_lines}</text>')
    y += ntag*20*1.35 + 20
    svg_parts.append(f'<text x="{W/2}" y="{y}" font-family="DejaVu Sans Mono" font-size="12" fill="{P["text3"]}" text-anchor="middle">{esc(footer_note)}</text>')
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
