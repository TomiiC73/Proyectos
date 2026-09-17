# -*- coding: utf-8 -*-
"""Diagramas agregados para alinear el resumen con la modalidad academica 2026:
regresiones (U2), sistemas expertos (U4), modelos ocultos de Markov (U5) y
procesamiento del lenguaje natural (U6)."""
import os
from dlib import Diagram

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


def d14_regresion():
    """Las tres regresiones del temario y que las separa."""
    d = Diagram(6.3, 4.55)
    d.title("Las tres regresiones del temario: qué cambia entre una y otra",
            y=4.38, fs=10.5)

    d.node("root", 3.15, 3.92,
           "Modelo lineal en los parámetros:  h(x) = w · x  = w₀ + w₁x₁ + … + wₙxₙ",
           w=5.9, kind="root", fs=8.4)

    d.node("lin", 1.12, 3.05,
           "REGRESIÓN LINEAL\nsalida continua\nh(x) = w · x",
           w=1.90, kind="unit", fs=7.8, minh=0.72)
    d.node("log", 3.15, 3.05,
           "REGRESIÓN LOGÍSTICA\nsalida en (0, 1)\nh(x) = 1 / (1 + e⁻ʷ˙ˣ)",
           w=1.90, kind="unit", fs=7.8, minh=0.72)
    d.node("pol", 5.18, 3.05,
           "REGRESIÓN POLINOMIAL\nse expande la entrada\nx → (x, x², x³, …)",
           w=1.90, kind="unit", fs=7.8, minh=0.72)
    d.edge("root", "lin")
    d.edge("root", "log")
    d.edge("root", "pol")

    d.node("lin2", 1.12, 2.10,
           "Para predecir un número.\nSe ajusta minimizando el\nerror cuadrático (MSE).",
           w=1.90, kind="topic", fs=7.4)
    d.node("log2", 3.15, 2.10,
           "Para clasificar. La salida\nse lee como probabilidad\nde pertenecer a la clase 1.",
           w=1.90, kind="topic", fs=7.4)
    d.node("pol2", 5.18, 2.10,
           "Para fronteras curvas.\nSigue siendo lineal en w:\nse resuelve igual.",
           w=1.90, kind="topic", fs=7.4)
    d.edge("lin", "lin2")
    d.edge("log", "log2")
    d.edge("pol", "pol2")

    d.node("sig", 3.15, 1.24,
           "El umbral duro (escalón) no es derivable en 0; la función logística "
           "(sigmoide) es su versión «blanda» y sí lo es → permite descenso por gradiente",
           w=5.9, kind="accent", fs=7.6)
    d.edge("log2", "sig")

    d.node("flex", 1.55, 0.45, "Subir el grado del polinomio\nbaja el sesgo…",
           w=2.75, kind="good", fs=7.4)
    d.node("over", 4.72, 0.45, "…pero sube la varianza:\nreaparece el sobreajuste",
           w=2.75, kind="bad", fs=7.4)
    d.edge("flex", "over")
    return d.save(os.path.join(OUT, "d14_regresion.png"))


def d11_expertos():
    """Anatomia de un sistema experto."""
    d = Diagram(6.3, 5.05)
    d.title("Sistema experto: qué lo compone y de dónde sale cada parte",
            y=4.88, fs=10.5)

    d.node("exp", 0.95, 4.28, "EXPERTO\nDEL DOMINIO", w=1.55, kind="accent",
           fs=7.8, weight="bold")
    d.node("ing", 3.15, 4.28, "INGENIERO DEL\nCONOCIMIENTO", w=1.75,
           kind="accent", fs=7.8, weight="bold")
    d.node("lib", 5.35, 4.28, "BIBLIOGRAFÍA\nY CASOS", w=1.55, kind="accent",
           fs=7.8, weight="bold")
    d.edge("exp", "ing", "entrevistas")
    d.edge("lib", "ing", "extracción")

    d.node("adq", 3.15, 3.42,
           "ADQUISICIÓN DEL CONOCIMIENTO\nidentificar la tarea · recopilar · elegir el "
           "vocabulario (ontología) · codificar axiomas · depurar",
           w=5.9, kind="root", fs=7.8)
    d.edge("ing", "adq")

    d.band(0.15, 1.32, 6.15, 2.92, "EL SISTEMA EXPERTO PROPIAMENTE DICHO")
    d.node("bc", 1.45, 2.42,
           "BASE DE CONOCIMIENTO\nreglas condición-acción\ny hechos del dominio",
           w=2.30, kind="unit", fs=7.6)
    d.node("mot", 4.55, 2.42,
           "MOTOR DE INFERENCIA\nencadenamiento hacia\nadelante o hacia atrás",
           w=2.30, kind="unit", fs=7.6)
    d.edge("bc", "mot")

    d.node("mem", 1.45, 1.70, "MEMORIA DE TRABAJO\nhechos del caso actual",
           w=2.30, kind="topic", fs=7.6)
    d.node("exl", 4.55, 1.70, "EXPLICACIÓN\npor qué concluyó eso",
           w=2.30, kind="topic", fs=7.6)
    d.edge("bc", "mem")
    d.edge("mot", "exl")

    d.node("hist", 3.15, 0.80,
           "DENDRAL (1971): primer sistema de conocimiento intenso · MYCIN: ~450 reglas, "
           "diagnóstico de infecciones sanguíneas, factores de certeza · R1/XCON (DEC, "
           "1982): miles de reglas, 40 millones de dólares de ahorro al año",
           w=5.9, kind="note", fs=7.4)

    d.caption(3.15, 0.20,
              "La lección de DENDRAL fue separar limpiamente el conocimiento (reglas) del "
              "razonamiento (motor). Su límite: el sistema no aprende de datos — todo lo "
              "que sabe hay que ponérselo a mano, y mantenerlo cuesta.",
              fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d11_expertos.png"))


def d12_markov():
    """Modelo oculto de Markov: estados ocultos, evidencia y tareas de inferencia."""
    d = Diagram(6.3, 4.95)
    d.title("Modelo oculto de Markov: el estado no se ve, la evidencia sí",
            y=4.78, fs=10.5)

    xs = [1.32, 2.62, 3.92, 5.22]
    et = ["Lluvia₀", "Lluvia₁", "Lluvia₂", "Lluvia₃"]
    ev = ["—", "Paraguas₁", "Paraguas₂", "Paraguas₃"]
    for i, x in enumerate(xs):
        d.node(f"x{i}", x, 3.92, et[i], w=1.06, kind="unit", fs=8.0,
               weight="bold", minh=0.40)
        if i:
            d.node(f"e{i}", x, 3.06, ev[i], w=1.06, kind="good", fs=8.0,
                   minh=0.40)
            d.edge(f"x{i}", f"e{i}")
    for i in range(3):
        d.edge(f"x{i}", f"x{i+1}")

    d.caption(0.20, 3.92, "OCULTO", fs=7.4, ha="left", weight="bold",
              color="#4C2A85")
    d.caption(0.20, 3.06, "OBSERVADO", fs=7.4, ha="left", weight="bold",
              color="#3E8E5A")

    d.node("tr", 1.65, 2.34,
           "MODELO DE TRANSICIÓN  P(Xₜ | Xₜ₋₁)\nhipótesis de Markov de primer orden:\n"
           "el estado actual sólo depende del anterior",
           w=2.95, kind="topic", fs=7.4)
    d.node("se", 4.65, 2.34,
           "MODELO SENSOR  P(Eₜ | Xₜ)\nla evidencia sólo depende\ndel estado actual",
           w=2.75, kind="topic", fs=7.4)

    d.node("mat", 3.15, 1.58,
           "Con una sola variable de estado discreta todo se vuelve matricial:  "
           "T = [[0,7  0,3],[0,3  0,7]]   y   Oₜ diagonal con P(eₜ | Xₜ = i)",
           w=5.9, kind="accent", fs=7.5)

    ys = 0.90
    tareas = [("FILTRADO\nP(Xₜ | e₁:ₜ)\n«¿llueve hoy?»", 0.86, 1.28),
              ("PREDICCIÓN\nP(Xₜ₊ₖ | e₁:ₜ)\n«¿lloverá en 3 días?»", 2.22, 1.28),
              ("SUAVIZADO\nP(Xₖ | e₁:ₜ), k < t\n«¿llovió el miércoles?»", 3.58, 1.28),
              ("EXPLICACIÓN MÁS PROBABLE\nargmax P(x₁:ₜ | e₁:ₜ)\nalgoritmo de Viterbi",
               5.15, 1.75)]
    for i, (t, x, w) in enumerate(tareas):
        d.node(f"t{i}", x, ys, t, w=w, kind="unit", fs=7.0, minh=0.68)

    d.caption(3.15, 0.24,
              "Las cuatro tareas usan el mismo algoritmo hacia delante-atrás: O(S²t) en "
              "tiempo. Viterbi cambia la sumatoria por una maximización y guarda punteros "
              "al mejor predecesor, por eso su espacio también es lineal en t.",
              fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d12_markov.png"))


def d13_pln():
    """Los dos enfoques del PLN que pide el temario."""
    d = Diagram(6.3, 5.75)
    d.title("Procesamiento del lenguaje natural: dos enfoques, un mismo problema",
            y=5.58, fs=10.5)

    d.node("root", 3.15, 5.08,
           "El lenguaje natural es ambiguo, vago y sin frontera nítida entre lo "
           "gramatical y lo agramatical → no se puede tratar como la lógica de primer "
           "orden; hay que decir qué tan probable es cada cadena",
           w=5.9, kind="root", fs=8.0)

    d.band(0.15, 2.62, 3.05, 4.62, "ENFOQUE CLÁSICO")
    d.node("bow", 1.58, 4.24, "Bolsa de palabras\n(naive Bayes)", w=2.60,
           kind="unit", fs=7.5)
    d.node("ng", 1.58, 3.66, "Modelos de n-gramas\n+ suavizado", w=2.60,
           kind="unit", fs=7.5)
    d.node("gr", 1.58, 3.10, "Gramática PCFG\ny léxico", w=2.60, kind="unit",
           fs=7.5)
    d.edge("bow", "ng")
    d.edge("ng", "gr")

    d.band(3.25, 2.62, 6.15, 4.62, "APORTES DEL APRENDIZAJE PROFUNDO")
    d.node("emb", 4.70, 4.24, "Word embeddings\nvectores densos", w=2.60,
           kind="unit", fs=7.5)
    d.node("rnn", 4.70, 3.66, "RNN y LSTM\ncontexto secuencial", w=2.60,
           kind="unit", fs=7.5)
    d.node("trf", 4.70, 3.10, "Seq2seq + atención\n→ Transformer", w=2.60,
           kind="unit", fs=7.5)
    d.edge("emb", "rnn")
    d.edge("rnn", "trf")

    d.node("par", 1.58, 2.16, "Análisis gramatical (parsing)\nCYK · chart parser",
           w=2.60, kind="topic", fs=7.4)
    d.edge("gr", "par")
    d.node("aug", 1.58, 1.44, "Gramáticas aumentadas\ncaso, número, palabra núcleo",
           w=2.60, kind="topic", fs=7.4)
    d.edge("par", "aug")

    d.node("aten", 4.70, 2.16,
           "Autoatención: consulta, clave\ny valor · atención multicabeza",
           w=2.60, kind="topic", fs=7.4)
    d.edge("trf", "aten")
    d.node("pos", 4.70, 1.44,
           "Embedding posicional: sin él\nel modelo ignora el orden",
           w=2.60, kind="topic", fs=7.4)
    d.edge("aten", "pos")

    d.node("cmp", 3.15, 0.72,
           "Ambos hacen lo mismo: asignar probabilidad a cadenas. El clásico lo hace "
           "contando secuencias vistas; el profundo, aprendiendo representaciones que "
           "generalizan a secuencias nunca vistas.",
           w=5.9, kind="accent", fs=7.5)

    d.caption(3.15, 0.20,
              "Los n-gramas tienen O(vⁿ) parámetros y una ventana fija; la RNN tiene O(1) "
              "y contexto en principio ilimitado; el Transformer además paraleliza, "
              "porque la autoatención no arrastra dependencia secuencial.",
              fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d13_pln.png"))


if __name__ == "__main__":
    for f in (d14_regresion, d11_expertos, d12_markov, d13_pln):
        print(f())
