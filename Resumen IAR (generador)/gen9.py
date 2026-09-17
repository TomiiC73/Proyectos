# -*- coding: utf-8 -*-
"""Diagrama e32: linea de tiempo de la historia de la IA (Unidad 1)."""
import os
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
from dlib import Diagram

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


# Los dos "inviernos" se marcan como bandas frias; los periodos de auge, no.
HITOS = [
    ("1943 \u2013 1955", "G\u00e9nesis",
     "McCulloch y Pitts modelan la neurona artificial; Hebb da la regla de "
     "aprendizaje; Turing publica el test.", "unit"),
    ("1956", "Taller de Dartmouth",
     "McCarthy acu\u00f1a el nombre \u00abinteligencia artificial\u00bb. Newell y Simon "
     "presentan el Te\u00f3rico L\u00f3gico.", "root"),
    ("1952 \u2013 1969", "Entusiasmo y grandes esperanzas",
     "\u00c9xitos en problemas de juguete. Simon predice en 1957 un campe\u00f3n de "
     "ajedrez en diez a\u00f1os; tard\u00f3 cuarenta.", "unit"),
    ("1966 \u2013 1973", "Dosis de realidad \u2014 primer invierno",
     "Los programas no ten\u00edan conocimiento del dominio. Minsky y Papert (1969) "
     "prueban que el perceptr\u00f3n simple s\u00f3lo separa clases linealmente "
     "separables; el informe Lighthill corta el fondeo.", "bad"),
    ("1969 \u2013 1979", "Sistemas basados en conocimiento",
     "El conocimiento del dominio, no el m\u00e9todo general, es lo que resuelve: "
     "DENDRAL y MYCIN.", "unit"),
    ("1980 \u2013 1988", "La IA se vuelve industria \u2014 segundo invierno",
     "R1 le ahorra 40 M US$ al a\u00f1o a DEC; el sector pasa de millones a miles de "
     "millones y colapsa al no cumplir lo prometido.", "bad"),
    ("1986 \u2013 presente", "Regreso de las redes neuronales",
     "Cuatro grupos reinventan la retropropagaci\u00f3n; el conexionismo vuelve.", "good"),
    ("2001 \u2013 presente", "Big data",
     "Los datos masivos pesan m\u00e1s que el ajuste fino del algoritmo "
     "(Banko y Brill).", "good"),
    ("2011 \u2013 presente", "Aprendizaje profundo",
     "ImageNet 2012 y el hardware paralelo (GPU/TPU).", "good"),
]

FILL = {"root": ("#4C2A85", "#3A1F66", "#FFFFFF"),
        "unit": ("#EDE4FB", "#7C4DCB", "#2C1758"),
        "bad":  ("#FBE6E6", "#B24A4A", "#4A1414"),
        "good": ("#E3F5E8", "#3E8E5A", "#12321F")}


def e32_historia():
    """Dos pasadas: primero se mide cada tarjeta, despues se apilan con una
    separacion constante. Con paso fijo las tarjetas de distinta altura dejan
    huecos desparejos."""
    GAP, TOP, BOT = 0.17, 0.50, 0.10
    xa = 1.32                       # eje vertical de la linea de tiempo
    x0 = xa + 0.22
    w = 6.30 - x0 - 0.10
    FS_T, FS_B = 8.6, 7.5
    LH = FS_B * 1.30 / 72.0

    probe = Diagram(6.30, 1.0)      # solo para medir el ajuste de linea
    cuerpos = [probe._wrap(t[2], FS_B, w - 0.24) for t in HITOS]
    probe.fig.clf()
    PAD, TH, SEP = 0.115, 0.135, 0.035   # relleno, alto del titulo, aire titulo-cuerpo
    alturas = [2 * PAD + TH + SEP + len(c) * LH for c in cuerpos]

    H = TOP + sum(alturas) + GAP * (len(HITOS) - 1) + BOT
    d = Diagram(6.30, H)
    ax = d.ax
    d.title("Los períodos de la historia de la IA", y=H - 0.26)

    y = H - TOP
    centros = []
    for hh in alturas:
        centros.append(y - hh / 2)
        y -= hh + GAP

    ax.plot([xa, xa], [centros[-1], centros[0]], color="#B3B9C9", lw=1.6, zorder=1)

    for (anio, tit, _t, kind), cuerpo, hh, yc in zip(HITOS, cuerpos, alturas, centros):
        fc, ec, tc = FILL[kind]
        ax.add_patch(Circle((xa, yc), 0.085, facecolor=fc, edgecolor=ec,
                            lw=1.4, zorder=4))
        ax.text(xa - 0.20, yc, anio, fontsize=8.4, ha="right", va="center",
                fontweight="bold", color="#3A4152", fontfamily="DejaVu Sans")
        ax.add_patch(FancyBboxPatch(
            (x0, yc - hh / 2), w, hh,
            boxstyle="round,pad=0,rounding_size=0.05",
            fc=fc, ec=ec, lw=1.1, zorder=2))
        yt = yc + hh / 2 - PAD - TH / 2
        ax.text(x0 + 0.12, yt, tit, fontsize=FS_T, ha="left", va="center",
                fontweight="bold", color=tc, fontfamily="DejaVu Sans")
        ax.text(x0 + 0.12, yc - hh / 2 + PAD + len(cuerpo) * LH / 2,
                chr(10).join(cuerpo), fontsize=FS_B, ha="left", va="center",
                color=tc, linespacing=1.30, fontfamily="DejaVu Sans")

    d.save(os.path.join(IMG, "e32_historia.png"))
    print("   e32_historia.png", round(H, 2), "in")


if __name__ == "__main__":
    e32_historia()
