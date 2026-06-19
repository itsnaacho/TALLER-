#!/usr/bin/env python3
"""Generador del Informe Taller 3 — Análisis de Redes Complejas con Gephi"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

# ── Colores institucionales ──────────────────────────────────────────────────
AZUL       = colors.HexColor("#1a4f8a")
AZUL_CLARO = colors.HexColor("#2e75b6")
AZUL_MUY_CLARO = colors.HexColor("#dce6f1")
GRIS_TABLA = colors.HexColor("#f2f2f2")
VERDE_DEST = colors.HexColor("#e2efda")
AMARILLO   = colors.HexColor("#fff2cc")
BLANCO     = colors.white
NEGRO      = colors.black
GRIS_BORDE = colors.HexColor("#bfbfbf")

W, H = A4
MARGIN = 2.2 * cm

# ── Estilos ──────────────────────────────────────────────────────────────────
def build_styles():
    base = getSampleStyleSheet()
    s = {}

    s["portada_titulo"] = ParagraphStyle(
        "portada_titulo", fontName="Helvetica-Bold",
        fontSize=22, textColor=AZUL, alignment=TA_CENTER,
        spaceAfter=6, leading=28
    )
    s["portada_sub"] = ParagraphStyle(
        "portada_sub", fontName="Helvetica-Bold",
        fontSize=14, textColor=AZUL_CLARO, alignment=TA_CENTER,
        spaceAfter=4, leading=18
    )
    s["portada_meta"] = ParagraphStyle(
        "portada_meta", fontName="Helvetica",
        fontSize=11, textColor=colors.HexColor("#404040"),
        alignment=TA_CENTER, spaceAfter=3, leading=16
    )
    s["portada_label"] = ParagraphStyle(
        "portada_label", fontName="Helvetica-Bold",
        fontSize=10, textColor=AZUL, alignment=TA_CENTER, spaceAfter=2
    )

    s["h1"] = ParagraphStyle(
        "h1", fontName="Helvetica-Bold",
        fontSize=13, textColor=AZUL, spaceBefore=14, spaceAfter=6,
        leading=16, borderPad=0
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="Helvetica-Bold",
        fontSize=11, textColor=AZUL_CLARO, spaceBefore=10, spaceAfter=4,
        leading=14
    )
    s["pregunta"] = ParagraphStyle(
        "pregunta", fontName="Helvetica-Bold",
        fontSize=10, textColor=AZUL, spaceBefore=8, spaceAfter=3,
        leading=13
    )
    s["body"] = ParagraphStyle(
        "body", fontName="Helvetica",
        fontSize=9.5, textColor=colors.HexColor("#222222"),
        spaceBefore=2, spaceAfter=4, leading=14, alignment=TA_JUSTIFY
    )
    s["nota"] = ParagraphStyle(
        "nota", fontName="Helvetica-Oblique",
        fontSize=8.5, textColor=colors.HexColor("#555555"),
        spaceBefore=2, spaceAfter=4, leading=12, alignment=TA_JUSTIFY,
        leftIndent=10, rightIndent=10
    )
    s["gephi"] = ParagraphStyle(
        "gephi", fontName="Helvetica-Oblique",
        fontSize=8, textColor=colors.HexColor("#444488"),
        spaceBefore=2, spaceAfter=4, leading=11,
        leftIndent=8, rightIndent=8
    )
    s["bullet"] = ParagraphStyle(
        "bullet", fontName="Helvetica",
        fontSize=9.5, textColor=colors.HexColor("#222222"),
        spaceBefore=1, spaceAfter=2, leading=13,
        leftIndent=14, firstLineIndent=-8
    )
    s["ref"] = ParagraphStyle(
        "ref", fontName="Helvetica",
        fontSize=8.5, textColor=colors.HexColor("#333333"),
        spaceBefore=2, spaceAfter=2, leading=12,
        leftIndent=18, firstLineIndent=-18, alignment=TA_JUSTIFY
    )
    s["th"] = ParagraphStyle(
        "th", fontName="Helvetica-Bold",
        fontSize=9, textColor=BLANCO, alignment=TA_CENTER, leading=11
    )
    s["td_c"] = ParagraphStyle(
        "td_c", fontName="Helvetica",
        fontSize=9, textColor=NEGRO, alignment=TA_CENTER, leading=11
    )
    s["td_l"] = ParagraphStyle(
        "td_l", fontName="Helvetica",
        fontSize=9, textColor=NEGRO, alignment=TA_LEFT, leading=11
    )
    s["td_b"] = ParagraphStyle(
        "td_b", fontName="Helvetica-Bold",
        fontSize=9, textColor=NEGRO, alignment=TA_CENTER, leading=11
    )
    return s

# ── Helpers ───────────────────────────────────────────────────────────────────
def hr(story):
    story.append(HRFlowable(width="100%", thickness=0.5, color=AZUL_CLARO,
                             spaceAfter=4, spaceBefore=4))

def sp(story, h=0.3):
    story.append(Spacer(1, h * cm))

def p(story, text, style):
    story.append(Paragraph(text, style))

def tabla_centralidad(story, S, headers, rows, highlight_rows=None):
    """Tabla estándar de centralidad con filas alternadas."""
    col_w = [(W - 2*MARGIN) / len(headers)] * len(headers)
    data = [[Paragraph(h, S["th"]) for h in headers]]
    for i, row in enumerate(rows):
        styled = [Paragraph(str(c), S["td_c"]) for c in row]
        data.append(styled)

    style_cmds = [
        ("BACKGROUND", (0,0), (-1,0), AZUL),
        ("GRID",       (0,0), (-1,-1), 0.4, GRIS_BORDE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [BLANCO, GRIS_TABLA]),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]
    if highlight_rows:
        for r in highlight_rows:
            style_cmds.append(("BACKGROUND", (0,r), (-1,r), VERDE_DEST))

    t = Table(data, colWidths=col_w)
    t.setStyle(TableStyle(style_cmds))
    story.append(t)

def tabla_params(story, S, rows, col_widths=None):
    """Tabla de parámetros (2 columnas: Parámetro | Valor)."""
    avail = W - 2 * MARGIN
    cw = col_widths or [avail * 0.55, avail * 0.45]
    data = [[Paragraph("Parámetro", S["th"]), Paragraph("Valor", S["th"])]]
    for k, v in rows:
        data.append([Paragraph(str(k), S["td_l"]), Paragraph(str(v), S["td_b"])])
    t = Table(data, colWidths=cw)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [BLANCO, GRIS_TABLA]),
        ("GRID", (0,0), (-1,-1), 0.4, GRIS_BORDE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(t)

def caja_gephi(story, S, texto):
    data = [[Paragraph(f"⚙ Gephi: {texto}", S["gephi"])]]
    t = Table(data, colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#eff3ff")),
        ("BOX", (0,0), (-1,-1), 0.5, AZUL_CLARO),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("RIGHTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    sp(story, 0.2)

def caja_nota(story, S, texto):
    data = [[Paragraph(f"ℹ {texto}", S["nota"])]]
    t = Table(data, colWidths=[W - 2*MARGIN])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AMARILLO),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#c9a800")),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(t)
    sp(story, 0.2)

# ── PORTADA ───────────────────────────────────────────────────────────────────
def build_portada(story, S):
    sp(story, 4)
    p(story, "TALLER 3", S["portada_titulo"])
    sp(story, 0.3)
    p(story, "Análisis de Redes Complejas utilizando Gephi", S["portada_sub"])
    p(story, "Red de Colaboración Científica ca-GrQc (SNAP — Stanford)", S["portada_meta"])
    sp(story, 2)
    hr(story)
    sp(story, 0.5)
    p(story, "Curso: Aproximación a las Políticas Públicas desde los Datos", S["portada_meta"])
    p(story, "Prof. Dr. Rodrigo Salas | 1er Semestre 2026", S["portada_meta"])
    sp(story, 0.5)
    p(story, "Estudiante: I. Tobar Suárez", S["portada_meta"])
    sp(story, 0.5)
    p(story, "Fecha de entrega: 19 de junio del 2026", S["portada_meta"])
    sp(story, 0.5)
    hr(story)
    story.append(PageBreak())

# ── SECCIÓN 1: DATASET ────────────────────────────────────────────────────────
def build_dataset(story, S):
    p(story, "1. Descripción del Dataset", S["h1"])
    hr(story)
    p(story, (
        "La red analizada corresponde al dataset <b>ca-GrQc</b> (<i>General Relativity and "
        "Quantum Cosmology Collaboration Network</i>), disponible en el repositorio SNAP de "
        "la Universidad de Stanford. Representa colaboraciones entre investigadores que "
        "publicaron artículos en la categoría de Relatividad General y Cosmología Cuántica "
        "de arXiv entre 1993 y 2003. Cada nodo representa un autor (identificado por un "
        "ID numérico anónimo) y cada arista indica que dos autores co-publicaron al menos "
        "una vez. La red es <b>no dirigida</b>."
    ), S["body"])
    sp(story, 0.3)
    tabla_params(story, S, [
        ("Nodos totales", "5.242"),
        ("Aristas totales", "14.496"),
        ("Tipo de grafo", "No dirigido, estático"),
        ("Componentes conexos", "355"),
        ("Componente principal — nodos", "4.158 (79,3 % del total)"),
        ("Componente principal — aristas", "13.428"),
        ("Diámetro de la red", "17"),
        ("Longitud promedio de camino", "6,05"),
        ("Grado promedio", "5,53"),
        ("Fuente", "SNAP Stanford — snap.stanford.edu/data/ca-GrQc.html"),
    ])
    sp(story, 0.3)
    caja_nota(story, S, (
        "Todos los cálculos de centralidad se realizaron exclusivamente sobre el "
        "<b>componente conexo principal</b> (4.158 nodos). Las métricas que dependen de "
        "caminos más cortos (Betweenness, Closeness) no son comparables entre componentes "
        "desconectados; calcularlas sobre el grafo completo introduce artefactos graves "
        "(p. ej., nodos con un único vecino dentro de un componente aislado obtienen "
        "Closeness = 1,0 de forma engañosa)."
    ))

# ── SECCIÓN 2: AUTORES MÁS INFLUYENTES ────────────────────────────────────────
def build_autores(story, S):
    p(story, "2. Identificación de los Autores más Influyentes", S["h1"])
    hr(story)
    p(story, (
        "Esta sección identifica los 10 autores más relevantes según cuatro métricas de "
        "centralidad calculadas sobre el componente principal (4.158 nodos). Cada métrica "
        "captura una dimensión distinta de la influencia en la red de colaboración."
    ), S["body"])

    # ── 2.1 Eigenvector ──────────────────────────────────────────────────────
    sp(story, 0.3)
    p(story, "2.1 Eigenvector Centrality — Autores más Influyentes", S["h2"])
    p(story, (
        "La centralidad de vector propio mide la influencia de un nodo considerando "
        "no solo cuántas conexiones tiene, sino también la importancia de sus vecinos. "
        "Un autor con alto Eigenvector colabora con otros autores igualmente activos e "
        "influyentes dentro de la red."
    ), S["body"])
    sp(story, 0.2)
    caja_gephi(story, S,
        "Statistics → Eigenvector Centrality. Luego Appearance → Nodes → Color → "
        "Ranking → Eigenvector Centrality.")
    sp(story, 0.2)

    tabla_centralidad(story, S,
        ["Rank", "Nodo (ID)", "Eigenvector Centrality"],
        [
            [1, 21012, "0,1556"], [2, 2741,  "0,1536"], [3, 12365, "0,1531"],
            [4, 21508, "0,1512"], [5, 9785,  "0,1509"], [6, 15003, "0,1504"],
            [7, 25346, "0,1491"], [8, 7956,  "0,1491"], [9, 14807, "0,1490"],
            [10, 12781, "0,1489"],
        ]
    )
    sp(story, 0.3)
    p(story, "¿Qué significa ser influyente en una red de colaboración científica?", S["pregunta"])
    p(story, (
        "Ser influyente en este contexto significa estar inserto en el <b>núcleo activo</b> "
        "de la red: no basta con co-publicar con muchos autores, sino que esos coautores "
        "también deben ser bien conectados. El nodo 21012, con el mayor valor (0,156), no "
        "solo posee el mayor número de colaboraciones directas de la red (81), sino que sus "
        "colaboradores son a su vez autores prolíficos. Esto lo convierte en un "
        "<i>catalizador</i> de la red: sus trabajos tienen un efecto multiplicador en la "
        "difusión de conocimiento, pues accede a otros investigadores importantes con solo "
        "un intermediario. A diferencia del simple conteo de colaboraciones, Eigenvector "
        "captura la <i>calidad</i> de las conexiones: un autor con pocas pero estratégicas "
        "colaboraciones puede superar a uno con muchos vínculos periféricos."
    ), S["body"])

    # ── 2.2 Degree ──────────────────────────────────────────────────────────
    sp(story, 0.3)
    p(story, "2.2 Degree Centrality — Autores más Colaborativos", S["h2"])
    p(story, (
        "El grado de un nodo cuenta el número de colaboradores únicos. Es la métrica más "
        "directa de actividad colaborativa: un grado alto indica un investigador "
        "prolífico que ha co-publicado con muchos autores distintos."
    ), S["body"])
    sp(story, 0.2)
    caja_gephi(story, S,
        "Statistics → Average Degree. En Data Laboratory ordenar la columna Degree de "
        "mayor a menor. Appearance → Nodes → Size → Ranking → Degree para visualizar.")
    sp(story, 0.2)

    tabla_centralidad(story, S,
        ["Rank", "Nodo (ID)", "Grado (N° colaboradores)"],
        [
            [1, 21012, 81],  [2, 21281, 79],  [3, 22691, 77],
            [4, 12365, 77],  [5, 6610,  68],  [6, 9785,  68],
            [7, 21508, 67],  [8, 17655, 66],  [9, 2741,  65],
            [10, 19423, 63],
        ]
    )
    sp(story, 0.3)
    p(story, (
        "¿Existe diferencia entre ser influyente y ser altamente colaborativo? "
        "¿Se observan autores que concentran gran parte de las colaboraciones?"
    ), S["pregunta"])
    p(story, (
        "<b>Sí existe una diferencia relevante.</b> El nodo 21012 lidera ambas métricas, "
        "pero a partir del segundo lugar las listas divergen. El nodo 21281 tiene el "
        "segundo mayor grado (79 colaboradores) pero no aparece en el top 10 de "
        "Eigenvector, lo que indica que sus colaboradores son menos centrales. "
        "Inversamente, nodos como 2741 (Eigenvector #2) tienen grado relativamente menor "
        "pero colaboran con autores muy influyentes."
    ), S["body"])
    p(story, (
        "En cuanto a concentración: el grado promedio de la red es ≈ 5,53. Los 10 autores "
        "más colaborativos acumulan entre 63 y 81 colaboraciones cada uno, es decir, entre "
        "<b>11 y 15 veces más que el promedio</b>. Esto es consistente con una distribución "
        "de ley de potencia, característica de redes libres de escala (<i>scale-free</i>), "
        "donde una minoría de nodos concentra una fracción desproporcionada de las "
        "conexiones."
    ), S["body"])

    # ── 2.3 Betweenness ─────────────────────────────────────────────────────
    sp(story, 0.3)
    p(story, "2.3 Betweenness Centrality — Autores con Mayor Intermediación", S["h2"])
    p(story, (
        "La centralidad de intermediación mide cuántos caminos más cortos entre pares "
        "de nodos pasan por un nodo dado. Un valor alto indica que el autor actúa como "
        "<b>puente estructural</b> entre distintos grupos o subcomunidades."
    ), S["body"])
    sp(story, 0.2)
    caja_gephi(story, S,
        "Statistics → Network Diameter (calcula Betweenness automáticamente). "
        "Appearance → Nodes → Color → Ranking → Betweenness Centrality.")
    sp(story, 0.2)

    tabla_centralidad(story, S,
        ["Rank", "Nodo (ID)", "Betweenness (norm.)", "Comunidad"],
        [
            [1,  13801, "0,0589", "C0"], [2, 9572,  "0,0408", "C0"],
            [3,  14599, "0,0405", "C0"], [4, 7689,  "0,0397", "C2"],
            [5,  13929, "0,0392", "C0"], [6, 5052,  "0,0388", "C3"],
            [7,  14485, "0,0374", "C1"], [8, 2710,  "0,0355", "C2"],
            [9,  14265, "0,0314", "C4"], [10, 17655, "0,0286", "C0"],
        ]
    )
    sp(story, 0.3)
    p(story, (
        "¿Qué ocurriría si estos autores fueran eliminados de la red? "
        "¿Existen comunidades que dependen de ellos para mantenerse conectadas?"
    ), S["pregunta"])
    p(story, (
        "El nodo 13801 concentra el valor más alto (0,059): el 5,9% de todos los caminos "
        "más cortos entre pares de autores del componente principal pasan por él. Su "
        "eliminación fragmentaría la red, desconectando grupos que actualmente se comunican "
        "a través de él. Si los tres nodos de mayor betweenness (13801, 9572, 14599) "
        "fueran eliminados simultáneamente, es probable que el componente principal se "
        "escindiera en múltiples subcomponentes, aumentando el número de componentes "
        "conexos y la distancia promedio entre los autores restantes."
    ), S["body"])
    p(story, (
        "Respecto a las <b>comunidades dependientes</b>: los nodos 13801, 9572, 14599 y "
        "13929 pertenecen a la comunidad C0 (la mayor, con 901 nodos) pero concentran la "
        "mayor parte de los caminos que conectan C0 con las comunidades externas. En "
        "particular, las comunidades C1, C2 y C3 (que en conjunto suman el 24% del "
        "componente principal) tienen vínculos inter-comunitarios que transitan en gran "
        "medida por estos nodos. El nodo 14485, perteneciente a C1, y los nodos 7689 y "
        "2710, de C2, cumplen además un rol de puente <i>interno</i> dentro de sus propias "
        "comunidades. Si estos nodos fueran eliminados, comunidades como C2 y C4 quedarían "
        "parcialmente aisladas del núcleo central de la red, fragmentando la difusión de "
        "conocimiento entre subcampos de la relatividad general."
    ), S["body"])

    # ── 2.4 Closeness ───────────────────────────────────────────────────────
    sp(story, 0.3)
    p(story, "2.4 Closeness Centrality — Autores con Mayor Cercanía", S["h2"])
    p(story, (
        "La centralidad de cercanía mide el inverso de la suma de las distancias más "
        "cortas desde un nodo hacia todos los demás nodos alcanzables. Un valor alto "
        "indica que el autor puede alcanzar al resto de la red en pocos pasos. "
        "<b>Importante:</b> este cálculo se realizó sobre el componente principal "
        "(4.158 nodos), garantizando la comparabilidad de los valores."
    ), S["body"])
    sp(story, 0.2)
    caja_gephi(story, S,
        "Statistics → Network Diameter (calcula Closeness automáticamente). "
        "Appearance → Nodes → Color → Ranking → Closeness Centrality.")
    sp(story, 0.2)

    tabla_centralidad(story, S,
        ["Rank", "Nodo (ID)", "Closeness (norm.)"],
        [
            [1,  13801, "0,2449"], [2, 14485, "0,2390"],
            [3,  9572,  "0,2383"], [4, 17655, "0,2382"],
            [5,  2654,  "0,2359"], [6, 21012, "0,2352"],
            [7,  12545, "0,2345"], [8, 25006, "0,2340"],
            [9,  12365, "0,2336"], [10, 22691, "0,2329"],
        ]
    )
    sp(story, 0.3)
    p(story, "¿Por qué estos autores pueden difundir conocimiento más rápidamente?", S["pregunta"])
    p(story, (
        "El nodo 13801 (Closeness = 0,245) puede alcanzar a cualquier otro autor del "
        "componente principal en un promedio de aproximadamente <b>4,08 pasos</b> "
        "(1/0,245 ≈ 4,08), frente a los 6,05 pasos del promedio de la red. Esta posición "
        "central implica que los hallazgos de estos autores llegan a más investigadores "
        "con menos intermediarios, confiriéndoles una <i>ventaja epistémica</i>: son los "
        "primeros en enterarse de avances en otras partes de la red y sus publicaciones "
        "se diseminan más rápidamente. En términos de política científica, estos autores "
        "son candidatos naturales a actuar como coordinadores de proyectos "
        "interdisciplinarios o redes de colaboración formales."
    ), S["body"])

    # ── 2.5 Cuadro Comparativo ───────────────────────────────────────────────
    story.append(PageBreak())
    p(story, "2.5 Cuadro Comparativo de Métricas de Centralidad", S["h2"])
    p(story, (
        "La siguiente tabla incluye <b>todos</b> los nodos que aparecen en el top 10 de "
        "al menos una de las cuatro métricas (27 nodos en total), ordenados de mayor a "
        "menor número de métricas en las que destacan. Las celdas en verde corresponden "
        "a autores presentes en 3 o más listas."
    ), S["body"])
    sp(story, 0.3)

    avail = W - 2*MARGIN
    cw = [avail*0.13, avail*0.155, avail*0.155, avail*0.195, avail*0.155, avail*0.11]

    # datos: nodo, degree, eigen, between, close, total
    comp_data = [
        # 3 métricas
        ("21012", "#1", "#1",  "—",   "#6",  3),
        ("12365", "#3", "#3",  "—",   "#9",  3),
        ("17655", "#8", "—",   "#10", "#4",  3),
        # 2 métricas
        ("2741",  "#9", "#2",  "—",   "—",   2),
        ("21508", "#7", "#4",  "—",   "—",   2),
        ("9785",  "#6", "#5",  "—",   "—",   2),
        ("22691", "#3", "—",   "—",   "#10", 2),
        ("13801", "—",  "—",   "#1",  "#1",  2),
        ("9572",  "—",  "—",   "#2",  "#3",  2),
        ("14485", "—",  "—",   "#7",  "#2",  2),
        # 1 métrica — Degree
        ("21281", "#2", "—",   "—",   "—",   1),
        ("6610",  "#5", "—",   "—",   "—",   1),
        ("19423", "#10","—",   "—",   "—",   1),
        # 1 métrica — Eigenvector
        ("15003", "—",  "#6",  "—",   "—",   1),
        ("25346", "—",  "#7",  "—",   "—",   1),
        ("7956",  "—",  "#8",  "—",   "—",   1),
        ("14807", "—",  "#9",  "—",   "—",   1),
        ("12781", "—",  "#10", "—",   "—",   1),
        # 1 métrica — Betweenness
        ("14599", "—",  "—",   "#3",  "—",   1),
        ("7689",  "—",  "—",   "#4",  "—",   1),
        ("13929", "—",  "—",   "#5",  "—",   1),
        ("5052",  "—",  "—",   "#6",  "—",   1),
        ("2710",  "—",  "—",   "#8",  "—",   1),
        ("14265", "—",  "—",   "#9",  "—",   1),
        # 1 métrica — Closeness
        ("2654",  "—",  "—",   "—",   "#5",  1),
        ("12545", "—",  "—",   "—",   "#7",  1),
        ("25006", "—",  "—",   "—",   "#8",  1),
    ]

    headers_comp = ["Nodo", "Degree", "Eigenvector", "Betweenness", "Closeness", "Total"]
    data_table = [[Paragraph(h, S["th"]) for h in headers_comp]]
    for row in comp_data:
        styled = [Paragraph(str(c), S["td_c"]) for c in row]
        data_table.append(styled)

    row_styles = [
        ("BACKGROUND", (0,0), (-1,0), AZUL),
        ("GRID", (0,0), (-1,-1), 0.4, GRIS_BORDE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [BLANCO, GRIS_TABLA]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
    ]
    # Verde para las filas con total=3 (filas 1,2,3)
    for i in [1, 2, 3]:
        row_styles.append(("BACKGROUND", (0,i), (-1,i), VERDE_DEST))

    t = Table(data_table, colWidths=cw)
    t.setStyle(TableStyle(row_styles))
    story.append(t)
    sp(story, 0.4)

    p(story, "Discusión de resultados", S["pregunta"])
    p(story, (
        "Los nodos <b>21012, 12365 y 17655</b> son los más versátiles de la red, "
        "apareciendo en 3 de las 4 métricas. El nodo 21012 domina en Degree, Eigenvector "
        "y Closeness: es el autor con más colaboraciones directas (81), está rodeado de "
        "coautores igualmente activos y puede difundir información rápidamente. Sin "
        "embargo, su ausencia del top de Betweenness indica que sus colaboraciones son "
        "densas <i>dentro</i> de su comunidad (C0) más que puentes hacia otras comunidades."
    ), S["body"])
    p(story, (
        "El nodo <b>13801</b> representa el perfil opuesto: lidera Betweenness y Closeness "
        "pero no aparece en Degree ni Eigenvector. Es un <i>conector estratégico</i>: "
        "no el más prolífico, pero sí el más indispensable para la cohesión global de la "
        "red. Su eliminación causaría mayor fragmentación estructural que la de cualquier "
        "otro autor. Esta divergencia entre métricas ilustra la multidimensionalidad de "
        "la influencia científica: un autor puede ser relevante por volumen, por calidad "
        "de sus conexiones, por su rol de intermediario o por su accesibilidad al resto "
        "de la red."
    ), S["body"])

# ── SECCIÓN 3: COMUNIDADES ────────────────────────────────────────────────────
def build_comunidades(story, S):
    story.append(PageBreak())
    p(story, "3. Identificación de las Comunidades de Autores", S["h1"])
    hr(story)

    # ── 3.1 Modularidad ─────────────────────────────────────────────────────
    p(story, "3.1 Detección de Comunidades — Algoritmo de Modularidad (Louvain)", S["h2"])
    p(story, (
        "Se aplicó el algoritmo de Modularidad de Gephi (variante greedy de Louvain, "
        "Blondel et al., 2008) con resolución = 1,0 sobre el componente principal "
        "(4.158 nodos). La modularidad Q obtenida fue de <b>0,80</b>, valor considerado "
        "muy alto (Q > 0,7 indica comunidades bien definidas)."
    ), S["body"])
    sp(story, 0.2)
    caja_gephi(story, S,
        "Statistics → Modularity (Resolution = 1,0). Appearance → Nodes → Color → "
        "Partition → Modularity Class para colorear por comunidad.")
    sp(story, 0.2)

    tabla_params(story, S, [
        ("Total de comunidades detectadas", "63"),
        ("Modularidad Q", "0,80 (muy alta)"),
        ("Comunidad más grande (C0)", "901 nodos (21,7% del componente principal)"),
        ("Comunidades con > 100 nodos", "10"),
        ("Comunidades con 20–100 nodos", "18"),
        ("Comunidades pequeñas (< 20 nodos)", "35"),
        ("Algoritmo", "Louvain greedy (Blondel et al., 2008)"),
    ])
    sp(story, 0.4)

    # Tabla distribución completa — top 20 explícito + agrupados
    p(story, "Distribución de tamaños de comunidades (top 20 explícito + resumen del resto)", S["gephi"])
    sp(story, 0.15)

    avail = W - 2*MARGIN
    cw3 = [avail*0.18, avail*0.18, avail*0.25, avail*0.39]
    dist_data = [
        [Paragraph(h, S["th"]) for h in ["Comunidad", "Nodos", "% Comp. Principal", "Acumulado"]],
        *[
            [Paragraph(str(c), S["td_c"]) for c in row]
            for row in [
                ["C0",  "901", "21,7%", "21,7%"],
                ["C1",  "395", " 9,5%", "31,2%"],
                ["C2",  "332", " 8,0%", "39,2%"],
                ["C3",  "270", " 6,5%", "45,7%"],
                ["C4",  "230", " 5,5%", "51,2%"],
                ["C5",  "222", " 5,3%", "56,5%"],
                ["C6",  "207", " 5,0%", "61,5%"],
                ["C7",  "152", " 3,7%", "65,2%"],
                ["C8",  "145", " 3,5%", "68,7%"],
                ["C9",  "129", " 3,1%", "71,8%"],
                ["C10", " 94", " 2,3%", "74,1%"],
                ["C11", " 82", " 2,0%", "76,1%"],
                ["C12", " 69", " 1,7%", "77,8%"],
                ["C13", " 66", " 1,6%", "79,4%"],
                ["C14", " 55", " 1,3%", "80,7%"],
                ["C15", " 53", " 1,3%", "82,0%"],
                ["C16", " 51", " 1,2%", "83,2%"],
                ["C17", " 47", " 1,1%", "84,3%"],
                ["C18", " 45", " 1,1%", "85,4%"],
                ["C19", " 44", " 1,1%", "86,5%"],
            ]
        ]
    ]
    # Filas agrupadas para el resto
    dist_data.append([
        Paragraph("C20–C37", S["td_c"]),
        Paragraph("~350 total", S["td_c"]),
        Paragraph("~8,4% (18 comun. de 20–43 nodos)", S["td_c"]),
        Paragraph("~94,9%", S["td_c"]),
    ])
    dist_data.append([
        Paragraph("C38–C62", S["td_c"]),
        Paragraph("~211 total", S["td_c"]),
        Paragraph("~5,1% (25 comun. de < 20 nodos)", S["td_c"]),
        Paragraph("100,0%", S["td_c"]),
    ])

    t = Table(dist_data, colWidths=cw3)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL),
        ("GRID", (0,0), (-1,-1), 0.4, GRIS_BORDE),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [BLANCO, GRIS_TABLA]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 3),
        ("BOTTOMPADDING", (0,0), (-1,-1), 3),
        # Destacar C0
        ("BACKGROUND", (0,1), (-1,1), VERDE_DEST),
        # Destacar filas agrupadas
        ("BACKGROUND", (0,21), (-1,22), AMARILLO),
        ("FONTNAME", (0,21), (-1,22), "Helvetica-Oblique"),
    ]))
    story.append(t)
    sp(story, 0.3)

    p(story, "¿La red está altamente fragmentada o concentrada?", S["pregunta"])
    p(story, (
        "La red presenta una <b>estructura intermedia</b>. La modularidad Q = 0,80 revela "
        "comunidades bien delimitadas con pocas conexiones inter-comunitarias, lo que "
        "indica cierta segmentación. Sin embargo, la distribución es marcadamente "
        "heterogénea: la comunidad más grande (C0) concentra el 21,7% de los nodos del "
        "componente principal, y las 5 primeras comunidades reúnen el 51,2%. La red "
        "no está ni uniformemente fragmentada ni excesivamente centralizada."
    ), S["body"])
    p(story, (
        "Cada comunidad detectada probablemente representa una subárea temática dentro "
        "de la relatividad general y la cosmología cuántica: grupos especializados en "
        "agujeros negros, ondas gravitacionales, gravedad cuántica de lazos, "
        "cosmología inflacionaria, etc. Las comunidades pequeñas (< 20 nodos) "
        "corresponden posiblemente a equipos reducidos o a investigadores con vínculos "
        "débiles con el núcleo principal de la red."
    ), S["body"])

    # ── 3.2 Comunidad más grande ─────────────────────────────────────────────
    sp(story, 0.4)
    p(story, "3.2 Análisis de la Comunidad más Grande (C0: 901 nodos)", S["h2"])
    caja_gephi(story, S,
        "Filters → Attributes → Partition → Modularity Class → seleccionar C0 → Filter. "
        "Ejecutar Statistics sobre el subgrafo filtrado para obtener métricas internas.")
    sp(story, 0.2)

    tabla_params(story, S, [
        ("Número de nodos",              "901"),
        ("Número de aristas",            "2.150"),
        ("Densidad",                     "0,0053 (baja)"),
        ("Clustering promedio",          "0,5115"),
        ("Autor más influyente (Eigenvector)", "Nodo 13929 (0,2369)"),
        ("Autor más colaborador (Degree)",     "Nodo 13801 (38 colaboradores)"),
        ("Mayor intermediación (Betweenness)", "Nodo 14599 (0,1283)"),
    ])
    sp(story, 0.3)

    p(story, "¿Qué características presenta esta comunidad? ¿Es una comunidad central?", S["pregunta"])
    p(story, (
        "La comunidad C0 es extensa (901 nodos) pero relativamente dispersa (densidad = "
        "0,0053). Sin embargo, su coeficiente de clustering de <b>0,51</b> es "
        "sorprendentemente alto para una comunidad de este tamaño: cuando dos autores "
        "comparten un colaborador, hay un 51% de probabilidad de que ellos también "
        "colaboren directamente. Esto evidencia la existencia de múltiples triángulos "
        "de colaboración y subgrupos cohesionados dentro de C0."
    ), S["body"])
    p(story, (
        "Notablemente, el autor más colaborador (13801), el más influyente (13929) y "
        "el mayor intermediario (14599) son tres nodos distintos, lo que sugiere "
        "<b>liderazgos especializados</b>: un conector estructural, un autor de alto "
        "perfil y un intermediario entre subgrupos. Esto indica que C0 no depende de "
        "un único nodo central sino de roles complementarios."
    ), S["body"])
    p(story, (
        "C0 <b>sí es la comunidad central</b> de la red global: concentra los nodos con "
        "mayor Betweenness y Closeness de toda la red (13801 lidera ambas métricas "
        "globales), lo que la posiciona como el núcleo articulador de todo el componente "
        "principal. La red global depende de C0 para mantener su cohesión."
    ), S["body"])

    # ── 3.3 Comunidad más compacta ───────────────────────────────────────────
    sp(story, 0.4)
    p(story, "3.3 Análisis de la Comunidad más Compacta (C17: 47 nodos)", S["h2"])
    p(story, (
        "Entre las comunidades con más de 20 autores, se identificó C17 como la de "
        "<b>mayor densidad</b> (0,684) y mayor coeficiente de clustering (0,860)."
    ), S["body"])
    caja_gephi(story, S,
        "Filters → Partition → Modularity Class → seleccionar C17. "
        "Statistics → Avg. Clustering Coefficient para obtener el coeficiente interno.")
    sp(story, 0.2)

    tabla_params(story, S, [
        ("Número de nodos",          "47"),
        ("Número de aristas",        "739"),
        ("Densidad",                 "0,684 (muy alta)"),
        ("Clustering promedio",      "0,860 (muy alto)"),
        ("Top autor (Degree)",       "Nodo 6512 (41 conexiones internas)"),
        ("Top autor (Eigenvector)",  "Nodo 6512 (0,171)"),
        ("Nodos con liderazgo similar", "Nodos 16654 y 17807 (degree 40, eigenvector 0,1708)"),
    ])
    sp(story, 0.3)

    p(story, "¿Por qué se considera compacta?", S["pregunta"])
    p(story, (
        "Con densidad = 0,684, esta comunidad es casi un grafo completo: de todas las "
        "posibles colaboraciones entre sus 47 miembros, el <b>68,4% existen "
        "efectivamente</b>. El coeficiente de clustering de 0,86 refuerza esta compacidad: "
        "cuando dos autores tienen un colaborador en común, hay un 86% de probabilidad "
        "de que ellos también colaboren directamente. Para comparación, el clustering "
        "promedio del componente principal es de aproximadamente 0,53."
    ), S["body"])

    p(story, "¿Qué implica para la colaboración científica?", S["pregunta"])
    p(story, (
        "Una densidad tan alta es característica de <b>equipos de investigación "
        "consolidados</b>, posiblemente adscritos a una misma institución o centrados "
        "en un problema científico muy específico que requiere colaboración estrecha y "
        "continua. La información y el conocimiento circulan muy rápidamente dentro del "
        "grupo. Sin embargo, una comunidad excesivamente cerrada corre el riesgo de "
        "convertirse en una cámara de eco, con escasa conexión hacia otras líneas de "
        "investigación, lo que podría limitar la innovación proveniente de perspectivas "
        "externas."
    ), S["body"])

    p(story, "¿Existe un liderazgo claramente identificado?", S["pregunta"])
    p(story, (
        "El nodo 6512 lidera tanto en Degree (41 conexiones) como en Eigenvector "
        "(0,171). Sin embargo, los nodos 16654 y 17807 tienen valores prácticamente "
        "idénticos (degree 40, eigenvector 0,1708), lo que sugiere un <b>liderazgo "
        "colectivo tripartito</b> más que una jerarquía piramidal. En comunidades "
        "altamente densas, el liderazgo tiende a distribuirse, lo que hace a la comunidad "
        "más resiliente ante la pérdida de cualquier miembro individual."
    ), S["body"])

# ── SECCIÓN 4: CONCLUSIONES ───────────────────────────────────────────────────
def build_conclusiones(story, S):
    story.append(PageBreak())
    p(story, "4. Síntesis y Conclusiones", S["h1"])
    hr(story)
    p(story, (
        "El análisis de la red ca-GrQc revela una red de colaboración científica con "
        "características típicas de las redes complejas reales: distribución "
        "heterogénea de grados, estructura comunitaria fuerte y nodos con roles "
        "estructurales especializados."
    ), S["body"])
    sp(story, 0.2)

    bullets = [
        ("<b>Distribución libre de escala:</b> una minoría de autores acumula una fracción "
         "desproporcionada de las colaboraciones (nodo 21012 con 81, frente a un promedio "
         "de 5,53). Esto es consistente con redes <i>scale-free</i> donde el 'rico se hace "
         "más rico' (preferential attachment)."),
        ("<b>Influencia ≠ colaboratividad:</b> el cuadro comparativo muestra que solo 3 nodos "
         "aparecen en 3 métricas simultáneamente, y las listas de Betweenness y Closeness "
         "divergen significativamente de las de Degree y Eigenvector. Ser el más "
         "colaborativo no implica ser el mejor conector estructural."),
        ("<b>El nodo 13801 es el más estratégico:</b> lidera tanto Betweenness (0,059) como "
         "Closeness (0,245). Su eliminación tendría consecuencias estructurales más severas "
         "que la de cualquier otro autor, potencialmente fragmentando comunidades enteras."),
        ("<b>Modularidad Q = 0,80:</b> la red está organizada en 63 comunidades bien "
         "definidas sobre el componente principal, reflejo de subcampos temáticos o grupos "
         "institucionales relativamente independientes dentro de la relatividad general y "
         "cosmología cuántica."),
        ("<b>C0 es el núcleo estructural:</b> con 901 nodos y los autores de mayor "
         "centralidad global, actúa como articulador de toda la red. C17 (47 nodos, "
         "densidad 0,684) representa el extremo opuesto: un grupo altamente cohesionado "
         "con liderazgo distribuido."),
    ]
    for b in bullets:
        p(story, f"• {b}", S["bullet"])
        sp(story, 0.1)

    sp(story, 0.3)
    p(story, "Tabla resumen — pasos en Gephi para replicar el análisis", S["h2"])
    sp(story, 0.15)

    avail = W - 2*MARGIN
    cw2 = [avail*0.35, avail*0.65]
    steps = [
        ("Importar datos",
         "File → Open → seleccionar CA-GrQc_gephi0112.gexf"),
        ("Filtrar comp. principal",
         "Filters → Topology → Giant Component → Filter"),
        ("Visualizar grafo",
         "Overview → Layout → ForceAtlas 2 → Run → Stop al estabilizarse"),
        ("Degree Centrality",
         "Statistics → Average Degree. Data Lab: ordenar columna Degree."),
        ("Betweenness y Closeness",
         "Statistics → Network Diameter (ambas se calculan juntas)"),
        ("Eigenvector Centrality",
         "Statistics → Eigenvector Centrality"),
        ("Comunidades",
         "Statistics → Modularity (Resolution = 1,0)"),
        ("Colorear por comunidad",
         "Appearance → Nodes → Color → Partition → Modularity Class"),
        ("Filtrar una comunidad",
         "Filters → Attributes → Partition → Modularity Class → valor → Filter"),
        ("Tamaño nodo por métrica",
         "Appearance → Nodes → Size → Ranking → métrica → Apply"),
    ]
    steps_data = [[Paragraph("Análisis", S["th"]), Paragraph("Pasos en Gephi 0.11.2", S["th"])]]
    for k, v in steps:
        steps_data.append([Paragraph(k, S["td_l"]), Paragraph(v, S["td_l"])])
    t = Table(steps_data, colWidths=cw2)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [BLANCO, GRIS_TABLA]),
        ("GRID", (0,0), (-1,-1), 0.4, GRIS_BORDE),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(t)

# ── REFERENCIAS ───────────────────────────────────────────────────────────────
def build_referencias(story, S):
    sp(story, 0.5)
    p(story, "Referencias", S["h1"])
    hr(story)
    refs = [
        ("Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). "
         "Fast unfolding of communities in large networks. "
         "<i>Journal of Statistical Mechanics: Theory and Experiment</i>, 2008(10), P10008."),
        ("Brandes, U. (2001). A faster algorithm for betweenness centrality. "
         "<i>Journal of Mathematical Sociology</i>, 25(2), 163–177."),
        ("Leskovec, J., Kleinberg, J., & Faloutsos, C. (2007). Graph evolution: "
         "Densification and shrinking diameters. "
         "<i>ACM Transactions on Knowledge Discovery from Data</i>, 1(1)."),
        ("Newman, M. E. J. (2004). Coauthorship networks and patterns of scientific "
         "collaboration. <i>Proceedings of the National Academy of Sciences</i>, "
         "101(Suppl. 1), 5200–5205."),
        ("SNAP — Stanford Network Analysis Project. <i>General Relativity and Quantum "
         "Cosmology Collaboration Network</i>. Recuperado de: "
         "snap.stanford.edu/data/ca-GrQc.html"),
        ("Gephi Consortium (2023). <i>Gephi 0.11.2 — The Open Graph Viz Platform</i>. "
         "Recuperado de: gephi.org"),
    ]
    for i, ref in enumerate(refs, 1):
        p(story, f"[{i}]  {ref}", S["ref"])
        sp(story, 0.1)

# ── NUMERACIÓN DE PÁGINAS ─────────────────────────────────────────────────────
class NumberedCanvas:
    def __init__(self, canvas, doc):
        self._canvas = canvas
        self._doc = doc

def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#888888"))
    page_num = canvas.getPageNumber()
    if page_num > 1:
        canvas.drawRightString(
            W - MARGIN, 1.2*cm,
            f"Taller 3 — Análisis de Redes Complejas | APPD 2026     Página {page_num - 1}"
        )
        canvas.drawString(
            MARGIN, 1.2*cm,
            "I. Tobar Suárez"
        )
        canvas.setStrokeColor(AZUL_CLARO)
        canvas.setLineWidth(0.5)
        canvas.line(MARGIN, 1.5*cm, W - MARGIN, 1.5*cm)
    canvas.restoreState()

# ── MAIN ──────────────────────────────────────────────────────────────────────
def main():
    output = "/home/user/TALLER-/Informe_Taller3_Final.pdf"
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=2.0*cm,
        title="Taller 3 — Análisis de Redes Complejas",
        author="I. Tobar Suárez",
    )
    S = build_styles()
    story = []

    build_portada(story, S)
    build_dataset(story, S)
    sp(story, 0.4)
    build_autores(story, S)
    build_comunidades(story, S)
    build_conclusiones(story, S)
    build_referencias(story, S)

    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"PDF generado: {output}")

if __name__ == "__main__":
    main()
