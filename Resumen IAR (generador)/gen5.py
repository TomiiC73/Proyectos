# -*- coding: utf-8 -*-
"""Diagramas de los EJEMPLOS concretos de las Unidades 1 y 2."""
import os
import numpy as np
from dlib import Diagram

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
SUCIO = "#E8DCC0"
LIMPIO = "#FFFFFF"


def e01_aspiradora():
    """Ejemplo de referencia: agente determinista en una grilla 2x2."""
    d = Diagram(6.3, 4.35)
    d.title("Ejemplo · La aspiradora en una grilla 2×2: mismo estado ⇒ misma acción",
            y=4.18, fs=10.2)

    # --- el mundo ---
    g = d.grid(0.62, 2.62, 0.68, 2, 2,
               labels={(0, 0): "A\nsucio", (1, 0): "B\nlimpio",
                       (0, 1): "C\nsucio", (1, 1): "D\nsucio"},
               fills={(0, 0): SUCIO, (0, 1): SUCIO, (1, 1): SUCIO},
               fs=7.4)
    ax = d.ax
    cx, cy = g(0, 0)
    ax.add_patch(__import__("matplotlib").patches.Circle(
        (cx, cy + 0.20), 0.075, fc="#4C2A85", ec="#2C1758", lw=0.8, zorder=6))
    d.caption(2.30, 3.30, "El agente (círculo morado)\nestá en A. Percibe sólo dos\n"
                          "cosas: en qué celda está\ny si esa celda está sucia.",
              fs=7.2, ha="left", maxw=1.75)

    # --- REAS ---
    d.node("reas", 4.95, 3.30,
           "REAS de este agente\n"
           "R: una celda limpia suma 1 punto por paso\n"
           "E: grilla 2×2, suciedad fija, sin obstáculos\n"
           "A: aspirar, arriba, abajo, izquierda, derecha\n"
           "S: sensor de posición y sensor de suciedad",
           w=2.40, kind="unit", fs=7.0)

    # --- tabla de la funcion del agente ---
    d.caption(3.15, 2.28, "LA FUNCIÓN DEL AGENTE: una fila por percepción, sin azar",
              fs=8.0, weight="bold", color="#2C1758")
    filas = [("[A, sucio]", "Aspirar"), ("[A, limpio]", "Derecha"),
             ("[B, sucio]", "Aspirar"), ("[B, limpio]", "Abajo"),
             ("[C, sucio]", "Aspirar"), ("[C, limpio]", "Derecha"),
             ("[D, sucio]", "Aspirar"), ("[D, limpio]", "Arriba")]
    x = 0.55
    for i, (p, a) in enumerate(filas):
        col, fil = i % 4, i // 4
        xx = 0.55 + col * 1.42
        yy = 1.86 - fil * 0.38
        d.node(f"f{i}", xx + 0.60, yy, f"{p}  →  {a}", w=1.26,
               kind="good" if a == "Aspirar" else "topic", fs=7.0, minh=0.30)

    d.node("det", 3.15, 0.70,
           "Es DETERMINISTA: la tabla no tiene probabilidades ni empates. Ante la misma "
           "percepción el agente hace siempre lo mismo, y el estado siguiente queda "
           "totalmente determinado por el estado actual más la acción.",
           w=5.9, kind="accent", fs=7.4)

    d.caption(3.15, 0.20,
              "Basta con cambiar una fila de esta tabla para tener otro agente. "
              "Si además la suciedad reapareciera al azar, el ambiente dejaría de ser "
              "determinista y esta tabla ya no alcanzaría.",
              fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e01_aspiradora.png"))


def e02_tipos_aspiradora():
    """Los cinco tipos de agente resolviendo la MISMA aspiradora."""
    d = Diagram(6.3, 3.55)
    d.title("Ejemplo · Los cinco tipos de agente, todos sobre la misma aspiradora",
            y=3.38, fs=10.2)

    filas = [
        ("REACTIVO SIMPLE",
         "«Si sucio → aspirar; si no → moverse.» No recuerda nada. Si no ve toda la "
         "grilla, puede pasar la vida yendo de A a B.", "topic"),
        ("REACTIVO BASADO EN MODELO",
         "Guarda un mapa interno: «C y D ya los limpié». Con eso funciona aunque el "
         "sensor sólo vea la celda actual.", "topic"),
        ("BASADO EN OBJETIVOS",
         "Su meta es «las cuatro celdas limpias». Puede planificar la ruta A→C→D→B "
         "antes de moverse.", "unit"),
        ("BASADO EN UTILIDAD",
         "Además compara: limpiar D primero gasta menos batería que ir por C. Elige "
         "el plan de mayor utilidad, no cualquiera que cumpla la meta.", "unit"),
        ("QUE APRENDE",
         "Descubre que la celda B se ensucia todos los días a la misma hora y cambia "
         "su recorrido sin que nadie se lo programe.", "root"),
    ]
    y = 2.90
    for i, (t, s, k) in enumerate(filas):
        d.node(f"n{i}", 1.32, y, t, w=2.15, kind=k, fs=7.4, weight="bold",
               minh=0.46)
        d.node(f"s{i}", 4.42, y, s, w=3.55, kind="note", fs=7.2, minh=0.46)
        if i:
            d.edge(f"n{i-1}", f"n{i}")
        y -= 0.58

    d.caption(3.15, 0.16,
              "Cada tipo agrega exactamente una cosa al anterior: memoria, meta, "
              "preferencia entre metas, y capacidad de mejorar solo.",
              fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "e02_tipos_aspiradora.png"))


def e03_patrones():
    """Reconocimiento de patrones: clasificar monedas por peso y diametro."""
    d = Diagram(6.3, 3.40)
    d.title("Ejemplo · Clasificar dos monedas midiendo peso y diámetro",
            y=3.23, fs=10.2)

    rng = np.random.default_rng(7)
    m = d.panel(0.70, 0.62, 2.35, 2.20, xlim=(20, 26), ylim=(3, 10),
                xlabel="diámetro (mm)", ylabel="peso (g)", frame="L")
    ax = d.ax
    a = rng.normal([21.5, 4.3], [0.35, 0.35], size=(18, 2))
    b = rng.normal([24.3, 7.6], [0.40, 0.45], size=(18, 2))
    for pts, c, mk in ((a, "#3E8E5A", "o"), (b, "#B24A4A", "^")):
        px = [m(u, v)[0] for u, v in pts]
        py = [m(u, v)[1] for u, v in pts]
        ax.scatter(px, py, s=11, c=c, marker=mk, zorder=5, linewidths=0)
    p1, p2 = m(20.6, 9.6), m(25.6, 3.5)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#4C2A85", lw=1.5, zorder=6)
    d.caption(m(21.3, 8.6)[0], m(21.3, 8.6)[1], "$100", fs=7.4, weight="bold",
              color="#3E8E5A")
    d.caption(m(24.6, 4.4)[0], m(24.6, 4.4)[1], "$500", fs=7.4, weight="bold",
              color="#B24A4A")

    d.node("s1", 4.72, 2.72, "1 · SENSADO\nuna balanza y un calibre",
           w=2.75, kind="accent", fs=7.4)
    d.node("s2", 4.72, 2.14,
           "2 · EXTRACCIÓN DE CARACTERÍSTICAS\nde toda la moneda me quedo con dos "
           "números: peso y diámetro", w=2.75, kind="accent", fs=7.4)
    d.node("s3", 4.72, 1.46,
           "3 · VECTOR DE PATRÓN\nx = (23,9 mm ; 7,2 g)", w=2.75, kind="topic",
           fs=7.4)
    d.node("s4", 4.72, 0.84,
           "4 · CLASIFICACIÓN\nla recta morada parte el plano: cae del lado "
           "$500 → esa es la respuesta", w=2.75, kind="good", fs=7.4)
    d.edge("s1", "s2")
    d.edge("s2", "s3")
    d.edge("s3", "s4")

    d.caption(1.87, 0.22,
              "El color no se mide: se decide. La frontera es lo que aprende el modelo.",
              fs=7.2, maxw=2.9)
    return d.save(os.path.join(OUT, "e03_patrones.png"))


def e04_sobreajuste():
    """Los tres regimenes: subajuste, buen ajuste, sobreajuste."""
    d = Diagram(6.3, 3.15)
    d.title("Ejemplo · El mismo conjunto de 10 puntos ajustado de tres maneras",
            y=2.98, fs=10.2)

    rng = np.random.default_rng(3)
    xs = np.linspace(0.5, 9.5, 10)
    ys = 2.2 + 0.55 * xs + rng.normal(0, 0.85, 10)
    ax = d.ax
    grados = [(1, "Grado 1 (recta)", "SUBAJUSTE\nel modelo es\ndemasiado rígido",
               "#B24A4A"),
              (3, "Grado 3", "BUEN AJUSTE\ncaptura la tendencia,\nno el ruido",
               "#3E8E5A"),
              (9, "Grado 9", "SOBREAJUSTE\npasa por todos los puntos\ny no generaliza",
               "#B24A4A")]
    for i, (g, tit, nota, col) in enumerate(grados):
        x0 = 0.55 + i * 2.00
        m = d.panel(x0, 1.28, 1.55, 1.30, xlim=(0, 10), ylim=(0, 10),
                    title=tit, frame="box", fs=6.6)
        px = [m(u, v)[0] for u, v in zip(xs, ys)]
        py = [m(u, v)[1] for u, v in zip(xs, ys)]
        ax.scatter(px, py, s=9, c="#2C1758", zorder=6, linewidths=0)
        c = np.polyfit(xs, ys, g)
        fx = np.linspace(0.4, 9.6, 200)
        fy = np.clip(np.polyval(c, fx), 0, 10)
        cx = [m(u, v)[0] for u, v in zip(fx, fy)]
        cy = [m(u, v)[1] for u, v in zip(fx, fy)]
        ax.plot(cx, cy, color="#4C2A85", lw=1.5, zorder=5)
        d.node(f"n{i}", x0 + 0.775, 0.86, nota, w=1.72,
               kind="bad" if col == "#B24A4A" else "good", fs=7.0, minh=0.44)

    d.node("mse", 3.15, 0.28,
           "El error de entrenamiento baja siempre al subir el grado; el error de test "
           "dibuja una «U». El grado 9 tiene error de entrenamiento casi cero y es el peor "
           "de los tres con datos nuevos.",
           w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e04_sobreajuste.png"))


def e05_regresiones():
    """Regresion lineal vs logistica, con datos concretos."""
    d = Diagram(6.3, 3.30)
    d.title("Ejemplo · Predecir un número frente a predecir una clase",
            y=3.13, fs=10.2)
    ax = d.ax

    # --- lineal: precio vs metros cuadrados ---
    m = d.panel(0.72, 1.30, 2.10, 1.42, xlim=(30, 130), ylim=(20, 130),
                xlabel="superficie (m²)", ylabel="precio (miles US$)",
                title="Regresión lineal", frame="L", fs=6.6)
    sup = np.array([40, 55, 62, 75, 80, 95, 102, 118])
    pre = np.array([32, 47, 51, 66, 72, 84, 95, 108])
    px = [m(u, v)[0] for u, v in zip(sup, pre)]
    py = [m(u, v)[1] for u, v in zip(sup, pre)]
    ax.scatter(px, py, s=13, c="#2C1758", zorder=6, linewidths=0)
    k = np.polyfit(sup, pre, 1)
    fx = np.array([33, 127])
    fy = np.polyval(k, fx)
    lx = [m(u, v)[0] for u, v in zip(fx, fy)]
    ly = [m(u, v)[1] for u, v in zip(fx, fy)]
    ax.plot(lx, ly, color="#4C2A85", lw=1.6, zorder=5)
    d.caption(1.98, 1.52, "h(x) ≈ 0,95·x − 6", fs=7.0, color="#4C2A85",
              weight="bold")

    # --- logistica: aprobar vs horas de estudio ---
    m2 = d.panel(3.62, 1.30, 2.10, 1.42, xlim=(0, 12), ylim=(-0.12, 1.12),
                 xlabel="horas de estudio", ylabel="P(aprobar)",
                 title="Regresión logística", frame="L", fs=6.6)
    hx = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    hy = np.array([0, 0, 0, 0, 1, 0, 1, 1, 1, 1])
    qx = [m2(u, v)[0] for u, v in zip(hx, hy)]
    qy = [m2(u, v)[1] for u, v in zip(hx, hy)]
    ax.scatter(qx, qy, s=13, c="#2C1758", zorder=6, linewidths=0)
    gx = np.linspace(0, 12, 200)
    gy = 1 / (1 + np.exp(-(gx - 5.3) * 1.15))
    sx = [m2(u, v)[0] for u, v in zip(gx, gy)]
    sy = [m2(u, v)[1] for u, v in zip(gx, gy)]
    ax.plot(sx, sy, color="#4C2A85", lw=1.6, zorder=5)
    a1, a2 = m2(0, 0.5), m2(12, 0.5)
    ax.plot([a1[0], a2[0]], [a1[1], a2[1]], ls=(0, (3, 3)), color="#C9962A",
            lw=1.0, zorder=4)
    d.caption(m2(9.6, 0.40)[0], m2(9.6, 0.40)[1], "umbral 0,5", fs=6.6,
              color="#C9962A")

    d.node("l", 1.77, 0.70,
           "La salida es un número cualquiera.\nSe ajusta minimizando el MSE.",
           w=2.55, kind="topic", fs=7.2)
    d.node("g", 4.67, 0.70,
           "La salida está entre 0 y 1 y se lee\ncomo probabilidad de la clase.",
           w=2.55, kind="topic", fs=7.2)
    d.caption(3.15, 0.20,
              "Con 6 horas de estudio el modelo devuelve ≈ 0,69: por encima de 0,5, así que "
              "predice «aprueba» — pero además dice cuánta confianza tiene, cosa que un "
              "umbral duro no puede hacer.",
              fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e05_regresiones.png"))


def e06_svm():
    """SVM: margen maximo y vectores de soporte."""
    d = Diagram(6.3, 3.20)
    d.title("Ejemplo · Entre todas las rectas que separan, la SVM elige una sola",
            y=3.03, fs=10.2)
    ax = d.ax

    A = np.array([[1.6, 5.4], [2.2, 6.4], [1.2, 4.2], [2.8, 5.2], [1.9, 7.1]])
    B = np.array([[5.4, 2.2], [6.4, 3.0], [4.6, 1.4], [6.9, 1.9], [5.9, 3.6]])

    def dibujar(x0, titulo, rectas, marcar):
        m = d.panel(x0, 0.98, 2.35, 1.72, xlim=(0, 8.5), ylim=(0, 8.5),
                    title=titulo, frame="box", fs=6.8)
        for pts, c, mk in ((A, "#3E8E5A", "o"), (B, "#B24A4A", "s")):
            ax.scatter([m(u, v)[0] for u, v in pts],
                       [m(u, v)[1] for u, v in pts],
                       s=14, c=c, marker=mk, zorder=6, linewidths=0)
        for (b, k, col, lw, ls) in rectas:
            fx = np.linspace(0.1, 8.4, 50)
            fy = b + k * fx
            ok = (fy > 0.1) & (fy < 8.4)
            ax.plot([m(u, v)[0] for u, v in zip(fx[ok], fy[ok])],
                    [m(u, v)[1] for u, v in zip(fx[ok], fy[ok])],
                    color=col, lw=lw, ls=ls, zorder=5)
        if marcar:
            for u, v in ((2.8, 5.2), (4.6, 1.4), (5.4, 2.2)):
                p = m(u, v)
                ax.scatter([p[0]], [p[1]], s=60, facecolors="none",
                           edgecolors="#C9962A", linewidths=1.3, zorder=7)
        return m

    dibujar(0.55, "Muchas rectas separan igual de bien",
            [(8.2, -1.0, "#8A8FA8", 1.0, "solid"),
             (9.6, -1.45, "#8A8FA8", 1.0, "solid"),
             (6.4, -0.62, "#8A8FA8", 1.0, "solid")], False)
    dibujar(3.42, "La SVM elige la del margen máximo",
            [(8.2, -1.0, "#4C2A85", 1.7, "solid"),
             (9.5, -1.0, "#7C4DCB", 0.9, (0, (3, 3))),
             (6.9, -1.0, "#7C4DCB", 0.9, (0, (3, 3)))], True)

    d.node("vs", 3.15, 0.52,
           "Los tres puntos con círculo naranja son los VECTORES DE SOPORTE: los únicos "
           "que definen la frontera. Mover cualquiera de los demás no cambia nada; mover "
           "uno de ellos, sí.",
           w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e06_svm.png"))


def e07_perceptron():
    """Perceptron aprendiendo la compuerta OR, paso a paso."""
    d = Diagram(6.3, 5.05)
    d.title("Ejemplo · Un perceptrón aprende la compuerta OR en cuatro épocas",
            y=4.88, fs=10.2)
    ax = d.ax

    m = d.panel(0.62, 2.95, 1.75, 1.40, xlim=(-0.4, 1.4), ylim=(-0.4, 1.4),
                xlabel="x₁", ylabel="x₂", title="OR es linealmente separable",
                frame="box", fs=6.6)
    fx = np.linspace(-0.4, 1.4, 200)
    fy = 1.0 - fx        # recta final aprendida: 0,5x1 + 0,5x2 - 0,5 = 0
    ok = (fy > -0.4) & (fy < 1.4)
    ax.plot([m(u, v)[0] for u, v in zip(fx[ok], fy[ok])],
            [m(u, v)[1] for u, v in zip(fx[ok], fy[ok])],
            color="#4C2A85", lw=1.6, zorder=5)
    for (u, v), y in (((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 1)):
        p = m(u, v)
        ax.scatter([p[0]], [p[1]], s=34, marker="o" if y else "X",
                   c="#3E8E5A" if y else "#B24A4A", zorder=6, linewidths=0)
        d.caption(p[0] + (0.17 if u == 0 else -0.17), p[1] + 0.13, str(y),
                  fs=7.0, weight="bold",
                  color="#3E8E5A" if y else "#B24A4A")

    d.node("neu", 4.32, 4.02,
           "y′ = escalón(w₀ + w₁x₁ + w₂x₂)\ncon escalón(z) = 1 si z ≥ 0, si no 0",
           w=3.50, kind="root", fs=7.6)
    d.node("reg", 4.32, 3.22,
           "REGLA DE APRENDIZAJE\nwᵢ ← wᵢ + α (y − y′) xᵢ\n"
           "Sólo se tocan los pesos cuando la salida está mal (y − y′ ≠ 0).",
           w=3.50, kind="accent", fs=7.4)

    d.caption(3.15, 2.48, "PRIMERA ÉPOCA, empezando con w = (0, 0, 0) y α = 0,5",
              fs=8.2, weight="bold", color="#2C1758")
    filas = [("(0,0) → y = 0", "z = 0,00 → y′ = 1  ✗", "w = (−0,5 ;  0 ;  0)"),
             ("(0,1) → y = 1", "z = −0,50 → y′ = 0  ✗", "w = (0 ;  0 ;  0,5)"),
             ("(1,0) → y = 1", "z = 0,00 → y′ = 1  ✓", "w sin cambios"),
             ("(1,1) → y = 1", "z = 0,50 → y′ = 1  ✓", "w sin cambios")]
    for i, (a, b, c) in enumerate(filas):
        y = 2.12 - i * 0.34
        d.node(f"a{i}", 1.05, y, a, w=1.25, kind="topic", fs=7.0, minh=0.26)
        d.node(f"b{i}", 2.72, y, b, w=1.90, kind="bad" if "✗" in b else "good",
               fs=7.0, minh=0.26)
        d.node(f"c{i}", 4.90, y, c, w=2.25, kind="note", fs=7.0, minh=0.26)

    d.node("fin", 3.15, 0.62,
           "Todavía quedan errores, así que el recorrido se repite. Recién en la CUARTA "
           "época el perceptrón pasa las cuatro filas sin equivocarse, con "
           "w = (−0,5 ; 0,5 ; 0,5): la recta 0,5x₁ + 0,5x₂ − 0,5 = 0, que es la dibujada.",
           w=5.9, kind="accent", fs=7.3)
    d.caption(3.15, 0.14,
              "La misma regla NO converge con XOR: no existe ninguna recta que lo separe, "
              "así que el algoritmo corrige para siempre sin llegar a nada.",
              fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e07_perceptron.png"))


def e08_red_xor():
    """Red multicapa resolviendo XOR: por que hace falta una capa oculta."""
    d = Diagram(6.3, 3.30)
    d.title("Ejemplo · XOR necesita una capa oculta: dos rectas en vez de una",
            y=3.13, fs=10.2)
    ax = d.ax

    m = d.panel(0.68, 1.02, 1.50, 1.50, xlim=(-0.35, 1.35), ylim=(-0.35, 1.35),
                xlabel="x₁", ylabel="x₂", title="XOR", frame="box", fs=6.6)
    for (u, v), y in (((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)):
        p = m(u, v)
        ax.scatter([p[0]], [p[1]], s=34, marker="o" if y else "X",
                   c="#3E8E5A" if y else "#B24A4A", zorder=6, linewidths=0)
    for b in (0.5, 1.5):
        fx = np.array([-0.3, 1.3])
        fy = b - fx
        ok = (fy > -0.3) & (fy < 1.3)
        ax.plot([m(u, v)[0] for u, v in zip(fx[ok], fy[ok])],
                [m(u, v)[1] for u, v in zip(fx[ok], fy[ok])],
                color="#4C2A85", lw=1.5, zorder=5)

    # --- la red ---
    capas = [("ENTRADA", ["x₁", "x₂"], 2.95, "topic"),
             ("OCULTA", ["h₁", "h₂"], 4.20, "unit"),
             ("SALIDA", ["y"], 5.45, "good")]
    pos = {}
    for cx, (tit, nodos, x, kind) in zip(range(3), capas):
        d.caption(x, 2.62, tit, fs=7.2, weight="bold", color="#2C1758")
        ys = [2.10, 1.44] if len(nodos) == 2 else [1.77]
        for n, y in zip(nodos, ys):
            d.node(n, x, y, n, w=0.46, kind=kind, fs=8.0, weight="bold",
                   minh=0.36, radius=0.18)
            pos[n] = (x, y)
    for a in ("x₁", "x₂"):
        for b in ("h₁", "h₂"):
            d.edge(a, b, style="-", lw=0.8, color="#8A8FA8")
    for b in ("h₁", "h₂"):
        d.edge(b, "y", style="-", lw=0.8, color="#8A8FA8")

    d.node("exp", 3.15, 0.52,
           "h₁ aprende «al menos uno» (OR) y h₂ aprende «los dos» (AND); la salida hace "
           "h₁ Y NO h₂. Si la activación fuera lineal, las dos capas se reducirían a una "
           "sola y volveríamos al perceptrón: la no linealidad es lo que agrega poder.",
           w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e08_red_xor.png"))


def e09_convolucion():
    """Una convolucion 3x3 calculada a mano sobre una imagen 5x5."""
    d = Diagram(6.3, 3.45)
    d.title("Ejemplo · Una convolución 3×3 detectando un borde vertical",
            y=3.28, fs=10.2)

    img = [[0, 0, 9, 9, 9],
           [0, 0, 9, 9, 9],
           [0, 0, 9, 9, 9],
           [0, 0, 9, 9, 9],
           [0, 0, 9, 9, 9]]
    lab = {(c, r): str(img[r][c]) for r in range(5) for c in range(5)}
    fil = {(c, r): ("#EDE4FB" if c < 3 and r < 3 else "#FFFFFF")
           for r in range(5) for c in range(5)}
    d.caption(0.98, 2.88, "IMAGEN 5×5", fs=7.6, weight="bold", color="#2C1758")
    d.grid(0.30, 1.28, 0.272, 5, 5, labels=lab, fills=fil, fs=7.0)

    ker = [[1, 0, -1], [1, 0, -1], [1, 0, -1]]
    kl = {(c, r): str(ker[r][c]) for r in range(3) for c in range(3)}
    d.caption(2.42, 2.88, "FILTRO 3×3", fs=7.6, weight="bold", color="#2C1758")
    d.grid(2.02, 1.55, 0.272, 3, 3, labels=kl,
           fills={(c, r): "#FFF3D6" for r in range(3) for c in range(3)}, fs=7.0)

    sal = [[-27, -27, 0], [-27, -27, 0], [-27, -27, 0]]
    sl = {(c, r): str(sal[r][c]) for r in range(3) for c in range(3)}
    d.caption(4.20, 2.88, "SALIDA 3×3", fs=7.6, weight="bold", color="#2C1758")
    d.grid(3.72, 1.55, 0.32, 3, 3, labels=sl,
           fills={(c, r): ("#E3F5E8" if sal[r][c] == 0 else "#FBE6E6")
                  for r in range(3) for c in range(3)}, fs=7.0)

    d.node("cta", 5.42, 2.06,
           "Primera celda:\n(1·0)+(0·0)+(−1·9)\n+(1·0)+(0·0)+(−1·9)\n"
           "+(1·0)+(0·0)+(−1·9)\n= −27",
           w=1.55, kind="unit", fs=7.0)

    d.node("txt", 3.15, 0.86,
           "El filtro se desliza sobre la imagen y en cada posición hace la suma de "
           "productos. Donde hay un salto de oscuro a claro devuelve un valor grande en "
           "módulo (−27); donde el color es uniforme devuelve 0. Eso es «detectar un "
           "borde», y los pesos del filtro NO se programan: se aprenden.",
           w=5.9, kind="accent", fs=7.3)
    d.caption(3.15, 0.22,
              "Con paso (stride) 1 y sin relleno (padding), una imagen 5×5 con filtro 3×3 "
              "da una salida 3×3: la imagen se achica. El relleno sirve justamente para "
              "evitar eso.", fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e09_convolucion.png"))


def e10_metricas():
    """Matriz de confusion con numeros concretos."""
    d = Diagram(6.3, 3.05)
    d.title("Ejemplo · 100 pacientes, un test, y por qué el 91 % de aciertos engaña",
            y=2.88, fs=10.2)

    d.caption(1.55, 2.50, "Resultado del test sobre 100 personas (10 enfermas)",
              fs=7.4, weight="bold", color="#2C1758")
    d.caption(1.06, 2.20, "Predice ENFERMO", fs=6.9, weight="bold")
    d.caption(2.18, 2.20, "Predice SANO", fs=6.9, weight="bold")
    d.caption(0.32, 1.86, "Enfermo", fs=6.9, weight="bold")
    d.caption(0.32, 1.42, "Sano", fs=6.9, weight="bold")
    d.node("vp", 1.06, 1.86, "VP = 6", w=1.00, kind="good", fs=8.2,
           weight="bold", minh=0.38)
    d.node("fn", 2.18, 1.86, "FN = 4", w=1.00, kind="bad", fs=8.2,
           weight="bold", minh=0.38)
    d.node("fp", 1.06, 1.42, "FP = 5", w=1.00, kind="bad", fs=8.2,
           weight="bold", minh=0.38)
    d.node("vn", 2.18, 1.42, "VN = 85", w=1.00, kind="good", fs=8.2,
           weight="bold", minh=0.38)

    mets = [("Accuracy = (6+85)/100 = 0,91", "topic"),
            ("Recall = 6/(6+4) = 0,60", "bad"),
            ("Especificidad = 85/(5+85) = 0,94", "topic"),
            ("Precision = 6/(6+5) = 0,55", "bad"),
            ("F₁ = 2·0,55·0,60 / (0,55+0,60) = 0,57", "accent")]
    for i, (t, k) in enumerate(mets):
        d.node(f"m{i}", 4.60, 2.42 - i * 0.40, t, w=3.20, kind=k, fs=7.2,
               minh=0.30)

    d.node("con", 3.15, 0.50,
           "El 91 % de accuracy suena bien, pero el test se pierde 4 de cada 10 enfermos "
           "(recall 0,60) y más de la mitad de sus alarmas son falsas (precision 0,55). "
           "Un test que dijera «sano» siempre tendría 90 % de accuracy y recall CERO: por "
           "eso en clases desbalanceadas la accuracy sola no sirve.",
           w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e10_metricas.png"))


if __name__ == "__main__":
    for f in (e01_aspiradora, e02_tipos_aspiradora, e03_patrones, e04_sobreajuste,
              e05_regresiones, e06_svm, e07_perceptron, e08_red_xor,
              e09_convolucion, e10_metricas):
        print(f())
