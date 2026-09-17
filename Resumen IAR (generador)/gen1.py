# -*- coding: utf-8 -*-
import os
from dlib import Diagram

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")
CX = 3.15
W = 5.4


def d00_mapa_general():
    d = Diagram(6.3, 7.75)
    d.node("root", CX, 7.42,
           "INTELIGENCIA ARTIFICIAL  ·  IAR (UTN FRC)  ·  Plan 2023, 6 unidades",
           w=W, kind="root", fs=9.0, weight="bold")

    d.node("u1", CX, 6.62,
           "UNIDAD 1 · Inteligencia artificial y agentes inteligentes\n"
           "Definición, objetivos y alcances · fundamentos · historia\n"
           "Enfoques · tipos de problema · estado del arte\n"
           "Agente racional · REAS · ambientes · estructura",
           w=W, kind="unit", fs=8.0)
    d.node("u2", CX, 5.50,
           "UNIDAD 2 · Aprendizaje automático  (28 hs)\n"
           "Reconocimiento de patrones · sensado · características\n"
           "Regresión lineal, logística y polinomial · SVM\n"
           "Redes neuronales artificiales y aprendizaje profundo",
           w=W, kind="unit", fs=8.0)
    d.node("u3", CX, 4.32,
           "UNIDAD 3 · Razonamiento en ambientes deterministas 1  (24 hs)\n"
           "Espacios problema · sistemas de producción · control\n"
           "Búsqueda no informada, informada y local · planificación\n"
           "Metaheurísticas · algoritmos genéticos",
           w=W, kind="unit", fs=8.0)
    d.node("u4", CX, 3.20,
           "UNIDAD 4 · Razonamiento en ambientes deterministas 2  (16 hs)\n"
           "Sistemas expertos: tipos de problema, dominio, componentes\n"
           "Lógica proposicional y de predicados · forma clausal\n"
           "Método de resolución",
           w=W, kind="unit", fs=8.0)
    d.node("u5", CX, 2.10,
           "UNIDAD 5 · Razonamiento bajo incertidumbre  (12 hs)\n"
           "Manejo del conocimiento incierto · probabilidad condicional\n"
           "Regla de Bayes · redes de creencia\n"
           "Modelos ocultos de Markov",
           w=W, kind="unit", fs=8.0)
    d.node("u6", CX, 1.02,
           "UNIDAD 6 · Procesamiento del lenguaje natural  (12 hs)\n"
           "Modelos de lenguaje · gramática · análisis gramatical\n"
           "Gramáticas aumentadas · word embeddings\n"
           "RNN y LSTM · secuencia-a-secuencia · Transformers",
           w=W, kind="unit", fs=8.0)

    d.edge("root", "u1")
    # Las etiquetas van corridas a la derecha para no tapar la linea de la flecha.
    d.edge("u1", "u2", "el agente puede aprender de los datos", lab_dx=1.55)
    d.edge("u2", "u3", "…o buscar en un espacio de estados", lab_dx=1.55)
    d.edge("u3", "u4", "…o representar lo que sabe y razonar", lab_dx=1.55)
    d.edge("u4", "u5", "…pero el conocimiento rara vez es cierto", lab_dx=1.55)
    d.edge("u5", "u6", "todo junto, aplicado al lenguaje humano", lab_dx=1.55)

    d.caption(3.15, 0.30,
              "Las seis unidades responden siempre a la misma pregunta —cómo decide un "
              "agente—; lo que cambia es qué información tiene y qué garantías puede dar. "
              "La Unidad 6 cierra el círculo: usa gramáticas (Unidad 4), probabilidad "
              "(Unidad 5) y redes profundas (Unidad 2) sobre un mismo problema.",
              fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d00_mapa_general.png"))


def d01_agente():
    d = Diagram(6.3, 3.45)
    d.title("El agente y su entorno de trabajo (REAS)", y=3.28)

    d.node("amb", 3.15, 1.72, "", w=5.95, kind="note", minh=2.30)
    d.caption(0.32, 2.72, "AMBIENTE", fs=8.2, ha="left",
              color="#5A6076", weight="bold")

    d.node("sens", 1.30, 2.18, "Sensores\n(percepciones)", w=1.5,
           kind="accent", fs=8.2)
    d.node("prog", 3.15, 1.60,
           "Programa del agente\nsecuencia de percepciones → acción",
           w=2.45, kind="unit", fs=8.2, weight="bold")
    d.node("act", 5.00, 2.18, "Actuadores\n(acciones)", w=1.5,
           kind="accent", fs=8.2)
    d.node("rend", 3.15, 0.82,
           "Medida de rendimiento: define qué es «lo correcto»",
           w=3.5, kind="good", fs=8.2)

    d.edge("sens", "prog", "percibe", fs=7.2, lab_dx=-0.30)
    d.edge("prog", "act", "actúa", fs=7.2, lab_dx=0.30)
    d.edge("rend", "prog", color="#3E8E5A")

    d.caption(3.15, 0.22,
              "Agente racional: para cada secuencia de percepciones emprende la acción "
              "que maximiza su medida de rendimiento, según la evidencia percibida y el "
              "conocimiento que tiene almacenado.", fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d01_agente.png"))


def d02_tipos_agente():
    d = Diagram(6.3, 2.85)
    d.title("Los cinco tipos de programa de agente, de menos a más capaz", y=2.70)

    xs = [0.75, 1.95, 3.15, 4.35, 5.55]
    labs = [
        ("Reactivo\nsimple", "reglas condición-acción sobre la percepción actual"),
        ("Reactivo con\nmodelo", "estado interno: cómo evoluciona el mundo"),
        ("Basado en\nobjetivos", "evalúa estados futuros contra una meta"),
        ("Basado en\nutilidad", "utilidad: resuelve metas en conflicto"),
        ("Que\naprende", "crítica + elemento de aprendizaje + generador de problemas"),
    ]
    kinds = ["topic", "topic", "topic", "topic", "unit"]
    for i, ((t, sub), k) in enumerate(zip(labs, kinds)):
        d.node(f"n{i}", xs[i], 2.10, t, w=1.02, kind=k, fs=8.2,
               weight="bold", minh=0.56)
        d.caption(xs[i], 1.46, sub, fs=7.0, maxw=1.08)
    for i in range(4):
        d.edge(f"n{i}", f"n{i+1}")

    d.caption(3.15, 0.50,
              "Cada tipo agrega lo que le faltaba al anterior: el reactivo simple sólo "
              "sirve si el entorno es totalmente observable; el modelo interno resuelve la "
              "observabilidad parcial; los objetivos permiten anticipar; la utilidad "
              "pondera metas en conflicto y probabilidad de éxito; y el que aprende "
              "mejora su propio desempeño con la experiencia.", fs=7.4, maxw=5.95)
    return d.save(os.path.join(OUT, "d02_tipos_agente.png"))


if __name__ == "__main__":
    for f in (d00_mapa_general, d01_agente, d02_tipos_agente):
        print(f())
