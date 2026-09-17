# -*- coding: utf-8 -*-
"""Diagramas de los EJEMPLOS concretos de las Unidades 5 y 6."""
import os
import numpy as np
from dlib import Diagram

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


def e21_bayes():
    """Regla de Bayes con numeros: la trampa de la baja prevalencia."""
    d = Diagram(6.3, 3.65)
    d.title("Ejemplo · El test da positivo: ¿cuál es la probabilidad de estar enfermo?",
            y=3.48, fs=10.2)

    d.node("dat", 3.15, 3.00,
           "1 de cada 1.000 personas tiene la enfermedad:  P(enf) = 0,001\n"
           "El test detecta al 99 % de los enfermos:  P(+ | enf) = 0,99\n"
           "Y da positivo al 5 % de los sanos:  P(+ | sano) = 0,05",
           w=5.9, kind="root", fs=7.5)

    d.node("b", 3.15, 2.28,
           "P(enf | +)  =  P(+ | enf) · P(enf)  /  P(+)",
           w=4.20, kind="accent", fs=8.4, minh=0.36)

    d.node("d1", 1.62, 1.68,
           "P(+) = 0,99·0,001 + 0,05·0,999\n= 0,00099 + 0,04995 = 0,05094",
           w=2.90, kind="topic", fs=7.2, minh=0.42)
    d.node("d2", 4.68, 1.68,
           "P(enf | +) = 0,00099 / 0,05094\n≈ 0,019   →   sólo 1,9 %",
           w=2.90, kind="good", fs=7.2, minh=0.42)
    d.edge("d1", "d2")

    d.caption(3.15, 1.16, "SOBRE 100.000 PERSONAS", fs=8.0, weight="bold",
              color="#2C1758")
    casos = [("100 enfermos", "topic"), ("99 dan positivo", "good"),
             ("99.900 sanos", "topic"), ("4.995 dan positivo", "bad")]
    for i, (t, k) in enumerate(casos):
        d.node(f"c{i}", 0.95 + i * 1.47, 0.82, t, w=1.30, kind=k, fs=7.0,
               minh=0.28)

    d.node("txt", 3.15, 0.32,
           "De los 5.094 positivos, sólo 99 son enfermos de verdad. La intuición falla "
           "porque ignora la probabilidad a priori: como los sanos son muchísimos más, "
           "aun un 5 % de falsos positivos produce más alarmas falsas que verdaderas.",
           w=5.9, kind="accent", fs=7.3)
    return d.save(os.path.join(OUT, "e21_bayes.png"))


def e22_red_bayesiana():
    """Red bayesiana de la alarma, con tablas y una consulta resuelta."""
    d = Diagram(6.3, 4.35)
    d.title("Ejemplo · La red de la alarma: cuatro tablas en lugar de una gigante",
            y=4.18, fs=10.2)

    d.node("rob", 1.55, 3.62, "Robo\nP = 0,001", w=1.35, kind="unit", fs=7.4,
           minh=0.44)
    d.node("ter", 4.05, 3.62, "Terremoto\nP = 0,002", w=1.35, kind="unit",
           fs=7.4, minh=0.44)
    d.node("ala", 2.80, 2.78, "Alarma", w=1.35, kind="root", fs=8.0,
           weight="bold", minh=0.40)
    d.node("juan", 1.55, 1.94, "Juan llama", w=1.35, kind="good", fs=7.4,
           minh=0.36)
    d.node("mar", 4.05, 1.94, "María llama", w=1.35, kind="good", fs=7.4,
           minh=0.36)
    d.edge("rob", "ala")
    d.edge("ter", "ala")
    d.edge("ala", "juan")
    d.edge("ala", "mar")

    d.node("t1", 5.42, 2.78,
           "P(Alarma | R, T)\nR∧T: 0,95\nR∧¬T: 0,94\n¬R∧T: 0,29\n¬R∧¬T: 0,001",
           w=1.55, kind="topic", fs=6.8)
    d.node("t2", 0.90, 1.30, "P(J | A) = 0,90\nP(J | ¬A) = 0,05", w=1.60,
           kind="topic", fs=6.8, minh=0.36)
    d.node("t3", 4.60, 1.30, "P(M | A) = 0,70\nP(M | ¬A) = 0,01", w=1.60,
           kind="topic", fs=6.8, minh=0.36)

    d.node("cta", 3.15, 0.78,
           "Con 5 variables booleanas, la distribución conjunta completa necesitaría "
           "2⁵ − 1 = 31 números. La red necesita sólo 10, porque cada variable depende "
           "únicamente de sus padres: Juan y María no se «escuchan» entre sí, sólo "
           "reaccionan a la alarma.",
           w=5.9, kind="accent", fs=7.3)
    d.caption(3.15, 0.22,
              "Ejemplo de consulta: si Juan y María llaman los dos, la probabilidad de "
              "que haya habido un robo sube de 0,001 a ≈ 0,28 — alto comparado con el "
              "punto de partida, pero todavía lejos de la certeza.",
              fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e22_red_bayesiana.png"))


def e23_hmm_paso():
    """Un paso de filtrado en el mundo del paraguas, con numeros."""
    d = Diagram(6.3, 3.55)
    d.title("Ejemplo · Un paso de filtrado en el mundo del paraguas",
            y=3.38, fs=10.2)

    d.node("mod", 3.15, 2.92,
           "P(Lluvia₀) = 0,5   ·   P(Lluviaₜ | Lluviaₜ₋₁) = 0,7   ·   "
           "P(Lluviaₜ | ¬Lluviaₜ₋₁) = 0,3\nP(Paraguas | Lluvia) = 0,9   ·   "
           "P(Paraguas | ¬Lluvia) = 0,2",
           w=5.9, kind="root", fs=7.4)

    pasos = [
        ("PASO 1 · PREDECIR", "Sin mirar nada todavía:\n"
         "P(Ll₁) = 0,7·0,5 + 0,3·0,5 = 0,5", "topic"),
        ("PASO 2 · OBSERVAR", "El director llega con paraguas.\n"
         "Se pesa con P(U₁ | Ll₁):\n0,9·0,5 = 0,45   y   0,2·0,5 = 0,10", "accent"),
        ("PASO 3 · NORMALIZAR", "0,45 / (0,45 + 0,10) = 0,818\n"
         "P(Lluvia₁ | paraguas) ≈ 0,82", "good"),
    ]
    for i, (t, s, k) in enumerate(pasos):
        x = 1.12 + i * 2.03
        d.node(f"t{i}", x, 2.20, t, w=1.85, kind=k, fs=7.4, weight="bold",
               minh=0.30)
        d.node(f"s{i}", x, 1.62, s, w=1.85, kind="note", fs=6.9, minh=0.50)
        if i:
            d.edge(f"t{i-1}", f"t{i}")

    d.node("d2", 3.15, 1.02,
           "SEGUNDO DÍA, otra vez con paraguas: predicción 0,7·0,82 + 0,3·0,18 = 0,627; "
           "se pesa 0,9·0,627 = 0,565 contra 0,2·0,373 = 0,075; normalizando queda "
           "P(Lluvia₂) ≈ 0,88. La creencia se refuerza con cada observación coherente.",
           w=5.9, kind="unit", fs=7.3)

    d.caption(3.15, 0.30,
              "Es la misma cuenta siempre: predecir con el modelo de transición, pesar "
              "con el modelo sensor, normalizar. Eso es la estimación recursiva — no hace "
              "falta guardar toda la historia, alcanza con la creencia del paso anterior.",
              fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e23_hmm_paso.png"))


def e24_difusa():
    """Grado de verdad frente a grado de creencia."""
    d = Diagram(6.3, 2.85)
    d.title("Ejemplo · «Probablemente llueve» no es lo mismo que «el día está caluroso»",
            y=2.68, fs=10.2)

    d.node("p", 1.62, 2.02,
           "GRADO DE CREENCIA (probabilidad)\n«Hay 70 % de probabilidad de que llueva»\n"
           "El evento es verdadero o falso; lo que es\nparcial es mi información sobre él.",
           w=2.90, kind="unit", fs=7.2)
    d.node("f", 4.68, 2.02,
           "GRADO DE VERDAD (lógica difusa)\n«El día está caluroso en grado 0,7»\n"
           "No falta información: el propio predicado\n«caluroso» no tiene un límite nítido.",
           w=2.90, kind="accent", fs=7.2)

    d.node("t", 3.15, 1.08,
           "Si mañana llueve, el primer enunciado pasa a ser verdadero o falso y el 70 % "
           "desaparece. En cambio, un día de 28 °C sigue siendo «caluroso en grado 0,7» "
           "aunque no haya ninguna incertidumbre sobre la temperatura: el grado es parte "
           "del significado del adjetivo, no de mi ignorancia.",
           w=5.9, kind="root", fs=7.3)

    d.node("gap", 3.15, 0.36,
           "Hasta acá llega lo que afirma el material de la cátedra. El desarrollo "
           "completo (conjuntos difusos, funciones de pertenencia, reglas SI-ENTONCES, "
           "fusificación y defusificación) requiere el apunte de Destéfanis, que no está "
           "en el material convertido — ver Apéndice A.",
           w=5.9, kind="bad", fs=7.2)
    return d.save(os.path.join(OUT, "e24_difusa.png"))


def e25_ngramas():
    """Modelo de bigramas contado sobre un corpus minimo."""
    d = Diagram(6.3, 3.70)
    d.title("Ejemplo · Un modelo de bigramas contado sobre tres oraciones",
            y=3.53, fs=10.2)

    d.node("cor", 3.15, 3.02,
           "CORPUS:   «el gato duerme»   ·   «el gato come»   ·   «el perro duerme»",
           w=5.9, kind="root", fs=7.6)

    d.caption(1.55, 2.58, "CONTEOS DE BIGRAMAS", fs=7.6, weight="bold",
              color="#2C1758")
    bi = [("el gato", "2"), ("el perro", "1"), ("gato duerme", "1"),
          ("gato come", "1"), ("perro duerme", "1")]
    for i, (b, c) in enumerate(bi):
        y = 2.24 - i * 0.30
        d.node(f"b{i}", 1.20, y, b, w=1.55, kind="topic", fs=7.0, minh=0.25)
        d.node(f"c{i}", 2.28, y, c, w=0.42, kind="accent", fs=7.0, minh=0.25)

    d.caption(4.60, 2.58, "PROBABILIDADES ESTIMADAS", fs=7.6, weight="bold",
              color="#2C1758")
    pr = [("P(gato | el) = 2/3 ≈ 0,67", "good"),
          ("P(perro | el) = 1/3 ≈ 0,33", "good"),
          ("P(duerme | gato) = 1/2 = 0,50", "topic"),
          ("P(come | gato) = 1/2 = 0,50", "topic"),
          ("P(come | perro) = 0/1 = 0  ✗", "bad")]
    for i, (t, k) in enumerate(pr):
        d.node(f"p{i}", 4.60, 2.24 - i * 0.30, t, w=2.85, kind=k, fs=7.0,
               minh=0.25)

    d.node("sua", 3.15, 0.62,
           "El último caso es el problema: «el perro come» es una oración perfectamente "
           "válida, pero el modelo le asigna probabilidad CERO sólo porque ese bigrama no "
           "apareció. El suavizado reserva una parte de la masa de probabilidad para los "
           "n-gramas nunca vistos — la versión más simple suma 1 a todos los conteos.",
           w=5.9, kind="accent", fs=7.3)
    d.caption(3.15, 0.14,
              "Con la oración completa: P(«el gato duerme») = P(el)·P(gato|el)·"
              "P(duerme|gato) ≈ 1 · 0,67 · 0,50 = 0,33.", fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e25_ngramas.png"))


def e26_arbol_sintactico():
    """Arbol de analisis sintactico de una oracion corta."""
    d = Diagram(6.3, 3.85)
    d.title("Ejemplo · El árbol de análisis de «el gato come pescado»",
            y=3.68, fs=10.2)

    niveles = {
        "O": (3.15, 3.12, "O", "root"),
        "SN": (1.60, 2.46, "SN", "unit"),
        "SV": (4.35, 2.46, "SV", "unit"),
        "Det": (0.95, 1.80, "Det", "topic"),
        "N1": (2.25, 1.80, "N", "topic"),
        "V": (3.65, 1.80, "V", "topic"),
        "N2": (5.05, 1.80, "N", "topic"),
    }
    for k, (x, y, t, kind) in niveles.items():
        d.node(k, x, y, t, w=0.58, kind=kind, fs=8.0, weight="bold", minh=0.34,
               radius=0.14)
    for a, b in (("O", "SN"), ("O", "SV"), ("SN", "Det"), ("SN", "N1"),
                 ("SV", "V"), ("SV", "N2")):
        d.edge(a, b, style="-", lw=0.9, color="#8A8FA8")

    palabras = [("el", 0.95, "Det"), ("gato", 2.25, "N1"),
                ("come", 3.65, "V"), ("pescado", 5.05, "N2")]
    for w, x, padre in palabras:
        d.node(f"w{w}", x, 1.18, w, w=0.86, kind="good", fs=7.6, minh=0.30)
        d.edge(padre, f"w{w}", style="-", lw=0.9, color="#8A8FA8")

    d.node("gr", 3.15, 0.66,
           "REGLAS USADAS:   O → SN SV   ·   SN → Det N   ·   SV → V N   ·   "
           "Det → «el»   ·   N → «gato» | «pescado»   ·   V → «come»",
           w=5.9, kind="accent", fs=7.3)
    d.caption(3.15, 0.18,
              "Analizar («parsear») es justamente esto: buscar un árbol cuyas hojas sean "
              "las palabras de la oración. En una gramática probabilística cada regla "
              "lleva además una probabilidad, y el análisis elige el árbol más probable.",
              fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e26_arbol_sintactico.png"))


def e27_embeddings():
    """Word embeddings: similitud y aritmetica de vectores."""
    d = Diagram(6.3, 3.55)
    d.title("Ejemplo · Palabras como vectores: la resta que codifica «capital de»",
            y=3.38, fs=10.2)
    ax = d.ax

    m = d.panel(0.72, 0.98, 2.95, 2.00, xlim=(0, 10), ylim=(0, 10),
                frame="box", fs=6.8)
    puntos = {"Atenas": (2.0, 2.6), "Grecia": (2.9, 6.0),
              "Oslo": (6.2, 3.0), "Noruega": (7.1, 6.4)}
    for w, (u, v) in puntos.items():
        p = m(u, v)
        ax.scatter([p[0]], [p[1]], s=26, c="#4C2A85", zorder=6, linewidths=0)
        d.caption(p[0], p[1] + 0.16, w, fs=7.0, weight="bold", color="#2C1758")
    for a, b in (("Atenas", "Grecia"), ("Oslo", "Noruega")):
        p1, p2 = m(*puntos[a]), m(*puntos[b])
        ax.annotate("", xy=p2, xytext=p1, zorder=5,
                    arrowprops=dict(arrowstyle="-|>", color="#C9962A", lw=1.4))
    d.caption(m(2.2, 4.4)[0] - 0.22, m(2.2, 4.4)[1], "mismo\nvector", fs=6.6,
              color="#C9962A", weight="bold")

    d.node("op", 4.95, 2.72,
           "«Atenas es a Grecia\ncomo Oslo es a …»",
           w=2.35, kind="unit", fs=7.6, minh=0.44)
    d.node("v", 4.95, 2.02,
           "D = C + (B − A)\n= Oslo + (Grecia − Atenas)",
           w=2.35, kind="accent", fs=7.4, minh=0.44)
    d.node("r", 4.95, 1.36,
           "El vector resultante cae\nmás cerca de «Noruega»\nque de cualquier otra palabra",
           w=2.35, kind="good", fs=7.2, minh=0.44)
    d.edge("op", "v")
    d.edge("v", "r")

    d.node("txt", 3.15, 0.62,
           "Cada palabra es un vector denso de unos cientos de dimensiones, aprendido de "
           "los textos: «se conoce una palabra por la compañía que mantiene». Ninguna "
           "dimensión suelta significa algo, pero las distancias y las direcciones sí.",
           w=5.9, kind="accent", fs=7.3)
    d.caption(3.15, 0.16,
              "Nada garantiza que un embedding capture una relación dada: son útiles "
              "porque funcionan bien como entrada de otras tareas, no porque resuelvan "
              "analogías.", fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e27_embeddings.png"))


def e28_atencion():
    """Matriz de atencion en una traduccion corta."""
    d = Diagram(6.3, 4.45)
    d.title("Ejemplo · Qué mira el traductor al generar cada palabra",
            y=4.28, fs=10.2)

    src = ["The", "front", "door", "is", "red"]
    tgt = ["La", "puerta", "de", "entrada", "es", "roja"]
    # Peso de atencion aproximado (fila = palabra generada, columna = fuente)
    W = [[0.8, 0.1, 0.1, 0.0, 0.0],
         [0.1, 0.1, 0.8, 0.0, 0.0],
         [0.0, 0.5, 0.4, 0.1, 0.0],
         [0.0, 0.8, 0.1, 0.1, 0.0],
         [0.0, 0.0, 0.1, 0.8, 0.1],
         [0.0, 0.0, 0.0, 0.1, 0.9]]

    cell = 0.34
    x0, y0 = 1.55, 1.45
    ax = d.ax
    for r in range(len(tgt)):
        for c in range(len(src)):
            v = W[r][c]
            cx = x0 + c * cell
            cy = y0 + (len(tgt) - 1 - r) * cell
            tono = int(255 - v * 165)
            ax.add_patch(__import__("matplotlib").patches.Rectangle(
                (cx, cy), cell, cell, fc=f"#{tono:02x}{tono:02x}"
                f"{min(255, tono + 40):02x}", ec="#D6CCEC", lw=0.5, zorder=3))
            if v >= 0.4:
                ax.text(cx + cell / 2, cy + cell / 2, f"{v:.1f}", ha="center",
                        va="center", fontsize=6.4, fontfamily="DejaVu Sans",
                        color="#FFFFFF" if v > 0.6 else "#1E2233", zorder=5)
    for c, w in enumerate(src):
        ax.text(x0 + c * cell + cell / 2, y0 + len(tgt) * cell + 0.10, w,
                ha="center", va="bottom", rotation=32, fontsize=6.8,
                fontfamily="DejaVu Sans", color="#2C1758", zorder=5)
    for r, w in enumerate(tgt):
        ax.text(x0 - 0.08, y0 + (len(tgt) - 1 - r) * cell + cell / 2, w,
                ha="right", va="center", fontsize=6.8, fontfamily="DejaVu Sans",
                color="#2C1758", zorder=5)
    d.caption(x0 + len(src) * cell / 2, y0 - 0.22, "palabras de la oración fuente",
              fs=6.8)

    d.node("q", 4.85, 3.50,
           "Al generar «puerta» el modelo\nmira sobre todo «door»; al generar\n"
           "«roja», sobre todo «red».", w=2.55, kind="unit", fs=7.2)
    d.node("w", 4.85, 2.74,
           "Sin atención, toda la oración\nfuente tenía que caber en un\núnico vector "
           "de estado.", w=2.55, kind="bad", fs=7.2)
    d.node("z", 4.85, 1.98,
           "Con atención, cada palabra\ngenerada arma su propio resumen\nponderado de la "
           "fuente.", w=2.55, kind="good", fs=7.2)
    d.edge("q", "w")
    d.edge("w", "z")

    d.node("txt", 3.15, 0.78,
           "Los pesos suman 1 en cada fila y NO se programan: salen de un softmax sobre "
           "los productos entre el estado del decodificador y cada estado del "
           "codificador. El Transformer lleva la idea un paso más: aplica la misma "
           "atención de la oración consigo misma (autoatención).",
           w=5.9, kind="accent", fs=7.3)
    d.caption(3.15, 0.18,
              "Notar el reordenamiento: «front door» son dos palabras en inglés y "
              "«puerta de entrada» son tres en español, en otro orden. La atención lo "
              "resuelve sin ninguna regla de alineación escrita a mano.",
              fs=7.2, maxw=6.0)
    return d.save(os.path.join(OUT, "e28_atencion.png"))


if __name__ == "__main__":
    for f in (e21_bayes, e22_red_bayesiana, e23_hmm_paso, e24_difusa,
              e25_ngramas, e26_arbol_sintactico, e27_embeddings, e28_atencion):
        print(f())
