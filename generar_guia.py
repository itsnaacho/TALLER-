#!/usr/bin/env python3
"""Guía de práctica Taller 3 — script + preguntas del profe + explicaciones desde cero"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY

W, H = A4
MARGIN = 2.0 * cm

# ── Colores ──────────────────────────────────────────────────────────────────
AZUL     = colors.HexColor("#1A4F8A")
AZUL_M   = colors.HexColor("#2E75B6")
AZUL_CL  = colors.HexColor("#DCE6F1")
VERDE    = colors.HexColor("#37864C")
VERDE_CL = colors.HexColor("#E2EFDA")
NARANJA  = colors.HexColor("#ED7D31")
NARAN_CL = colors.HexColor("#FCE4D6")
MORADO   = colors.HexColor("#70307A")
MOR_CL   = colors.HexColor("#EDE1F5")
ROJO     = colors.HexColor("#C00000")
ROJO_CL  = colors.HexColor("#FFE6E6")
GRIS     = colors.HexColor("#555555")
GRIS_CL  = colors.HexColor("#F2F2F2")
AMARILLO = colors.HexColor("#FFF2CC")
AMAR_B   = colors.HexColor("#BF8F00")
NEGRO    = colors.HexColor("#222222")
BLANCO   = colors.white

# ── Estilos ──────────────────────────────────────────────────────────────────
def estilos():
    s = {}
    def st(name, **kw):
        defaults = dict(fontName="Helvetica", fontSize=10, textColor=NEGRO, leading=14)
        defaults.update(kw)
        s[name] = ParagraphStyle(name, **defaults)
    # Títulos
    st("h_portada",  fontName="Helvetica-Bold", fontSize=26, textColor=BLANCO,
       alignment=TA_CENTER, leading=32)
    st("sub_portada",fontName="Helvetica",      fontSize=13, textColor=colors.HexColor("#DCE6F1"),
       alignment=TA_CENTER, leading=18, spaceAfter=4)
    st("h1",  fontName="Helvetica-Bold", fontSize=14, textColor=AZUL,
       spaceBefore=14, spaceAfter=5, leading=18)
    st("h2",  fontName="Helvetica-Bold", fontSize=11.5, textColor=AZUL_M,
       spaceBefore=10, spaceAfter=4, leading=15)
    st("h3",  fontName="Helvetica-Bold", fontSize=10.5, textColor=VERDE,
       spaceBefore=7, spaceAfter=3, leading=13)
    # Cuerpo
    st("body", fontSize=10, leading=14.5, spaceAfter=4, alignment=TA_JUSTIFY)
    st("body_b", fontName="Helvetica-Bold", fontSize=10, leading=14.5, spaceAfter=4)
    st("bullet", fontSize=10, leading=14, spaceAfter=3,
       leftIndent=14, firstLineIndent=-8, alignment=TA_LEFT)
    st("nota", fontName="Helvetica-Oblique", fontSize=9, textColor=GRIS,
       leading=12, spaceAfter=3, leftIndent=10, rightIndent=10, alignment=TA_JUSTIFY)
    # Persona A / B
    st("personaA", fontName="Helvetica-Bold", fontSize=11, textColor=AZUL,
       spaceBefore=6, spaceAfter=2, leading=14)
    st("personaB", fontName="Helvetica-Bold", fontSize=11, textColor=VERDE,
       spaceBefore=6, spaceAfter=2, leading=14)
    # Script / diálogos
    st("script", fontName="Helvetica", fontSize=10, textColor=NEGRO,
       leading=14.5, spaceAfter=3, leftIndent=12, alignment=TA_JUSTIFY)
    st("pregunta_profe", fontName="Helvetica-Bold", fontSize=10.5, textColor=ROJO,
       spaceBefore=8, spaceAfter=2, leading=14)
    st("respuesta",      fontName="Helvetica", fontSize=10, textColor=NEGRO,
       spaceAfter=3, leading=14.5, leftIndent=10, alignment=TA_JUSTIFY)
    st("th", fontName="Helvetica-Bold", fontSize=9.5, textColor=BLANCO,
       alignment=TA_CENTER, leading=12)
    st("td", fontName="Helvetica",     fontSize=9.5, textColor=NEGRO,
       alignment=TA_LEFT,   leading=12)
    st("td_c", fontName="Helvetica",   fontSize=9.5, textColor=NEGRO,
       alignment=TA_CENTER, leading=12)
    return s

# ── Helpers ───────────────────────────────────────────────────────────────────
def sp(story, h=0.3): story.append(Spacer(1, h*cm))
def hr(story, color=AZUL_M):
    story.append(HRFlowable(width="100%", thickness=0.6, color=color,
                             spaceBefore=4, spaceAfter=6))

def caja(story, S, texto, bg, borde, label=None, label_color=None):
    avail = W - 2*MARGIN
    filas = []
    if label:
        filas.append([Paragraph(f"<b>{label}</b>", ParagraphStyle(
            "lbl", fontName="Helvetica-Bold", fontSize=9,
            textColor=label_color or borde, leading=11))])
    filas.append([Paragraph(texto, S["body"])])
    t = Table(filas, colWidths=[avail])
    cmds = [
        ("BACKGROUND", (0,0), (-1,-1), bg),
        ("BOX",        (0,0), (-1,-1), 0.8, borde),
        ("LEFTPADDING",(0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0),(-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]
    t.setStyle(TableStyle(cmds))
    story.append(t)
    sp(story, 0.2)

def caja_pregunta(story, S, pregunta, respuesta):
    avail = W - 2*MARGIN
    data = [
        [Paragraph(f"❓  {pregunta}", ParagraphStyle(
            "pq", fontName="Helvetica-Bold", fontSize=10.5,
            textColor=ROJO, leading=14))],
        [Paragraph(respuesta, S["body"])],
    ]
    t = Table(data, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), ROJO_CL),
        ("BACKGROUND", (0,1), (0,1), GRIS_CL),
        ("BOX",        (0,0), (-1,-1), 0.8, ROJO),
        ("LINEBELOW",  (0,0), (0,0),   0.4, ROJO),
        ("LEFTPADDING",(0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0),(-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(t)
    sp(story, 0.25)

def script_bloque(story, S, persona, texto, color):
    avail = W - 2*MARGIN
    lbl_style = ParagraphStyle("lbl2", fontName="Helvetica-Bold",
                                fontSize=9.5, textColor=color, leading=12)
    data = [
        [Paragraph(f"🎤  {persona}:", lbl_style)],
        [Paragraph(f'"{texto}"', S["script"])],
    ]
    t = Table(data, colWidths=[avail])
    bg = AZUL_CL if color == AZUL else VERDE_CL
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,0), bg),
        ("BACKGROUND", (0,1), (0,1), BLANCO),
        ("BOX",        (0,0), (-1,-1), 0.6, color),
        ("LEFTPADDING",(0,0), (-1,-1), 10),
        ("RIGHTPADDING",(0,0),(-1,-1), 10),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(t)
    sp(story, 0.18)

def analogia(story, S, emoji, titulo, texto):
    caja(story, S, f"<b>{emoji}  {titulo}:</b>  {texto}",
         bg=AMARILLO, borde=AMAR_B)

def footer_cb(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRIS)
    pn = canvas.getPageNumber()
    if pn > 1:
        canvas.drawRightString(W - MARGIN, 1.0*cm,
            f"Guía de Práctica · Taller 3 · APPD 2026     Página {pn - 1}")
        canvas.drawString(MARGIN, 1.0*cm, "I. Tobar Suárez · Confidencial — solo para práctica")
    canvas.restoreState()

# ═══════════════════════════════════════════════════════════════════════════════
def build(story, S):

    # ── PORTADA ───────────────────────────────────────────────────────────────
    avail = W - 2*MARGIN

    # Simulamos portada con una tabla grande de fondo azul
    portada_data = [[Paragraph(
        "<br/><br/><br/>GUÍA DE PRÁCTICA<br/>",
        S["h_portada"]),
    ], [Paragraph(
        "Taller 3 · Análisis de Redes Complejas con Gephi",
        S["sub_portada"]),
    ], [Paragraph(
        "Script para la presentación + preguntas del profe<br/>"
        "con respuestas listas para usar",
        S["sub_portada"]),
    ], [Paragraph(
        "<br/>Para las dos personas — incluyendo quien no sabe nada todavía<br/><br/>",
        S["sub_portada"]),
    ]]
    pt = Table(portada_data, colWidths=[avail])
    pt.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), AZUL),
        ("LEFTPADDING",(0,0), (-1,-1), 20),
        ("RIGHTPADDING",(0,0),(-1,-1), 20),
        ("TOPPADDING", (0,0), (-1,-1), 10),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    story.append(pt)
    sp(story, 0.5)

    caja(story, S,
        "📌  <b>Cómo usar esta guía:</b> léela completa antes de la presentación. "
        "Cada concepto tiene una analogía para entenderlo fácil. "
        "El script dice exactamente qué dice cada uno. "
        "Las preguntas del profe tienen respuesta lista.",
        bg=AMARILLO, borde=AMAR_B)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PARTE 0 — DE QUÉ SE TRATA ESTO (para el que no sabe nada)
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PARTE 0 — ¿De qué se trata esto? (lee esto primero)", S["h1"]))
    hr(story)

    story.append(Paragraph("¿Qué es una red de colaboración científica?", S["h2"]))
    story.append(Paragraph(
        "Imagina que cada investigador del mundo es una persona en Instagram. "
        "Cada vez que dos investigadores publican un artículo juntos, se 'siguen mutuamente'. "
        "El dataset ca-GrQc es como el Instagram de los físicos que estudian relatividad general "
        "y cosmología cuántica entre 1993 y 2003.",
        S["body"]))
    sp(story, 0.2)

    analogia(story, S, "📸", "Analogía clave",
        "Nodo = persona. Arista = publicaron juntos. Red = el Instagram de los físicos.")

    story.append(Paragraph("¿Qué hicimos con Gephi?", S["h2"]))
    story.append(Paragraph(
        "Gephi es un programa que visualiza redes y calcula estadísticas sobre ellas. "
        "Nosotros importamos la red de los físicos y le preguntamos: "
        "¿quiénes son los más importantes?, ¿hay grupos?, ¿quién conecta a quién?",
        S["body"]))
    sp(story, 0.2)

    story.append(Paragraph("Los números clave del dataset:", S["h2"]))
    datos = [
        ["Qué", "Número", "Qué significa en simple"],
        ["Nodos (autores)", "5.242", "5.242 físicos distintos en la red"],
        ["Aristas (colaboraciones)", "14.496", "14.496 pares que publicaron juntos"],
        ["Componentes conexos", "355",
         "355 grupos separados — como 355 islas en el océano"],
        ["Componente principal", "4.158 nodos (79,3%)",
         "La isla más grande donde vive la mayoría"],
        ["Grado promedio", "5,53",
         "En promedio, cada físico publicó con solo 5 o 6 colegas"],
    ]
    t = Table([[Paragraph(c, S["th"] if i==0 else (S["td_c"] if j==1 else S["td"]))
                for j,c in enumerate(row)]
               for i,row in enumerate(datos)],
              colWidths=[avail*0.25, avail*0.22, avail*0.53])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), AZUL),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BLANCO, GRIS_CL]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#BFBFBF")),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]))
    story.append(t)
    sp(story, 0.3)

    caja(story, S,
        "⚠️  <b>Por qué usamos solo el componente principal (4.158 nodos):</b> "
        "si calculas métricas sobre las 355 islas separadas, los resultados no tienen "
        "sentido. Por ejemplo, un físico que publicó solo con su colega en una islita "
        "aparecería como 'el más cercano de todos' — ¡porque solo tiene 1 vecino! "
        "Así que trabajamos solo con la isla grande.",
        bg=NARAN_CL, borde=NARANJA)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PARTE 1 — LAS 4 MÉTRICAS EXPLICADAS DESDE CERO
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PARTE 1 — Las 4 Métricas (con analogías)", S["h1"]))
    hr(story)

    # ── 1.1 EIGENVECTOR ──────────────────────────────────────────────────────
    story.append(Paragraph("1.1  Eigenvector Centrality — ¿Quién es el más influyente?", S["h2"]))
    analogia(story, S, "🌟", "Analogía",
        "No es lo mismo tener 100 amigos cualquiera que tener 100 amigos famosos. "
        "El Eigenvector mide esto: si tus coautores son muy importantes, tú también subes. "
        "Es como el PageRank de Google para científicos.")
    story.append(Paragraph(
        "Un físico con Eigenvector alto no necesariamente publicó con muchos, "
        "sino que los pocos o muchos con quienes publicó son también muy importantes.",
        S["body"]))
    sp(story, 0.15)
    story.append(Paragraph("<b>Nuestros resultados — Top 3:</b>", S["body_b"]))
    for r, n, v in [("1°","21012","0,1556"),("2°","2741","0,1536"),("3°","12365","0,1531")]:
        story.append(Paragraph(f"• Nodo {n} → {v}  (puesto {r})", S["bullet"]))
    sp(story, 0.15)
    caja(story, S,
        "<b>Respuesta a la pregunta del profe:</b> 'Ser influyente en esta red significa "
        "estar rodeado de coautores que también son importantes. No basta con publicar "
        "mucho — importa con quién publicas. El nodo 21012 tiene 81 colaboraciones con "
        "autores igualmente activos, lo que lo convierte en el núcleo de la red.'",
        bg=AZUL_CL, borde=AZUL)

    # ── 1.2 DEGREE ───────────────────────────────────────────────────────────
    story.append(Paragraph("1.2  Degree Centrality — ¿Quién más colabora?", S["h2"]))
    analogia(story, S, "📇", "Analogía",
        "Simplemente: ¿cuántos números de teléfono tienes en tus contactos? "
        "No importa si son importantes o no. Solo cuántos son.")
    story.append(Paragraph(
        "El grado promedio de esta red es 5,53. El nodo 21012 tiene 81. "
        "Eso es 15 veces más que el promedio — es un outlier enorme.",
        S["body"]))
    sp(story, 0.15)
    story.append(Paragraph("<b>Nuestros resultados — Top 3:</b>", S["body_b"]))
    for r, n, v in [("1°","21012","81 coautores"),("2°","21281","79 coautores"),
                    ("3° (empate)","22691 y 12365","77 coautores")]:
        story.append(Paragraph(f"• Nodo {n} → {v}  (puesto {r})", S["bullet"]))
    sp(story, 0.15)
    caja(story, S,
        "<b>Diferencia entre influyente y colaborativo:</b> el nodo 21281 tiene 79 coautores "
        "(2° en Degree) pero NO aparece en el top de Eigenvector. Eso significa que sus "
        "coautores son menos importantes. En cambio, nodos como 2741 tienen menos coautores "
        "pero sí aparecen en Eigenvector porque publican con gente muy conectada. "
        "<b>Ser prolífico ≠ ser influyente.</b>",
        bg=NARAN_CL, borde=NARANJA)

    # ── 1.3 BETWEENNESS ──────────────────────────────────────────────────────
    story.append(Paragraph("1.3  Betweenness Centrality — ¿Quién conecta grupos distintos?", S["h2"]))
    analogia(story, S, "🌉", "Analogía",
        "Imagina una fiesta donde hay 5 grupos de amigos distintos que no se conocen entre sí. "
        "Pero tú conoces a alguien de cada grupo. Eres el puente. Sin ti, esos grupos "
        "no se conectan. Eso es el Betweenness: mide cuántos caminos entre otros "
        "pasan por ti.")
    story.append(Paragraph(
        "Un valor de 0,059 (nodo 13801) significa que el 5,9% de TODOS los caminos "
        "más cortos entre pares de autores de la red pasan por ese nodo.",
        S["body"]))
    sp(story, 0.15)
    story.append(Paragraph("<b>Nuestros resultados — Top 3:</b>", S["body_b"]))
    for r, n, v, c in [("1°","13801","0,0589","C0"),
                        ("2°","9572","0,0408","C0"),
                        ("3°","14599","0,0405","C0")]:
        story.append(Paragraph(f"• Nodo {n} → {v} (comunidad {c})  (puesto {r})", S["bullet"]))
    sp(story, 0.15)
    caja(story, S,
        "<b>¿Qué pasa si los eliminamos?</b> Si sacamos al nodo 13801, el 5,9% de las "
        "conexiones de la red se cortan. Las comunidades C1, C2 y C3 (que en total "
        "tienen el 24% de los nodos) quedarían parcialmente aisladas porque dependen "
        "de estos puentes para conectarse al resto. Es como cortar el único puente "
        "entre dos ciudades.",
        bg=MOR_CL, borde=MORADO)

    # ── 1.4 CLOSENESS ────────────────────────────────────────────────────────
    story.append(Paragraph("1.4  Closeness Centrality — ¿Quién difunde información más rápido?", S["h2"]))
    analogia(story, S, "📣", "Analogía",
        "¿Quién puede pasar el chisme más rápido en la escuela? "
        "El que está en el centro del patio y conoce a alguien de cada grupo. "
        "Closeness mide qué tan 'central' estás geográficamente en la red: "
        "cuántos pasos necesitas para llegar a todos.")
    story.append(Paragraph(
        "El nodo 13801 tiene Closeness = 0,245. Eso significa que llega a "
        "cualquier autor en promedio en 4,08 pasos (1/0,245). "
        "El promedio de la red necesita 6,05 pasos.",
        S["body"]))
    sp(story, 0.15)
    story.append(Paragraph("<b>Nuestros resultados — Top 3:</b>", S["body_b"]))
    for r, n, v, ps in [("1°","13801","0,2449","4,08 pasos"),
                         ("2°","14485","0,2390","4,18 pasos"),
                         ("3°","9572","0,2383","4,20 pasos")]:
        story.append(Paragraph(f"• Nodo {n} → {v} = aprox. {ps}  (puesto {r})", S["bullet"]))
    sp(story, 0.15)
    caja(story, S,
        "<b>¿Por qué difunden más rápido?</b> Están en el centro geográfico de la red. "
        "Un hallazgo científico que parta de ellos llega a más investigadores "
        "en menos intermediarios. También son los primeros en enterarse de "
        "avances de otros grupos. Ventaja clara en una red de conocimiento.",
        bg=VERDE_CL, borde=VERDE)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PARTE 2 — CUADRO COMPARATIVO
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PARTE 2 — Cuadro Comparativo: ¿quién aparece en más rankings?", S["h1"]))
    hr(story)
    story.append(Paragraph(
        "La tarea pide un cuadro comparativo para ver qué autores dominan en más métricas. "
        "De los 27 autores que aparecen en algún top 10, estos son los más versátiles:",
        S["body"]))
    sp(story, 0.2)

    comp = [
        ["Nodo", "Degree", "Eigenvector", "Betweenness", "Closeness", "Total"],
        ["21012", "✓ #1",  "✓ #1",  "—",    "✓ #6",  "3 de 4"],
        ["12365", "✓ #3",  "✓ #3",  "—",    "✓ #9",  "3 de 4"],
        ["17655", "✓ #8",  "—",     "✓ #10","✓ #4",  "3 de 4"],
        ["2741",  "✓ #9",  "✓ #2",  "—",    "—",     "2 de 4"],
        ["13801", "—",     "—",     "✓ #1", "✓ #1",  "2 de 4"],
        ["9572",  "—",     "—",     "✓ #2", "✓ #3",  "2 de 4"],
        ["14485", "—",     "—",     "✓ #7", "✓ #2",  "2 de 4"],
        ["...otros 20 nodos","(1 métrica c/u)","—","—","—","1 de 4"],
    ]
    cw = [avail*c for c in [0.12,0.14,0.17,0.17,0.14,0.12]]
    # Ajustamos para que sume al ancho disponible
    cw = [avail*0.13, avail*0.14, avail*0.17, avail*0.19, avail*0.14, avail*0.13]

    rows_t = []
    for i, row in enumerate(comp):
        st_name = "th" if i == 0 else "td_c"
        rows_t.append([Paragraph(c, S[st_name]) for c in row])

    t = Table(rows_t, colWidths=cw)
    cmds = [
        ("BACKGROUND",(0,0),(-1,0), AZUL),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#BFBFBF")),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BLANCO, GRIS_CL]),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),4),
    ]
    # Destacar top 3 en verde
    for ri in [1,2,3]:
        cmds.append(("BACKGROUND",(0,ri),(-1,ri),VERDE_CL))
    t.setStyle(TableStyle(cmds))
    story.append(t)
    sp(story, 0.3)

    caja(story, S,
        "<b>Conclusión del cuadro:</b> nadie domina las 4 métricas a la vez. "
        "El nodo 21012 es el más 'completo' (top en colaboraciones, influencia y cercanía). "
        "El nodo 13801 es el más estratégico (lidera Betweenness y Closeness, aunque "
        "no tenga tantos coautores). Hay perfiles distintos de importancia en la red.",
        bg=AZUL_CL, borde=AZUL)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PARTE 3 — COMUNIDADES
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PARTE 3 — Comunidades de Autores", S["h1"]))
    hr(story)

    story.append(Paragraph("¿Qué es el algoritmo de Modularidad?", S["h2"]))
    analogia(story, S, "📱", "Analogía",
        "Es como detectar los grupos de WhatsApp dentro de una lista de contactos. "
        "El algoritmo mira quién chatea más con quién y los agrupa automáticamente. "
        "Aquí 'chatear' = co-publicar. El resultado Q = 0,80 significa que los grupos "
        "detectados son muy reales (entre 0 y 1, más cercano a 1 = mejor).")
    sp(story, 0.2)

    story.append(Paragraph("Resultados generales:", S["h2"]))
    for txt_b in [
        "• <b>63 comunidades detectadas</b> sobre el componente principal.",
        "• <b>Modularidad Q = 0,80</b> → estructura comunitaria muy marcada (muy bueno).",
        "• La comunidad más grande (C0) tiene <b>901 nodos</b> = el 21,7% de todos.",
        "• <b>10 comunidades grandes</b> (>100 nodos), 18 medianas, 35 pequeñas.",
    ]:
        story.append(Paragraph(txt_b, S["bullet"]))
    sp(story, 0.2)
    caja(story, S,
        "<b>¿Está fragmentada o concentrada?</b> Es un punto intermedio. "
        "Hay un grupo dominante (C0) pero también muchos grupos chicos y medianos. "
        "Cada comunidad probablemente representa una línea de investigación específica "
        "dentro de la relatividad general: agujeros negros, ondas gravitacionales, "
        "cosmología inflacionaria, gravedad cuántica de lazos, etc.",
        bg=AZUL_CL, borde=AZUL)

    sp(story, 0.3)
    story.append(Paragraph("Comunidad más grande — C0 (901 nodos):", S["h2"]))
    for txt_b in [
        "• <b>Nodos:</b> 901  |  <b>Aristas:</b> 2.150  |  <b>Densidad:</b> 0,0053 (baja — es grande y dispersa)",
        "• <b>Clustering promedio:</b> 0,51 → si dos autores comparten un coautor, hay 51% de que también colaboren entre sí",
        "• <b>Más influyente (Eigenvector):</b> Nodo 13929",
        "• <b>Más colaborativo (Degree):</b> Nodo 13801 (38 coautores dentro de C0)",
        "• <b>Mayor intermediación (Betweenness):</b> Nodo 14599",
        "• <b>¿Es central?</b> SÍ — el nodo 13801 tiene el mayor Betweenness y Closeness de TODA la red",
    ]:
        story.append(Paragraph(txt_b, S["bullet"]))
    sp(story, 0.15)
    caja(story, S,
        "<b>Importante para responder:</b> tres autores distintos lideran cada métrica en C0. "
        "No hay un solo 'jefe'. Hay liderazgos especializados: uno es el más influyente, "
        "otro el más colaborativo, otro el que une los subgrupos.",
        bg=NARAN_CL, borde=NARANJA)

    sp(story, 0.3)
    story.append(Paragraph("Comunidad más compacta — C17 (47 nodos):", S["h2"]))
    for txt_b in [
        "• <b>Nodos:</b> 47  |  <b>Aristas:</b> 739  |  <b>Densidad:</b> 0,684 (muy alta)",
        "• <b>Clustering:</b> 0,860 → si A y B comparten un coautor, hay 86% que A y B también publiquen juntos",
        "• <b>En comparación:</b> C0 tiene densidad 0,005 — C17 es 137 veces más densa",
        "• El 68,4% de TODAS las colaboraciones posibles entre sus 47 miembros existen",
        "• <b>Liderazgo:</b> Nodo 6512 lidera, pero los nodos 16654 y 17807 tienen casi los mismos valores",
    ]:
        story.append(Paragraph(txt_b, S["bullet"]))
    sp(story, 0.15)
    caja(story, S,
        "<b>¿Por qué es compacta?</b> Porque casi todos colaboran con todos. "
        "Es como un equipo de investigación del mismo laboratorio o proyecto específico. "
        "<b>Liderazgo compartido</b> entre 3 autores → la comunidad es más resiliente. "
        "<b>Riesgo:</b> tan cerrada que puede ser una 'cámara de eco' — poca conexión con afuera.",
        bg=VERDE_CL, borde=VERDE)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PARTE 4 — SCRIPT DE LA PRESENTACIÓN
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PARTE 4 — Script de la Presentación (quién dice qué)", S["h1"]))
    hr(story)

    caja(story, S,
        "⏱  <b>Tiempo total: 10–15 minutos.</b>  "
        "Persona A habla en las slides de métricas (slides 3–6 + slide 8). "
        "Persona B habla en la slide del dataset, cuadro comparativo, comunidades y conclusiones. "
        "Pueden intercambiar si prefieren. Lo importante es que AMBOS entiendan TODO "
        "por si el profe pregunta a cualquiera.",
        bg=AMARILLO, borde=AMAR_B)
    sp(story, 0.3)

    # Slide 1 — Portada
    story.append(Paragraph("Slide 1 — Portada (15 seg)", S["h3"]))
    script_bloque(story, S, "Persona B", "Buenas, somos ... y ... vamos a presentar el Taller 3 "
        "sobre análisis de redes complejas usando Gephi, con la red de colaboración "
        "científica ca-GrQc de Stanford.", VERDE)

    # Slide 2 — Dataset
    story.append(Paragraph("Slide 2 — Dataset (1–2 min)", S["h3"]))
    script_bloque(story, S, "Persona B",
        "La red que analizamos representa colaboraciones entre físicos que publicaron "
        "en arXiv entre 1993 y 2003. Cada nodo es un autor y cada arista significa "
        "que dos autores publicaron juntos al menos una vez. "
        "Tiene 5.242 autores y 14.496 colaboraciones. "
        "Importante: la red tiene 355 grupos separados, así que todos los cálculos "
        "los hicimos solo sobre el grupo principal de 4.158 nodos — si no, "
        "los resultados salen mal por los grupos aislados.", VERDE)

    # Slide 3 — Eigenvector
    story.append(Paragraph("Slide 3 — Eigenvector Centrality (2 min)", S["h3"]))
    script_bloque(story, S, "Persona A",
        "La primera métrica es el Eigenvector Centrality. Básicamente mide qué tan "
        "importantes son tus coautores — no solo cuántos tienes. "
        "El nodo con ID 21012 tiene el valor más alto con 0,156. "
        "Esto significa que no solo tiene 81 colaboraciones, sino que esos coautores "
        "también son muy activos e influyentes. "
        "La pregunta del profe era qué significa ser influyente acá: "
        "ser influyente es estar en el núcleo de la red, rodeado de gente igual de activa. "
        "No es lo mismo publicar con cualquiera que publicar con los más conectados.", AZUL)

    # Slide 4 — Degree
    story.append(Paragraph("Slide 4 — Degree Centrality (1.5 min)", S["h3"]))
    script_bloque(story, S, "Persona A",
        "El Degree simplemente cuenta con cuántos autores distintos publicaste. "
        "El nodo 21012 de nuevo lidera con 81 colaboraciones — 15 veces más que el promedio. "
        "La diferencia con Eigenvector es clara: el nodo 21281 tiene 79 coautores "
        "pero no aparece entre los más influyentes, porque sus coautores son menos importantes. "
        "Sí se observa una concentración fuerte — pocos autores acumulan casi todas las colaboraciones, "
        "lo que es típico de una red libre de escala.", AZUL)

    # Slide 5 — Betweenness
    story.append(Paragraph("Slide 5 — Betweenness Centrality (2 min)", S["h3"]))
    script_bloque(story, S, "Persona A",
        "El Betweenness mide cuántos caminos entre otros pares de autores pasan por ti. "
        "El nodo 13801 tiene el valor más alto: el 5,9% de todos los caminos de la red "
        "pasan por él. Si lo eliminamos, esos caminos se cortan. "
        "Sobre la pregunta de comunidades que dependen de estos nodos: "
        "los nodos 13801, 9572 y 14599 están en la comunidad C0 pero actúan como puentes "
        "hacia C1, C2 y C3. Si los sacamos, esas comunidades que representan el 24% de la red "
        "quedarían parcialmente aisladas.", AZUL)

    # Slide 6 — Closeness
    story.append(Paragraph("Slide 6 — Closeness Centrality (1.5 min)", S["h3"]))
    script_bloque(story, S, "Persona A",
        "El Closeness mide qué tan cerca estás de todos en la red. "
        "El nodo 13801 lidera acá también con 0,245, lo que significa que puede "
        "llegar a cualquier autor en solo 4 pasos, mientras el promedio necesita 6. "
        "Por eso pueden difundir conocimiento más rápido: su trabajo llega a más "
        "personas en menos intermediarios. Son como el 'centro geográfico' de la red.", AZUL)

    # Slide 7 — Comparativo
    story.append(Paragraph("Slide 7 — Cuadro Comparativo (1.5 min)", S["h3"]))
    script_bloque(story, S, "Persona B",
        "Acá vemos quién aparece en más rankings. Hay 27 autores que aparecen en algún top 10. "
        "Solo 3 aparecen en 3 métricas: el 21012, el 12365 y el 17655. "
        "El 21012 es el más completo — top en colaboraciones, influencia y cercanía. "
        "Pero hay un punto interesante: el nodo 13801 aparece solo en 2 métricas, "
        "pero lidera Betweenness y Closeness, que son las más importantes para la "
        "cohesión de la red. Es más estratégico que el 21012 a pesar de tener menos coautores. "
        "Esto confirma que influencia es multidimensional — no hay un solo tipo de importancia.", VERDE)

    # Slide 8 — Comunidades
    story.append(Paragraph("Slide 8 — Comunidades: Modularidad (2 min)", S["h3"]))
    script_bloque(story, S, "Persona B",
        "Usamos el algoritmo de Modularidad de Gephi para detectar comunidades. "
        "Encontramos 63 comunidades con un valor Q de 0,80, que es muy alto — "
        "significa que los grupos son reales y bien definidos. "
        "La red no está ni completamente fragmentada ni centralizada: "
        "hay una comunidad grande, C0 con 901 nodos, y muchas pequeñas. "
        "Cada comunidad probablemente representa una línea de investigación distinta "
        "dentro de la física teórica.", VERDE)

    # Slide 9 — C0
    story.append(Paragraph("Slide 9 — Comunidad más grande C0 (1.5 min)", S["h3"]))
    script_bloque(story, S, "Persona B",
        "La comunidad C0 tiene 901 nodos, 2.150 aristas y una densidad baja de 0,005. "
        "Pero su clustering de 0,51 es sorprendentemente alto para su tamaño. "
        "Algo importante: los tres autores que lideran cada métrica dentro de C0 "
        "son distintos. No hay un solo jefe sino tres roles especializados. "
        "¿Es central? Sí — el nodo 13801, que vive en C0, "
        "tiene el mayor Betweenness y Closeness de toda la red.", VERDE)

    # Slide 10 — C17
    story.append(Paragraph("Slide 10 — Comunidad más compacta C17 (1.5 min)", S["h3"]))
    script_bloque(story, S, "Persona B",
        "Entre las comunidades con más de 20 autores, C17 es la más compacta "
        "con densidad 0,684 y clustering 0,860. "
        "Eso significa que el 68% de todas las colaboraciones posibles entre sus "
        "47 miembros existen de verdad. Es casi como si todos publicaran con todos. "
        "Probablemente es un equipo de investigación de una misma institución. "
        "El liderazgo está repartido entre 3 autores con valores casi idénticos, "
        "lo que hace a la comunidad resiliente. "
        "El riesgo es que sea muy cerrada hacia afuera.", VERDE)

    # Slide 11 — Conclusiones
    story.append(Paragraph("Slide 11 — Conclusiones (1 min)", S["h3"]))
    script_bloque(story, S, "Persona B",
        "Para cerrar, los cinco hallazgos principales: "
        "primero, la red es libre de escala — pocos concentran muchas colaboraciones. "
        "Segundo, ser colaborativo, influyente, puente y cercano son cosas distintas. "
        "Tercero, el nodo 13801 es el más crítico para la cohesión de la red. "
        "Cuarto, hay 63 comunidades bien definidas que probablemente representan "
        "líneas de investigación específicas. "
        "Y quinto, C0 es el núcleo disperso y C17 es el equipo compacto — dos extremos dentro de la misma red.",
        VERDE)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PARTE 5 — PREGUNTAS DEL PROFE
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PARTE 5 — Preguntas que puede hacer el Profe", S["h1"]))
    hr(story)

    caja(story, S,
        "⚠️  Estas son las preguntas más probables. <b>Cualquiera de los dos</b> "
        "debe poder responder cualquiera. Léanlas en voz alta juntos antes de la presentación.",
        bg=ROJO_CL, borde=ROJO)
    sp(story, 0.3)

    preguntas = [
        ("¿Por qué calcularon las métricas solo sobre el componente principal y no sobre toda la red?",
         "Porque las métricas que usan caminos más cortos (Betweenness y Closeness) no tienen sentido "
         "entre nodos que no están conectados. Si las calculas sobre el grafo completo, un nodo aislado "
         "con un solo vecino obtiene Closeness = 1,0 — lo que es un error, no un resultado real. "
         "Por eso la práctica estándar es trabajar solo con el componente principal."),

        ("¿Qué es una red libre de escala?",
         "Es una red donde pocos nodos tienen muchas conexiones y la mayoría tiene muy pocas. "
         "La distribución de grados sigue una ley de potencia: hay un nodo con 81 coautores "
         "mientras el promedio es 5,53. Es como en Instagram: unos pocos influencers tienen "
         "millones de seguidores y el 99% tiene decenas. Este fenómeno ocurre en redes "
         "donde 'el rico se hace más rico' — los autores ya famosos atraen más colaboradores."),

        ("¿Qué significa una modularidad Q = 0,80?",
         "La modularidad va de 0 a 1. Un valor cercano a 1 significa que las comunidades "
         "detectadas son muy reales: hay muchas conexiones dentro de cada grupo y pocas "
         "conexiones entre grupos. Con Q = 0,80 podemos confiar en que las 63 comunidades "
         "detectadas reflejan agrupaciones reales de investigadores, no son aleatorias."),

        ("¿Por qué el nodo 21012 no aparece entre los de mayor Betweenness?",
         "Porque sus colaboraciones son densas dentro de su propia comunidad (C0), "
         "no entre comunidades distintas. El Betweenness mide puentes entre grupos, "
         "y el 21012 es muy activo dentro de un grupo pero no conecta grupos diferentes. "
         "El nodo 13801, en cambio, tiene pocas colaboraciones pero las que tiene "
         "conectan comunidades que de otro modo no se hablarían."),

        ("¿Qué diferencia hay entre Closeness y Betweenness?",
         "Ambos miden 'posición en la red' pero de formas distintas. "
         "Betweenness mide cuántos caminos entre otros pasan por ti — eres un puente. "
         "Closeness mide qué tan corta es tu distancia promedio al resto — estás en el centro. "
         "Pueden coincidir (el 13801 lidera ambas) o no (el 21012 tiene alto Closeness "
         "pero bajo Betweenness). Son dimensiones distintas de la centralidad."),

        ("Si eliminas los top 3 de Betweenness, ¿qué le pasa a la red?",
         "Probablemente el componente principal se fragmenta en varios subcomponentes. "
         "Los nodos 13801, 9572 y 14599 están en C0 y actúan como puentes hacia C1, C2 y C3. "
         "Si los eliminamos, esas comunidades que representan el 24% de los nodos "
         "quedarían parcialmente aisladas. La distancia promedio entre los autores "
         "restantes aumentaría significativamente."),

        ("¿Qué representa cada comunidad en términos reales?",
         "Probablemente cada comunidad es una línea de investigación específica dentro "
         "de la relatividad general y cosmología cuántica: grupos de agujeros negros, "
         "ondas gravitacionales, cosmología inflacionaria, gravedad cuántica de lazos, etc. "
         "También pueden representar grupos de una misma institución o que comparten "
         "metodologías similares. No podemos saberlo con certeza porque los IDs son anónimos."),

        ("¿Por qué C17 es más compacta que C0 si C0 es mucho más grande?",
         "Porque la densidad no depende del tamaño — depende de la proporción de conexiones "
         "existentes sobre las posibles. C0 tiene 901 nodos: las posibles conexiones son "
         "901×900/2 = 405.450, pero solo tiene 2.150 → densidad 0,005. "
         "C17 tiene 47 nodos: las posibles son 47×46/2 = 1.081, y tiene 739 → densidad 0,684. "
         "Grupos pequeños y cohesionados siempre tienen más densidad que grupos grandes y dispersos."),

        ("¿Qué es el coeficiente de clustering?",
         "Mide qué probabilidad hay de que dos vecinos de un nodo también sean vecinos entre sí. "
         "Clustering = 0,86 en C17 significa: si A y B son coautores del mismo autor, "
         "hay 86% de probabilidad de que A y B también hayan publicado juntos. "
         "Es una medida de qué tanto se forman triángulos de colaboración en la red."),

        ("¿Cuál de los dos autores eliminó más 'daño' a la red: el 21012 o el 13801?",
         "El 13801 causa más daño estructural. El 21012 tiene más colaboraciones, "
         "pero sus conexiones son densas dentro de C0. Si lo sacas, C0 pierde su autor "
         "más colaborativo pero la red sigue conectada. El 13801 en cambio lidera "
         "Betweenness y Closeness: es el puente entre C0 y otras comunidades. "
         "Sin él, partes de la red se desconectan. Es el nodo más crítico para la cohesión global."),

        ("¿Gephi les da el valor de Closeness correcto cuando hay componentes desconectados?",
         "No directamente — ese es un punto metodológico importante que manejamos. "
         "Gephi calcula Closeness por componente, lo que hace que nodos en componentes "
         "pequeños obtengan valores artificialmente altos (un nodo con un solo vecino "
         "tiene distancia 1 a su único vecino → Closeness = 1,0). "
         "Por eso filtramos el grafo al componente principal antes de calcular."),
    ]

    for i, (q, a) in enumerate(preguntas, 1):
        caja_pregunta(story, S, f"Pregunta {i}: {q}", a)

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════════
    # PARTE 6 — GLOSARIO RÁPIDO
    # ══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("PARTE 6 — Glosario Rápido (para memorizar los términos)", S["h1"]))
    hr(story)

    glosario = [
        ["Término", "En simple", "Analogía"],
        ["Nodo", "Un autor (persona)", "Una persona en Instagram"],
        ["Arista", "Una co-publicación", "Seguirse mutuamente"],
        ["Grado (Degree)", "N° de coautores", "N° de contactos en el teléfono"],
        ["Eigenvector", "Influencia ponderada por vecinos", "Tener amigos famosos"],
        ["Betweenness", "% de caminos que pasan por ti", "El único que conoce a todos los grupos"],
        ["Closeness", "Inverso de distancia promedio", "El que pasa el chisme más rápido"],
        ["Modularidad Q", "Qué tan bien definidas están las comunidades", "Qué tan claros son los grupos de WhatsApp"],
        ["Densidad", "% de conexiones existentes vs. posibles", "Qué tan amigos son todos entre sí"],
        ["Clustering", "Prob. que dos vecinos sean vecinos entre sí", "Si tus dos mejores amigos se conocen"],
        ["Componente principal", "El grupo más grande conectado", "La isla más grande"],
        ["Red libre de escala", "Pocos nodos con muchas conexiones", "Influencers vs. usuarios normales"],
    ]
    cw2 = [avail*0.22, avail*0.38, avail*0.40]
    rows_g = []
    for i, row in enumerate(glosario):
        sty = S["th"] if i == 0 else S["td"]
        sty_c = S["th"] if i == 0 else S["td"]
        rows_g.append([Paragraph(c, sty) for c in row])
    t = Table(rows_g, colWidths=cw2)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),AZUL),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BLANCO, GRIS_CL]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#BFBFBF")),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),4),("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(t)
    sp(story, 0.4)

    # División de roles
    story.append(Paragraph("División de roles entre los dos:", S["h2"]))
    div = [
        [Paragraph("Persona A (slides 3–6)", S["th"]),
         Paragraph("Persona B (slides 2, 7–11)", S["th"])],
        [Paragraph("• Explica Eigenvector Centrality\n• Explica Degree Centrality\n"
                   "• Explica Betweenness Centrality\n• Explica Closeness Centrality\n"
                   "• Maneja las tablas y gráficos de métricas\n"
                   "• Sabe responder preguntas 4, 5, 6, 11",
                   S["td"]),
         Paragraph("• Presenta el dataset y contexto\n• Explica el cuadro comparativo\n"
                   "• Explica comunidades y Modularidad\n• Analiza C0 y C17\n"
                   "• Entrega las conclusiones\n"
                   "• Sabe responder preguntas 1, 2, 3, 7, 8, 9, 10",
                   S["td"])],
    ]
    t2 = Table(div, colWidths=[avail*0.5, avail*0.5])
    t2.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0),AZUL),
        ("BACKGROUND",(1,0),(1,0),VERDE),
        ("BACKGROUND",(0,1),(0,1),AZUL_CL),
        ("BACKGROUND",(1,1),(1,1),VERDE_CL),
        ("GRID",(0,0),(-1,-1),0.6,colors.HexColor("#BFBFBF")),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),10),
    ]))
    story.append(t2)
    sp(story, 0.3)

    caja(story, S,
        "💡  <b>Tip final:</b> el profe puede preguntarle a cualquiera sobre cualquier tema. "
        "Léanse los scripts del otro también. En especial la diferencia entre las 4 métricas "
        "y por qué usamos solo el componente principal — eso seguro lo pregunta.",
        bg=AMARILLO, borde=AMAR_B)

# ── Main ─────────────────────────────────────────────────────────────────────
def main():
    output = "/home/user/TALLER-/Guia_Practica_Taller3.pdf"
    doc = SimpleDocTemplate(
        output, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=1.8*cm,
        title="Guía de Práctica Taller 3",
    )
    S = estilos()
    story = []
    build(story, S)
    doc.build(story, onFirstPage=footer_cb, onLaterPages=footer_cb)
    print(f"Generado: {output}")

if __name__ == "__main__":
    main()
