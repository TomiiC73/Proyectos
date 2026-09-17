# -*- coding: utf-8 -*-
"""Motor de armado del .docx: estilos, marcadores, hipervinculos internos,
cajas destacadas e imagenes insertadas a escala 1:1."""
import re
import docx
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

MORADO = RGBColor(0x4C, 0x2A, 0x85)
MORADO_OSC = RGBColor(0x2C, 0x17, 0x58)
GRIS = RGBColor(0x5A, 0x60, 0x76)
NEGRO = RGBColor(0x1E, 0x22, 0x33)
LINK = RGBColor(0x6D, 0x3F, 0xC4)

FUENTE = "Calibri"
_bm_id = [1000]


# --------------------------------------------------------------- utilidades
def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn(k), v)
    return e


def shade(par, fill):
    par._p.get_or_add_pPr().append(_el("w:shd", **{"w:val": "clear",
                                                   "w:color": "auto",
                                                   "w:fill": fill}))


def border(par, color="7C4DCB", sz="6", sides=("left",), space="8"):
    pPr = par._p.get_or_add_pPr()
    bdr = pPr.find(qn("w:pBdr"))
    if bdr is None:
        bdr = OxmlElement("w:pBdr")
        pPr.append(bdr)
    for s in sides:
        bdr.append(_el(f"w:{s}", **{"w:val": "single", "w:sz": sz,
                                    "w:space": space, "w:color": color}))


def bookmark(par, name):
    _bm_id[0] += 1
    i = str(_bm_id[0])
    par._p.insert(0, _el("w:bookmarkStart", **{"w:id": i, "w:name": name}))
    par._p.append(_el("w:bookmarkEnd", **{"w:id": i}))


def _fmt(run, bold=False, italic=False, size=None, color=None, name=None):
    run.bold = bold
    run.italic = italic
    if size:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    run.font.name = name or FUENTE
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name or FUENTE)
    return run


TOKEN = re.compile(r"(\*\*.+?\*\*|__.+?__|`[^`\n]+`|\[\[[^\]|]+\|[^\]]+\]\])")
CODE_INLINE = RGBColor(0x5B, 0x3A, 0x8E)
# *cursiva* con un solo asterisco, sin pisar **negrita** ni notaciones como A* o C*
ITAL1 = re.compile(r"(?<![\w*])\*(?!\s)([^*\n]{1,250}?)(?<!\s)\*(?![\w*])")


def add_rich(par, text, size=10.5, color=NEGRO, bold=False, italic=False):
    """Soporta **negrita**, __cursiva__, *cursiva*, `monoespaciado` y
    [[marcador|texto del enlace]], incluyendo marcas anidadas."""
    text = ITAL1.sub(r"__\1__", text)
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**") and len(part) > 4:
            add_rich(par, part[2:-2], size, color, True, italic)
        elif part.startswith("__") and part.endswith("__") and len(part) > 4:
            add_rich(par, part[2:-2], size, color, bold, True)
        elif part.startswith("`") and part.endswith("`") and len(part) > 2:
            # nombres de funciones/variables: se distinguen por la fuente
            _fmt(par.add_run(part[1:-1]), bold=bold, italic=italic,
                 size=size * 0.93, color=CODE_INLINE, name="Consolas")
        elif part.startswith("[[") and part.endswith("]]"):
            anchor, label = part[2:-2].split("|", 1)
            h = _el("w:hyperlink", **{"w:anchor": anchor})
            par._p.append(h)
            r = par.add_run(label)
            h.append(r._element)
            _fmt(r, bold=bold, italic=italic, size=size, color=LINK)
            r.font.underline = True
        else:
            _fmt(par.add_run(part), bold=bold, italic=italic, size=size,
                 color=color)
    return par


# --------------------------------------------------------------- documento
def new_doc():
    doc = Document()
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21.0), Cm(29.7)
    s.left_margin = s.right_margin = Cm(2.2)
    s.top_margin = Cm(2.0)
    s.bottom_margin = Cm(2.0)

    n = doc.styles["Normal"]
    n.font.name = FUENTE
    n.font.size = Pt(10.5)
    n.font.color.rgb = NEGRO
    n.element.rPr.rFonts.set(qn("w:eastAsia"), FUENTE)
    n.paragraph_format.space_after = Pt(6)
    n.paragraph_format.line_spacing = 1.12

    for name, size, color, before, after in [
            ("Heading 1", 17, MORADO, 0, 10),
            ("Heading 2", 13, MORADO, 14, 5),
            ("Heading 3", 11.5, MORADO_OSC, 10, 3)]:
        st = doc.styles[name]
        st.font.name = FUENTE
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = color
        st.element.rPr.rFonts.set(qn("w:eastAsia"), FUENTE)
        st.paragraph_format.space_before = Pt(before)
        st.paragraph_format.space_after = Pt(after)
        st.paragraph_format.keep_with_next = True
    for name in ("List Bullet", "List Bullet 2", "List Bullet 3"):
        st = doc.styles[name]
        st.font.name = FUENTE
        st.font.size = Pt(10.5)
        st.font.color.rgb = NEGRO
        st.paragraph_format.space_after = Pt(3)
        st.paragraph_format.line_spacing = 1.10
    return doc


def add_toc(doc, levels="1-3"):
    p = doc.add_paragraph()
    r = p.add_run()
    fld = _el("w:fldChar", **{"w:fldCharType": "begin"})
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = f' TOC \\o "{levels}" \\h \\z \\u '
    sep = _el("w:fldChar", **{"w:fldCharType": "separate"})
    txt = OxmlElement("w:t")
    txt.text = "Actualizá el índice con clic derecho › Actualizar campos › Toda la tabla."
    end = _el("w:fldChar", **{"w:fldCharType": "end"})
    for e in (fld, instr, sep, txt, end):
        r._r.append(e)


def h(doc, level, text, bm=None):
    p = doc.add_heading(text, level=level)
    if bm:
        bookmark(p, bm)
    return p


def para(doc, text, size=10.5, align=None, space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    if align:
        p.alignment = align
    add_rich(p, text, size=size)
    return p


def bullets(doc, items, level=1):
    style = {1: "List Bullet", 2: "List Bullet 2", 3: "List Bullet 3"}[level]
    for it in items:
        p = doc.add_paragraph(style=style)
        p.paragraph_format.space_after = Pt(2.5)
        add_rich(p, it, size=10.5)


def box(doc, title, text, fill="F3EEFC", color="7C4DCB"):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.left_indent = Cm(0.25)
    p.paragraph_format.keep_with_next = True   # que el titulo no quede huerfano
    shade(p, fill)
    border(p, color=color, sz="18", sides=("left",))
    _fmt(p.add_run(title), bold=True, size=9.5, color=MORADO_OSC)
    q = doc.add_paragraph()
    q.paragraph_format.space_before = Pt(0)
    q.paragraph_format.space_after = Pt(10)
    q.paragraph_format.left_indent = Cm(0.25)
    shade(q, fill)
    border(q, color=color, sz="18", sides=("left",))
    add_rich(q, text, size=9.5, color=GRIS)
    return q


def figure(doc, path, n, caption, width_in=6.30):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(path, width=Inches(width_in))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_after = Pt(12)
    _fmt(c.add_run(f"Figura {n} — {caption}"), italic=True, size=8.5, color=GRIS)


def page_break(doc):
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def rule(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(8)
    border(p, color="D6CCEC", sz="6", sides=("bottom",), space="1")


def footer_pagenum(doc):
    ftr = doc.sections[0].footer.paragraphs[0]
    ftr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = ftr.add_run()
    _fmt(r, size=8.5, color=GRIS)
    for t, kind in ((None, "begin"), ("PAGE", "instr"), (None, "separate"),
                    ("1", "text"), (None, "end")):
        if kind == "instr":
            e = OxmlElement("w:instrText")
            e.set(qn("xml:space"), "preserve")
            e.text = " PAGE "
        elif kind == "text":
            e = OxmlElement("w:t")
            e.text = t
        else:
            e = _el("w:fldChar", **{"w:fldCharType": kind})
        r._r.append(e)


def code(doc, texto, lang="python", size=8.2, fill="F4F5F8", bar="7C4DCB"):
    """Bloque de codigo fuente. Una linea = un parrafo, para que Word no
    rejustifique ni pierda la indentacion (en Python la sangria es sintaxis)."""
    lineas = texto.rstrip("\n").split("\n")
    for i, ln in enumerate(lineas):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(5 if i == 0 else 0)
        pf.space_after = Pt(5 if i == len(lineas) - 1 else 0)
        pf.left_indent = Pt(9)
        pf.right_indent = Pt(2)
        pf.line_spacing = 1.0
        pf.keep_with_next = i < len(lineas) - 1
        shade(p, fill)
        border(p, color=bar, sz="18", sides=("left",), space="6")
        r = p.add_run(ln if ln else " ")
        _fmt(r, size=size, color=RGBColor(0x24, 0x29, 0x38), name="Consolas")
        r._r.find(qn("w:t")).set(qn("xml:space"), "preserve")
    return None


def salida(doc, texto, size=8.2, fill="EFF3EC", bar="3E8E5A", etiqueta="Salida"):
    """Salida real de la ejecucion. Verde para distinguirla del codigo."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.left_indent = Pt(9)
    _fmt(p.add_run(etiqueta.upper()), size=7.2, bold=True,
         color=RGBColor(0x3E, 0x8E, 0x5A))
    lineas = texto.rstrip("\n").split("\n")
    for i, ln in enumerate(lineas):
        p = doc.add_paragraph()
        pf = p.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(6 if i == len(lineas) - 1 else 0)
        pf.left_indent = Pt(9)
        pf.right_indent = Pt(2)
        pf.line_spacing = 1.0
        pf.keep_with_next = i < len(lineas) - 1
        shade(p, fill)
        border(p, color=bar, sz="18", sides=("left",), space="6")
        r = p.add_run(ln if ln else " ")
        _fmt(r, size=size, color=RGBColor(0x1B, 0x3A, 0x26), name="Consolas")
        r._r.find(qn("w:t")).set(qn("xml:space"), "preserve")
    return None
