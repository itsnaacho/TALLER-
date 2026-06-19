#!/usr/bin/env python3
"""Generador PPT Taller 3 — Análisis de Redes Complejas · Estilo universitario moderno"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ── Paleta de colores ────────────────────────────────────────────────────────
AZUL_OSC  = RGBColor(0x1A, 0x4F, 0x8A)   # azul universidad oscuro
AZUL_MED  = RGBColor(0x2E, 0x75, 0xB6)   # azul medio
AZUL_CLAR = RGBColor(0xBD, 0xD7, 0xEE)   # azul claro fondo
VERDE     = RGBColor(0x37, 0x86, 0x4C)   # verde acento
VERDE_CL  = RGBColor(0xE2, 0xEF, 0xDA)   # verde claro tabla
GRIS      = RGBColor(0x59, 0x59, 0x59)   # gris texto
GRIS_CL   = RGBColor(0xF2, 0xF2, 0xF2)   # gris claro fila par
BLANCO    = RGBColor(0xFF, 0xFF, 0xFF)
NEGRO     = RGBColor(0x00, 0x00, 0x00)
NARANJA   = RGBColor(0xED, 0x7D, 0x31)   # acento naranja
ROJO_CL   = RGBColor(0xFF, 0xE6, 0xE6)

# Dimensiones 16:9
W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

blank_layout = prs.slide_layouts[6]  # completamente en blanco

# ── Helpers ───────────────────────────────────────────────────────────────────
def add_rect(slide, x, y, w, h, fill=None, line=None, line_w=None):
    shape = slide.shapes.add_shape(1, x, y, w, h)  # MSO_SHAPE_TYPE.RECTANGLE
    shape.line.fill.background()
    if fill:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill
    else:
        shape.fill.background()
    if line:
        shape.line.color.rgb = line
        if line_w:
            shape.line.width = line_w
    else:
        shape.line.fill.background()
    return shape

def add_text(slide, text, x, y, w, h, size=18, bold=False, color=NEGRO,
             align=PP_ALIGN.LEFT, italic=False, wrap=True):
    txBox = slide.shapes.add_textbox(x, y, w, h)
    tf = txBox.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = "Calibri"
    return txBox

def add_multiline(slide, lines, x, y, w, h, size=14, bold=False, color=NEGRO,
                  align=PP_ALIGN.LEFT, line_spacing=None):
    """lines: lista de (texto, bold_override, size_override, color_override)"""
    txBox = slide.shapes.add_textbox(x, y, w, h)
    tf = txBox.text_frame
    tf.word_wrap = True
    first = True
    for item in lines:
        if isinstance(item, str):
            txt, b, sz, col = item, bold, size, color
        else:
            txt = item[0]
            b   = item[1] if len(item) > 1 else bold
            sz  = item[2] if len(item) > 2 else size
            col = item[3] if len(item) > 3 else color

        if first:
            p = tf.paragraphs[0]
            first = False
        else:
            p = tf.add_paragraph()
        p.alignment = align
        run = p.add_run()
        run.text = txt
        run.font.size = Pt(sz)
        run.font.bold = b
        run.font.color.rgb = col
        run.font.name = "Calibri"
    return txBox

def add_table(slide, data, x, y, w, h, header_fill=AZUL_OSC,
              col_widths=None, font_size=11, alt_rows=True):
    rows = len(data)
    cols = len(data[0])
    tbl  = slide.shapes.add_table(rows, cols, x, y, w, h).table

    if col_widths:
        total = sum(col_widths)
        for i, cw in enumerate(col_widths):
            tbl.columns[i].width = int(w * cw / total)

    for r, row in enumerate(data):
        for c, cell_val in enumerate(row):
            cell = tbl.cell(r, c)
            cell.text = str(cell_val)
            tf = cell.text_frame
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            run = tf.paragraphs[0].runs[0] if tf.paragraphs[0].runs else tf.paragraphs[0].add_run()
            run.font.name = "Calibri"
            run.font.size = Pt(font_size)

            if r == 0:
                cell.fill.solid()
                cell.fill.fore_color.rgb = header_fill
                run.font.bold = True
                run.font.color.rgb = BLANCO
            else:
                if alt_rows and r % 2 == 0:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = GRIS_CL
                else:
                    cell.fill.solid()
                    cell.fill.fore_color.rgb = BLANCO
                run.font.color.rgb = NEGRO
    return tbl

def chip(slide, text, x, y, w=Inches(1.6), h=Inches(0.35),
         fill=AZUL_MED, text_color=BLANCO, size=10):
    """Pequeña etiqueta/chip redondeado (simulated with rect)."""
    r = add_rect(slide, x, y, w, h, fill=fill)
    add_text(slide, text, x, y, w, h, size=size, bold=True,
             color=text_color, align=PP_ALIGN.CENTER)

def bar_manual(slide, valores, etiquetas, x, y, w, h,
               bar_color=AZUL_MED, label_color=GRIS, max_val=None):
    """Gráfico de barras horizontal dibujado manualmente."""
    n = len(valores)
    if max_val is None:
        max_val = max(valores) * 1.05
    bar_h = h / (n * 1.5)
    gap   = bar_h * 0.5
    label_w = Inches(1.1)
    val_w   = Inches(0.5)
    chart_w = w - label_w - val_w

    for i, (val, lbl) in enumerate(zip(valores, etiquetas)):
        yi = y + i * (bar_h + gap)
        # etiqueta izquierda
        add_text(slide, str(lbl), x, yi, label_w, bar_h,
                 size=9, color=GRIS, align=PP_ALIGN.RIGHT)
        # barra
        bw = chart_w * (val / max_val)
        add_rect(slide, x + label_w + Inches(0.05), yi, bw, bar_h, fill=bar_color)
        # valor
        add_text(slide, str(val), x + label_w + bw + Inches(0.08), yi,
                 val_w, bar_h, size=9, bold=True, color=AZUL_OSC)

def slide_header(slide, title, subtitle=None, accent_color=AZUL_MED):
    """Franja superior azul con título."""
    add_rect(slide, 0, 0, W, Inches(1.15), fill=AZUL_OSC)
    add_text(slide, title, Inches(0.4), Inches(0.08), W - Inches(5),
             Inches(0.55), size=22, bold=True, color=BLANCO)
    if subtitle:
        add_text(slide, subtitle, Inches(0.4), Inches(0.62), W - Inches(5),
                 Inches(0.42), size=13, color=AZUL_CLAR)
    # línea decorativa
    add_rect(slide, 0, Inches(1.15), W, Inches(0.055), fill=accent_color)
    # numeración (se añade después)

def slide_footer(slide, num, total=13):
    """Pie de página discreto."""
    add_rect(slide, 0, H - Inches(0.38), W, Inches(0.38), fill=AZUL_OSC)
    add_text(slide, "Taller 3 · Análisis de Redes Complejas · APPD 2026   |   I. Tobar Suárez",
             Inches(0.3), H - Inches(0.36), Inches(9), Inches(0.34),
             size=8, color=AZUL_CLAR)
    add_text(slide, f"{num}/{total}", W - Inches(1.1), H - Inches(0.36),
             Inches(0.8), Inches(0.34), size=8, bold=True,
             color=BLANCO, align=PP_ALIGN.RIGHT)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 1 — PORTADA
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)

# Fondo degradado simulado — dos rectángulos
add_rect(sl, 0, 0, W, H, fill=AZUL_OSC)
add_rect(sl, 0, 0, W * 0.55, H, fill=RGBColor(0x0D, 0x2F, 0x5C))

# Línea vertical decorativa
add_rect(sl, W * 0.55 - Inches(0.06), 0, Inches(0.06), H, fill=AZUL_MED)

# Ícono de red (círculos decorativos — simulación)
for cx, cy, r, op in [
    (W*0.73, H*0.28, Inches(0.55), RGBColor(0x2E,0x75,0xB6)),
    (W*0.86, H*0.48, Inches(0.38), RGBColor(0x2E,0x75,0xB6)),
    (W*0.69, H*0.55, Inches(0.28), RGBColor(0x1A,0x4F,0x8A)),
    (W*0.80, H*0.25, Inches(0.20), RGBColor(0x37,0x86,0x4C)),
    (W*0.92, H*0.32, Inches(0.25), RGBColor(0x1A,0x4F,0x8A)),
]:
    add_rect(sl, cx, cy, r, r, fill=op)

# Texto portada
add_text(sl, "TALLER 3", Inches(0.55), Inches(1.2), Inches(6.5), Inches(0.7),
         size=13, bold=False, color=AZUL_CLAR, align=PP_ALIGN.LEFT)
add_text(sl, "Análisis de Redes\nComplejas con Gephi",
         Inches(0.55), Inches(1.8), Inches(6.5), Inches(2.0),
         size=36, bold=True, color=BLANCO, align=PP_ALIGN.LEFT)
add_rect(sl, Inches(0.55), Inches(3.85), Inches(2.5), Inches(0.05), fill=VERDE)
add_text(sl, "Red de Colaboración Científica ca-GrQc\nSNAP — Stanford University",
         Inches(0.55), Inches(3.95), Inches(6.5), Inches(0.9),
         size=13, color=AZUL_CLAR, align=PP_ALIGN.LEFT)

add_text(sl, "Curso: Aproximación a las Políticas Públicas desde los Datos",
         Inches(0.55), Inches(5.1), Inches(6.5), Inches(0.4),
         size=11, color=AZUL_CLAR)
add_text(sl, "Prof. Dr. Rodrigo Salas  ·  1er Semestre 2026",
         Inches(0.55), Inches(5.48), Inches(6.5), Inches(0.35),
         size=11, color=AZUL_CLAR)
add_text(sl, "I. Tobar Suárez  ·  19 de junio del 2026",
         Inches(0.55), Inches(5.86), Inches(6.5), Inches(0.35),
         size=11, bold=True, color=BLANCO)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 2 — AGENDA
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Contenido de la Presentación")
slide_footer(sl, 2)

items = [
    ("01", "Descripción del Dataset ca-GrQc"),
    ("02", "Eigenvector Centrality — Autores más influyentes"),
    ("03", "Degree Centrality — Autores más colaborativos"),
    ("04", "Betweenness Centrality — Autores puente"),
    ("05", "Closeness Centrality — Autores más cercanos"),
    ("06", "Cuadro comparativo de métricas"),
    ("07", "Comunidades — Algoritmo de Modularidad"),
    ("08", "Comunidad más grande (C0)"),
    ("09", "Comunidad más compacta (C17)"),
    ("10", "Síntesis y Conclusiones"),
]

col1 = items[:5]
col2 = items[5:]

for i, (num, txt) in enumerate(col1):
    y = Inches(1.45) + i * Inches(0.94)
    add_rect(sl, Inches(0.5), y, Inches(0.55), Inches(0.55), fill=AZUL_OSC)
    add_text(sl, num, Inches(0.5), y + Inches(0.05), Inches(0.55), Inches(0.45),
             size=14, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
    add_text(sl, txt, Inches(1.15), y + Inches(0.08), Inches(5.2), Inches(0.44),
             size=12.5, color=GRIS)

for i, (num, txt) in enumerate(col2):
    y = Inches(1.45) + i * Inches(0.94)
    add_rect(sl, Inches(7.1), y, Inches(0.55), Inches(0.55), fill=AZUL_MED)
    add_text(sl, num, Inches(7.1), y + Inches(0.05), Inches(0.55), Inches(0.45),
             size=14, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
    add_text(sl, txt, Inches(7.75), y + Inches(0.08), Inches(5.2), Inches(0.44),
             size=12.5, color=GRIS)

add_rect(sl, Inches(6.6), Inches(1.35), Inches(0.05), Inches(5.5), fill=AZUL_CLAR)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 3 — DATASET
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Descripción del Dataset", "ca-GrQc · General Relativity and Quantum Cosmology")
slide_footer(sl, 3)

add_text(sl, "Red de colaboración científica de arXiv (1993–2003). Cada nodo = autor, cada arista = co-publicación.",
         Inches(0.4), Inches(1.3), Inches(12.5), Inches(0.45), size=12, color=GRIS)

# Tarjetas de estadísticas
cards = [
    ("5.242", "Nodos (autores)", AZUL_OSC),
    ("14.496", "Aristas (colaboraciones)", AZUL_MED),
    ("355", "Componentes conexos", VERDE),
    ("4.158", "Nodos en componente\nprincipal (79,3%)", NARANJA),
]
for i, (val, lbl, col) in enumerate(cards):
    cx = Inches(0.4) + i * Inches(3.2)
    add_rect(sl, cx, Inches(1.85), Inches(3.0), Inches(1.65), fill=col)
    add_text(sl, val, cx, Inches(2.0), Inches(3.0), Inches(0.8),
             size=30, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
    add_text(sl, lbl, cx, Inches(2.82), Inches(3.0), Inches(0.55),
             size=10, color=RGBColor(0xDD,0xEA,0xF7), align=PP_ALIGN.CENTER)

# Info adicional
add_rect(sl, Inches(0.4), Inches(3.7), Inches(12.5), Inches(0.06), fill=AZUL_CLAR)

info_items = [
    ("Tipo de grafo", "No dirigido, estático"),
    ("Diámetro", "17 saltos"),
    ("Longitud promedio de camino", "6,05 pasos"),
    ("Grado promedio", "5,53 colaboraciones"),
    ("Fuente", "SNAP Stanford (snap.stanford.edu/data/ca-GrQc.html)"),
]
for i, (k, v) in enumerate(info_items):
    y = Inches(3.9) + i * Inches(0.56)
    add_text(sl, k + ":", Inches(0.5), y, Inches(3.8), Inches(0.48),
             size=11, bold=True, color=AZUL_OSC)
    add_text(sl, v, Inches(4.2), y, Inches(8.5), Inches(0.48),
             size=11, color=GRIS)

# Nota metodológica
add_rect(sl, Inches(0.4), H - Inches(1.15), Inches(12.5), Inches(0.68),
         fill=RGBColor(0xFF,0xF2,0xCC))
add_text(sl, "⚠  Nota metodológica: todas las métricas de centralidad se calcularon sobre el "
             "componente principal (4.158 nodos) para garantizar comparabilidad. "
             "Calcularlas sobre el grafo completo genera artefactos graves en componentes aislados.",
         Inches(0.6), H - Inches(1.1), Inches(12.2), Inches(0.62),
         size=9.5, color=RGBColor(0x5C,0x40,0x00), italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 4 — EIGENVECTOR
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Eigenvector Centrality", "¿Quiénes son los autores más influyentes?", accent_color=VERDE)
slide_footer(sl, 4)

# Definición
add_rect(sl, Inches(0.4), Inches(1.3), Inches(5.8), Inches(1.4),
         fill=RGBColor(0xE8, 0xF4, 0xFD))
add_text(sl, "¿Qué mide?", Inches(0.5), Inches(1.32), Inches(5.6), Inches(0.38),
         size=11, bold=True, color=AZUL_OSC)
add_text(sl, "No solo cuántas conexiones tiene un nodo, sino cuán importantes son "
             "sus vecinos. Alta influencia = estar rodeado de autores igualmente influyentes.",
         Inches(0.5), Inches(1.68), Inches(5.6), Inches(0.9),
         size=10.5, color=GRIS)

# Tabla top 10
tabla_data = [
    ["Rank", "Nodo ID", "Eigenvector"],
    ["1", "21012", "0,1556"],
    ["2", "2741",  "0,1536"],
    ["3", "12365", "0,1531"],
    ["4", "21508", "0,1512"],
    ["5", "9785",  "0,1509"],
    ["6", "15003", "0,1504"],
    ["7", "25346", "0,1491"],
    ["8", "7956",  "0,1491"],
    ["9", "14807", "0,1490"],
    ["10","12781", "0,1489"],
]
add_table(sl, tabla_data, Inches(0.4), Inches(2.85), Inches(5.8), Inches(3.8),
          col_widths=[1, 1.5, 2])

# Gráfico de barras
bar_vals = [0.1556, 0.1536, 0.1531, 0.1512, 0.1509, 0.1504, 0.1491, 0.1491, 0.1490, 0.1489]
bar_lbs  = ["21012","2741","12365","21508","9785","15003","25346","7956","14807","12781"]
bar_manual(sl, bar_vals, bar_lbs,
           Inches(6.5), Inches(1.3), Inches(6.5), Inches(5.2),
           bar_color=AZUL_MED, max_val=0.165)

# Respuesta pregunta
add_rect(sl, Inches(0.4), H - Inches(1.0), Inches(5.8), Inches(0.58),
         fill=VERDE_CL)
add_text(sl, "💡  El nodo 21012 tiene 81 colaboraciones directas con autores igualmente activos. "
             "Influencia ≠ cantidad de vínculos — importa la calidad de las conexiones.",
         Inches(0.5), H - Inches(0.98), Inches(5.7), Inches(0.56),
         size=9, color=NEGRO, italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 5 — DEGREE
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Degree Centrality", "¿Quiénes tienen más colaboraciones?", accent_color=NARANJA)
slide_footer(sl, 5)

add_rect(sl, Inches(0.4), Inches(1.3), Inches(5.8), Inches(1.4),
         fill=RGBColor(0xFD, 0xF0, 0xE8))
add_text(sl, "¿Qué mide?", Inches(0.5), Inches(1.32), Inches(5.6), Inches(0.38),
         size=11, bold=True, color=NARANJA)
add_text(sl, "Número de colaboradores únicos de cada autor. Medida directa de actividad "
             "colaborativa. El grado promedio de la red es solo 5,53.",
         Inches(0.5), Inches(1.68), Inches(5.6), Inches(0.9),
         size=10.5, color=GRIS)

tabla_data = [
    ["Rank", "Nodo ID", "Grado"],
    ["1",  "21012", "81"],
    ["2",  "21281", "79"],
    ["3",  "22691", "77"],
    ["4",  "12365", "77"],
    ["5",  "6610",  "68"],
    ["6",  "9785",  "68"],
    ["7",  "21508", "67"],
    ["8",  "17655", "66"],
    ["9",  "2741",  "65"],
    ["10", "19423", "63"],
]
add_table(sl, tabla_data, Inches(0.4), Inches(2.85), Inches(5.8), Inches(3.8),
          header_fill=NARANJA, col_widths=[1, 1.5, 2])

bar_vals = [81, 79, 77, 77, 68, 68, 67, 66, 65, 63]
bar_lbs  = ["21012","21281","22691","12365","6610","9785","21508","17655","2741","19423"]
bar_manual(sl, bar_vals, bar_lbs,
           Inches(6.5), Inches(1.3), Inches(6.5), Inches(5.2),
           bar_color=NARANJA, max_val=90)

add_rect(sl, Inches(0.4), H - Inches(1.0), Inches(5.8), Inches(0.58), fill=RGBColor(0xFF,0xF0,0xDD))
add_text(sl, "💡  El nodo 21012 tiene 81 colaboraciones: 15× más que el promedio. "
             "Distribución tipo ley de potencia — red libre de escala (scale-free).",
         Inches(0.5), H - Inches(0.98), Inches(5.7), Inches(0.56),
         size=9, color=NEGRO, italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 6 — BETWEENNESS
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Betweenness Centrality", "¿Quiénes actúan como puente entre grupos?", accent_color=RGBColor(0x70,0x30,0xA0))
slide_footer(sl, 6)

add_rect(sl, Inches(0.4), Inches(1.3), Inches(5.8), Inches(1.4),
         fill=RGBColor(0xF3, 0xE8, 0xFD))
add_text(sl, "¿Qué mide?", Inches(0.5), Inches(1.32), Inches(5.6), Inches(0.38),
         size=11, bold=True, color=RGBColor(0x70,0x30,0xA0))
add_text(sl, "Fracción de caminos mínimos entre todos los pares de nodos que "
             "pasan por un autor. Alto valor → puente estructural entre comunidades.",
         Inches(0.5), Inches(1.68), Inches(5.6), Inches(0.9),
         size=10.5, color=GRIS)

tabla_data = [
    ["Rank", "Nodo ID", "Betweenness", "Comunidad"],
    ["1",  "13801", "0,0589", "C0"],
    ["2",  "9572",  "0,0408", "C0"],
    ["3",  "14599", "0,0405", "C0"],
    ["4",  "7689",  "0,0397", "C2"],
    ["5",  "13929", "0,0392", "C0"],
    ["6",  "5052",  "0,0388", "C3"],
    ["7",  "14485", "0,0374", "C1"],
    ["8",  "2710",  "0,0355", "C2"],
    ["9",  "14265", "0,0314", "C4"],
    ["10", "17655", "0,0286", "C0"],
]
add_table(sl, tabla_data, Inches(0.4), Inches(2.85), Inches(5.8), Inches(3.8),
          header_fill=RGBColor(0x70,0x30,0xA0), col_widths=[0.8, 1.3, 1.8, 1.3])

# Esquema visual de puente
add_rect(sl, Inches(6.5), Inches(1.3), Inches(6.5), Inches(5.2),
         fill=RGBColor(0xFA,0xFA,0xFA))
# Comunidades como círculos (representación esquemática)
for cx, cy, r, lbl, col in [
    (Inches(8.0),  Inches(2.6), Inches(0.8),  "C0\n901 nodos", AZUL_OSC),
    (Inches(10.5), Inches(2.0), Inches(0.55), "C1\n395 nodos", AZUL_MED),
    (Inches(11.2), Inches(3.5), Inches(0.5),  "C2\n332 nodos", VERDE),
    (Inches(9.4),  Inches(4.4), Inches(0.45), "C3\n270 nodos", NARANJA),
]:
    add_rect(sl, cx - r/2, cy - r/2, r, r, fill=col)
    add_text(sl, lbl, cx - r/2, cy - r*0.35, r, r*0.7,
             size=8, color=BLANCO, bold=True, align=PP_ALIGN.CENTER)

# Flechas/líneas representadas como rectángulos delgados
for x1, y1, x2, y2 in [
    (Inches(8.8),  Inches(2.4), Inches(9.95), Inches(2.25)),
    (Inches(8.8),  Inches(2.9), Inches(10.75),Inches(3.25)),
    (Inches(8.6),  Inches(3.1), Inches(9.2),  Inches(4.0)),
]:
    add_rect(sl, x1, y1, x2-x1, Inches(0.04), fill=AZUL_CLAR)

add_text(sl, "Nodo 13801\n(puente C0→C1,C2,C3)",
         Inches(6.8), Inches(4.8), Inches(3.5), Inches(0.6),
         size=10, bold=True, color=AZUL_OSC, align=PP_ALIGN.CENTER)

add_rect(sl, Inches(0.4), H - Inches(1.0), Inches(5.8), Inches(0.58), fill=RGBColor(0xF3,0xE8,0xFD))
add_text(sl, "💡  Si se eliminan 13801 + 9572 + 14599, el componente principal podría "
             "fragmentarse. Las comunidades C1, C2 y C3 (24% de los nodos) quedarían parcialmente aisladas.",
         Inches(0.5), H - Inches(0.98), Inches(5.7), Inches(0.56),
         size=9, color=NEGRO, italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 7 — CLOSENESS
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Closeness Centrality", "¿Quiénes difunden información más rápido?", accent_color=VERDE)
slide_footer(sl, 7)

add_rect(sl, Inches(0.4), Inches(1.3), Inches(5.8), Inches(1.4),
         fill=RGBColor(0xE8, 0xF6, 0xEE))
add_text(sl, "¿Qué mide?", Inches(0.5), Inches(1.32), Inches(5.6), Inches(0.38),
         size=11, bold=True, color=VERDE)
add_text(sl, "Inverso de la suma de distancias a todos los nodos alcanzables. "
             "Valor alto → el autor llega al resto de la red en muy pocos pasos.",
         Inches(0.5), Inches(1.68), Inches(5.6), Inches(0.9),
         size=10.5, color=GRIS)

tabla_data = [
    ["Rank", "Nodo ID", "Closeness"],
    ["1",  "13801", "0,2449"],
    ["2",  "14485", "0,2390"],
    ["3",  "9572",  "0,2383"],
    ["4",  "17655", "0,2382"],
    ["5",  "2654",  "0,2359"],
    ["6",  "21012", "0,2352"],
    ["7",  "12545", "0,2345"],
    ["8",  "25006", "0,2340"],
    ["9",  "12365", "0,2336"],
    ["10", "22691", "0,2329"],
]
add_table(sl, tabla_data, Inches(0.4), Inches(2.85), Inches(5.8), Inches(3.8),
          header_fill=VERDE, col_widths=[1, 1.5, 2])

# Panel derecho — visualización conceptual de pasos
add_rect(sl, Inches(6.5), Inches(1.3), Inches(6.5), Inches(5.2),
         fill=RGBColor(0xF0, 0xF8, 0xF2))
add_text(sl, "Distancia media al resto de la red",
         Inches(6.7), Inches(1.4), Inches(6.1), Inches(0.45),
         size=12, bold=True, color=VERDE)

comparaciones = [
    ("Nodo 13801 (top Closeness)", 4.08, VERDE),
    ("Nodo promedio de la red",    6.05, GRIS),
    ("Nodo periférico (aprox.)",   9.50, RGBColor(0xC0,0xC0,0xC0)),
]
for i, (lbl, val, col) in enumerate(comparaciones):
    y = Inches(2.1) + i * Inches(1.4)
    add_text(sl, lbl, Inches(6.7), y, Inches(6.1), Inches(0.38), size=10, bold=True, color=col)
    bw = Inches(5.5) * (val / 10)
    add_rect(sl, Inches(6.7), y + Inches(0.42), bw, Inches(0.45), fill=col)
    add_text(sl, f"{val} pasos", Inches(6.7) + bw + Inches(0.1), y + Inches(0.42),
             Inches(1.5), Inches(0.45), size=10, bold=True, color=col)

add_rect(sl, Inches(0.4), H - Inches(1.0), Inches(5.8), Inches(0.58), fill=VERDE_CL)
add_text(sl, "💡  El nodo 13801 alcanza a cualquier autor del componente principal "
             "en solo 4,08 pasos (vs. 6,05 del promedio). Ventaja epistémica: "
             "recibe y disemina conocimiento más rápido.",
         Inches(0.5), H - Inches(0.98), Inches(5.7), Inches(0.56),
         size=9, color=NEGRO, italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 8 — CUADRO COMPARATIVO
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Cuadro Comparativo de Métricas", "¿Qué autores dominan en más dimensiones?")
slide_footer(sl, 8)

tabla_data = [
    ["Nodo",  "Degree", "Eigenvector", "Betweenness", "Closeness", "Total"],
    ["21012", "#1 ✓",   "#1 ✓",        "—",           "#6 ✓",     "3"],
    ["12365", "#3 ✓",   "#3 ✓",        "—",           "#9 ✓",     "3"],
    ["17655", "#8 ✓",   "—",           "#10 ✓",       "#4 ✓",     "3"],
    ["2741",  "#9 ✓",   "#2 ✓",        "—",           "—",        "2"],
    ["21508", "#7 ✓",   "#4 ✓",        "—",           "—",        "2"],
    ["9785",  "#6 ✓",   "#5 ✓",        "—",           "—",        "2"],
    ["22691", "#3 ✓",   "—",           "—",           "#10 ✓",    "2"],
    ["13801", "—",       "—",           "#1 ✓",        "#1 ✓",     "2"],
    ["9572",  "—",       "—",           "#2 ✓",        "#3 ✓",     "2"],
    ["14485", "—",       "—",           "#7 ✓",        "#2 ✓",     "2"],
    ["21281", "#2 ✓",   "—",           "—",           "—",        "1"],
    ["…otros 17 nodos", "(1 métrica c/u)", "—", "—",  "—",        "1"],
]
add_table(sl, tabla_data, Inches(0.3), Inches(1.3), Inches(8.5), Inches(5.5),
          col_widths=[1.4, 1.4, 1.7, 1.8, 1.6, 1.1], font_size=10)

# Panel de análisis
add_rect(sl, Inches(9.0), Inches(1.3), Inches(4.1), Inches(5.5),
         fill=RGBColor(0xEA, 0xF4, 0xFF))

add_text(sl, "Perfiles destacados", Inches(9.1), Inches(1.4), Inches(3.9), Inches(0.45),
         size=12, bold=True, color=AZUL_OSC)

perfiles = [
    ("🏆 El más versátil", "Nodo 21012\nDegree + Eigenvector + Closeness", AZUL_OSC),
    ("🌉 El puente clave",  "Nodo 13801\nBetweenness + Closeness #1", RGBColor(0x70,0x30,0xA0)),
    ("⚡ Influencia alta",  "Nodo 12365\nDegree + Eigenvector + Closeness", VERDE),
]
for i, (titulo, desc, col) in enumerate(perfiles):
    y = Inches(1.95) + i * Inches(1.55)
    add_rect(sl, Inches(9.1), y, Inches(3.8), Inches(1.35), fill=col)
    add_text(sl, titulo, Inches(9.2), y + Inches(0.08), Inches(3.6), Inches(0.45),
             size=10.5, bold=True, color=BLANCO)
    add_text(sl, desc, Inches(9.2), y + Inches(0.5), Inches(3.6), Inches(0.75),
             size=9.5, color=RGBColor(0xDD,0xEE,0xFF))

add_text(sl, "Conclusión: influencia es multidimensional.\nNingún autor domina todas las métricas.",
         Inches(9.1), Inches(6.6), Inches(3.9), Inches(0.55),
         size=9.5, italic=True, color=AZUL_OSC)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 9 — COMUNIDADES
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Detección de Comunidades", "Algoritmo de Modularidad de Louvain · Q = 0,80")
slide_footer(sl, 9)

# Estadísticas generales
stats = [
    ("63", "comunidades\ndetectadas", AZUL_OSC),
    ("0,80", "Modularidad Q\n(muy alta)", VERDE),
    ("901", "nodos en la\ncomunidad mayor", AZUL_MED),
    ("10", "comunidades\ncon > 100 nodos", NARANJA),
]
for i, (val, lbl, col) in enumerate(stats):
    cx = Inches(0.4) + i * Inches(3.2)
    add_rect(sl, cx, Inches(1.3), Inches(3.0), Inches(1.5), fill=col)
    add_text(sl, val, cx, Inches(1.38), Inches(3.0), Inches(0.75),
             size=28, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
    add_text(sl, lbl, cx, Inches(2.1), Inches(3.0), Inches(0.6),
             size=9.5, color=RGBColor(0xDD,0xEE,0xFF), align=PP_ALIGN.CENTER)

# Tabla distribución
tabla_data = [
    ["Comunidad", "Nodos", "% del componente"],
    ["C0",  "901", "21,7%"],
    ["C1",  "395", " 9,5%"],
    ["C2",  "332", " 8,0%"],
    ["C3",  "270", " 6,5%"],
    ["C4",  "230", " 5,5%"],
    ["C5–C9", "895 (total)", "21,5%"],
    ["C10–C19","561 (total)","13,5%"],
    ["C20–C37","~350 total", " 8,4%"],
    ["C38–C62","~211 total", " 5,1%"],
]
add_table(sl, tabla_data, Inches(0.4), Inches(3.0), Inches(5.5), Inches(4.0),
          col_widths=[1.8, 1.8, 2.5], font_size=10)

# Gráfico de distribución (barras)
bar_vals2 = [901, 395, 332, 270, 230, 895, 561]
bar_lbs2  = ["C0","C1","C2","C3","C4","C5–C9","C10–C19"]
bar_manual(sl, bar_vals2, bar_lbs2,
           Inches(6.2), Inches(3.0), Inches(6.8), Inches(3.8),
           bar_color=AZUL_MED, max_val=1000)

add_rect(sl, Inches(0.4), H - Inches(1.0), Inches(12.5), Inches(0.58),
         fill=VERDE_CL)
add_text(sl, "💡  La red no está ni completamente fragmentada ni centralizada. "
             "Estructura intermedia: grandes comunidades temáticas + muchos grupos pequeños. "
             "Cada comunidad = posible subárea de la relatividad general.",
         Inches(0.6), H - Inches(0.98), Inches(12.2), Inches(0.56),
         size=9.5, color=NEGRO, italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 10 — COMUNIDAD MÁS GRANDE
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Comunidad más Grande — C0", "901 nodos · El núcleo articulador de la red")
slide_footer(sl, 10)

tabla_data = [
    ["Parámetro",                     "Valor"],
    ["Número de nodos",               "901"],
    ["Número de aristas",             "2.150"],
    ["Densidad",                      "0,0053 (baja)"],
    ["Clustering promedio",           "0,5115 (sorprendentemente alto)"],
    ["Autor más influyente (Eigen.)", "Nodo 13929 (0,2369)"],
    ["Autor más colaborador (Deg.)",  "Nodo 13801 (38 colab.)"],
    ["Mayor intermediación (Betw.)",  "Nodo 14599 (0,1283)"],
]
add_table(sl, tabla_data, Inches(0.4), Inches(1.3), Inches(6.2), Inches(4.6),
          col_widths=[3.5, 3], font_size=10.5)

# Panel conceptual
add_rect(sl, Inches(6.9), Inches(1.3), Inches(6.1), Inches(4.6),
         fill=RGBColor(0xEA, 0xF2, 0xFF))
add_text(sl, "¿Qué nos dice esto?", Inches(7.0), Inches(1.38), Inches(5.9), Inches(0.45),
         size=12, bold=True, color=AZUL_OSC)

insights = [
    ("Liderazgos especializados:", "3 nodos distintos dominan cada métrica → no hay un solo 'jefe'", AZUL_OSC),
    ("Alta cohesión interna:", "Clustering 0,51 → triángulos de colaboración frecuentes", VERDE),
    ("Núcleo global:", "Concentra los nodos de mayor Betweenness y Closeness de TODA la red", NARANJA),
]
for i, (titulo, desc, col) in enumerate(insights):
    y = Inches(1.95) + i * Inches(1.25)
    add_rect(sl, Inches(7.0), y, Inches(0.08), Inches(0.9), fill=col)
    add_text(sl, titulo, Inches(7.2), y, Inches(5.6), Inches(0.38),
             size=10.5, bold=True, color=col)
    add_text(sl, desc, Inches(7.2), y + Inches(0.4), Inches(5.6), Inches(0.5),
             size=10, color=GRIS)

add_rect(sl, Inches(0.4), H - Inches(1.05), Inches(12.5), Inches(0.62),
         fill=AZUL_CLAR)
add_text(sl, "C0 SÍ es la comunidad central. El nodo 13801 (miembro de C0) tiene el mayor "
             "Betweenness y Closeness de toda la red → C0 actúa como 'hub' global.",
         Inches(0.6), H - Inches(1.03), Inches(12.2), Inches(0.6),
         size=10, bold=True, color=AZUL_OSC)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 11 — COMUNIDAD MÁS COMPACTA
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Comunidad más Compacta — C17", "47 nodos · Densidad 0,684 · Clustering 0,860", accent_color=VERDE)
slide_footer(sl, 11)

tabla_data = [
    ["Parámetro",               "Valor"],
    ["Número de nodos",         "47"],
    ["Número de aristas",       "739"],
    ["Densidad",                "0,684 (muy alta)"],
    ["Clustering promedio",     "0,860 (muy alto)"],
    ["Top autor (Degree)",      "Nodo 6512 (41 conexiones)"],
    ["Top autor (Eigenvector)", "Nodo 6512 (0,171)"],
    ["Liderazgo similar",       "Nodos 16654 y 17807 (deg. 40)"],
]
add_table(sl, tabla_data, Inches(0.4), Inches(1.3), Inches(5.8), Inches(4.5),
          header_fill=VERDE, col_widths=[3, 3], font_size=10.5)

# Visualización conceptual de densidad
add_rect(sl, Inches(6.5), Inches(1.3), Inches(6.5), Inches(5.6),
         fill=RGBColor(0xF0, 0xFA, 0xF2))
add_text(sl, "Comparativa de densidad", Inches(6.7), Inches(1.38), Inches(6.0), Inches(0.4),
         size=12, bold=True, color=VERDE)

comparativas = [
    ("C17 (más compacta)", 0.684, VERDE),
    ("C0 (más grande)",    0.005, AZUL_OSC),
    ("Red completa",       0.001, GRIS),
]
for i, (lbl, val, col) in enumerate(comparativas):
    y = Inches(1.95) + i * Inches(1.3)
    add_text(sl, lbl, Inches(6.7), y, Inches(6.1), Inches(0.38), size=10.5, bold=True, color=col)
    bw = Inches(5.5) * val
    bw = max(bw, Inches(0.08))
    add_rect(sl, Inches(6.7), y + Inches(0.44), bw, Inches(0.5), fill=col)
    add_text(sl, f"{val:.3f}", Inches(6.7) + bw + Inches(0.1), y + Inches(0.44),
             Inches(1.2), Inches(0.5), size=10, bold=True, color=col)

add_text(sl, "→ El 68,4% de todas las colaboraciones posibles entre sus 47 miembros existen.",
         Inches(6.7), Inches(5.45), Inches(6.1), Inches(0.5),
         size=10, color=VERDE, italic=True)

add_rect(sl, Inches(0.4), H - Inches(1.05), Inches(12.5), Inches(0.62), fill=VERDE_CL)
add_text(sl, "💡  Alta densidad → equipo de investigación consolidado (misma institución o problema científico específico). "
             "Liderazgo tripartito (6512, 16654, 17807) → mayor resiliencia. Riesgo: 'cámara de eco'.",
         Inches(0.6), H - Inches(1.03), Inches(12.2), Inches(0.6),
         size=9.5, color=NEGRO, italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 12 — CONCLUSIONES
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=RGBColor(0xF7, 0xF9, 0xFC))
slide_header(sl, "Síntesis y Conclusiones")
slide_footer(sl, 12)

conclusiones = [
    (AZUL_OSC, "Red libre de escala",
     "Una minoría de autores concentra la mayoría de colaboraciones "
     "(nodo 21012: 81 vs. promedio de 5,53). Distribución tipo ley de potencia."),
    (VERDE, "Influencia es multidimensional",
     "Ningún nodo domina las 4 métricas. Ser colaborativo ≠ ser influyente ≠ ser un puente."),
    (RGBColor(0x70,0x30,0xA0), "El nodo 13801 es el más estratégico",
     "Lidera Betweenness Y Closeness. Su eliminación fragmentaría la red más que "
     "la de cualquier otro autor. Es el 'puente crítico'."),
    (NARANJA, "Comunidades bien definidas (Q=0,80)",
     "63 comunidades detectadas = subcampos temáticos o grupos institucionales "
     "de la relatividad general y cosmología cuántica."),
    (RGBColor(0x0A, 0x70, 0x70), "Dos tipos de organización",
     "C0 (901 nodos): nucleo disperso pero articulador. "
     "C17 (47 nodos, densidad 0,68): equipo cohesionado y cerrado."),
]

for i, (col, titulo, desc) in enumerate(conclusiones):
    y = Inches(1.35) + i * Inches(1.08)
    add_rect(sl, Inches(0.4), y, Inches(0.35), Inches(0.9), fill=col)
    add_text(sl, titulo, Inches(0.85), y + Inches(0.04), Inches(11.8), Inches(0.4),
             size=11.5, bold=True, color=col)
    add_text(sl, desc, Inches(0.85), y + Inches(0.46), Inches(11.8), Inches(0.5),
             size=10.5, color=GRIS)

# ═══════════════════════════════════════════════════════════════════════════════
#  SLIDE 13 — REFERENCIAS
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank_layout)
add_rect(sl, 0, 0, W, H, fill=AZUL_OSC)
add_rect(sl, 0, 0, W, Inches(1.5), fill=RGBColor(0x0D, 0x2F, 0x5C))
add_text(sl, "Referencias", Inches(0.5), Inches(0.4), Inches(12.0), Inches(0.75),
         size=24, bold=True, color=BLANCO)
add_rect(sl, Inches(0.5), Inches(1.45), Inches(2.5), Inches(0.05), fill=VERDE)

refs = [
    "[1]  Blondel, V. D. et al. (2008). Fast unfolding of communities in large networks. Journal of Statistical Mechanics, P10008.",
    "[2]  Brandes, U. (2001). A faster algorithm for betweenness centrality. Journal of Mathematical Sociology, 25(2), 163–177.",
    "[3]  Leskovec, J., Kleinberg, J., & Faloutsos, C. (2007). Graph evolution: Densification and shrinking diameters. ACM TKDD, 1(1).",
    "[4]  Newman, M. E. J. (2004). Coauthorship networks and patterns of scientific collaboration. PNAS, 101(S1), 5200–5205.",
    "[5]  SNAP Stanford — General Relativity and Quantum Cosmology Collaboration Network. snap.stanford.edu/data/ca-GrQc.html",
    "[6]  Gephi Consortium (2023). Gephi 0.11.2 — The Open Graph Viz Platform. gephi.org",
]
for i, ref in enumerate(refs):
    y = Inches(1.7) + i * Inches(0.72)
    add_text(sl, ref, Inches(0.5), y, Inches(12.3), Inches(0.65),
             size=10, color=AZUL_CLAR)

add_text(sl, "¡Gracias por su atención!",
         Inches(0.5), H - Inches(1.4), Inches(12.0), Inches(0.7),
         size=20, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
add_rect(sl, Inches(4.5), H - Inches(0.75), Inches(4.3), Inches(0.05), fill=VERDE)

# ── Guardar ───────────────────────────────────────────────────────────────────
output = "/home/user/TALLER-/Taller3_Presentacion.pptx"
prs.save(output)
print(f"PPT generado: {output}")
