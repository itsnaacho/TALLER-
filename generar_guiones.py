#!/usr/bin/env python3
"""Guiones de presentación basados en el PPT real subido"""

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

P1_COLOR  = AZUL      # Persona 1
P1_BG     = AZUL_CL
P2_COLOR  = VERDE     # Persona 2
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
    mk("sub_port",fontName="Helvetica",      fontSize=12, textColor=colors.HexColor("#BBDEFB"),
       alignment=TA_CENTER, leading=17, spaceAfter=4)
    mk("h1",  fontName="Helvetica-Bold", fontSize=15, textColor=AZUL,
       spaceBefore=16, spaceAfter=6, leading=19)
    mk("h2",  fontName="Helvetica-Bold", fontSize=12, textColor=AZUL_M,
       spaceBefore=12, spaceAfter=5, leading=16)
    mk("h3",  fontName="Helvetica-Bold", fontSize=11, textColor=NEGRO,
       spaceBefore=10, spaceAfter=3, leading=15)
    mk("body",fontSize=10.5, leading=15.5, spaceAfter=5, alignment=TA_JUSTIFY)
    mk("body_c",fontSize=10.5, leading=15.5, spaceAfter=5, alignment=TA_CENTER)
    mk("bullet",fontSize=10.5, leading=15, spaceAfter=4,
       leftIndent=16, firstLineIndent=-8)
    mk("nota", fontName="Helvetica-Oblique", fontSize=9.5, textColor=GRIS,
       leading=13, spaceAfter=4, leftIndent=10, rightIndent=10, alignment=TA_JUSTIFY)
    mk("slide_num", fontName="Helvetica-Bold", fontSize=9, textColor=AZUL_M,
       spaceBefore=10, spaceAfter=2, leading=12)
    mk("habla",fontName="Helvetica-Bold", fontSize=11.5, textColor=NEGRO,
       spaceBefore=10, spaceAfter=3, leading=15)
    mk("guion",fontName="Helvetica", fontSize=11, textColor=NEGRO,
       leading=16.5, spaceAfter=4, leftIndent=6, alignment=TA_JUSTIFY)
    mk("apunte",fontName="Helvetica-Oblique", fontSize=9.5, textColor=GRIS,
       leading=13, spaceAfter=4, leftIndent=14, alignment=TA_LEFT)
    mk("th",  fontName="Helvetica-Bold", fontSize=9.5, textColor=BLANCO,
       alignment=TA_CENTER, leading=12)
    mk("td",  fontName="Helvetica",     fontSize=9.5, textColor=NEGRO,
       alignment=TA_LEFT, leading=13)
    return d

def sp(s, h=0.25): s.append(Spacer(1, h*cm))
def hr(s, c=AZUL_M): s.append(HRFlowable(width="100%", thickness=0.7,
                                            color=c, spaceBefore=3, spaceAfter=5))

def slide_box(story, st, num_txt, titulo, p1=True):
    """Encabezado de slide dentro del guión."""
    color = P1_COLOR if p1 else P2_COLOR
    bg    = P1_BG    if p1 else P2_BG
    data = [[
        Paragraph(f"📊 {num_txt}", ParagraphStyle("sn2",fontName="Helvetica-Bold",
            fontSize=9,textColor=color,leading=12)),
        Paragraph(titulo, ParagraphStyle("st2",fontName="Helvetica-Bold",
            fontSize=11,textColor=color,leading=14))
    ]]
    t = Table(data, colWidths=[avail*0.18, avail*0.82])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("BOX",(0,0),(-1,-1),1.0,color),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("LEFTPADDING",(0,0),(-1,-1),8),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(t)
    sp(story, 0.12)

def dice(story, st, persona, texto, p1=True):
    """Bloque de lo que dice la persona."""
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
        ("BACKGROUND",(0,0),(0,0), bg),
        ("BACKGROUND",(0,1),(0,1), BLANCO),
        ("BOX",(0,0),(-1,-1),0.7,color),
        ("LINEBELOW",(0,0),(0,0),0.4,color),
        ("LEFTPADDING",(0,0),(-1,-1),10),
        ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(t)
    sp(story, 0.15)

def apunte(story, st, texto):
    data = [[Paragraph(f"📌 {texto}", st["apunte"])]]
    t = Table(data, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), AMARILLO),
        ("BOX",(0,0),(-1,-1),0.5, AMAR_B),
        ("LEFTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    story.append(t)
    sp(story, 0.12)

def caja(story, st, texto, bg, borde):
    data = [[Paragraph(texto, st["body"])]]
    t = Table(data, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), bg),
        ("BOX",(0,0),(-1,-1),0.8, borde),
        ("LEFTPADDING",(0,0),(-1,-1),10),
        ("RIGHTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(t)
    sp(story, 0.2)

def footer_cb(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(GRIS)
    if canvas.getPageNumber() > 1:
        canvas.drawRightString(W-MARGIN, 0.9*cm,
            f"Guiones Taller 3 · APPD 2026     Página {canvas.getPageNumber()-1}")
        canvas.drawString(MARGIN, 0.9*cm, "Confidencial — solo para práctica")
    canvas.restoreState()

# ═══════════════════════════════════════════════════════════════════════════════
def build(story, st):

    # ── PORTADA ───────────────────────────────────────────────────────────────
    port_data = [
        [Paragraph("GUIONES DE PRESENTACIÓN", st["h_port"])],
        [Paragraph("Taller 3 · Análisis de Redes Complejas con Gephi", st["sub_port"])],
        [Paragraph("Persona 1  +  Persona 2  ·  10 a 15 minutos", st["sub_port"])],
        [Paragraph("APPD 2026 · Prof. Dr. Rodrigo Salas", st["sub_port"])],
        [Paragraph(" ", st["sub_port"])],
    ]
    t = Table(port_data, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), AZUL),
        ("LEFTPADDING",(0,0),(-1,-1),20),
        ("RIGHTPADDING",(0,0),(-1,-1),20),
        ("TOPPADDING",(0,0),(-1,-1),12),
        ("BOTTOMPADDING",(0,0),(-1,-1),10),
    ]))
    story.append(t)
    sp(story, 0.5)

    # Qué hay en este documento
    caja(story, st,
        "📖  <b>Qué hay en este documento</b><br/>"
        "1. Explicación de qué se trata el trabajo (para entenderlo desde cero)<br/>"
        "2. Guión completo de Persona 1 con sus slides y lo que debe decir<br/>"
        "3. Guión completo de Persona 2 con sus slides y lo que debe decir<br/>"
        "4. Señales de paso para coordinar entre los dos",
        bg=AZUL_CL, borde=AZUL)

    # División de slides
    sp(story, 0.2)
    div = [
        [Paragraph("🎤 Persona 1", ParagraphStyle("d1",fontName="Helvetica-Bold",
            fontSize=11,textColor=P1_COLOR,leading=14,alignment=TA_CENTER)),
         Paragraph("🎙 Persona 2", ParagraphStyle("d2",fontName="Helvetica-Bold",
            fontSize=11,textColor=P2_COLOR,leading=14,alignment=TA_CENTER))],
        [Paragraph(
            "Slide 1 — Portada<br/>"
            "Slide 2 — Contenido/Agenda<br/>"
            "Slide 3 — Dataset<br/>"
            "Slide 4 — Eigenvector Centrality<br/>"
            "Slide 5 — Degree Centrality<br/>"
            "Slide 6 — Betweenness Centrality<br/>"
            "<b>→ ~6–7 minutos</b>",
            ParagraphStyle("dt1",fontName="Helvetica",fontSize=10,textColor=NEGRO,
                           leading=15,leftIndent=8)),
         Paragraph(
            "Slide 7 — Closeness Centrality<br/>"
            "Slide 8 — Cuadro Comparativo<br/>"
            "Slide 9 — Comunidades (Modularidad)<br/>"
            "Slide 10 — Comunidad más grande C0<br/>"
            "Slide 11 — Comunidad más compacta C17<br/>"
            "Slide 12 — Conclusiones · Slide 13 — Cierre<br/>"
            "<b>→ ~7–8 minutos</b>",
            ParagraphStyle("dt2",fontName="Helvetica",fontSize=10,textColor=NEGRO,
                           leading=15,leftIndent=8))],
    ]
    td = Table(div, colWidths=[avail*0.5, avail*0.5])
    td.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), P1_BG),
        ("BACKGROUND",(1,0),(1,0), P2_BG),
        ("BACKGROUND",(0,1),(0,1), BLANCO),
        ("BACKGROUND",(1,1),(1,1), BLANCO),
        ("BOX",(0,0),(-1,-1),1.0, GRIS),
        ("INNERGRID",(0,0),(-1,-1),0.5, GRIS),
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("TOPPADDING",(0,0),(-1,-1),8),
        ("BOTTOMPADDING",(0,0),(-1,-1),8),
        ("LEFTPADDING",(0,0),(-1,-1),10),
    ]))
    story.append(td)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # DE QUÉ SE TRATA — EXPLICACIÓN DESDE CERO
    # ═══════════════════════════════════════════════════════════════════════════
    story.append(Paragraph("¿De qué se trata este trabajo? — Explicación desde cero", st["h1"]))
    hr(story)

    story.append(Paragraph("El contexto en una frase:", st["h2"]))
    caja(story, st,
        "Analizamos con un programa llamado <b>Gephi</b> una red de físicos que publicaron "
        "artículos científicos juntos entre 1993 y 2003, y respondemos: "
        "¿quiénes son los más importantes?, ¿por qué?, ¿hay grupos?, ¿quién conecta esos grupos?",
        bg=AZUL_CL, borde=AZUL)

    story.append(Paragraph("¿Qué es una 'red de colaboración científica'?", st["h2"]))
    story.append(Paragraph(
        "Imagínate una red social como Instagram, pero de físicos. Cada físico es una cuenta "
        "(un <b>nodo</b> en la red). Cada vez que dos físicos publican un artículo juntos, "
        "aparece una conexión entre ellos (una <b>arista</b>). "
        "El resultado es una red enorme con 5.242 físicos y 14.496 conexiones.", st["body"]))

    story.append(Paragraph("¿Qué es Gephi?", st["h2"]))
    story.append(Paragraph(
        "Gephi es un programa gratuito que te muestra esta red visualmente (como una telaraña) "
        "y calcula estadísticas sobre ella. Nosotros lo usamos para responder las preguntas "
        "del taller: quiénes son más influyentes, cuántos grupos hay, etc.", st["body"]))

    story.append(Paragraph("¿Qué son las 4 métricas que analizamos?", st["h2"]))
    metricas = [
        ["Métrica", "¿Qué mide?", "Analogía simple"],
        ["Eigenvector\nCentrality",
         "Si tus coautores son importantes,\ntú también subes en el ranking.",
         "No es lo mismo tener 100 amigos\ncualquiera que 100 amigos famosos."],
        ["Degree\nCentrality",
         "Simplemente: ¿con cuántos\nautores distintos publicaste?",
         "¿Cuántos contactos tienes\nen el teléfono?"],
        ["Betweenness\nCentrality",
         "¿Por cuántos caminos entre\notros autores pasas tú?",
         "Eres el único que conoce\na todos los grupos en una fiesta."],
        ["Closeness\nCentrality",
         "¿Qué tan cerca estás\ndel resto de la red?",
         "El que puede pasar el chisme\nmás rápido en toda la escuela."],
    ]
    cws = [avail*0.22, avail*0.40, avail*0.38]
    rows = [[Paragraph(c, st["th"] if i==0 else st["td"]) for c in row]
            for i,row in enumerate(metricas)]
    t = Table(rows, colWidths=cws)
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,0),AZUL),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),[BLANCO,GRIS_CL]),
        ("GRID",(0,0),(-1,-1),0.4,colors.HexColor("#BFBFBF")),
        ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ("LEFTPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(t)
    sp(story, 0.3)

    story.append(Paragraph("¿Qué son las 'comunidades'?", st["h2"]))
    story.append(Paragraph(
        "Son grupos de físicos que publican mucho entre sí. El programa los detecta "
        "automáticamente usando el <b>algoritmo de Modularidad</b> — básicamente detecta "
        "los 'grupos de WhatsApp' dentro de la red. Nosotros encontramos 63 comunidades. "
        "Cada una probablemente es una línea de investigación distinta: "
        "agujeros negros, ondas gravitacionales, gravedad cuántica, etc.", st["body"]))

    story.append(Paragraph("¿Por qué solo usamos el 'componente principal'?", st["h2"]))
    caja(story, st,
        "La red tiene 355 grupos separados sin conexión entre sí (como 355 islas). "
        "Si calculamos métricas sobre todas las islas juntas, los resultados salen mal: "
        "un físico con un solo colega en una isla chica aparece como 'el más cercano de todos'. "
        "Por eso trabajamos solo con la isla grande: 4.158 físicos que sí están conectados.",
        bg=NARAN_CL, borde=NARANJA)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # GUIÓN PERSONA 1
    # ═══════════════════════════════════════════════════════════════════════════
    data_port = [[Paragraph("🎤  GUIÓN — PERSONA 1", ParagraphStyle(
        "gp1", fontName="Helvetica-Bold", fontSize=18, textColor=BLANCO,
        leading=22, alignment=TA_CENTER))],
        [Paragraph("Slides 1 al 6  ·  aprox. 6–7 minutos", ParagraphStyle(
        "gp1s", fontName="Helvetica", fontSize=12, textColor=AZUL_CL,
        leading=16, alignment=TA_CENTER))]]
    t = Table(data_port, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), P1_COLOR),
        ("TOPPADDING",(0,0),(-1,-1),14),
        ("BOTTOMPADDING",(0,0),(-1,-1),14),
    ]))
    story.append(t)
    sp(story, 0.4)

    caja(story, st,
        "📌  <b>Antes de empezar:</b> tú abres la presentación. "
        "Habla tranquilo, no muy rápido. "
        "Cuando termines tu última slide, dile al profe 'le paso la palabra a mi compañero/a' "
        "y miras a Persona 2 como señal.",
        bg=AMARILLO, borde=AMAR_B)
    sp(story, 0.2)

    # ── SLIDE 1 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 1", "Portada", p1=True)
    dice(story, st, "Persona 1",
        "Buenos días, profesor. Somos [nombre 1] y [nombre 2]. "
        "Vamos a presentar el Taller 3, que consiste en analizar una red de "
        "colaboración científica usando Gephi. "
        "La red se llama ca-GrQc y viene del repositorio SNAP de Stanford.",
        p1=True)
    apunte(story, st, "Tiempo aprox: 20 segundos. No te enredes con más detalles aquí.")

    # ── SLIDE 2 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 2", "Contenido / Agenda", p1=True)
    dice(story, st, "Persona 1",
        "En esta presentación vamos a cubrir dos grandes bloques. "
        "Primero, identificamos los autores más influyentes usando cuatro métricas distintas: "
        "Eigenvector, Degree, Betweenness y Closeness. "
        "Después analizamos las comunidades de autores usando el algoritmo de Modularidad. "
        "Cerramos con las conclusiones principales.",
        p1=True)
    apunte(story, st, "Solo lee el índice con calma. No te quedes pegado aquí.")

    # ── SLIDE 3 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 3", "Descripción del Dataset", p1=True)
    dice(story, st, "Persona 1",
        "La red que analizamos representa colaboraciones entre físicos que publicaron "
        "en la plataforma arXiv entre 1993 y 2003. "
        "Cada nodo es un autor y cada arista significa que dos autores publicaron juntos "
        "al menos una vez. "
        "En total tenemos 5.242 autores y 14.496 colaboraciones. "
        "La red tiene 355 grupos desconectados entre sí, así que para los cálculos "
        "trabajamos solo con el grupo principal, que tiene 4.158 autores — "
        "el 79% de la red. "
        "Si no lo hacemos así, algunas métricas dan resultados engañosos.",
        p1=True)
    apunte(story, st,
        "Señala los 4 números grandes de la slide. "
        "La nota metodológica es importante — el profe puede preguntar por eso.")

    # ── SLIDE 4 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 4", "Eigenvector Centrality — autores más influyentes", p1=True)
    dice(story, st, "Persona 1",
        "La primera métrica es Eigenvector Centrality. "
        "Lo que mide no es solo cuántos coautores tienes, sino qué tan importantes son esos coautores. "
        "Si publicas con autores muy conectados, tu puntaje sube. "
        "El nodo número 21012 tiene el valor más alto con 0,156. "
        "Eso significa que no solo tiene muchas colaboraciones — tiene 81 en total — "
        "sino que sus coautores también son activos e influyentes dentro de la red. "
        "Es básicamente el núcleo de todo. "
        "Entonces, respecto a la pregunta del profe: ser influyente en una red científica "
        "no es lo mismo que publicar mucho. "
        "Lo que importa es con quién publicas.",
        p1=True)
    apunte(story, st,
        "Señala la tabla del top 10 y el gráfico de barras. "
        "El punto clave es la distinción: cantidad de coautores ≠ influencia.")

    # ── SLIDE 5 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 5", "Degree Centrality — autores más colaborativos", p1=True)
    dice(story, st, "Persona 1",
        "La segunda métrica es Degree Centrality. Esta sí es más simple: "
        "mide cuántos coautores distintos tiene cada autor. "
        "El nodo 21012 vuelve a liderar con 81 colaboraciones — "
        "eso es 15 veces más que el promedio de la red, que es solo 5,53. "
        "Entonces, respecto a si hay diferencia entre ser influyente y ser colaborativo: "
        "sí, hay una diferencia importante. "
        "Por ejemplo, el nodo 21281 tiene 79 coautores, el segundo mayor de la red, "
        "pero no aparece entre los más influyentes. "
        "Eso nos dice que sus coautores son menos importantes. "
        "Y sí se observa una concentración clara: "
        "pocos autores concentran la mayoría de las colaboraciones, "
        "lo que es típico de lo que se llama una red libre de escala.",
        p1=True)
    apunte(story, st,
        "Señala el nodo 21281 en la tabla — ahí está el contraste clave. "
        "'Red libre de escala' es un concepto que puede preguntar el profe.")

    # ── SLIDE 6 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 6", "Betweenness Centrality — autores puente", p1=True)
    dice(story, st, "Persona 1",
        "La tercera métrica es Betweenness Centrality. "
        "Esta mide cuántos caminos entre otros pares de autores pasan por ti. "
        "Un valor alto significa que eres un puente: sin ti, grupos distintos no se conectan. "
        "El nodo 13801 tiene el valor más alto: el 5,9% de todos los caminos de la red pasan por él. "
        "Si lo eliminamos, se corta esa conexión. "
        "Y aquí lo interesante: los nodos 13801, 9572 y 14599 están en la comunidad C0, "
        "pero actúan como puentes hacia C1, C2 y C3. "
        "Esas tres comunidades representan el 24% de los autores del componente principal. "
        "Si sacamos los tres puentes principales al mismo tiempo, "
        "la red probablemente se fragmentaría y esas comunidades quedarían aisladas.",
        p1=True)
    apunte(story, st,
        "Señala el esquema visual de la derecha con las comunidades. "
        "Luego entrégate a Persona 2 con claridad.")

    # TRANSICIÓN
    sp(story, 0.2)
    data_tr = [[Paragraph(
        "➡  TRANSICIÓN  —  Persona 1 le dice a Persona 2:",
        ParagraphStyle("tr",fontName="Helvetica-Bold",fontSize=10,
                       textColor=BLANCO,leading=13))],
        [Paragraph(
        '"Le paso la palabra a mi compañero/a, que va a continuar con Closeness Centrality."',
        ParagraphStyle("trt",fontName="Helvetica-Oblique",fontSize=10.5,
                       textColor=NEGRO,leading=14))]]
    t = Table(data_tr, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(0,0), NARANJA),
        ("BACKGROUND",(0,1),(0,1), NARAN_CL),
        ("BOX",(0,0),(-1,-1),1.0, NARANJA),
        ("LEFTPADDING",(0,0),(-1,-1),10),
        ("TOPPADDING",(0,0),(-1,-1),6),
        ("BOTTOMPADDING",(0,0),(-1,-1),6),
    ]))
    story.append(t)

    story.append(PageBreak())

    # ═══════════════════════════════════════════════════════════════════════════
    # GUIÓN PERSONA 2
    # ═══════════════════════════════════════════════════════════════════════════
    data_port2 = [[Paragraph("🎙  GUIÓN — PERSONA 2", ParagraphStyle(
        "gp2", fontName="Helvetica-Bold", fontSize=18, textColor=BLANCO,
        leading=22, alignment=TA_CENTER))],
        [Paragraph("Slides 7 al 13  ·  aprox. 7–8 minutos", ParagraphStyle(
        "gp2s", fontName="Helvetica", fontSize=12, textColor=colors.HexColor("#C8E6C9"),
        leading=16, alignment=TA_CENTER))]]
    t = Table(data_port2, colWidths=[avail])
    t.setStyle(TableStyle([
        ("BACKGROUND",(0,0),(-1,-1), P2_COLOR),
        ("TOPPADDING",(0,0),(-1,-1),14),
        ("BOTTOMPADDING",(0,0),(-1,-1),14),
    ]))
    story.append(t)
    sp(story, 0.4)

    caja(story, st,
        "📌  <b>Antes de empezar tu parte:</b> espera a que Persona 1 te dé la señal "
        "y avanza tú al slide 7. "
        "Tú cierras la presentación — termina con seguridad y espera las preguntas.",
        bg=AMARILLO, borde=AMAR_B)
    sp(story, 0.2)

    # ── SLIDE 7 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 7", "Closeness Centrality — quiénes difunden más rápido", p1=False)
    dice(story, st, "Persona 2",
        "Gracias. Voy a continuar con la cuarta métrica: Closeness Centrality. "
        "Esta mide qué tan cerca estás del resto de la red en promedio. "
        "Un valor alto significa que puedes llegar a cualquier autor en muy pocos pasos. "
        "El nodo 13801 lidera también acá con un valor de 0,245, "
        "lo que significa que alcanza a cualquier autor en promedio en 4 pasos. "
        "El promedio de la red necesita 6 pasos. "
        "Por eso estos autores pueden difundir conocimiento más rápido: "
        "su trabajo llega a más investigadores con menos intermediarios. "
        "Están en el centro geográfico de la red.",
        p1=False)
    apunte(story, st,
        "Señala la comparativa visual de pasos de la derecha. "
        "El contraste 4,08 vs 6,05 es el punto que hay que marcar bien.")

    # ── SLIDE 8 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 8", "Cuadro Comparativo de Métricas", p1=False)
    dice(story, st, "Persona 2",
        "Ahora en el cuadro comparativo vemos quién aparece en más rankings. "
        "En total, 27 autores aparecen en algún top 10. "
        "Solo tres de ellos están en tres métricas a la vez: los nodos 21012, 12365 y 17655. "
        "El nodo 21012 es el más completo: lidera en colaboraciones, influencia y cercanía. "
        "Pero hay algo importante: el nodo 13801 aparece solo en dos métricas, "
        "Betweenness y Closeness, pero lidera ambas con el puesto número 1. "
        "Eso lo hace más estratégico que el 21012 para la cohesión de toda la red. "
        "La conclusión es que la influencia en una red científica es multidimensional: "
        "ningún autor domina todo, y hay distintos tipos de importancia.",
        p1=False)
    apunte(story, st,
        "Señala las filas verdes (los de 3 métricas) y luego la fila del 13801. "
        "Esa comparación 21012 vs 13801 es el punto más rico de esta slide.")

    # ── SLIDE 9 ───────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 9", "Detección de Comunidades — Modularidad", p1=False)
    dice(story, st, "Persona 2",
        "Ahora pasamos al segundo bloque: las comunidades. "
        "Usamos el algoritmo de Modularidad de Gephi, que detecta automáticamente "
        "grupos de autores que colaboran mucho entre sí. "
        "Encontramos 63 comunidades con un valor de modularidad Q igual a 0,80. "
        "Ese valor es muy alto — está cerca de 1, que es el máximo. "
        "Significa que las comunidades detectadas son reales y bien definidas. "
        "La comunidad más grande, que llamamos C0, tiene 901 autores, "
        "que es el 21,7% del componente principal. "
        "Las 5 primeras comunidades juntas reúnen más de la mitad de los autores. "
        "Entonces respondiendo la pregunta: la red no está ni completamente fragmentada "
        "ni completamente centralizada. "
        "Es una estructura intermedia, con un núcleo grande y muchos grupos pequeños. "
        "Cada comunidad probablemente representa una línea de investigación específica "
        "dentro de la relatividad general: agujeros negros, ondas gravitacionales, etc.",
        p1=False)
    apunte(story, st,
        "Señala la tabla de distribución y el gráfico de barras. "
        "Nombra las comunidades C0 a C4 como las más grandes.")

    # ── SLIDE 10 ──────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 10", "Comunidad más Grande — C0 (901 nodos)", p1=False)
    dice(story, st, "Persona 2",
        "La comunidad más grande es C0, con 901 nodos y 2.150 aristas. "
        "Su densidad es baja, 0,005, lo que tiene sentido porque es muy grande. "
        "Pero su clustering promedio es 0,51, que es sorprendentemente alto para su tamaño. "
        "Eso significa que cuando dos autores comparten un coautor, "
        "hay un 51% de probabilidad de que ellos también hayan publicado juntos. "
        "Se forman muchos triángulos de colaboración dentro de C0. "
        "Una cosa interesante: los tres autores que lideran cada métrica dentro de C0 son distintos. "
        "No hay un solo jefe — hay liderazgos especializados. "
        "Y respondiendo si es central: sí, definitivamente. "
        "El nodo 13801, que vive en C0, tiene el mayor Betweenness y Closeness de toda la red. "
        "C0 actúa como el núcleo que conecta todo.",
        p1=False)
    apunte(story, st,
        "Señala la tabla izquierda fila por fila. "
        "El punto de los 3 liderazgos distintos es lo más interesante — "
        "el profe puede preguntar sobre eso.")

    # ── SLIDE 11 ──────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 11", "Comunidad más Compacta — C17 (47 nodos)", p1=False)
    dice(story, st, "Persona 2",
        "La comunidad más compacta entre las relevantes con más de 20 autores es C17, "
        "con solo 47 nodos pero una densidad de 0,684 y un clustering de 0,860. "
        "Para entender qué tan alto es eso: el 68% de todas las colaboraciones posibles "
        "entre sus 47 miembros existen de verdad. Casi todos publican con casi todos. "
        "Eso nos dice que probablemente es un equipo de investigación de la misma institución "
        "o trabajando en un problema muy específico que requiere colaboración muy estrecha. "
        "En cuanto al liderazgo: el nodo 6512 lidera en grado e Eigenvector, "
        "pero los nodos 16654 y 17807 tienen valores casi idénticos. "
        "Entonces hay un liderazgo compartido entre tres autores, no una jerarquía clara. "
        "Eso hace a la comunidad más resiliente. "
        "El riesgo de una comunidad tan densa es que sea muy cerrada hacia afuera, "
        "lo que puede limitar las ideas nuevas que entran.",
        p1=False)
    apunte(story, st,
        "Señala la comparativa de densidad. El contraste C17 0,684 vs C0 0,005 "
        "es impactante — úsalo.")

    # ── SLIDE 12 ──────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 12", "Síntesis y Conclusiones", p1=False)
    dice(story, st, "Persona 2",
        "Para cerrar, los cinco hallazgos principales. "
        "Primero, la red es libre de escala: unos pocos autores tienen muchísimas colaboraciones "
        "y la mayoría tiene muy pocas. El nodo 21012 tiene 81 cuando el promedio es 5,53. "
        "Segundo, la influencia es multidimensional: ser colaborativo, ser influyente, "
        "ser puente y estar cerca son cosas distintas y ningún autor domina todas. "
        "Tercero, el nodo 13801 es el más crítico para la cohesión de la red: "
        "si lo sacamos, la red se fragmenta más que con cualquier otro. "
        "Cuarto, hay 63 comunidades bien definidas con una modularidad de 0,80, "
        "que reflejan subcampos de investigación reales. "
        "Y quinto, C0 es el núcleo disperso que conecta todo, "
        "y C17 es el extremo opuesto: un equipo pequeño y muy compacto.",
        p1=False)
    apunte(story, st,
        "Lee las 5 conclusiones con pausa entre cada una. "
        "No te apures — esto es el cierre, se puede tomar el tiempo.")

    # ── SLIDE 13 ──────────────────────────────────────────────────────────────
    slide_box(story, st, "SLIDE 13", "Referencias y Cierre", p1=False)
    dice(story, st, "Persona 2",
        "Eso sería todo de nuestra parte. "
        "Las referencias principales incluyen el trabajo de Blondel del 2008 "
        "que describe el algoritmo de Louvain que usamos para detectar comunidades, "
        "y el repositorio SNAP de Stanford donde descargamos la red. "
        "Quedamos a disposición para cualquier pregunta, profesor.",
        p1=False)
    apunte(story, st,
        "Di esto con calma y mira al profe al terminar. "
        "No tengas miedo si llegan preguntas — ya las practicaron.")

    sp(story, 0.3)

    # ═══════════════════════════════════════════════════════════════════════════
    # RESPUESTAS RÁPIDAS PARA PREGUNTAS EN VIVO
    # ═══════════════════════════════════════════════════════════════════════════
    story.append(PageBreak())
    story.append(Paragraph("Respuestas cortas para las preguntas más probables", st["h1"]))
    hr(story)
    caja(story, st,
        "⚡  <b>Si el profe pregunta algo, cualquiera de los dos puede responder. "
        "Estas son las respuestas más importantes memorizadas en una frase.</b>",
        bg=ROJO_CL, borde=ROJO)
    sp(story, 0.2)

    qa = [
        ("¿Por qué solo el componente principal?",
         "Porque las métricas de caminos no funcionan entre grupos desconectados. "
         "Un nodo aislado con un solo vecino aparece como 'el más cercano' y eso es falso."),
        ("¿Qué es una red libre de escala?",
         "Una red donde pocos nodos tienen muchísimas conexiones y la mayoría tiene muy pocas. "
         "Como Instagram: unos pocos influencers con millones de seguidores y el resto con decenas."),
        ("¿Qué significa Q = 0,80?",
         "La modularidad va de 0 a 1. Un valor cercano a 1 indica que las comunidades detectadas "
         "son reales y bien separadas — hay muchas conexiones dentro de cada grupo y pocas entre grupos."),
        ("¿Por qué 13801 es más importante que 21012?",
         "El 21012 tiene más coautores pero están concentrados en su comunidad. "
         "El 13801 conecta comunidades distintas — si lo sacas, la red se rompe. "
         "Es más estratégico aunque tenga menos colaboraciones."),
        ("¿Qué diferencia hay entre Betweenness y Closeness?",
         "Betweenness: ¿cuántos caminos entre otros pasan por ti? (eres un puente). "
         "Closeness: ¿qué tan corta es tu distancia al resto? (estás en el centro). "
         "Pueden coincidir en el mismo nodo o no."),
        ("¿Por qué C17 tiene mayor densidad que C0 si C0 es más grande?",
         "La densidad no depende del tamaño, sino de la proporción de conexiones posibles que existen. "
         "C0 tiene 901 nodos → más de 400 mil pares posibles, solo 2.150 existen. "
         "C17 tiene 47 nodos → 1.081 pares posibles, 739 existen. Son mundos distintos."),
        ("¿Qué representa cada comunidad en la realidad?",
         "Probablemente cada comunidad es una línea de investigación específica: "
         "agujeros negros, ondas gravitacionales, cosmología inflacionaria, gravedad cuántica de lazos, etc. "
         "No podemos saberlo con certeza porque los IDs son anónimos."),
        ("¿Qué es el clustering?",
         "Si A y B tienen un coautor en común, el clustering mide la probabilidad de que A y B "
         "también hayan publicado juntos. En C17 es 0,86: un 86% de probabilidad."),
    ]

    for q, a in qa:
        data_qa = [
            [Paragraph(f"❓ {q}", ParagraphStyle("qq",fontName="Helvetica-Bold",
                fontSize=10.5,textColor=ROJO,leading=14))],
            [Paragraph(a, st["body"])],
        ]
        t = Table(data_qa, colWidths=[avail])
        t.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(0,0), ROJO_CL),
            ("BACKGROUND",(0,1),(0,1), GRIS_CL),
            ("BOX",(0,0),(-1,-1),0.7, ROJO),
            ("LINEBELOW",(0,0),(0,0),0.4, ROJO),
            ("LEFTPADDING",(0,0),(-1,-1),10),
            ("TOPPADDING",(0,0),(-1,-1),5),
            ("BOTTOMPADDING",(0,0),(-1,-1),5),
        ]))
        story.append(t)
        sp(story, 0.18)

    sp(story, 0.3)
    caja(story, st,
        "✅  <b>Tip final:</b> si no saben la respuesta a algo, no inventen. "
        "Digan: 'Esa parte no la analizamos en detalle, pero lo que sí podemos decir es...' "
        "y conéctenlo con algo que sí saben. El profe valora la honestidad.",
        bg=VERDE_CL, borde=VERDE)

def main():
    out = "/home/user/TALLER-/Guiones_Presentacion_Taller3.pdf"
    doc = SimpleDocTemplate(out, pagesize=A4,
        leftMargin=MARGIN, rightMargin=MARGIN,
        topMargin=MARGIN, bottomMargin=1.8*cm)
    st = S()
    story = []
    build(story, st)
    doc.build(story, onFirstPage=footer_cb, onLaterPages=footer_cb)
    print(f"Generado: {out}")

if __name__ == "__main__":
    main()
