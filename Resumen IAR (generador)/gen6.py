# -*- coding: utf-8 -*-
"""Diagramas de los EJEMPLOS concretos de las Unidades 3 y 4."""
import os
import numpy as np
from dlib import Diagram

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


def e11_espacio_estados():
    """Espacio de estados de la aspiradora de 2 celdas (Russell y Norvig)."""
    d = Diagram(6.3, 4.05)
    d.title("Ejemplo · El espacio de estados completo de la aspiradora de 2 celdas",
            y=3.88, fs=10.2)

    # 8 estados = 2 posiciones del agente x 4 configuraciones de suciedad.
    # Columnas ordenadas para que las transiciones de la fila de arriba queden
    # entre columnas contiguas; las de abajo se dibujan como arcos.
    conf = [("suc", "suc"), ("lim", "suc"), ("suc", "lim"), ("lim", "lim")]
    for j, (sa, sb) in enumerate(conf):
        for i, donde in enumerate(("A", "B")):
            x = 0.88 + j * 1.52
            y = 3.32 - i * 0.85
            k = "good" if (sa, sb) == ("lim", "lim") else "topic"
            d.node(f"s{j}{i}", x, y, f"A:{sa}   B:{sb}\nagente en {donde}",
                   w=1.32, kind=k, fs=6.8, minh=0.44)

    VERDE = "#3E8E5A"
    # Aspirar con el agente en A: limpia la celda A (fila de arriba, contiguas)
    d.edge("s00", "s10", color=VERDE, lw=1.3)
    d.edge("s20", "s30", color=VERDE, lw=1.3)
    # Aspirar con el agente en B: limpia la celda B (fila de abajo, en arco)
    d.edge("s01", "s21", color=VERDE, lw=1.3, rad=0.34)
    d.edge("s11", "s31", color=VERDE, lw=1.3, rad=0.34)
    # Izquierda / Derecha: sólo cambian dónde está el agente
    for j in range(4):
        d.edge(f"s{j}0", f"s{j}1", style="<|-|>", lw=1.0, color="#8A8FA8")

    d.caption(1.75, 1.60, "— Aspirar", fs=7.2, color=VERDE, weight="bold")
    d.caption(4.10, 1.60, "↕ Izquierda / Derecha", fs=7.2, color="#5A6076",
              weight="bold")

    d.node("txt", 3.15, 1.16,
           "Ocho estados y tres acciones: eso es TODO el espacio de estados. Buscar una "
           "solución es encontrar un camino desde el estado inicial hasta cualquiera de "
           "los dos estados verdes (las dos celdas limpias).",
           w=5.9, kind="accent", fs=7.3)
    d.node("nod", 3.15, 0.46,
           "Ojo con la diferencia: hay 8 ESTADOS, pero infinitos NODOS — el agente puede "
           "ir y volver de A a B para siempre, generando caminos cada vez más largos "
           "sobre los mismos ocho estados. Por eso hace falta la lista cerrada.",
           w=5.9, kind="note", fs=7.3)
    return d.save(os.path.join(OUT, "e11_espacio_estados.png"))


def e12_produccion():
    """Sistema de produccion: reglas, memoria de trabajo y estrategia de control."""
    d = Diagram(6.3, 3.95)
    d.title("Ejemplo · La misma aspiradora escrita como sistema de producción",
            y=3.78, fs=10.2)

    d.caption(1.55, 3.42, "BASE DE REGLAS (memoria a largo plazo)", fs=7.6,
              weight="bold", color="#2C1758")
    reglas = ["R1: SI En(x) ∧ Sucio(x)\n      ENTONCES Aspirar",
              "R2: SI En(x) ∧ ¬Sucio(x) ∧ Sucio(y)\n      ENTONCES Ir(y)",
              "R3: SI ninguna celda está sucia\n      ENTONCES Detenerse"]
    for i, r in enumerate(reglas):
        d.node(f"r{i}", 1.55, 3.02 - i * 0.56, r, w=2.85, kind="unit", fs=7.0,
               minh=0.44)

    d.caption(4.75, 3.42, "MEMORIA DE TRABAJO (corto plazo)", fs=7.6,
              weight="bold", color="#2C1758")
    d.node("mt", 4.75, 3.02, "En(A)\nSucio(A)\nSucio(B)", w=2.35, kind="accent",
           fs=7.4, minh=0.44)
    d.node("cc", 4.75, 2.32,
           "CONJUNTO CONFLICTO\nR1 y R2 podrían dispararse:\nlas dos tienen sus "
           "condiciones satisfechas", w=2.35, kind="bad", fs=7.0, minh=0.44)
    d.node("ec", 4.75, 1.58,
           "ESTRATEGIA DE CONTROL\ndesempata: «la regla más\nespecífica primero» → gana R1",
           w=2.35, kind="good", fs=7.0, minh=0.44)
    d.edge("mt", "cc")
    d.edge("cc", "ec")

    d.node("ciclo", 3.15, 0.92,
           "CICLO: emparejar (qué reglas aplican) → resolver el conflicto (cuál se "
           "dispara) → actuar (modificar la memoria de trabajo). Se repite hasta que "
           "ninguna regla aplica o se alcanza la meta.",
           w=5.9, kind="root", fs=7.3)
    d.caption(3.15, 0.28,
              "La estrategia de control es la que decide el orden de exploración: es "
              "exactamente el mismo papel que cumple el tipo de cola en un algoritmo de "
              "búsqueda (FIFO da anchura, LIFO da profundidad).",
              fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e12_produccion.png"))


def e13_arbol_busqueda():
    """Arbol de busqueda: orden de expansion en anchura y en profundidad."""
    d = Diagram(6.3, 3.85)
    d.title("Ejemplo · El mismo árbol recorrido en anchura y en profundidad",
            y=3.68, fs=10.2)

    # arbol binario de profundidad 3: A / B C / D E F G
    coord = {"A": (0, 0), "B": (-1, 1), "C": (1, 1),
             "D": (-1.5, 2), "E": (-0.5, 2), "F": (0.5, 2), "G": (1.5, 2)}
    padres = {"B": "A", "C": "A", "D": "B", "E": "B", "F": "C", "G": "C"}
    ordenes = [("PRIMERO EN ANCHURA (cola FIFO)",
                {"A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7}, 0.30),
               ("PRIMERO EN PROFUNDIDAD (pila LIFO)",
                {"A": 1, "B": 2, "D": 3, "E": 4, "C": 5, "F": 6, "G": 7}, 3.28)]

    for tit, orden, x0 in ordenes:
        d.caption(x0 + 1.36, 3.24, tit, fs=7.4, weight="bold", color="#2C1758")
        base = {}
        for n, (cx, cy) in coord.items():
            x = x0 + 1.36 + cx * 0.62
            y = 2.86 - cy * 0.62
            base[n] = (x, y)
            d.node(f"{x0}{n}", x, y, f"{n}\n{orden[n]}", w=0.44, kind="unit",
                   fs=7.0, weight="bold", minh=0.40, radius=0.20)
        for hijo, padre in padres.items():
            d.edge(f"{x0}{padre}", f"{x0}{hijo}", style="-", lw=0.9,
                   color="#8A8FA8")
        seq = " → ".join(sorted(orden, key=orden.get))
        d.caption(x0 + 1.36, 0.86, seq, fs=7.2, weight="bold", color="#4C2A85")

    d.node("cmp", 3.15, 0.44,
           "El árbol es idéntico; lo único que cambia es el tipo de cola. Anchura "
           "almacena O(bᵈ) nodos pero encuentra la solución más superficial; "
           "profundidad almacena sólo O(b·m) pero puede irse por una rama infinita.",
           w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e13_arbol_busqueda.png"))


def e14_astar():
    """A* sobre un grafo chico, con g, h y f calculados."""
    d = Diagram(6.3, 3.98)
    d.title("Ejemplo · A* paso a paso: por qué nunca expande el nodo B",
            y=3.81, fs=10.2)

    nodos = {"S": (0.80, 3.05, "S\nh=5"), "A": (2.15, 3.38, "A\nh=4"),
             "B": (2.15, 2.52, "B\nh=3"), "C": (3.50, 3.38, "C\nh=2"),
             "G": (4.55, 2.88, "G\nh=0")}
    for n, (x, y, t) in nodos.items():
        d.node(n, x, y, t, w=0.60, kind="root" if n in "SG" else "unit",
               fs=7.2, weight="bold", minh=0.44, radius=0.16)
    aristas = [("S", "A", "1"), ("S", "B", "4"), ("A", "C", "2"),
               ("C", "G", "2"), ("B", "G", "3")]
    for a, b, c in aristas:
        d.edge(a, b, c, style="-", fs=7.0, lw=1.1)

    d.caption(5.62, 3.50, "h = estimación\nde lo que falta\nhasta G", fs=6.8,
              maxw=1.20)
    d.caption(5.62, 2.72, "los números\nsobre las líneas\nson costos reales",
              fs=6.8, maxw=1.20)

    d.caption(3.15, 2.10, "ORDEN DE EXPANSIÓN — siempre el menor f = g + h",
              fs=8.0, weight="bold", color="#2C1758")
    pasos = [("1º  S", "g=0  h=5", "f = 5", "good"),
             ("2º  A", "g=1  h=4", "f = 5", "good"),
             ("3º  C", "g=3  h=2", "f = 5", "good"),
             ("4º  G", "g=5  h=0", "f = 5  ✓ solución", "good"),
             ("—   B", "g=4  h=3", "f = 7  nunca se expande", "bad")]
    for i, (a, b, c, k) in enumerate(pasos):
        y = 1.74 - i * 0.30
        d.node(f"p{i}", 0.95, y, a, w=0.90, kind="topic", fs=7.0, minh=0.25)
        d.node(f"q{i}", 2.28, y, b, w=1.40, kind="topic", fs=7.0, minh=0.25)
        d.node(f"r{i}", 4.35, y, c, w=2.55, kind=k, fs=7.0, minh=0.25)

    d.caption(3.15, 0.20,
              "B queda en la frontera con f = 7. Como A* expande siempre el menor f y "
              "encuentra G con f = 5, B nunca llega a expandirse: la heurística ahorró "
              "trabajo sin perder la solución óptima.", fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e14_astar.png"))


def e15_8puzzle():
    """h1 y h2 calculadas sobre el 8-puzle (ejemplo de Russell y Norvig)."""
    d = Diagram(6.3, 3.55)
    d.title("Ejemplo · Las dos heurísticas del 8-puzle, contadas sobre el mismo tablero",
            y=3.38, fs=10.2)

    ini = [["7", "2", "4"], ["5", "", "6"], ["8", "3", "1"]]
    fin = [["", "1", "2"], ["3", "4", "5"], ["6", "7", "8"]]
    d.caption(1.02, 3.02, "ESTADO ACTUAL", fs=7.6, weight="bold", color="#2C1758")
    d.grid(0.53, 1.88, 0.33, 3, 3,
           labels={(c, r): ini[r][c] for r in range(3) for c in range(3)},
           fills={(c, r): ("#F2F4F8" if not ini[r][c] else "#EDE4FB")
                  for r in range(3) for c in range(3)}, fs=9.0)
    d.caption(2.52, 3.02, "OBJETIVO", fs=7.6, weight="bold", color="#2C1758")
    d.grid(2.03, 1.88, 0.33, 3, 3,
           labels={(c, r): fin[r][c] for r in range(3) for c in range(3)},
           fills={(c, r): ("#F2F4F8" if not fin[r][c] else "#E3F5E8")
                  for r in range(3) for c in range(3)}, fs=9.0)

    d.node("h1", 4.62, 2.72,
           "h₁ = fichas mal colocadas\nLas 8 fichas están fuera de lugar → h₁ = 8",
           w=2.90, kind="unit", fs=7.4)
    d.node("h2", 4.62, 2.00,
           "h₂ = distancia Manhattan\nSuma de casillas horizontales y verticales que "
           "le falta recorrer a cada ficha", w=2.90, kind="unit", fs=7.4)

    d.caption(3.15, 1.52, "CUENTA DE h₂, ficha por ficha", fs=8.0, weight="bold",
              color="#2C1758")
    cuentas = [("1→3", "2→1", "3→2", "4→2"), ("5→2", "6→3", "7→3", "8→2")]
    for f, fila in enumerate(cuentas):
        for c, t in enumerate(fila):
            d.node(f"c{f}{c}", 1.30 + c * 0.92, 1.16 - f * 0.28, t, w=0.80,
                   kind="topic", fs=7.0, minh=0.23)
    d.node("tot", 5.05, 1.02, "h₂ = 18", w=1.20, kind="accent", fs=8.6,
           weight="bold", minh=0.40)

    d.node("dom", 3.15, 0.42,
           "Las dos son admisibles (nunca sobrestiman: el costo real de este tablero es "
           "26 movimientos). Pero h₂ ≥ h₁ en todo nodo, así que h₂ DOMINA a h₁ y expande "
           "menos nodos: siempre conviene la heurística más grande que siga siendo "
           "admisible.", w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e15_8puzzle.png"))


def e16_colinas():
    """Ascension de colinas atrapada en un maximo local; temple simulado escapa."""
    d = Diagram(6.3, 3.95)
    d.title("Ejemplo · Por qué la ascensión de colinas se queda con la loma equivocada",
            y=3.78, fs=10.2)
    ax = d.ax

    fx = np.linspace(0, 10, 400)
    fy = (2.2 * np.exp(-((fx - 2.4) ** 2) / 1.6) +
          4.0 * np.exp(-((fx - 7.0) ** 2) / 2.2) + 0.6)
    m = d.panel(0.72, 1.42, 4.00, 1.62, xlim=(0, 10), ylim=(0, 5.2),
                xlabel="estados vecinos (el «paisaje» del problema)",
                ylabel="valor", frame="L", fs=6.8)
    ax.plot([m(u, v)[0] for u, v in zip(fx, fy)],
            [m(u, v)[1] for u, v in zip(fx, fy)],
            color="#4C2A85", lw=1.7, zorder=5)

    for xx, lab, col, dy in ((2.4, "MÁXIMO LOCAL\naquí se detiene", "#B24A4A", 0.42),
                             (7.0, "MÁXIMO GLOBAL\nlo que buscábamos", "#3E8E5A", 0.42)):
        yy = (2.2 * np.exp(-((xx - 2.4) ** 2) / 1.6) +
              4.0 * np.exp(-((xx - 7.0) ** 2) / 2.2) + 0.6)
        p = m(xx, yy)
        ax.scatter([p[0]], [p[1]], s=40, c=col, zorder=7, linewidths=0)
        d.caption(p[0], p[1] + dy, lab, fs=6.8, color=col, weight="bold")

    p0 = m(0.9, (2.2 * np.exp(-((0.9 - 2.4) ** 2) / 1.6) +
                 4.0 * np.exp(-((0.9 - 7.0) ** 2) / 2.2) + 0.6))
    ax.scatter([p0[0]], [p0[1]], s=34, marker="s", c="#2C1758", zorder=7,
               linewidths=0)
    d.caption(p0[0] - 0.02, p0[1] - 0.26, "arranque", fs=6.8, color="#2C1758")

    d.node("hc", 5.48, 2.86, "ASCENSIÓN\nDE COLINAS\nsólo sube:\nse traba",
           w=1.42, kind="bad", fs=6.9)
    d.node("ts", 5.48, 1.86, "TEMPLE\nSIMULADO\na veces baja:\npuede escapar",
           w=1.42, kind="good", fs=6.9)

    d.node("txt", 3.15, 0.80,
           "La ascensión de colinas sólo acepta vecinos mejores, así que desde el "
           "arranque sube la primera loma y ahí se queda: cualquier movimiento empeora. "
           "El temple simulado acepta un movimiento malo con probabilidad e^(−ΔE/T), y "
           "esa probabilidad se va achicando a medida que baja la temperatura T.",
           w=5.9, kind="accent", fs=7.3)
    d.caption(3.15, 0.18,
              "Con T alta el algoritmo casi hace un paseo aleatorio (diversificación); "
              "con T baja se parece a la ascensión de colinas (intensificación).",
              fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e16_colinas.png"))


def e17_genetico():
    """Una generacion completa de un algoritmo genetico, con numeros."""
    d = Diagram(6.3, 4.30)
    d.title("Ejemplo · Una generación de un algoritmo genético maximizando f(x) = x²",
            y=4.13, fs=10.2)
    d.node("set", 3.15, 3.72,
           "Cromosoma = 5 bits que codifican x entre 0 y 31.  Idoneidad = f(x) = x².",
           w=5.9, kind="root", fs=7.6)

    cab = ["Cromosoma", "x", "f(x) = x²", "% del total", "Copias"]
    anchos = [1.22, 0.62, 0.98, 1.12, 0.78]
    xs, acc = [], 0.72
    for w in anchos:
        xs.append(acc + w / 2)
        acc += w + 0.06
    for x, w, t in zip(xs, anchos, cab):
        d.node(f"h{t}", x, 3.28, t, w=w, kind="accent", fs=7.0, weight="bold",
               minh=0.26)

    filas = [("0 1 1 0 1", "13", "169", "14,4 %", "1"),
             ("1 1 0 0 0", "24", "576", "49,2 %", "2"),
             ("0 1 0 0 0", "8", "64", "5,5 %", "0"),
             ("1 0 0 1 1", "19", "361", "30,9 %", "1")]
    for i, fila in enumerate(filas):
        y = 2.96 - i * 0.30
        for j, (x, w, t) in enumerate(zip(xs, anchos, fila)):
            k = "good" if (j == 4 and t != "0") else ("bad" if t == "0" else "topic")
            d.node(f"f{i}{j}", x, y, t, w=w, kind=k, fs=7.0, minh=0.25)
    d.node("tot", 3.15, 1.66, "Total 1170   ·   Promedio 292,5   ·   Máximo 576",
           w=4.60, kind="note", fs=7.2, minh=0.26)

    d.node("cru", 1.62, 1.14,
           "CRUCE\n0110|1 × 1100|0 → 01100 (12) y 11001 (25)\n"
           "11|000 × 10|011 → 11011 (27) y 10000 (16)",
           w=2.85, kind="unit", fs=7.0)
    d.node("res", 4.68, 1.14,
           "NUEVA GENERACIÓN\nf = 144, 625, 729, 256\nTotal 1754 · Promedio 438,5 · "
           "Máximo 729", w=2.85, kind="good", fs=7.0)
    d.edge("cru", "res")

    d.node("txt", 3.15, 0.44,
           "En una sola generación el promedio subió de 292 a 438 y el mejor individuo "
           "de 576 a 729, sin que nadie le explique al algoritmo qué es una x grande. "
           "La selección premia lo bueno, el cruce combina piezas y la mutación (acá no "
           "aplicada) evita que la población se estanque.",
           w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e17_genetico.png"))


def e18_bloques():
    """Planificacion STRIPS en el mundo de los bloques."""
    d = Diagram(6.3, 4.45)
    d.title("Ejemplo · Planificación STRIPS en el mundo de los bloques",
            y=4.28, fs=10.2)

    def torre(x0, y0, pila, tit, col):
        if tit.strip():
            d.caption(x0 + 0.33, y0 + len(pila) * 0.36 + 0.30, tit, fs=7.4,
                      weight="bold", color="#2C1758")
        for i, b in enumerate(pila):
            d.node(f"{tit}{b}", x0 + 0.33, y0 + i * 0.36 + 0.18, b, w=0.52,
                   kind=col, fs=8.4, weight="bold", minh=0.30)
        d.ax.plot([x0 - 0.10, x0 + 0.76], [y0, y0], color="#5A6076", lw=1.6,
                  zorder=2)

    torre(0.42, 2.55, ["C", "A"], "INICIAL", "unit")
    torre(1.32, 2.55, ["B"], " ", "unit")
    torre(2.60, 2.55, ["C", "B", "A"], "OBJETIVO", "good")

    d.caption(2.28, 2.95, "→", fs=15.0, color="#4C2A85", weight="bold")

    d.node("est", 5.02, 3.55,
           "Estado inicial (conjunción de literales positivos):\n"
           "Sobre(A, C) ∧ SobreMesa(C) ∧ SobreMesa(B) ∧ Libre(A) ∧ Libre(B)",
           w=2.30, kind="topic", fs=6.9)
    d.node("obj", 5.02, 2.78,
           "Objetivo (estado parcialmente especificado):\nSobre(A, B) ∧ Sobre(B, C)",
           w=2.30, kind="good", fs=6.9)

    d.node("acc", 3.15, 1.95,
           "ESQUEMA DE ACCIÓN   Mover(b, x, y)\n"
           "PRECOND:  Sobre(b, x) ∧ Libre(b) ∧ Libre(y)\n"
           "EFECTO:  Sobre(b, y) ∧ Libre(x)  ∧  ¬Sobre(b, x) ∧ ¬Libre(y)",
           w=5.9, kind="root", fs=7.3)

    plan = ["1 · Mover(A, C, Mesa)\nahora C queda libre",
            "2 · Mover(B, Mesa, C)\nB va sobre C",
            "3 · Mover(A, Mesa, B)\nse cumple el objetivo"]
    for i, t in enumerate(plan):
        d.node(f"p{i}", 1.20 + i * 1.95, 1.15, t, w=1.75, kind="unit", fs=7.0,
               minh=0.42)
        if i:
            d.edge(f"p{i-1}", f"p{i}")

    d.node("hip", 3.15, 0.44,
           "Hipótesis STRIPS: todo literal que la acción no menciona queda igual. Por eso "
           "no hace falta decir «B sigue sobre la mesa» después de mover A — así se evita "
           "el problema del marco.", w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e18_bloques.png"))


def e19_experto_reglas():
    """Encadenamiento hacia adelante en un sistema experto minimo."""
    d = Diagram(6.3, 4.85)
    d.title("Ejemplo · Un sistema experto de tres reglas: el auto no arranca",
            y=4.68, fs=10.2)

    d.caption(1.58, 4.28, "BASE DE CONOCIMIENTO", fs=7.6, weight="bold",
              color="#2C1758")
    reglas = ["R1: SI luces_apagadas ∧ arranque_mudo\n      ENTONCES batería_descargada",
              "R2: SI batería_descargada\n      ENTONCES no_arranca",
              "R3: SI tanque_vacío\n      ENTONCES no_arranca"]
    for i, r in enumerate(reglas):
        d.node(f"r{i}", 1.58, 3.90 - i * 0.58, r, w=2.90, kind="unit", fs=7.0,
               minh=0.44)

    d.caption(4.78, 4.28, "HECHOS OBSERVADOS", fs=7.6, weight="bold",
              color="#2C1758")
    d.node("h1", 4.78, 3.90, "luces_apagadas", w=2.20, kind="accent", fs=7.2,
           minh=0.28)
    d.node("h2", 4.78, 3.46, "arranque_mudo", w=2.20, kind="accent", fs=7.2,
           minh=0.28)

    d.caption(3.15, 2.28, "ENCADENAMIENTO HACIA ADELANTE — de los datos a la conclusión",
              fs=8.0, weight="bold", color="#2C1758")
    d.node("t1", 1.05, 1.80, "Hechos\niniciales", w=1.20, kind="topic", fs=7.0,
           minh=0.42)
    d.node("t2", 2.72, 1.80, "R1 se dispara\n→ batería_descargada", w=1.85,
           kind="unit", fs=7.0, minh=0.42)
    d.node("t3", 4.90, 1.80, "R2 se dispara\n→ no_arranca  ✓", w=1.85,
           kind="good", fs=7.0, minh=0.42)
    d.edge("t1", "t2")
    d.edge("t2", "t3")

    d.node("atr", 3.15, 1.04,
           "HACIA ATRÁS, el mismo caso se recorre al revés: se parte de la hipótesis "
           "«no_arranca», se ve qué reglas la concluyen (R2 y R3), y se pregunta por sus "
           "premisas. R3 se descarta al comprobar que hay nafta; R2 obliga a probar "
           "«batería_descargada», que R1 confirma.",
           w=5.9, kind="note", fs=7.3)
    d.node("cmp", 3.15, 0.36,
           "Hacia adelante conviene cuando hay pocos datos y muchas conclusiones "
           "posibles; hacia atrás, cuando hay una hipótesis concreta que confirmar — como "
           "un diagnóstico.", w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e19_experto_reglas.png"))


def e20_resolucion():
    """Refutacion por resolucion: paso a paso hasta la clausula vacia."""
    d = Diagram(6.3, 4.15)
    d.title("Ejemplo · Demostrar por resolución que «Juan se moja»",
            y=3.98, fs=10.2)

    d.node("bc", 3.15, 3.55,
           "BASE DE CONOCIMIENTO:  «Si llueve y Juan sale, Juan se moja».  Llueve.  "
           "Juan sale.\nQUEREMOS PROBAR:  Moja",
           w=5.9, kind="root", fs=7.4)

    d.node("f1", 1.20, 2.86, "(Ll ∧ S) ⇒ M\nen FNC:  ¬Ll ∨ ¬S ∨ M", w=2.10,
           kind="unit", fs=7.2, minh=0.44)
    d.node("f2", 3.35, 2.86, "Ll", w=0.70, kind="unit", fs=7.6, weight="bold",
           minh=0.44)
    d.node("f3", 4.35, 2.86, "S", w=0.70, kind="unit", fs=7.6, weight="bold",
           minh=0.44)
    d.node("f4", 5.55, 2.86, "¬M\n(negación de\nlo que se prueba)", w=1.35,
           kind="bad", fs=7.0, minh=0.44)

    d.node("p1", 1.95, 2.02, "¬Ll ∨ ¬S ∨ M   con   Ll\n→   ¬S ∨ M", w=2.60,
           kind="topic", fs=7.2, minh=0.42)
    d.node("p2", 4.55, 2.02, "¬S ∨ M   con   S\n→   M", w=2.20, kind="topic",
           fs=7.2, minh=0.42)
    d.node("p3", 3.15, 1.28, "M   con   ¬M   →   □   (cláusula vacía)", w=3.60,
           kind="good", fs=7.6, weight="bold", minh=0.42)
    d.edge("f1", "p1")
    d.edge("p1", "p2")
    d.edge("p2", "p3")
    d.edge("f4", "p3")

    d.node("txt", 3.15, 0.64,
           "La resolución es una REFUTACIÓN: no se demuestra M directamente, se agrega ¬M "
           "y se busca una contradicción. Llegar a la cláusula vacía significa que el "
           "conjunto es insatisfacible, y por lo tanto la base de conocimiento implica M.",
           w=5.9, kind="accent", fs=7.3)
    d.caption(3.15, 0.16,
              "Todo tiene que estar antes en forma normal conjuntiva: una conjunción de "
              "disyunciones de literales. Por eso el primer paso siempre es convertir "
              "«⇒» en «¬ ∨».", fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e20_resolucion.png"))


if __name__ == "__main__":
    for f in (e11_espacio_estados, e12_produccion, e13_arbol_busqueda, e14_astar,
              e15_8puzzle, e16_colinas, e17_genetico, e18_bloques,
              e19_experto_reglas, e20_resolucion):
        print(f())
