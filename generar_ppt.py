#!/usr/bin/env python3
"""PPT Taller 3 — versión estudiante: lenguaje simple, preguntas del profe visibles"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Paleta ───────────────────────────────────────────────────────────────────
AZUL      = RGBColor(0x1A, 0x4F, 0x8A)
AZUL_M    = RGBColor(0x2E, 0x75, 0xB6)
AZUL_CL   = RGBColor(0xBD, 0xD7, 0xEE)
AZUL_BG   = RGBColor(0xF0, 0xF5, 0xFB)
VERDE     = RGBColor(0x37, 0x86, 0x4C)
VERDE_CL  = RGBColor(0xE2, 0xEF, 0xDA)
NARANJA   = RGBColor(0xED, 0x7D, 0x31)
NARANJA_CL= RGBColor(0xFC, 0xE4, 0xD6)
MORADO    = RGBColor(0x70, 0x30, 0xA0)
MORADO_CL = RGBColor(0xED, 0xE1, 0xF5)
GRIS      = RGBColor(0x55, 0x55, 0x55)
GRIS_CL   = RGBColor(0xF2, 0xF2, 0xF2)
BLANCO    = RGBColor(0xFF, 0xFF, 0xFF)
NEGRO     = RGBColor(0x22, 0x22, 0x22)
AMARILLO  = RGBColor(0xFF, 0xF2, 0xCC)
AMARILLO_B= RGBColor(0xBF, 0x8F, 0x00)

W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
blank = prs.slide_layouts[6]

# ── Primitivos ────────────────────────────────────────────────────────────────
def rect(sl, x, y, w, h, fill=None, line=None):
    s = sl.shapes.add_shape(1, x, y, w, h)
    s.fill.solid() if fill else s.fill.background()
    if fill: s.fill.fore_color.rgb = fill
    s.line.fill.background() if not line else None
    if line: s.line.color.rgb = line
    else: s.line.fill.background()
    return s

def txt(sl, text, x, y, w, h, size=14, bold=False, color=NEGRO,
        align=PP_ALIGN.LEFT, italic=False):
    tb = sl.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    r.font.name = "Calibri"
    return tb

def tabla(sl, data, x, y, w, h, col_ws=None, hdr_color=AZUL, fsize=10.5):
    rows, cols = len(data), len(data[0])
    t = sl.shapes.add_table(rows, cols, x, y, w, h).table
    if col_ws:
        total = sum(col_ws)
        for i, cw in enumerate(col_ws):
            t.columns[i].width = int(w * cw / total)
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            cell = t.cell(r, c)
            cell.text = str(val)
            tf = cell.text_frame
            tf.paragraphs[0].alignment = PP_ALIGN.CENTER
            run = (tf.paragraphs[0].runs[0]
                   if tf.paragraphs[0].runs
                   else tf.paragraphs[0].add_run())
            run.font.name = "Calibri"
            run.font.size = Pt(fsize)
            if r == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = hdr_color
                run.font.bold = True; run.font.color.rgb = BLANCO
            else:
                bg = GRIS_CL if r % 2 == 0 else BLANCO
                cell.fill.solid(); cell.fill.fore_color.rgb = bg
                run.font.color.rgb = NEGRO
    return t

def barra_h(sl, vals, labs, x, y, w, h, color=AZUL_M, max_v=None):
    """Gráfico de barras horizontal dibujado a mano."""
    n = len(vals)
    if max_v is None: max_v = max(vals) * 1.08
    bar_h = h / (n * 1.6)
    gap   = bar_h * 0.6
    lw    = Inches(1.0)
    vw    = Inches(0.55)
    cw    = w - lw - vw
    for i, (v, l) in enumerate(zip(vals, labs)):
        yi = y + i * (bar_h + gap)
        txt(sl, str(l), x, yi, lw, bar_h, size=8.5, color=GRIS, align=PP_ALIGN.RIGHT)
        bw = max(cw * (v / max_v), Inches(0.06))
        rect(sl, x + lw + Inches(0.06), yi, bw, bar_h, fill=color)
        txt(sl, str(v), x + lw + bw + Inches(0.08), yi, vw, bar_h,
            size=8.5, bold=True, color=AZUL)

def header(sl, num, total, titulo, color_linea=AZUL_M):
    rect(sl, 0, 0, W, Inches(1.1), fill=AZUL)
    txt(sl, titulo, Inches(0.4), Inches(0.2), W - Inches(2.5), Inches(0.75),
        size=20, bold=True, color=BLANCO)
    txt(sl, f"{num} / {total}", W - Inches(1.8), Inches(0.3), Inches(1.5), Inches(0.55),
        size=13, color=AZUL_CL, align=PP_ALIGN.RIGHT)
    rect(sl, 0, Inches(1.1), W, Inches(0.07), fill=color_linea)

def footer(sl):
    rect(sl, 0, H - Inches(0.38), W, Inches(0.38), fill=AZUL)
    txt(sl, "Taller 3 · Análisis de Redes Complejas · APPD 2026  ·  I. Tobar Suárez",
        Inches(0.3), H - Inches(0.36), W - Inches(0.6), Inches(0.34),
        size=8, color=AZUL_CL, align=PP_ALIGN.CENTER)

def caja_pregunta(sl, texto):
    """Caja destacada con la pregunta del profesor."""
    rect(sl, Inches(0.35), H - Inches(1.55), W - Inches(0.7), Inches(1.12), fill=AMARILLO)
    rect(sl, Inches(0.35), H - Inches(1.55), Inches(0.08), Inches(1.12), fill=AMARILLO_B)
    txt(sl, "Pregunta del profe:", Inches(0.55), H - Inches(1.52), W - Inches(1.0), Inches(0.35),
        size=9, bold=True, color=AMARILLO_B)
    txt(sl, texto, Inches(0.55), H - Inches(1.18), W - Inches(1.0), Inches(0.78),
        size=10.5, color=RGBColor(0x3D, 0x2B, 0x00), italic=False)

def caja_respuesta(sl, texto, color_bg=VERDE_CL, color_borde=VERDE):
    rect(sl, Inches(0.35), H - Inches(1.55), W - Inches(0.7), Inches(1.12), fill=color_bg)
    rect(sl, Inches(0.35), H - Inches(1.55), Inches(0.08), Inches(1.12), fill=color_borde)
    txt(sl, "Respuesta:", Inches(0.55), H - Inches(1.52), W - Inches(1.0), Inches(0.35),
        size=9, bold=True, color=color_borde)
    txt(sl, texto, Inches(0.55), H - Inches(1.18), W - Inches(1.0), Inches(0.78),
        size=10.5, color=NEGRO)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — PORTADA
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL)
rect(sl, 0, 0, Inches(0.5), H, fill=VERDE)
rect(sl, 0, H * 0.62, W, H * 0.38, fill=RGBColor(0x0D, 0x2F, 0x5C))

txt(sl, "TALLER 3", Inches(0.85), Inches(1.0), Inches(11.0), Inches(0.7),
    size=14, color=AZUL_CL, bold=False)
txt(sl, "Análisis de Redes\nComplejas con Gephi",
    Inches(0.85), Inches(1.65), Inches(10.5), Inches(2.1),
    size=38, bold=True, color=BLANCO)
rect(sl, Inches(0.85), Inches(3.75), Inches(3.5), Inches(0.07), fill=VERDE)
txt(sl, "Red ca-GrQc — SNAP Stanford  ·  Colaboración científica 1993–2003",
    Inches(0.85), Inches(3.9), Inches(11.0), Inches(0.55),
    size=13, color=AZUL_CL)

txt(sl, "Curso: Aproximación a las Políticas Públicas desde los Datos",
    Inches(0.85), Inches(4.85), Inches(11.0), Inches(0.4), size=11, color=AZUL_CL)
txt(sl, "Prof. Dr. Rodrigo Salas  ·  1er Semestre 2026",
    Inches(0.85), Inches(5.22), Inches(11.0), Inches(0.4), size=11, color=AZUL_CL)
txt(sl, "I. Tobar Suárez  ·  19 de junio 2026",
    Inches(0.85), Inches(5.6), Inches(11.0), Inches(0.45), size=12, bold=True, color=BLANCO)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — ¿DE QUÉ SE TRATA? (Dataset)
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 1, 10, "¿Qué red analizamos?")
footer(sl)

txt(sl, "Red de colaboración científica entre autores de física (arXiv, 1993–2003).",
    Inches(0.5), Inches(1.25), Inches(12.3), Inches(0.5), size=13, color=GRIS)

# 4 datos clave como tarjetas grandes
cards = [
    ("5.242", "autores\n(nodos)", AZUL),
    ("14.496", "co-publicaciones\n(aristas)", AZUL_M),
    ("355", "grupos\ndesconectados", VERDE),
    ("79,3%", "en el grupo\nprincipal", NARANJA),
]
for i, (v, l, c) in enumerate(cards):
    cx = Inches(0.5) + i * Inches(3.18)
    rect(sl, cx, Inches(1.85), Inches(2.95), Inches(1.8), fill=c)
    txt(sl, v, cx, Inches(1.95), Inches(2.95), Inches(0.95),
        size=32, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
    txt(sl, l, cx, Inches(2.88), Inches(2.95), Inches(0.65),
        size=10, color=RGBColor(0xDD, 0xEE, 0xFF), align=PP_ALIGN.CENTER)

rect(sl, Inches(0.5), Inches(3.78), W - Inches(1.0), Inches(0.05), fill=AZUL_CL)

# Datos adicionales simples
info = [
    ("Cada nodo =", "un autor (ID anónimo)"),
    ("Cada arista =", "publicaron juntos al menos 1 vez"),
    ("Red =", "no dirigida (la colaboración es mutua)"),
    ("Calculamos todo sobre =", "el grupo principal (4.158 nodos), no el grafo completo"),
]
for i, (k, v) in enumerate(info):
    y = Inches(3.95) + i * Inches(0.58)
    txt(sl, k, Inches(0.6), y, Inches(3.5), Inches(0.5), size=11, bold=True, color=AZUL)
    txt(sl, v, Inches(4.1), y, Inches(8.8), Inches(0.5), size=11, color=GRIS)

rect(sl, Inches(0.5), H - Inches(0.88), W - Inches(1.0), Inches(0.46), fill=AMARILLO)
txt(sl, "⚠  Importante: calcular métricas sobre el grafo completo (con nodos aislados) "
        "da resultados falsos. Por eso trabajamos solo con el grupo principal.",
    Inches(0.65), H - Inches(0.87), W - Inches(1.3), Inches(0.44),
    size=9.5, color=RGBColor(0x5C, 0x40, 0x00), italic=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — EIGENVECTOR CENTRALITY
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 2, 10, "¿Quiénes son los autores más influyentes?  →  Eigenvector Centrality",
       color_linea=VERDE)
footer(sl)

# Qué mide — en lenguaje simple
rect(sl, Inches(0.4), Inches(1.25), Inches(5.9), Inches(1.1), fill=AZUL_CL)
txt(sl, "¿Qué mide el Eigenvector Centrality?",
    Inches(0.5), Inches(1.28), Inches(5.7), Inches(0.38), size=10.5, bold=True, color=AZUL)
txt(sl, "No solo cuántos coautores tienes, sino qué tan importantes son esos coautores.\n"
        "Si colaboras con autores muy conectados, tu puntaje sube.",
    Inches(0.5), Inches(1.62), Inches(5.7), Inches(0.65), size=10, color=NEGRO)

# Tabla
tabla_d = [
    ["#", "Nodo (ID)", "Eigenvector"],
    ["1",  "21012", "0,1556"],
    ["2",  "2741",  "0,1536"],
    ["3",  "12365", "0,1531"],
    ["4",  "21508", "0,1512"],
    ["5",  "9785",  "0,1509"],
    ["6",  "15003", "0,1504"],
    ["7",  "25346", "0,1491"],
    ["8",  "7956",  "0,1491"],
    ["9",  "14807", "0,1490"],
    ["10", "12781", "0,1489"],
]
tabla(sl, tabla_d, Inches(0.4), Inches(2.5), Inches(5.9), Inches(3.65),
      col_ws=[1, 1.8, 2], hdr_color=AZUL, fsize=10)

# Gráfico
barra_h(sl,
        [0.1556,0.1536,0.1531,0.1512,0.1509,0.1504,0.1491,0.1491,0.1490,0.1489],
        ["21012","2741","12365","21508","9785","15003","25346","7956","14807","12781"],
        Inches(6.6), Inches(1.25), Inches(6.4), Inches(4.8),
        color=AZUL_M, max_v=0.165)

caja_respuesta(sl,
    "Ser influyente = estar rodeado de coautores que también son importantes. "
    "El nodo 21012 tiene 81 colaboraciones con autores igualmente activos → "
    "es el núcleo de la red. No es lo mismo que tener muchos coautores cualquiera.",
    color_bg=AZUL_CL, color_borde=AZUL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — DEGREE CENTRALITY
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 3, 10, "¿Quiénes tienen más colaboraciones?  →  Degree Centrality",
       color_linea=NARANJA)
footer(sl)

rect(sl, Inches(0.4), Inches(1.25), Inches(5.9), Inches(1.1), fill=NARANJA_CL)
txt(sl, "¿Qué mide el Degree Centrality?",
    Inches(0.5), Inches(1.28), Inches(5.7), Inches(0.38), size=10.5, bold=True, color=NARANJA)
txt(sl, "Simplemente: ¿con cuántos autores distintos has publicado?\n"
        "El grado promedio de esta red es solo 5,53.",
    Inches(0.5), Inches(1.62), Inches(5.7), Inches(0.65), size=10, color=NEGRO)

tabla_d = [
    ["#", "Nodo (ID)", "N° coautores"],
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
tabla(sl, tabla_d, Inches(0.4), Inches(2.5), Inches(5.9), Inches(3.65),
      col_ws=[1, 1.8, 2], hdr_color=NARANJA, fsize=10)

barra_h(sl, [81,79,77,77,68,68,67,66,65,63],
        ["21012","21281","22691","12365","6610","9785","21508","17655","2741","19423"],
        Inches(6.6), Inches(1.25), Inches(6.4), Inches(4.8),
        color=NARANJA, max_v=90)

caja_respuesta(sl,
    "Sí hay diferencia: el nodo 21281 tiene 79 coautores (top 2 en Degree) "
    "pero no aparece en el top de Eigenvector → sus coautores son menos importantes. "
    "Además, el nodo 21012 tiene 81 colaboraciones vs. promedio 5,53 → 15 veces más. "
    "Unos pocos concentran casi todo.",
    color_bg=NARANJA_CL, color_borde=NARANJA)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — BETWEENNESS CENTRALITY
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 4, 10, "¿Quiénes conectan grupos distintos?  →  Betweenness Centrality",
       color_linea=MORADO)
footer(sl)

rect(sl, Inches(0.4), Inches(1.25), Inches(5.9), Inches(1.1), fill=MORADO_CL)
txt(sl, "¿Qué mide el Betweenness Centrality?",
    Inches(0.5), Inches(1.28), Inches(5.7), Inches(0.38), size=10.5, bold=True, color=MORADO)
txt(sl, "¿Por cuántos caminos entre otros pares de autores pasa este nodo?\n"
        "Alto valor = puente entre grupos. Si lo sacas, la red se rompe.",
    Inches(0.5), Inches(1.62), Inches(5.7), Inches(0.65), size=10, color=NEGRO)

tabla_d = [
    ["#", "Nodo (ID)", "Betweenness", "Comunidad"],
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
tabla(sl, tabla_d, Inches(0.4), Inches(2.5), Inches(5.9), Inches(3.65),
      col_ws=[0.7, 1.5, 1.7, 1.3], hdr_color=MORADO, fsize=10)

# Panel derecho — respuesta visual
rect(sl, Inches(6.6), Inches(1.25), Inches(6.4), Inches(4.8), fill=MORADO_CL)
txt(sl, "¿Qué pasa si eliminamos al nodo 13801?",
    Inches(6.75), Inches(1.35), Inches(6.0), Inches(0.5),
    size=12, bold=True, color=MORADO)

puntos = [
    "El 5,9% de TODOS los caminos de la red pasan por él.",
    "Se desconectarían comunidades que solo se hablan a través suyo.",
    "C1, C2 y C3 (24% de los nodos) dependen de estos puentes.",
    "Si eliminamos los top 3 (13801, 9572, 14599) juntos → la red se fragmenta.",
    "Estos autores no tienen los más coautores, pero su posición es clave.",
]
for i, p_txt in enumerate(puntos):
    y = Inches(1.95) + i * Inches(0.72)
    rect(sl, Inches(6.75), y + Inches(0.15), Inches(0.18), Inches(0.18), fill=MORADO)
    txt(sl, p_txt, Inches(7.05), y, Inches(5.8), Inches(0.65), size=10, color=NEGRO)

caja_respuesta(sl,
    "Si los sacamos, la red se rompe en pedazos. Las comunidades C1, C2, C3 "
    "quedarían aisladas. Son 'puentes críticos' aunque no sean los más colaborativos.",
    color_bg=MORADO_CL, color_borde=MORADO)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — CLOSENESS CENTRALITY
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 5, 10, "¿Quiénes llegan más rápido a todos?  →  Closeness Centrality",
       color_linea=VERDE)
footer(sl)

rect(sl, Inches(0.4), Inches(1.25), Inches(5.9), Inches(1.1), fill=VERDE_CL)
txt(sl, "¿Qué mide el Closeness Centrality?",
    Inches(0.5), Inches(1.28), Inches(5.7), Inches(0.38), size=10.5, bold=True, color=VERDE)
txt(sl, "Qué tan cerca estás del resto de la red en promedio.\n"
        "Valor alto = llegas a todos en pocos pasos intermedios.",
    Inches(0.5), Inches(1.62), Inches(5.7), Inches(0.65), size=10, color=NEGRO)

tabla_d = [
    ["#", "Nodo (ID)", "Closeness"],
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
tabla(sl, tabla_d, Inches(0.4), Inches(2.5), Inches(5.9), Inches(3.65),
      col_ws=[1, 1.8, 2], hdr_color=VERDE, fsize=10)

# Comparativa visual de pasos
rect(sl, Inches(6.6), Inches(1.25), Inches(6.4), Inches(4.8), fill=VERDE_CL)
txt(sl, "¿Cuántos pasos necesita para llegar a todos?",
    Inches(6.75), Inches(1.35), Inches(6.1), Inches(0.5),
    size=12, bold=True, color=VERDE)

comparativas = [
    ("Nodo 13801 (top 1)",  4.08, VERDE),
    ("Promedio de la red",  6.05, AZUL_M),
    ("Nodo periférico",     9.50, RGBColor(0xB0,0xB0,0xB0)),
]
for i, (lbl, val, col) in enumerate(comparativas):
    y = Inches(2.05) + i * Inches(1.3)
    txt(sl, f"{lbl}  →  {val:.2f} pasos", Inches(6.75), y, Inches(6.1), Inches(0.4),
        size=11, bold=True, color=col)
    bw = Inches(5.0) * (val / 10)
    rect(sl, Inches(6.75), y + Inches(0.48), bw, Inches(0.45), fill=col)

txt(sl, "El nodo 13801 llega a cualquier autor\nen solo 4 saltos. El promedio necesita 6.",
    Inches(6.75), Inches(5.45), Inches(6.0), Inches(0.55),
    size=10, italic=True, color=VERDE)

caja_respuesta(sl,
    "Pueden difundir un hallazgo científico más rápido: en solo 4 pasos llegan "
    "a todos los autores de la red. También se enteran antes de los avances de otros. "
    "Están en el 'centro geográfico' de la red.",
    color_bg=VERDE_CL, color_borde=VERDE)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — CUADRO COMPARATIVO
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 6, 10, "¿Cuáles autores aparecen en más rankings?  →  Cuadro Comparativo")
footer(sl)

txt(sl, "27 autores aparecen en algún top 10.  Aquí los que más se repiten:",
    Inches(0.4), Inches(1.2), Inches(12.5), Inches(0.45), size=12, color=GRIS)

tabla_d = [
    ["Nodo",  "Degree", "Eigenvector", "Betweenness", "Closeness", "Total métricas"],
    # 3 métricas — verde
    ["21012", "✓ #1", "✓ #1",  "—",    "✓ #6",  "3 de 4"],
    ["12365", "✓ #3", "✓ #3",  "—",    "✓ #9",  "3 de 4"],
    ["17655", "✓ #8", "—",     "✓ #10","✓ #4",  "3 de 4"],
    # 2 métricas
    ["2741",  "✓ #9", "✓ #2",  "—",    "—",     "2 de 4"],
    ["21508", "✓ #7", "✓ #4",  "—",    "—",     "2 de 4"],
    ["9785",  "✓ #6", "✓ #5",  "—",    "—",     "2 de 4"],
    ["13801", "—",    "—",     "✓ #1", "✓ #1",  "2 de 4"],
    ["9572",  "—",    "—",     "✓ #2", "✓ #3",  "2 de 4"],
    ["14485", "—",    "—",     "✓ #7", "✓ #2",  "2 de 4"],
    # resto agrupado
    ["17 nodos más", "(1 métrica c/u)", "—", "—", "—", "1 de 4"],
]
t = tabla(sl, tabla_d, Inches(0.4), Inches(1.75), Inches(8.3), Inches(5.35),
          col_ws=[1.3,1.3,1.6,1.8,1.5,1.7], hdr_color=AZUL, fsize=9.5)

# Colorear las filas de 3 métricas en verde
for ri in [1, 2, 3]:
    for ci in range(6):
        cell = t.cell(ri, ci)
        cell.fill.solid()
        cell.fill.fore_color.rgb = VERDE_CL

# Panel resumen
rect(sl, Inches(8.95), Inches(1.75), Inches(4.1), Inches(5.35), fill=AZUL_CL)
txt(sl, "Lo que concluimos:", Inches(9.05), Inches(1.85), Inches(3.9), Inches(0.45),
    size=12, bold=True, color=AZUL)

conclusiones = [
    ("Nadie domina las 4 métricas a la vez.",),
    ("21012 = el más 'completo': top en colaboraciones, influencia y cercanía.",),
    ("13801 = el más 'estratégico': no tiene muchos coautores, pero conecta todo.",),
    ("Influencia, colaboratividad, intermediación y cercanía son cosas distintas.",),
]
for i, (c,) in enumerate(conclusiones):
    y = Inches(2.4) + i * Inches(1.1)
    rect(sl, Inches(9.05), y + Inches(0.15), Inches(0.18), Inches(0.18), fill=AZUL)
    txt(sl, c, Inches(9.35), y, Inches(3.6), Inches(0.85), size=10.5, color=NEGRO)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — COMUNIDADES (MODULARITY)
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 7, 10, "¿Cuántas comunidades hay en la red?  →  Algoritmo de Modularidad")
footer(sl)

# KPIs
kpis = [
    ("63", "comunidades\ndetectadas", AZUL),
    ("Q = 0,80", "modularidad\n(muy alta)", VERDE),
    ("901", "nodos en la\ncomunidad mayor", AZUL_M),
    ("35", "comunidades\npequeñas (< 20)", NARANJA),
]
for i, (v, l, c) in enumerate(kpis):
    cx = Inches(0.4) + i * Inches(3.22)
    rect(sl, cx, Inches(1.25), Inches(3.05), Inches(1.55), fill=c)
    txt(sl, v, cx, Inches(1.32), Inches(3.05), Inches(0.85),
        size=26, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
    txt(sl, l, cx, Inches(2.15), Inches(3.05), Inches(0.55),
        size=9.5, color=RGBColor(0xDD,0xEE,0xFF), align=PP_ALIGN.CENTER)

# Tabla distribución
tabla_d = [
    ["Comunidad", "Nodos", "% del grupo principal"],
    ["C0",         "901",  "21,7%"],
    ["C1",         "395",  " 9,5%"],
    ["C2",         "332",  " 8,0%"],
    ["C3",         "270",  " 6,5%"],
    ["C4",         "230",  " 5,5%"],
    ["C5 a C9",    "895",  "21,5% (total 5 comun.)"],
    ["C10 a C19",  "561",  "13,5% (total 10 comun.)"],
    ["C20 a C37",  "~350", " 8,4% (total 18 comun.)"],
    ["C38 a C62",  "~211", " 5,1% (total 25 comun.)"],
]
tabla(sl, tabla_d, Inches(0.4), Inches(3.0), Inches(5.8), Inches(3.6),
      col_ws=[1.7, 1.5, 3.5], hdr_color=AZUL, fsize=10)

# Gráfico
barra_h(sl, [901, 395, 332, 270, 230, 895, 561],
        ["C0","C1","C2","C3","C4","C5–C9","C10–C19"],
        Inches(6.5), Inches(3.0), Inches(6.5), Inches(3.6),
        color=AZUL_M, max_v=1000)

caja_respuesta(sl,
    "La red NO está ni completamente fragmentada ni centralizada. "
    "Hay un grupo grande (C0 con 21,7%) y muchos grupos chicos. "
    "Cada comunidad probablemente = una línea de investigación dentro "
    "de la relatividad general (agujeros negros, ondas gravitacionales, etc.).",
    color_bg=AZUL_CL, color_borde=AZUL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — COMUNIDAD MÁS GRANDE (C0)
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 8, 10, "¿Cómo es la comunidad más grande?  →  Comunidad C0 (901 nodos)",
       color_linea=AZUL_M)
footer(sl)

tabla_d = [
    ["Qué miramos",                       "Resultado"],
    ["a) Número de nodos",                "901"],
    ["b) Número de aristas",              "2.150"],
    ["c) Densidad",                       "0,0053 → baja (dispersa)"],
    ["d) Autor más influyente (Eigenvc.)",  "Nodo 13929  (valor 0,2369)"],
    ["e) Autor más colaborativo (Degree)", "Nodo 13801  (38 coautores)"],
    ["f) Mayor intermediación (Betw.)",   "Nodo 14599  (valor 0,1283)"],
    ["Clustering promedio",               "0,51  → sorprendentemente alto"],
]
tabla(sl, tabla_d, Inches(0.4), Inches(1.28), Inches(7.0), Inches(4.5),
      col_ws=[3.5, 3.5], hdr_color=AZUL, fsize=11)

# Panel análisis
rect(sl, Inches(7.65), Inches(1.28), Inches(5.4), Inches(4.5), fill=AZUL_CL)
txt(sl, "Lo que encontramos:", Inches(7.8), Inches(1.38), Inches(5.1), Inches(0.4),
    size=12, bold=True, color=AZUL)

pts = [
    "3 autores distintos lideran cada métrica → no hay un solo 'jefe'.",
    "Clustering 0,51 = cuando 2 autores tienen un coautor en común, hay 51% de\nprobabilidad de que colaboren entre sí. Muchos triángulos.",
    "¿Es central? SÍ → el nodo 13801 (que vive en C0) tiene el mayor\nBetweenness y Closeness de TODA la red.",
]
for i, p_txt in enumerate(pts):
    y = Inches(1.9) + i * Inches(1.2)
    rect(sl, Inches(7.8), y + Inches(0.12), Inches(0.22), Inches(0.22), fill=AZUL)
    txt(sl, p_txt, Inches(8.15), y, Inches(4.8), Inches(0.95), size=10, color=NEGRO)

caja_respuesta(sl,
    "C0 es el núcleo de toda la red. Es grande pero no tan densa. "
    "El liderazgo está repartido entre 3 autores con roles distintos: "
    "el más influyente, el más colaborativo y el que une los subgrupos.",
    color_bg=AZUL_CL, color_borde=AZUL)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — COMUNIDAD MÁS COMPACTA (C17)
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 9, 10, "¿Cuál es la comunidad más compacta?  →  Comunidad C17 (47 nodos)",
       color_linea=VERDE)
footer(sl)

tabla_d = [
    ["Qué miramos",                      "Resultado"],
    ["a) Mayor densidad",                "0,684  →  muy alta"],
    ["b) Mayor clustering",              "0,860  →  muy alto"],
    ["Número de nodos",                  "47"],
    ["Número de aristas",                "739"],
    ["Top autor (Degree + Eigenvector)", "Nodo 6512  (41 conexiones internas)"],
    ["¿Liderazgo claro?",               "3 autores casi iguales: 6512, 16654, 17807"],
]
tabla(sl, tabla_d, Inches(0.4), Inches(1.28), Inches(6.5), Inches(4.2),
      col_ws=[3.5, 3.5], hdr_color=VERDE, fsize=11)

# Comparativa densidad visual
rect(sl, Inches(7.1), Inches(1.28), Inches(5.9), Inches(4.2), fill=VERDE_CL)
txt(sl, "Comparativa de densidad:", Inches(7.25), Inches(1.38), Inches(5.6), Inches(0.4),
    size=12, bold=True, color=VERDE)

comps = [
    ("C17 (más compacta)", 0.684, VERDE),
    ("C0 (más grande)",    0.005, AZUL),
    ("Red completa",       0.001, GRIS),
]
for i, (lbl, v, col) in enumerate(comps):
    y = Inches(1.95) + i * Inches(1.1)
    txt(sl, f"{lbl}  →  {v:.3f}", Inches(7.25), y, Inches(5.6), Inches(0.38),
        size=10.5, bold=True, color=col)
    bw = max(Inches(4.8) * v, Inches(0.07))
    rect(sl, Inches(7.25), y + Inches(0.45), bw, Inches(0.4), fill=col)

txt(sl, "El 68,4% de todas las colaboraciones posibles\nentre sus 47 miembros realmente existen.",
    Inches(7.25), Inches(5.12), Inches(5.6), Inches(0.55),
    size=10, italic=True, color=VERDE)

caja_respuesta(sl,
    "Es compacta porque casi todos colaboran con todos. Probablemente es un equipo "
    "del mismo laboratorio o proyecto. Liderazgo compartido entre 3 autores → "
    "más resiliente. Riesgo: muy cerrada hacia afuera (cámara de eco).",
    color_bg=VERDE_CL, color_borde=VERDE)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — CONCLUSIONES
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL_BG)
header(sl, 10, 10, "Lo más importante que encontramos")
footer(sl)

conclusiones = [
    (AZUL,    "La red es 'libre de escala'",
              "Pocos autores tienen MUCHAS colaboraciones. "
              "El nodo 21012 tiene 81 coautores vs. un promedio de 5,53. "
              "La mayoría tiene muy pocos."),
    (VERDE,   "Ser colaborativo ≠ ser influyente ≠ ser un puente",
              "Cada métrica mide algo distinto. Ningún autor domina las 4 a la vez. "
              "Hay que mirar todas para entender bien el rol de cada uno."),
    (MORADO,  "El nodo 13801 es el más crítico para la red",
              "No tiene los más coautores, pero conecta todo. "
              "Su eliminación partiría la red más que la de cualquier otro autor."),
    (NARANJA, "Hay 63 comunidades bien definidas (Q = 0,80)",
              "La red no está fragmentada al azar: hay grupos temáticos claros "
              "dentro de la relatividad general y cosmología cuántica."),
    (RGBColor(0x0A,0x70,0x70),
              "Dos tipos de comunidad bien distintos",
              "C0 (901 nodos, baja densidad) = núcleo central disperso. "
              "C17 (47 nodos, densidad 0,68) = equipo compacto y cerrado."),
]
for i, (col, titulo, desc) in enumerate(conclusiones):
    y = Inches(1.28) + i * Inches(1.08)
    rect(sl, Inches(0.4), y, Inches(0.4), Inches(0.88), fill=col)
    txt(sl, titulo, Inches(0.95), y + Inches(0.04), Inches(11.9), Inches(0.38),
        size=11.5, bold=True, color=col)
    txt(sl, desc, Inches(0.95), y + Inches(0.44), Inches(11.9), Inches(0.5),
        size=10.5, color=GRIS)

# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — CIERRE
# ═══════════════════════════════════════════════════════════════════════════════
sl = prs.slides.add_slide(blank)
rect(sl, 0, 0, W, H, fill=AZUL)
rect(sl, 0, 0, Inches(0.5), H, fill=VERDE)
rect(sl, 0, H * 0.65, W, H * 0.35, fill=RGBColor(0x0D,0x2F,0x5C))

txt(sl, "¡Gracias!", Inches(0.85), Inches(1.8), Inches(11.0), Inches(1.4),
    size=50, bold=True, color=BLANCO, align=PP_ALIGN.CENTER)
rect(sl, Inches(4.0), Inches(3.3), Inches(5.3), Inches(0.08), fill=VERDE)

txt(sl, "Taller 3 · Análisis de Redes Complejas con Gephi",
    Inches(0.85), Inches(3.55), Inches(11.5), Inches(0.5),
    size=14, color=AZUL_CL, align=PP_ALIGN.CENTER)
txt(sl, "I. Tobar Suárez  ·  Prof. Dr. Rodrigo Salas  ·  APPD 2026",
    Inches(0.85), Inches(4.05), Inches(11.5), Inches(0.5),
    size=12, color=AZUL_CL, align=PP_ALIGN.CENTER)

refs = [
    "Blondel et al. (2008). Fast unfolding of communities in large networks. J. Statistical Mechanics.",
    "Brandes (2001). A faster algorithm for betweenness centrality. J. Mathematical Sociology.",
    "Leskovec, Kleinberg & Faloutsos (2007). Graph evolution. ACM TKDD.",
    "Newman (2004). Coauthorship networks. PNAS 101(S1).",
    "SNAP Stanford: snap.stanford.edu/data/ca-GrQc.html  ·  Gephi 0.11.2: gephi.org",
]
for i, r in enumerate(refs):
    y = Inches(5.05) + i * Inches(0.42)
    txt(sl, f"[{i+1}] {r}", Inches(0.85), y, Inches(11.5), Inches(0.38),
        size=8.5, color=AZUL_CL, italic=True)

# ── Guardar ───────────────────────────────────────────────────────────────────
out = "/home/user/TALLER-/Taller3_Presentacion.pptx"
prs.save(out)
print(f"Generado: {out}")
