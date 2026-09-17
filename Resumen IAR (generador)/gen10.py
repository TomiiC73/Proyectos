# -*- coding: utf-8 -*-
"""Diagramas de la Unidad 6 (PLN clasico de la catedra) y de la Unidad 2."""
import os
from matplotlib.patches import FancyBboxPatch, Circle, Polygon
from dlib import Diagram

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")

MOR, MORO = "#7C4DCB", "#2C1758"
AMB_F, AMB_E, AMB_T = "#FFF3D6", "#C9962A", "#4A3608"
GRIS = "#5A6076"


# ================================================= e33  ETAPAS DE LA COMUNICACION
def e33_comunicacion():
    """Las nueve etapas de la catedra: tres del lado del emisor y seis del
    receptor, sobre el ejemplo 'El auto esta roto'."""
    EMI = ["Intención", "Generación", "Síntesis"]
    REC = ["Percepción", "Análisis sintáctico",
           "Interpretación semántica", "Interpretación pragmática",
           "Desambiguación", "Incorporación"]
    hb, gap = 0.345, 0.085
    TOP, AG = 0.72, 0.62
    # se despeja H para que el borde inferior de la caja verde caiga en 0.12
    H = 0.37 + 0.22 + len(REC) * (hb + gap) + 0.30 + AG + TOP
    d = Diagram(6.30, H)
    ax = d.ax
    d.title("Las nueve etapas de la comunicación", y=H - 0.26)

    xL, xR, w = 0.18, 3.36, 2.76
    yag = H - TOP - AG / 2
    d.node("a1", xL + w / 2, yag, "Agente 1  ·  emisor", w=w, kind="unit",
           fs=9.2, minh=AG)
    d.node("a2", xR + w / 2, yag, "Agente 2  ·  receptor", w=w, kind="unit",
           fs=9.2, minh=AG)
    ax.annotate("", xy=(xR - 0.04, yag), xytext=(xL + w + 0.04, yag),
                arrowprops=dict(arrowstyle="-|>", color=MOR, lw=1.7,
                                shrinkA=0, shrinkB=0))
    # el rotulo va ARRIBA de las cajas: el hueco entre ellas es muy angosto
    ax.text((xL + w + xR) / 2, yag + AG / 2 + 0.06,
            "«El auto está roto»", fontsize=8.0, ha="center",
            va="bottom", style="italic", color=MORO)

    ytop = yag - AG / 2 - 0.30
    n = 0
    for col_x, etapas in ((xL, EMI), (xR, REC)):
        for k, e in enumerate(etapas):
            n += 1
            yc = ytop - k * (hb + gap) - hb / 2
            ax.add_patch(FancyBboxPatch(
                (col_x, yc - hb / 2), w, hb,
                boxstyle="round,pad=0,rounding_size=0.05",
                fc=AMB_F, ec=AMB_E, lw=1.0, zorder=3))
            ax.text(col_x + w / 2, yc, f"{n}. {e}", fontsize=8.4, ha="center",
                    va="center", color=AMB_T, fontfamily="DejaVu Sans")
            if k:
                ax.annotate("", xy=(col_x + w / 2, yc + hb / 2 + 0.004),
                            xytext=(col_x + w / 2, yc + hb / 2 + gap - 0.004),
                            arrowprops=dict(arrowstyle="-|>", color=AMB_E,
                                            lw=1.0, shrinkA=0, shrinkB=0))

    # la base de conocimiento del emisor, de donde sale la intencion
    ax.text(xL + w / 2, ytop - 3 * (hb + gap) - 0.30,
            "parte de su base de conocimiento", fontsize=7.8, ha="center",
            va="center", color=GRIS, style="italic")

    # resultado, debajo de la columna del receptor
    yres = ytop - len(REC) * (hb + gap) - 0.22
    d.node("kb", xR + w / 2, yres, "Roto(c_auto) entra a la base de "
           "conocimiento del agente 2", w=w, kind="good", fs=8.2, minh=0.50)
    ax.annotate("", xy=(xR + w / 2, yres + 0.26),
                xytext=(xR + w / 2, yres + 0.26 + 0.20),
                arrowprops=dict(arrowstyle="-|>", color="#3E8E5A", lw=1.2,
                                shrinkA=0, shrinkB=0))

    d.save(os.path.join(IMG, "e33_comunicacion.png"))
    print("   e33_comunicacion.png", round(H, 2), "in")


# ================================================= e34  ARBOL GRAMATICAL
def e34_arbol():
    """Arbol de 'El auto esta roto' con la gramatica e0 de la catedra, y la
    composicion semantica de abajo hacia arriba en ambar."""
    d = Diagram(6.30, 3.86)
    ax = d.ax
    d.title("Árbol gramatical y composición semántica de "
            "«El auto está roto»", y=3.66)

    def nodo(x, y, cat, sem, w=1.34):
        ax.add_patch(FancyBboxPatch(
            (x - w / 2, y - 0.21), w, 0.42,
            boxstyle="round,pad=0,rounding_size=0.05",
            fc="#EDE4FB", ec=MOR, lw=1.2, zorder=3))
        ax.text(x, y, cat, fontsize=9.4, ha="center", va="center",
                fontweight="bold", color=MORO, fontfamily="DejaVu Sans")
        if sem:
            ax.text(x, y - 0.325, sem, fontsize=7.6, ha="center", va="center",
                    color=AMB_T, fontfamily="DejaVu Sans",
                    bbox=dict(boxstyle="round,pad=0.13", fc=AMB_F, ec=AMB_E,
                              lw=0.8))

    def arco(x1, y1, x2, y2):
        ax.plot([x1, x2], [y1 - 0.21 - 0.20, y2 + 0.21], color=GRIS, lw=1.1,
                zorder=1)

    yS, yF, yC, yH = 3.16, 2.34, 1.44, 0.62
    nodo(3.15, yS, "S", "Roto(c_auto)")
    nodo(1.575, yF, "FN", "c_auto")
    nodo(4.725, yF, "FV", "λs Roto(s)")
    arco(3.15, yS, 1.575, yF); arco(3.15, yS, 4.725, yF)

    nodo(0.85, yC, "Artículo", "λx x", w=1.26)
    nodo(2.30, yC, "Sustantivo", "c_auto", w=1.26)
    nodo(4.00, yC, "Verbo", "λP λs P(s)", w=1.26)
    nodo(5.45, yC, "Adjetivo", "λx Roto(x)", w=1.26)
    arco(1.575, yF, 0.85, yC); arco(1.575, yF, 2.30, yC)
    arco(4.725, yF, 4.00, yC); arco(4.725, yF, 5.45, yC)

    for x, pal in [(0.85, "el"), (2.30, "auto"), (4.00, "está"),
                   (5.45, "roto")]:
        ax.plot([x, x], [yC - 0.21 - 0.20, yH + 0.17], color=GRIS, lw=1.1,
                zorder=1)
        ax.add_patch(FancyBboxPatch(
            (x - 0.46, yH - 0.17), 0.92, 0.34,
            boxstyle="round,pad=0,rounding_size=0.05",
            fc="#FFFFFF", ec="#8A8FA8", lw=1.0, zorder=3))
        ax.text(x, yH, pal, fontsize=9.2, ha="center", va="center",
                style="italic", color="#1E2233", fontfamily="DejaVu Sans")

    d.caption(3.15, 0.16, "morado: categoría gramatical   ·   "
              "ámbar: su significado (.sem)   ·   hojas: las palabras",
              fs=7.6)
    d.save(os.path.join(IMG, "e34_arbol.png"))
    print("   e34_arbol.png")


if __name__ == "__main__":
    e33_comunicacion()
    e34_arbol()
