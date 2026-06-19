#!/usr/bin/env python3
"""Guiones de presentación basados en el PPT real subido — v2: lenguaje natural, 5 min c/u"""

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

AZUL      = colors.HexColor("#1A4F8A")
AZUL_M    = colors.HexColor("#2E75B6")
AZUL_CL   = colors.HexColor("#DCE6F1")
AZUL_BG   = colors.HexColor("#F0F5FB")
VERDE     = colors.HexColor("#2E7D32")
VERDE_CL  = colors.HexColor("#E8F5E9")
NARANJA   = colors.HexColor("#E65100")
NARAN_CL  = colors.HexColor("#FFF3E0")
MORADO    = colors.HexColor("#6A1B9A")
MOR_CL    = colors.HexColor("#F3E5F5")
ROJO      = colors.HexColor("#B71C1C")
ROJO_CL   = colors.HexColor("#FFEBEE")
GRIS      = colors.HexColor("#555555")
GRIS_CL   = colors.HexColor("#F5F5F5")
AMARILLO  = colors.HexColor("#FFF8E1")
AMAR_B    = colors.HexColor("#F57F17")
NEGRO     = colors.HexColor("#212121")
BLANCO    = colors.white

P1_COLOR  = AZUL
P1_BG     = AZUL_CL
P2_COLOR  = VERDE
P2_BG     = VERDE_CL

avail = W - 2*MARGIN


def S():
    d = {}

    def mk(name, **kw):
        base = dict(fontName="Helvetica", fontSize=10, textColor=NEGRO,
                    leading=15, spaceAfter=4)
        base.update(kw)
        d[name] = ParagraphStyle(name, **base)

    mk("h_port",  fontName="Helvetica-Bold", fontSize=22, textColor=BLANCO,
       alignment=TA_CENTER, leading=28, spaceAfter=6)
    mk("sub_port", fontName="Helvetica",     fontSize=12, textColor=colors.HexColor("#BBDEFB"),
       alignment=TA_CENTER, leading=17, spaceAfter=4)
    mk("h1",  fontName="Helvetica-Bold", fontSize=15, textColor=AZUL,
       spaceBefore=16, spaceAfter=6, leading=19)
    mk("h2",  fontName="Helvetica-Bold", fontSize=12, textColor=AZUL_M,
       spaceBefore=12, spaceAfter=5, leading=16)
    mk("h3",  fontName="Helvetica-Bold", fontSize=11, textColor=NEGRO,
       spaceBefore=10, spaceAfter=3, leading=15)
    mk("body",  fontSize=10.5, leading=15.5, spaceAfter=5, alignment=TA_JUSTIFY)
    mk("body_c", fontSize=10.5, leading=15.5, spaceAfter=5, alignment=TA_CENTER)
    mk("bullet", fontSize=10.5, leading=15, spaceAfter=4,
       leftIndent=16, firstLineIndent=-8)
    mk("nota",  fontName="Helvetica-Oblique", fontSize=9.5, textColor=GRIS,
       leading=13, spaceAfter=4, leftIndent=10, rightIndent=10, alignment=TA_JUSTIFY)
    mk("slide_num", fontName="Helvetica-Bold", fontSize=9, textColor=AZUL_M,
       spaceBefore=10, spaceAfter=2, leading=12)
    mk("habla", fontName="Helvetica-Bold", fontSize=11.5, textColor=NEGRO,
       spaceBefore=10, spaceAfter=3, leading=15)
    mk("guion", fontName="Helvetica", fontSize=11, textColor=NEGRO,
       leading=16.5, spaceAfter=4, leftIndent=6, alignment=TA_JUSTIFY)
    mk("apunte", fontName="Helvetica-Oblique", fontSize=9.5, textColor=GRIS,
       leading=13, spaceAfter=4, leftIndent=14, alignment=TA_LEFT)
    mk("th",  fontName="Helvetica-Bold", fontSize=9.5, textColor=BLANCO,
       alignment=TA_CENTER, leading=12)
    mk("td",  fontName="Helvetica",     fontSize=9.5, textColor=NEGRO,
       alignment=TA_LEFT, leading=13)
    return d


def sp(s, h=0.25):
    s.append(Spacer(1, h * cm))


def hr(s, c=AZUL_M):
    s.append(HRFlowable(width="100%", thickness=0.7, color=c, spaceBefore=3, spaceAfter=5))


def slide_box(story, st, num_txt, titulo, p1=True):
    color = P1_COLOR if p1 else P2_COLOR
    bg    = P1_BG    if p1 else P2_BG
    data = [[
        Paragraph(f"SLIDE {num_txt}", ParagraphStyle("sn2", fontName="Helvetica-Bold",
            fontSize=9, textColor=color, leading=12)),
        Paragraph(titulo, ParagraphStyle("st2", fontName="Helvetica-Bold",
            fontSize=11, textColor=color, leading=14))
    ]]
    t = Table(data, colWidths=[avail * 0.18, avail * 0.82])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX",        (0, 0), (-1, -1), 1.0, color),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING",(0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    sp(story, 0.12)


def dice(story, st, persona, texto, p1=True):
    color = P1_COLOR if p1 else P2_COLOR
    bg    = P1_BG    if p1 else P2_BG
    emoji = "🎤" if p1 else "🎙"
    data = [
        [Paragraph(f'{emoji} {persona} dice:', ParagraphStyle("pn",
            fontName="Helvetica-Bold", fontSize=9.5, textColor=color, leading=12))],
        [Paragraph(f'"{texto}"', st["guion"])],
    ]
    t = Table(data, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), bg),
        ("BACKGROUND", (0, 1), (0, 1), BLANCO),
        ("BOX",        (0, 0), (-1, -1), 0.7, color),
        ("LINEBELOW",  (0, 0), (0, 0), 0.4, color),
        ("LEFTPADDING",(0, 0), (-1, -1), 10),
        ("RIGHTPADDING",(0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    sp(story, 0.15)


def apunte(story, st, texto):
    data = [[Paragraph(f"📌 {texto}", st["apunte"])]]
    t = Table(data, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMARILLO),
        ("BOX",        (0, 0), (-1, -1), 0.5, AMAR_B),
        ("LEFTPADDING",(0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(t)
    sp(story, 0.12)


def caja(story, st, texto, bg, borde):
    data = [[Paragraph(texto, st["body"])]]
    t = Table(data, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX",        (0, 0), (-1, -1), 0.8, borde),
        ("LEFTPADDING",(0, 0), (-1, -1), 10),
        ("RIGHTPADDING",(0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    sp(story, 0.2)


def footer_cb(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRIS)
    if canvas.getPageNumber() > 1:
        canvas.drawRightString(W - MARGIN, 0.9 * cm,
            f"Guiones Taller 3 · APPD 2026     Página {canvas.getPageNumber() - 1}")
        canvas.drawString(MARGIN, 0.9 * cm, "Confidencial — solo para práctica")
    canvas.restoreState()


# ═══════════════════════════════════════════════════════════════════════════════
def build(story, st):

    # ── PORTADA ───────────────────────────────────────────────────────────────
    port_data = [
        [Paragraph("GUIONES DE PRESENTACIÓN", st["h_port"])],
        [Paragraph("Taller 3 · Análisis de Redes Complejas con Gephi", st["sub_port"])],
        [Paragraph("Persona 1  +  Persona 2  ·  5 minutos cada uno", st["sub_port"])],
        [Paragraph("APPD 2026 · Prof. Dr. Rodrigo Salas", st["sub_port"])],
        [Paragraph(" ", st["sub_port"])],
    ]
    t = Table(port_data, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AZUL),
        ("LEFTPADDING",(0, 0), (-1, -1), 20),
        ("RIGHTPADDING",(0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    story.append(t)
    sp(story, 0.5)

    caja(story, st,
        "📖  <b>Qué hay en este documento</b><br/>"
        "1. Explicación de qué se trata el trabajo (para entenderlo desde cero)<br/>"
        "2. Guión de Persona 1 — Slides 1 al 6 — aprox. 5 minutos<br/>"
        "3. Guión de Persona 2 — Slides 7 al 13 — aprox. 5 minutos<br/>"
        "4. Q&A rápido con las preguntas más probables del profesor",
        bg=AZUL_CL, borde=AZUL)

    sp(story, 0.2)
    div = [
        [Paragraph("🎤 Persona 1", ParagraphStyle("d1", fontName="Helvetica-Bold",
             fontSize=11, textColor=P1_COLOR, leading=14, alignment=TA_CENTER)),
         Paragraph("🎙 Persona 2", ParagraphStyle("d2", fontName="Helvetica-Bold",
             fontSize=11, textColor=P2_COLOR, leading=14, alignment=TA_CENTER))],
        [Paragraph(
            "Slide 1 — Portada<br/>"
            "Slide 2 — Agenda<br/>"
            "Slide 3 — Dataset<br/>"
            "Slide 4 — Eigenvector Centrality<br/>"
            "Slide 5 — Degree Centrality<br/>"
            "Slide 6 — Betweenness Centrality<br/>"
            "<b>→ ~5 minutos</b>",
            ParagraphStyle("dt1", fontName="Helvetica", fontSize=10, textColor=NEGRO,
                           leading=15, leftIndent=8)),
         Paragraph(
            "Slide 7 — Closeness Centrality<br/>"
            "Slide 8 — Cuadro Comparativo<br/>"
            "Slide 9 — Comunidades (Modularidad)<br/>"
            "Slide 10 — Comunidad más grande C0<br/>"
            "Slide 11 — Comunidad más compacta C17<br/>"
            "Slide 12 — Conclusiones · Slide 13 — Cierre<br/>"
            "<b>→ ~5 minutos</b>",
            ParagraphStyle("dt2", fontName="Helvetica", fontSize=10, textColor=NEGRO,
                           leading=15, leftIndent=8))],
    ]
    td = Table(div, colWidths=[avail * 0.5, avail * 0.5])
    td.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), P1_BG),
        ("BACKGROUND", (1, 0), (1, 0), P2_BG),
        ("BACKGROUND", (0, 1), (0, 1), BLANCO),
        ("BACKGROUND", (1, 1), (1, 1), BLANCO),
        ("BOX",        (0, 0), (-1, -1), 1.0, GRIS),
        ("INNERGRID",  (0, 0), (-1, -1), 0.5, GRIS),
        ("VALIGN",     (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",(0, 0), (-1, -1), 10),
    ]))
    story.append(td)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # DE QUÉ SE TRATA — EXPLICACIÓN DESDE CERO
    # ═══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("¿De qué se trata este trabajo? — Explicación desde cero", st["h1"]))
    hr(story)

    story.append(Paragraph("En una frase:", st["h2"]))
    caja(story, st,
        "Analizamos con <b>Gephi</b> una red de físicos que publicaron artículos juntos entre 1993 y 2003, "
        "y respondemos: ¿quiénes son los más influyentes?, ¿quién conecta distintos grupos?, "
        "¿cuántos grupos hay y cómo son?",
        bg=AZUL_CL, borde=AZUL)

    story.append(Paragraph("¿Qué es la red?", st["h2"]))
    story.append(Paragraph(
        "Imagínate LinkedIn pero de físicos. Cada físico es un nodo. "
        "Si dos físicos publicaron un paper juntos, hay una arista entre ellos. "
        "La red tiene <b>5.242 físicos</b> y <b>14.496 conexiones</b>.", st["body"]))

    story.append(Paragraph("¿Qué es Gephi?", st["h2"]))
    story.append(Paragraph(
        "Un programa gratuito que muestra la red visualmente (como una telaraña) y calcula "
        "estadísticas: quién es más importante, qué grupos existen, quién conecta esos grupos.", st["body"]))

    story.append(Paragraph("Las 4 métricas que analizamos:", st["h2"]))
    metricas = [
        ["Métrica", "¿Qué mide?", "Analogía simple"],
        ["Eigenvector\nCentrality",
         "No importa solo cuántos coautores tienes,\nsino qué tan importantes son esos coautores.",
         "No es lo mismo 100 amigos cualquiera\nque 100 amigos famosos."],
        ["Degree\nCentrality",
         "¿Con cuántos autores distintos\npublicaste? Cantidad pura.",
         "¿Cuántos contactos tienes\nen el teléfono?"],
        ["Betweenness\nCentrality",
         "¿Por cuántos caminos entre otros\nautores pasas tú?",
         "Eres el único que conoce a todos\nlos grupos en una fiesta."],
        ["Closeness\nCentrality",
         "¿Qué tan cerca estás del resto\nde la red en promedio?",
         "El que pasa el chisme más rápido\npor toda la escuela."],
    ]
    cws = [avail * 0.22, avail * 0.40, avail * 0.38]
    rows = [[Paragraph(c, st["th"] if i == 0 else st["td"]) for c in row]
            for i, row in enumerate(metricas)]
    t = Table(rows, colWidths=cws)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BLANCO, GRIS_CL]),
        ("GRID",       (0, 0), (-1, -1), 0.4, colors.HexColor("#BFBFBF")),
        ("VALIGN",     (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",(0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    sp(story, 0.3)

    story.append(Paragraph("¿Qué son las comunidades?", st["h2"]))
    story.append(Paragraph(
        "Son grupos de físicos que publican mucho entre sí. Gephi los detecta automáticamente "
        "con el <b>algoritmo de Modularidad</b>. Encontramos <b>63 comunidades</b>. "
        "Cada una probablemente es una línea de investigación distinta: "
        "agujeros negros, ondas gravitacionales, gravedad cuántica, etc.", st["body"]))

    story.append(Paragraph("¿Por qué solo usamos el componente principal?", st["h2"]))
    caja(story, st,
        "La red tiene 355 subgrupos desconectados entre sí (como 355 islas). "
        "Si calculamos las métricas sobre todo junto, los resultados salen mal — "
        "un físico aislado con un solo colega aparece como 'el más cercano de todos'. "
        "Por eso trabajamos solo con la isla grande: <b>4.158 físicos</b> (79% del total).",
        bg=NARAN_CL, borde=NARANJA)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # GUIÓN PERSONA 1
    # ═══════════════════════════════════════════════════════════════════════════
    data_port = [
        [Paragraph("🎤  GUIÓN — PERSONA 1", ParagraphStyle(
            "gp1", fontName="Helvetica-Bold", fontSize=18, textColor=BLANCO,
            leading=22, alignment=TA_CENTER))],
        [Paragraph("Slides 1 al 6  ·  aprox. 5 minutos", ParagraphStyle(
            "gp1s", fontName="Helvetica", fontSize=12, textColor=AZUL_CL,
            leading=16, alignment=TA_CENTER))],
    ]
    t = Table(data_port, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), P1_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(t)
    sp(story, 0.4)

    caja(story, st,
        "📌  <b>Antes de empezar:</b> tú abres la presentación. Habla tranquilo, "
        "no muy rápido. Cuando termines slide 6, dile al profe 'le paso la palabra a mi compañero/a' "
        "y míra a Persona 2 como señal.",
        bg=AMARILLO, borde=AMAR_B)
    sp(story, 0.2)

    # ── SLIDE 1 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "1", "Portada", p1=True)
    dice(story, st, "Persona 1",
        "Buenos días, profesor. Somos [nombre 1] y [nombre 2]. "
        "Hoy presentamos el Taller 3, que trata de analizar una red de colaboración científica "
        "usando Gephi. La red se llama ca-GrQc y viene del repositorio SNAP de Stanford.",
        p1=True)
    apunte(story, st, "~20 segundos. No te enredes con más detalles aquí.")

    # ── SLIDE 2 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "2", "Agenda", p1=True)
    dice(story, st, "Persona 1",
        "La presentación tiene dos partes principales. "
        "Primero identificamos los autores más influyentes usando cuatro métricas distintas: "
        "Eigenvector, Degree, Betweenness y Closeness. "
        "Después vemos los grupos de colaboración que se forman en la red. "
        "Terminamos con las conclusiones.",
        p1=True)
    apunte(story, st, "Lee el índice con calma. No te quedes pegado aquí.")

    # ── SLIDE 3 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "3", "Dataset", p1=True)
    dice(story, st, "Persona 1",
        "La red representa a físicos que publicaron juntos entre 1993 y 2003. "
        "Cada autor es un nodo y si dos autores publicaron juntos, hay una arista entre ellos. "
        "En total hay 5.242 autores y 14.496 conexiones. "
        "Pero la red tiene 355 subgrupos desconectados entre sí, "
        "así que para los cálculos usamos solo el grupo principal, "
        "que tiene 4.158 autores — el 79% del total. "
        "Si no lo hacemos así, algunas métricas dan resultados que no tienen sentido.",
        p1=True)
    apunte(story, st,
        "Señala los 4 números grandes de la slide. "
        "La nota del componente principal es importante — el profe puede preguntar por eso.")

    # ── SLIDE 4 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "4", "Eigenvector Centrality", p1=True)
    dice(story, st, "Persona 1",
        "La primera métrica es Eigenvector Centrality. "
        "La idea es que no importa solo cuántos coautores tienes, "
        "sino qué tan importantes son esos coautores. "
        "O sea, no es lo mismo publicar con 10 desconocidos que con 10 autores muy activos en la red. "
        "El nodo 21012 lidera con un valor de 0,156 y 81 coautores. "
        "Sus colaboradores también son muy influyentes, entonces su puntaje sube mucho. "
        "Básicamente es el núcleo de la red.",
        p1=True)
    apunte(story, st,
        "Señala el top 10 y el gráfico. El punto clave: cantidad de coautores no es lo mismo que influencia.")

    # ── SLIDE 5 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "5", "Degree Centrality", p1=True)
    dice(story, st, "Persona 1",
        "La segunda métrica es Degree Centrality, que es más directa: "
        "simplemente cuenta cuántos coautores distintos tiene cada autor. "
        "El nodo 21012 vuelve a liderar con 81 — eso es 15 veces el promedio de la red, que es 5,53. "
        "Pero hay algo interesante: el nodo 21281 tiene 79 coautores, casi lo mismo, "
        "pero no aparece entre los más influyentes en Eigenvector. "
        "Eso significa que sus coautores son menos importantes. "
        "Y sí se ve concentración: pocos autores tienen muchísimas colaboraciones "
        "y la mayoría tiene muy pocas. Eso es una red libre de escala.",
        p1=True)
    apunte(story, st,
        "Señala al nodo 21281 en la tabla. Ahí está el contraste clave entre ser colaborativo vs influyente.")

    # ── SLIDE 6 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "6", "Betweenness Centrality", p1=True)
    dice(story, st, "Persona 1",
        "La tercera métrica es Betweenness Centrality. "
        "Esta mide cuántos caminos entre otros pares de autores pasan por ti. "
        "Si tienes un valor alto, eres un puente: sin ti, grupos distintos no se comunican. "
        "El nodo 13801 es el más crítico: el 5,9% de todos los caminos de la red pasan por él. "
        "Está en la comunidad C0, pero conecta hacia C1, C2 y C3, "
        "que juntas tienen el 24% de los autores del componente principal. "
        "Si lo sacáramos, esas comunidades quedarían aisladas.",
        p1=True)
    apunte(story, st,
        "Señala el esquema visual. Luego entrégate a Persona 2 con claridad.")

    # TRANSICIÓN
    sp(story, 0.2)
    data_tr = [
        [Paragraph("➡  TRANSICIÓN — Persona 1 le dice a Persona 2:",
            ParagraphStyle("tr", fontName="Helvetica-Bold", fontSize=10,
                           textColor=BLANCO, leading=13))],
        [Paragraph(
            '"Le paso la palabra a mi compañero/a, que continúa con Closeness Centrality."',
            ParagraphStyle("trt", fontName="Helvetica-Oblique", fontSize=10.5,
                           textColor=NEGRO, leading=14))],
    ]
    t = Table(data_tr, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), NARANJA),
        ("BACKGROUND", (0, 1), (0, 1), NARAN_CL),
        ("BOX",        (0, 0), (-1, -1), 1.0, NARANJA),
        ("LEFTPADDING",(0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(t)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # GUIÓN PERSONA 2
    # ═══════════════════════════════════════════════════════════════════════════
    data_port2 = [
        [Paragraph("🎙  GUIÓN — PERSONA 2", ParagraphStyle(
            "gp2", fontName="Helvetica-Bold", fontSize=18, textColor=BLANCO,
            leading=22, alignment=TA_CENTER))],
        [Paragraph("Slides 7 al 13  ·  aprox. 5 minutos", ParagraphStyle(
            "gp2s", fontName="Helvetica", fontSize=12, textColor=colors.HexColor("#C8E6C9"),
            leading=16, alignment=TA_CENTER))],
    ]
    t = Table(data_port2, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), P2_COLOR),
        ("TOPPADDING", (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
    ]))
    story.append(t)
    sp(story, 0.4)

    caja(story, st,
        "📌  <b>Antes de empezar:</b> espera a que Persona 1 te dé la señal y avanza al slide 7. "
        "Tú cierras la presentación — termina con seguridad y espera las preguntas.",
        bg=AMARILLO, borde=AMAR_B)
    sp(story, 0.2)

    # ── SLIDE 7 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "7", "Closeness Centrality", p1=False)
    dice(story, st, "Persona 2",
        "Gracias. La cuarta y última métrica es Closeness Centrality, "
        "que mide qué tan central estás dentro de la red. "
        "Para entenderlo: imagínense que la red es un colegio con 4 mil alumnos "
        "y para mandar un mensaje tienen que pasárselo por intermediarios, uno por uno. "
        "Si estás en el centro del colegio, le llegas a cualquiera en pocos pasos. "
        "Si estás en una esquina, tienes que pasar por muchos intermediarios. "
        "El nodo 13801 es el que está más al centro de toda la red: "
        "llega a cualquier autor en solo 4 pasos en promedio, "
        "mientras que el autor promedio necesita 6 pasos. "
        "Eso lo convierte en el autor que puede difundir su trabajo más rápido "
        "a más gente en toda la red.",
        p1=False)
    apunte(story, st,
        "Señala el contraste 4,08 pasos vs 6,05 pasos. La analogía del colegio ayuda mucho acá.")

    # ── SLIDE 8 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "8", "Cuadro Comparativo", p1=False)
    dice(story, st, "Persona 2",
        "Este slide resume todo lo que analizamos. "
        "Hicimos cuatro rankings, uno por cada métrica, "
        "y la pregunta es: ¿hay autores que sean importantes en varios rankings a la vez? "
        "En total, 27 autores distintos aparecen en algún top 10. "
        "Pero solo tres aparecen en tres rankings al mismo tiempo: el 21012, el 12365 y el 17655. "
        "El 21012 es el más colaborativo y el más influyente. "
        "Pero el nodo 13801 es el número 1 en las dos métricas de conectividad: "
        "Betweenness y Closeness. "
        "O sea, es el puente más importante Y el más céntrico de la red. "
        "Eso lo hace más estratégico que el 21012 para que la red funcione, "
        "aunque tenga menos coautores. "
        "La conclusión es que ser importante en una red científica no es una sola cosa: "
        "hay distintos tipos de importancia y ningún autor domina todo.",
        p1=False)
    apunte(story, st,
        "Señala la fila del 13801 y la del 21012. Ese contraste es el punto más rico de la slide.")

    # ── SLIDE 9 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "9", "Comunidades — Modularidad", p1=False)
    dice(story, st, "Persona 2",
        "Pasamos al segundo bloque del trabajo: las comunidades. "
        "La pregunta acá es si hay grupos de físicos que publican mucho entre sí "
        "y poco con el resto. Para detectarlos, usamos el algoritmo de Modularidad de Gephi, "
        "que busca automáticamente grupos con muchas conexiones internas y pocas hacia afuera. "
        "Encontramos 63 grupos. "
        "Y calculamos un valor llamado Q, que es básicamente la nota de qué tan bien definidos "
        "están esos grupos. Va de 0 a 1: si Q fuera 0, los grupos no son reales. "
        "Si fuera 1, son perfectos. Nosotros obtuvimos Q igual a 0,80, que es muy alto, "
        "entonces podemos decir con confianza que estas 63 comunidades son reales. "
        "La más grande, C0, tiene 901 autores, que es casi el 22% de toda la red. "
        "Y las 5 primeras juntas concentran más de la mitad de todos los autores.",
        p1=False)
    apunte(story, st,
        "Señala la tabla y el gráfico. Explica el Q primero, luego los números de C0 a C4.")

    # ── SLIDE 10 ──────────────────────────────────────────────────────────────
    slide_box(story, st, "10", "Comunidad más grande — C0 (901 nodos)", p1=False)
    dice(story, st, "Persona 2",
        "Veamos la comunidad más grande en detalle. C0 tiene 901 autores. "
        "Para entender cómo está conectada internamente miramos dos cosas. "
        "Primero, la densidad: 0,005. "
        "Eso significa que de todas las colaboraciones posibles entre sus 901 miembros, "
        "solo existe el 0,5%. "
        "O sea, C0 es enorme pero dispersa — no todos se conocen entre sí. "
        "Segundo, el clustering: 0,51. "
        "Si dos autores de C0 tienen un coautor en común, "
        "hay 51% de probabilidad de que ellos también hayan publicado juntos. "
        "Algo importante: los líderes de cada métrica dentro de C0 son distintos. "
        "No hay un solo jefe — hay distintos tipos de liderazgo especializado. "
        "Y el nodo 13801, que es el puente más crítico de toda la red, vive en C0. "
        "O sea, C0 no solo es la comunidad más grande, sino también el núcleo que conecta todo.",
        p1=False)
    apunte(story, st,
        "Señala la tabla fila por fila. El punto de los liderazgos distintos es lo más interesante.")

    # ── SLIDE 11 ──────────────────────────────────────────────────────────────
    slide_box(story, st, "11", "Comunidad más compacta — C17 (47 nodos)", p1=False)
    dice(story, st, "Persona 2",
        "Para contrastar con C0, veamos C17, la comunidad más compacta. "
        "Tiene solo 47 autores — mucho más pequeña. "
        "Pero su densidad es 0,684: el 68% de todas las colaboraciones posibles "
        "entre esos 47 autores existen de verdad. "
        "Y su clustering es 0,86: si dos miembros comparten un coautor, "
        "hay 86% de probabilidad de que ellos también hayan publicado juntos. "
        "Casi todos publican con casi todos. "
        "Probablemente es un equipo de la misma institución o trabajando en un problema muy específico, "
        "donde la colaboración es estrecha y constante. "
        "Si comparamos con C0, que tiene densidad de solo 0,005, "
        "son mundos completamente distintos: "
        "C0 es grande y dispersa, C17 es pequeña y todos se conocen.",
        p1=False)
    apunte(story, st,
        "El contraste C17 densidad 0,684 vs C0 densidad 0,005 es impactante — úsalo.")

    # ── SLIDE 12 ──────────────────────────────────────────────────────────────
    slide_box(story, st, "12", "Conclusiones", p1=False)
    dice(story, st, "Persona 2",
        "Para cerrar, los cinco hallazgos más importantes del análisis. "
        "Uno: la red es libre de escala. "
        "Unos pocos autores concentran la mayoría de las colaboraciones — "
        "el nodo 21012 tiene 81 coautores cuando el promedio es solo 5,53. "
        "Como Instagram, donde unos pocos tienen millones de seguidores y el resto tiene decenas. "
        "Dos: la influencia es multidimensional. "
        "Ser popular, ser influyente, ser un puente y estar cerca de todos son cosas distintas, "
        "y ningún autor domina en todo. "
        "Tres: el nodo 13801 es el más crítico para la cohesión de la red. "
        "Si lo sacamos, grupos enteros quedan desconectados — es el más importante "
        "aunque no sea el más famoso. "
        "Cuatro: encontramos 63 comunidades con un Q de 0,80, "
        "lo que indica que son grupos reales, probablemente líneas de investigación distintas. "
        "Y cinco: dentro de esas comunidades hay dos extremos — "
        "C0, que es enorme y dispersa pero conecta todo, "
        "y C17, que es pequeña pero casi todos sus miembros se conocen entre sí.",
        p1=False)
    apunte(story, st,
        "Lee cada punto con pausa. Este es el cierre — tómate el tiempo, no te apures.")

    # ── SLIDE 13 ──────────────────────────────────────────────────────────────
    slide_box(story, st, "13", "Cierre y Referencias", p1=False)
    dice(story, st, "Persona 2",
        "Eso es todo de nuestra parte. "
        "Las referencias principales son el paper de Blondel del año 2008, "
        "que describe el algoritmo de Louvain que usamos para detectar las comunidades, "
        "y el repositorio SNAP de Stanford, de donde descargamos la red. "
        "Quedamos disponibles para cualquier pregunta, profesor.",
        p1=False)
    apunte(story, st,
        "Di esto tranquilo, mira al profe al terminar y espera con seguridad. No agregues nada más.")

    sp(story, 0.3)

    # ═══════════════════════════════════════════════════════════════════════════
    # Q&A RÁPIDO
    # ═══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Q&A — Respuestas cortas para las preguntas más probables", st["h1"]))
    hr(story)
    caja(story, st,
        "⚡  <b>Cualquiera de los dos puede responder. "
        "Estas son las respuestas más importantes en una frase.</b>",
        bg=ROJO_CL, borde=ROJO)
    sp(story, 0.2)

    qa = [
        ("¿Por qué solo el componente principal?",
         "Porque las métricas de caminos no funcionan entre grupos desconectados. "
         "Un nodo aislado con un solo vecino aparece como 'el más cercano de todos' y eso es falso."),
        ("¿Qué es una red libre de escala?",
         "Una red donde pocos nodos tienen muchísimas conexiones y la mayoría tiene muy pocas. "
         "Como Instagram: unos pocos con millones de seguidores y el resto con decenas."),
        ("¿Qué significa Q = 0,80?",
         "La modularidad va de 0 a 1. Un valor de 0,80 indica que las comunidades son reales y "
         "bien separadas — hay muchas conexiones dentro de cada grupo y pocas entre grupos."),
        ("¿Por qué 13801 es más importante que 21012?",
         "El 21012 tiene más coautores pero concentrados en su comunidad. "
         "El 13801 conecta comunidades distintas — si lo sacas, la red se rompe. "
         "Es más estratégico aunque tenga menos colaboraciones."),
        ("¿Qué diferencia hay entre Betweenness y Closeness?",
         "Betweenness: ¿por cuántos caminos entre otros pasas tú? → eres un puente. "
         "Closeness: ¿qué tan corta es tu distancia al resto? → estás en el centro geográfico."),
        ("¿Por qué C17 tiene mayor densidad que C0 si C0 es más grande?",
         "La densidad no depende del tamaño sino de la proporción de conexiones posibles que existen. "
         "C0 tiene 901 nodos → más de 400 mil pares posibles, solo 2.150 existen. "
         "C17 tiene 47 nodos → 1.081 pares posibles, 739 existen."),
        ("¿Qué representa cada comunidad en la realidad?",
         "Probablemente cada comunidad es una línea de investigación específica: "
         "agujeros negros, ondas gravitacionales, cosmología inflacionaria, etc. "
         "No podemos confirmarlo porque los IDs son anónimos."),
        ("¿Qué es el clustering coefficient?",
         "Si A y B tienen un coautor en común, mide la probabilidad de que A y B "
         "también hayan publicado juntos. En C17 es 0,86 — un 86% de probabilidad."),
    ]

    for q, a in qa:
        data_qa = [
            [Paragraph(f"❓ {q}", ParagraphStyle("qq", fontName="Helvetica-Bold",
                fontSize=10.5, textColor=ROJO, leading=14))],
            [Paragraph(a, st["body"])],
        ]
        t = Table(data_qa, colWidths=[avail])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), ROJO_CL),
            ("BACKGROUND", (0, 1), (0, 1), GRIS_CL),
            ("BOX",        (0, 0), (-1, -1), 0.7, ROJO),
            ("LINEBELOW",  (0, 0), (0, 0), 0.4, ROJO),
            ("LEFTPADDING",(0, 0), (-1, -1), 10),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        story.append(t)
        sp(story, 0.18)

    sp(story, 0.3)
    caja(story, st,
        "✅  <b>Tip final:</b> si no saben la respuesta a algo, no inventen. "
        "Digan: 'Esa parte no la analizamos en detalle, pero lo que sí podemos decir es...' "
        "El profe valora la honestidad.",
        bg=VERDE_CL, borde=VERDE)


def main():
    out = "/home/user/TALLER-/Guiones_Presentacion_Taller3.pdf"
    doc = SimpleDocTemplate(out, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=1.8 * cm)
    st = S()
    story = []
    build(story, st)
    doc.build(story, onFirstPage=footer_cb, onLaterPages=footer_cb)
    print(f"Generado: {out}")


if __name__ == "__main__":
    main()
