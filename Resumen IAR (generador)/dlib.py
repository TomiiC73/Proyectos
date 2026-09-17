# -*- coding: utf-8 -*-
"""Mini-libreria para dibujar mapas conceptuales legibles y a escala.

Todo el sistema de coordenadas esta en PULGADAS y coincide 1:1 con el tamano
final de la figura, de modo que un fontsize de 9 pt en el diagrama se imprime
como 9 pt reales en el Word (las imagenes se insertan al ancho exacto de la
figura). Asi no hay reescalado y el texto nunca queda microscopico.
"""
import textwrap
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# Paleta (clara, pensada para impresion en A4 blanco y negro/color)
PALETTE = {
    "root":   dict(fc="#4C2A85", ec="#3A1F66", tc="#FFFFFF", lw=1.4),
    "unit":   dict(fc="#EDE4FB", ec="#7C4DCB", tc="#2C1758", lw=1.3),
    "topic":  dict(fc="#FFFFFF", ec="#8A8FA8", tc="#1E2233", lw=1.0),
    "accent": dict(fc="#FFF3D6", ec="#C9962A", tc="#4A3608", lw=1.1),
    "good":   dict(fc="#E3F5E8", ec="#3E8E5A", tc="#12321F", lw=1.1),
    "bad":    dict(fc="#FBE6E6", ec="#B24A4A", tc="#4A1414", lw=1.1),
    "note":   dict(fc="#F2F4F8", ec="#B3B9C9", tc="#3A4152", lw=0.9),
}

FONT = "DejaVu Sans"


class Diagram:
    def __init__(self, w, h, dpi=300, bg="#FFFFFF"):
        self.w, self.h, self.dpi = w, h, dpi
        self.fig = plt.figure(figsize=(w, h), dpi=dpi)
        self.fig.patch.set_facecolor(bg)
        self.ax = self.fig.add_axes([0, 0, 1, 1])
        self.ax.set_xlim(0, w)
        self.ax.set_ylim(0, h)
        self.ax.axis("off")
        self.ax.set_facecolor(bg)
        self.fig.canvas.draw()
        self._rend = self.fig.canvas.get_renderer()
        self.nodes = {}

    # ---------- medicion real de texto ----------
    def _measure(self, s, fs, weight="normal"):
        t = self.ax.text(0, 0, s, fontsize=fs, fontfamily=FONT,
                         fontweight=weight, alpha=0)
        bb = t.get_window_extent(self._rend)
        t.remove()
        return bb.width / self.dpi, bb.height / self.dpi

    def _wrap(self, s, fs, maxw, weight="normal"):
        """Envuelve respetando saltos manuales '\n' y el ancho maximo real."""
        out = []
        for para in s.split("\n"):
            words, line = para.split(), ""
            for wd in words:
                cand = (line + " " + wd).strip()
                if self._measure(cand, fs, weight)[0] <= maxw or not line:
                    line = cand
                else:
                    out.append(line)
                    line = wd
            out.append(line)
        return out

    # ---------- nodos ----------
    def node(self, nid, x, y, text, w=1.7, kind="topic", fs=8.5,
             weight="normal", pad=0.09, minh=0.0, radius=0.055):
        st = PALETTE[kind]
        lines = self._wrap(text, fs, w - 2 * pad, weight)
        lh = fs * 1.32 / 72.0
        h = max(minh, len(lines) * lh + 2 * pad)
        box = FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle=f"round,pad=0,rounding_size={radius}",
            fc=st["fc"], ec=st["ec"], lw=st["lw"], zorder=3,
            mutation_aspect=1)
        self.ax.add_patch(box)
        self.ax.text(x, y, "\n".join(lines), ha="center", va="center",
                     fontsize=fs, fontfamily=FONT, fontweight=weight,
                     color=st["tc"], linespacing=1.32, zorder=4)
        self.nodes[nid] = (x, y, w, h)
        return nid

    def _anchor(self, nid, tx, ty, gap=0.045):
        """Punto del borde del rectangulo en direccion a (tx,ty)."""
        x, y, w, h = self.nodes[nid]
        dx, dy = tx - x, ty - y
        if dx == 0 and dy == 0:
            return x, y
        hw, hh = w / 2 + gap, h / 2 + gap
        sx = abs(dx) / hw if dx else 0
        sy = abs(dy) / hh if dy else 0
        s = max(sx, sy)
        return x + dx / s, y + dy / s

    # ---------- aristas ----------
    def edge(self, a, b, label=None, fs=7.2, style="-|>", color="#5A6076",
             lw=1.15, rad=0.0, dashed=False, lab_dx=0.0, lab_dy=0.0,
             lab_bg="#FFFFFF"):
        ax_, ay_, _, _ = self.nodes[a]
        bx_, by_, _, _ = self.nodes[b]
        p1 = self._anchor(a, bx_, by_)
        p2 = self._anchor(b, ax_, ay_)
        # Si las cajas estan tan juntas que los anclajes se cruzan, la flecha
        # saldria invertida: en ese caso se pegan los anclajes al borde.
        if (p2[0] - p1[0]) * (bx_ - ax_) + (p2[1] - p1[1]) * (by_ - ay_) <= 0:
            p1 = self._anchor(a, bx_, by_, gap=0.0)
            p2 = self._anchor(b, ax_, ay_, gap=0.0)
        # Flecha demasiado corta: la punta seria mas larga que la linea.
        if ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5 < 0.17:
            p1 = self._anchor(a, bx_, by_, gap=0.0)
            p2 = self._anchor(b, ax_, ay_, gap=0.0)
        arr = FancyArrowPatch(
            p1, p2, arrowstyle=style, mutation_scale=11,
            color=color, lw=lw, zorder=2,
            connectionstyle=f"arc3,rad={rad}",
            linestyle=(0, (4, 3)) if dashed else "solid",
            shrinkA=0, shrinkB=0)
        self.ax.add_patch(arr)
        if label:
            mx, my = (p1[0] + p2[0]) / 2 + lab_dx, (p1[1] + p2[1]) / 2 + lab_dy
            self.ax.text(mx, my, label, ha="center", va="center", fontsize=fs,
                         fontfamily=FONT, color="#3A4152", zorder=5,
                         bbox=dict(fc=lab_bg, ec="none", pad=1.4))

    # ---------- extras ----------
    def title(self, s, fs=11.5, y=None, color="#2C1758"):
        self.ax.text(self.w / 2, y if y is not None else self.h - 0.22, s,
                     ha="center", va="center", fontsize=fs, fontfamily=FONT,
                     fontweight="bold", color=color)

    def caption(self, x, y, s, fs=7.4, ha="center", color="#5A6076",
                weight="normal", maxw=None):
        if maxw:
            s = "\n".join(self._wrap(s, fs, maxw, weight))
        self.ax.text(x, y, s, ha=ha, va="center", fontsize=fs,
                     fontfamily=FONT, color=color, fontweight=weight,
                     linespacing=1.3)

    def band(self, x0, y0, x1, y1, label=None, color="#7C4DCB", fs=7.6):
        self.ax.add_patch(FancyBboxPatch(
            (x0, y0), x1 - x0, y1 - y0,
            boxstyle="round,pad=0,rounding_size=0.07",
            fc="none", ec=color, lw=0.9, ls=(0, (5, 3)), zorder=1))
        if label:
            self.ax.text(x0 + 0.07, y1 - 0.11, label, ha="left", va="center",
                         fontsize=fs, fontfamily=FONT, color=color,
                         fontweight="bold", zorder=5,
                         bbox=dict(fc="#FFFFFF", ec="none", pad=1.5))

    # ---------- panel con ejes para ejemplos con datos ----------
    def panel(self, x0, y0, w, h, xlim=(0, 1), ylim=(0, 1), xlabel=None,
              ylabel=None, title=None, fs=6.8, frame="L"):
        """Dibuja un recuadro de ejes y devuelve el mapeo dato -> pulgadas.

        `frame` puede ser "L" (solo ejes izquierdo e inferior), "box" (marco
        completo) o "none". El mapeo devuelto se usa para dibujar cualquier
        cosa dentro del panel manteniendo la escala en pulgadas del lienzo.
        """
        (xa, xb), (ya, yb) = xlim, ylim

        def m(dx, dy):
            return (x0 + (dx - xa) / (xb - xa) * w,
                    y0 + (dy - ya) / (yb - ya) * h)

        if frame == "box":
            self.ax.add_patch(FancyBboxPatch(
                (x0, y0), w, h, boxstyle="round,pad=0,rounding_size=0.02",
                fc="none", ec="#8A8FA8", lw=0.9, zorder=3))
        elif frame == "L":
            self.ax.plot([x0, x0, x0 + w], [y0 + h, y0, y0],
                         color="#5A6076", lw=1.0, zorder=3)
        if title:
            self.ax.text(x0 + w / 2, y0 + h + 0.14, title, ha="center",
                         va="center", fontsize=fs + 0.6, fontfamily=FONT,
                         fontweight="bold", color="#2C1758", zorder=5)
        if xlabel:
            self.ax.text(x0 + w / 2, y0 - 0.16, xlabel, ha="center",
                         va="center", fontsize=fs, fontfamily=FONT,
                         color="#5A6076", zorder=5)
        if ylabel:
            self.ax.text(x0 - 0.17, y0 + h / 2, ylabel, rotation=90,
                         ha="center", va="center", fontsize=fs,
                         fontfamily=FONT, color="#5A6076", zorder=5)
        return m

    # ---------- grilla tipo tablero (mundo de la aspiradora, 8-puzle) ----------
    def grid(self, x0, y0, cell, cols, rows, labels=None, fills=None,
             fs=8.0, ec="#5A6076", lw=1.1, tc="#1E2233"):
        """Dibuja una grilla de `cols`x`rows` con la celda (0,0) arriba-izq.

        `labels` y `fills` son diccionarios {(col, fila): valor}.
        """
        labels, fills = labels or {}, fills or {}
        for r in range(rows):
            for c in range(cols):
                cx = x0 + c * cell
                cy = y0 + (rows - 1 - r) * cell
                self.ax.add_patch(FancyBboxPatch(
                    (cx, cy), cell, cell,
                    boxstyle="round,pad=0,rounding_size=0.02",
                    fc=fills.get((c, r), "#FFFFFF"), ec=ec, lw=lw, zorder=3))
                t = labels.get((c, r))
                if t:
                    self.ax.text(cx + cell / 2, cy + cell / 2, t, ha="center",
                                 va="center", fontsize=fs, fontfamily=FONT,
                                 color=tc, linespacing=1.25, zorder=4)
        return lambda c, r: (x0 + c * cell + cell / 2,
                             y0 + (rows - 1 - r) * cell + cell / 2)

    def save(self, path):
        self.fig.savefig(path, dpi=self.dpi, facecolor=self.fig.get_facecolor())
        plt.close(self.fig)
        return path
