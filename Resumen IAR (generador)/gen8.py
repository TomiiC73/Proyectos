# -*- coding: utf-8 -*-
"""Diagramas nuevos: arquitectura del perceptron y temas apoyados en Colabs."""
import os
import numpy as np
from dlib import Diagram, PALETTE

IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
os.makedirs(IMG, exist_ok=True)


def out(d, n):
    d.save(os.path.join(IMG, n))
    print("  ", n)


# ============================================ e29 ARQUITECTURA DEL PERCEPTRON
def e29_arquitectura():
    d = Diagram(6.30, 4.02)
    # recorta el aire de abajo sin romper la escala 1:1
    # (4.02 unidades de dato sobre 4.02 pulgadas de figura)
    d.ax.set_ylim(0.28, 4.30)
    d.title("Arquitectura del perceptrón simple", y=4.16)

    ax = d.ax
    ycen = 2.40
    # --- entradas ---
    ent = [("x\u2080 = 1", 3.62), ("x\u2081", 3.02), ("x\u2082", 2.42), ("x\u2099", 1.62)]
    for lab, y in ent:
        d.node("in_" + lab, 0.62, y, lab, w=0.78, kind="topic", fs=9.5, minh=0.36)
    ax.text(0.62, 1.84, "\u22ee", fontsize=13, ha="center", va="center",
            color="#5A6076")

    # --- sumador ---
    from matplotlib.patches import Circle
    sx, sy = 3.05, ycen
    ax.add_patch(Circle((sx, sy), 0.40, facecolor="#EDE4FB",
                        edgecolor="#7C4DCB", lw=1.4, zorder=3))
    ax.text(sx, sy, "\u03a3", fontsize=19, ha="center", va="center",
            color="#2C1758", zorder=4)

    # --- flechas entrada -> sumador, con los pesos sobre la linea ---
    pesos = ["w\u2080 = \u2212\u03b8", "w\u2081", "w\u2082", "w\u2099"]
    for (lab, y), wl in zip(ent, pesos):
        ax.annotate("", xy=(sx - 0.42, sy + (y - ycen) * 0.30),
                    xytext=(1.03, y),
                    arrowprops=dict(arrowstyle="-|>", color="#5A6076", lw=1.1,
                                    shrinkA=0, shrinkB=0))
        mx = 1.03 + (sx - 0.42 - 1.03) * 0.46
        my = y + ((sy + (y - ycen) * 0.30) - y) * 0.46
        ax.text(mx, my + 0.13, wl, fontsize=8.6, ha="center", va="center",
                color="#4A3608",
                bbox=dict(boxstyle="round,pad=0.16", fc="#FFF3D6",
                          ec="#C9962A", lw=0.8))

    # --- funcion de activacion ---
    fx0, fy0, fw, fh = 3.90, ycen - 0.52, 1.05, 1.04
    ax.add_patch(__import__("matplotlib").patches.FancyBboxPatch(
        (fx0, fy0), fw, fh, boxstyle="round,pad=0.02,rounding_size=0.05",
        fc="#FFFFFF", ec="#8A8FA8", lw=1.1, zorder=3))
    # dibujo del escalon dentro de la caja
    px0, py0 = fx0 + 0.16, fy0 + 0.20
    pw, ph = fw - 0.32, fh - 0.44
    ax.plot([px0, px0 + pw / 2, px0 + pw / 2, px0 + pw],
            [py0, py0, py0 + ph, py0 + ph],
            color="#4C2A85", lw=1.8, zorder=4, solid_joinstyle="miter")
    ax.plot([px0 + pw / 2, px0 + pw / 2], [py0, py0 + ph], color="#4C2A85",
            lw=1.8, zorder=4)
    ax.text(fx0 + fw / 2, fy0 + fh - 0.11, "escalón", fontsize=7.8,
            ha="center", va="center", color="#2C1758", zorder=5)
    ax.text(px0 - 0.04, py0 + ph, "1", fontsize=7.0, ha="right", va="center",
            color="#5A6076", zorder=5)
    ax.text(px0 - 0.04, py0, "0", fontsize=7.0, ha="right", va="center",
            color="#5A6076", zorder=5)

    ax.annotate("", xy=(fx0 - 0.02, ycen), xytext=(sx + 0.42, ycen),
                arrowprops=dict(arrowstyle="-|>", color="#5A6076", lw=1.2,
                                shrinkA=0, shrinkB=0))
    ax.text((sx + 0.42 + fx0) / 2, ycen + 0.15, "Net", fontsize=8.4,
            ha="center", va="center", color="#2C1758")

    # --- salida ---
    d.node("out", 5.62, ycen, "y\u2032", w=0.70, kind="accent", fs=11, minh=0.40)
    ax.annotate("", xy=(5.62 - 0.36, ycen), xytext=(fx0 + fw + 0.02, ycen),
                arrowprops=dict(arrowstyle="-|>", color="#5A6076", lw=1.2,
                                shrinkA=0, shrinkB=0))

    # --- etiquetas de las cuatro partes ---
    for x, txt in [(0.62, "1. Entradas"), (3.05, "3. Sumador"),
                   (4.42, "4. Activación"), (5.62, "Salida")]:
        ax.text(x, 3.88, txt, fontsize=8.2, ha="center", va="center",
                color="#7C4DCB", fontweight="bold")
    ax.text(1.95, 3.88, "2. Pesos", fontsize=8.2, ha="center", va="center",
            color="#7C4DCB", fontweight="bold")

    d.caption(3.15, 1.05, "Net = \u03a3 w\u1d62x\u1d62        "
              "y\u2032 = f(Net) = 1 si Net \u2265 0, si no 0", fs=9.2,
              color="#1E2233")
    d.caption(3.15, 0.62,
              "El sesgo se implementa como un peso más (w\u2080) sobre una entrada "
              "fija en 1:\nasí el umbral \u03b8 se aprende igual que los otros pesos.",
              fs=7.9)
    out(d, "e29_perceptron_arq.png")


if __name__ == "__main__":
    e29_arquitectura()


# ================================================ e30 TABLA DE VERDAD (LOGICA)
def e30_tabla_verdad():
    d = Diagram(6.30, 3.60)
    d.title("Tablas de verdad de las cinco conectivas", y=3.38)
    ax = d.ax

    cols = ["P", "Q", "\u00acP", "P\u2227Q", "P\u2228Q",
            "P\u21d2Q", "P\u21d4Q"]
    F, V = "F", "V"
    filas = [
        [F, F, V, F, F, V, V],
        [F, V, V, F, V, V, F],
        [V, F, F, F, V, F, F],
        [V, V, F, V, V, V, V],
    ]
    x0, y0 = 0.72, 1.28
    cw, ch = 0.69, 0.38
    # cabecera
    for c, name in enumerate(cols):
        cx = x0 + c * cw + cw / 2
        fc = "#EDE4FB" if c < 2 else "#4C2A85"
        tc = "#2C1758" if c < 2 else "#FFFFFF"
        ax.add_patch(__import__("matplotlib").patches.FancyBboxPatch(
            (x0 + c * cw, y0 + 4 * ch), cw, ch,
            boxstyle="round,pad=0,rounding_size=0.02",
            fc=fc, ec="#7C4DCB", lw=1.0, zorder=3))
        ax.text(cx, y0 + 4 * ch + ch / 2, name, fontsize=9.4, ha="center",
                va="center", color=tc, fontweight="bold", zorder=4)
    # celdas
    for r, fila in enumerate(filas):
        yy = y0 + (3 - r) * ch
        for c, v in enumerate(fila):
            resalta = (r == 0 or r == 1) and c == 5
            fc = "#FFF3D6" if resalta else ("#F7F8FB" if c < 2 else "#FFFFFF")
            ax.add_patch(__import__("matplotlib").patches.Rectangle(
                (x0 + c * cw, yy), cw, ch, fc=fc,
                ec="#C9962A" if resalta else "#B3B9C9",
                lw=1.3 if resalta else 0.8, zorder=3))
            ax.text(x0 + c * cw + cw / 2, yy + ch / 2, v, fontsize=9.2,
                    ha="center", va="center", zorder=4,
                    color="#8A5A00" if resalta else "#1E2233",
                    fontweight="bold" if resalta else "normal")

    d.caption(3.15, 1.00,
              "V = verdadero, F = falso.  Las dos filas marcadas son las que "
              "suelen sorprender:", fs=8.0, color="#1E2233")
    ax.add_patch(__import__("matplotlib").patches.FancyBboxPatch(
        (0.72, 0.26), 4.83, 0.58,
        boxstyle="round,pad=0,rounding_size=0.04",
        fc="#FFF3D6", ec="#C9962A", lw=1.1, zorder=3))
    ax.text(3.13, 0.55,
            "P \u21d2 Q es VERDADERA siempre que P sea falsa.\n"
            "«Si 5 es par, entonces Napoleón vive» es una sentencia verdadera.",
            fontsize=8.0, ha="center", va="center", color="#4A3608", zorder=4,
            linespacing=1.45)
    out(d, "e30_tabla_verdad.png")


# ======================================= e31 LAS TRES ETAPAS DE UN PROYECTO ML
def e31_etapas_ml():
    d = Diagram(6.30, 4.05)
    d.ax.set_ylim(0.20, 4.25)
    d.title("Las tres etapas de un proyecto de aprendizaje supervisado", y=4.08)
    ax = d.ax
    import matplotlib.patches as mp

    etapas = [
        ("Etapa 1\nPreparación\nde los datos", [
            ("Reconocimiento de patrones",
             "traducir el fenómeno real a un dominio\nmodelable computacionalmente"),
            ("Sensado / adquisición",
             "recolección rigurosa e imparcial del\nconjunto de datos histórico"),
            ("Extracción de características",
             "reducción de dimensionalidad y preproceso\nde las variables predictoras (X)"),
        ]),
        ("Etapa 2\nModelado y\noptimización", [
            ("Selección del algoritmo",
             "elegir el modelo adecuado a la topología\nde los datos (regresión, RNA, SVM)"),
            ("Entrenamiento",
             "ajuste iterativo de los parámetros internos\nsólo sobre el conjunto de entrenamiento"),
            ("Ajuste de hiperparámetros",
             "calibración por validación cruzada"),
        ]),
        ("Etapa 3\nEvaluación\ndel modelo", [
            ("Propósito",
             "cuantificar la generalización del estimador\nfrente a observaciones nuevas"),
            ("Aplicación de métricas",
             "tasas de error, sensibilidad, especificidad\ny exactitud global"),
            ("Diagnóstico gráfico",
             "matriz de confusión y espacio ROC"),
        ]),
    ]

    y = 3.42
    for i, (nombre, filas) in enumerate(etapas):
        alto = 0.98
        # flecha-etiqueta de la etapa
        ax.add_patch(mp.Polygon(
            [[0.30, y + alto / 2], [1.38, y + alto / 2], [1.62, y],
             [1.38, y - alto / 2], [0.30, y - alto / 2]],
            closed=True, fc="#4C2A85", ec="#3A1F66", lw=1.1, zorder=4))
        ax.text(0.93, y, nombre, fontsize=8.2, ha="center", va="center",
                color="#FFFFFF", fontweight="bold", zorder=5, linespacing=1.35)
        # sub-cajas
        sy = y + alto / 2 - 0.165
        for tit, det in filas:
            ax.add_patch(mp.FancyBboxPatch(
                (1.76, sy - 0.155), 4.28, 0.31,
                boxstyle="round,pad=0,rounding_size=0.03",
                fc="#F7F8FB" if i % 2 == 0 else "#FFFFFF",
                ec="#B3B9C9", lw=0.85, zorder=3))
            ax.text(1.86, sy + 0.075, tit, fontsize=7.5, ha="left",
                    va="center", color="#2C1758", fontweight="bold", zorder=4)
            ax.text(1.86, sy - 0.068, " ".join(det.split()), fontsize=6.5,
                    ha="left", va="center", color="#4A5163", zorder=4)
            sy -= 0.335
        y -= 1.16

    d.caption(3.15, 0.38,
              "Fuente: presentación «Aprendizaje Automático» de la cátedra "
              "(Casatti y Guzmán).", fs=7.0)
    out(d, "e31_etapas_ml.png")
