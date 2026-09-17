# -*- coding: utf-8 -*-
import os
from dlib import Diagram

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


def d06_busqueda():
    d = Diagram(6.3, 5.80)
    d.title("Estrategias de búsqueda: qué garantiza cada una", y=5.63, fs=10.5)

    d.node("root", 3.15, 5.14,
           "Búsqueda en el espacio de estados: nodo, frontera, expandir.\n"
           "Se juzga con cuatro criterios: completitud · optimalidad · "
           "complejidad en tiempo · complejidad en espacio",
           w=5.7, kind="root", fs=8.0)

    d.band(0.10, 0.96, 3.08, 4.68)
    d.band(3.22, 1.82, 6.20, 4.68)

    d.node("bl", 1.59, 4.38,
           "NO INFORMADA (a ciegas)\nsólo usa la definición del problema",
           w=2.80, kind="unit", fs=7.8, weight="bold")
    d.node("br", 4.71, 4.38,
           "INFORMADA (heurística)\nusa h(n): costo estimado hasta el objetivo",
           w=2.80, kind="unit", fs=7.8, weight="bold")
    d.edge("root", "bl")
    d.edge("root", "br")

    izq = [
        ("Primero en anchura", "completa; óptima si los costos son iguales; O(b^(d+1)) en tiempo y en espacio"),
        ("Costo uniforme", "expande el nodo de menor g(n); óptima con cualquier función de costo"),
        ("Primero en profundidad", "sólo O(b·m) de memoria, pero no es completa ni óptima"),
        ("Profundidad iterativa", "memoria de la primera y garantías de la segunda: la preferida si no se conoce d"),
        ("Bidireccional", "busca desde los dos extremos: O(b^(d/2)), pero hay que guardar un árbol entero"),
    ]
    ys = [3.78, 3.14, 2.50, 1.86, 1.22]
    for i, ((t, s), y) in enumerate(zip(izq, ys)):
        d.node(f"i{i}", 1.59, y, t + "\n" + s, w=2.80, kind="topic", fs=7.3)

    d.node("r0", 4.71, 3.78,
           "Voraz primero el mejor\nf(n) = h(n): va directo al objetivo, pero no es "
           "óptima ni completa", w=2.80, kind="topic", fs=7.3)
    d.node("r1", 4.71, 2.98,
           "A*\nf(n) = g(n) + h(n): completa y óptima si h es admisible (nunca "
           "sobrestima) o consistente en búsqueda en grafos; es óptimamente "
           "eficiente", w=2.80, kind="good", fs=7.3)
    d.node("r2", 4.71, 2.16,
           "Memoria acotada: A*PI y BRPM\nmisma optimalidad con espacio lineal, "
           "a costa de regenerar nodos", w=2.80, kind="topic", fs=7.3)

    d.caption(4.71, 1.34,
              "De dónde sale una buena h: del costo óptimo de un problema relajado. "
              "En el 8-puzle, h₁ = fichas mal colocadas y h₂ = distancia de Manhattan; "
              "h₂ domina a h₁ y expande menos nodos.", fs=7.2, maxw=2.85)

    d.caption(3.15, 0.48,
              "La búsqueda no informada sólo distingue objetivo de no-objetivo; la "
              "informada agrega conocimiento del dominio. Ese conocimiento es lo que "
              "convierte un problema exponencial en uno tratable, aunque A* siga "
              "quedándose sin memoria antes que sin tiempo.", fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d06_busqueda.png"))


def d07_metaheuristicas():
    d = Diagram(6.3, 4.75)
    d.title("Metaheurísticas: el equilibrio entre explorar y explotar", y=4.58,
            fs=10.5)

    d.node("root", 3.15, 4.10,
           "Metaheurística: familia de técnicas de optimización aproximada que dan "
           "soluciones aceptables en tiempo razonable. «Meta» = metodología general "
           "que guía el diseño de heurísticas concretas.",
           w=5.7, kind="root", fs=8.0)

    d.node("div", 1.62, 3.30,
           "DIVERSIFICACIÓN (exploración)\nvisitar regiones no exploradas para no "
           "encerrarse en una zona", w=2.75, kind="accent", fs=7.5)
    d.node("int", 4.68, 3.30,
           "INTENSIFICACIÓN (explotación)\nprofundizar en las regiones prometedoras "
           "ya encontradas", w=2.75, kind="accent", fs=7.5)
    d.edge("div", "int", style="<|-|>", color="#C9962A")

    ejes = [
        (1.62, 2.52, "Inspiradas en la naturaleza vs. no",
         "genéticos, hormigas, enjambre, recocido simulado"),
        (4.68, 2.52, "Con memoria vs. sin memoria",
         "tabú recuerda y prohíbe · local, GRASP y recocido no"),
        (1.62, 1.84, "Deterministas vs. estocásticas",
         "el mismo punto de partida ¿lleva siempre al mismo final?"),
        (4.68, 1.84, "Basadas en población vs. en una solución",
         "genéticos y PSO exploran · local y recocido explotan"),
        (3.15, 1.16, "Iterativas vs. voraces (greedy)",
         "partir de una solución completa y transformarla, o construirla variable "
         "por variable"),
    ]
    for i, (x, y, t, s) in enumerate(ejes):
        d.node(f"e{i}", x, y, t + "\n" + s, w=2.75, kind="topic", fs=7.3)

    d.node("warn", 3.15, 0.50,
           "CUÁNDO NO USARLAS: si el problema tiene un algoritmo exacto de tiempo "
           "polinómico (camino más corto, árbol de expansión mínimo), aplicar una "
           "metaheurística es un error frecuente. Primero analizar la complejidad.",
           w=5.7, kind="bad", fs=7.5)
    return d.save(os.path.join(OUT, "d07_metaheuristicas.png"))


def d08_logica():
    d = Diagram(6.3, 4.95)
    d.title("De la base de conocimiento a la conclusión", y=4.78, fs=10.5)

    d.node("root", 3.15, 4.32,
           "Agente basado en conocimiento: DECIR (agregar sentencias) y PREGUNTAR "
           "(consultar) sobre una base de conocimiento BC",
           w=5.7, kind="root", fs=8.0)

    d.node("sin", 1.60, 3.58,
           "SINTAXIS\nqué sentencias están bien formadas", w=2.80,
           kind="topic", fs=7.6)
    d.node("sem", 4.70, 3.58,
           "SEMÁNTICA\nen qué modelos (mundos posibles) es verdadera cada sentencia",
           w=2.80, kind="topic", fs=7.6)
    d.edge("root", "sin")
    d.edge("root", "sem")

    d.node("imp", 3.15, 2.82,
           "IMPLICACIÓN  BC ⊨ α : en todo modelo donde la BC es verdadera, α "
           "también lo es. Es la aguja que está en el pajar.",
           w=5.2, kind="unit", fs=7.8)
    d.edge("sin", "imp")
    d.edge("sem", "imp")

    d.node("inf", 3.15, 2.10,
           "INFERENCIA  BC ⊢ᵢ α : el algoritmo i encuentra la aguja. Se le pide que "
           "sea SÓLIDO (sólo deriva lo implicado) y COMPLETO (deriva todo lo implicado).",
           w=5.2, kind="unit", fs=7.8)
    d.edge("imp", "inf")

    d.node("m1", 1.20, 1.16,
           "Comprobación de modelos\nenumera todos los modelos (tabla de verdad): "
           "sólido y completo, pero explota exponencialmente",
           w=1.85, kind="topic", fs=7.2)
    d.node("m2", 3.15, 1.16,
           "Encadenamiento\nhacia adelante (dirigido por los datos) o hacia atrás "
           "(dirigido por el objetivo): tiempo lineal, pero sólo con cláusulas de Horn",
           w=1.85, kind="topic", fs=7.2)
    d.node("m3", 5.10, 1.16,
           "Resolución\nexige forma normal conjuntiva; refuta la negación de la "
           "consulta hasta la cláusula vacía. Completa para toda la lógica proposicional",
           w=1.85, kind="good", fs=7.2)
    d.edge("inf", "m1")
    d.edge("inf", "m2")
    d.edge("inf", "m3")

    d.caption(3.15, 0.24,
              "La lógica clásica es monótona: agregar sentencias a la BC puede aumentar "
              "el conjunto de conclusiones, nunca invalidar una ya obtenida. Eso permite "
              "aplicar una regla en cuanto sus premisas están, sin revisar el resto.",
              fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d08_logica.png"))


def d09_planificacion():
    d = Diagram(6.3, 4.15)
    d.title("Planificación clásica: representar para poder descomponer", y=3.98,
            fs=10.5)

    d.node("root", 3.15, 3.48,
           "PROBLEMA DE PLANIFICACIÓN (lenguaje STRIPS)\n"
           "Estado = conjunción de literales positivos · Objetivo = estado "
           "parcialmente especificado · Acción = nombre + PRECOND + EFECTO",
           w=5.7, kind="root", fs=8.0)

    d.node("a1", 1.20, 2.50,
           "Progresión\nbúsqueda hacia delante desde el estado inicial; factor de "
           "ramificación enorme", w=1.85, kind="topic", fs=7.2)
    d.node("a2", 3.15, 2.50,
           "Regresión\nhacia atrás desde el objetivo; sólo considera acciones "
           "relevantes, ramifica mucho menos", w=1.85, kind="topic", fs=7.2)
    d.node("a3", 5.10, 2.50,
           "Orden parcial (POP)\nmínimo compromiso: resuelve subobjetivos por "
           "separado y los combina", w=1.85, kind="topic", fs=7.2)
    d.edge("root", "a1")
    d.edge("root", "a2")
    d.edge("root", "a3")

    d.node("gp", 3.15, 1.36,
           "GRAFO DE PLANIFICACIÓN — niveles alternados de literales (S₀, S₁, …) y "
           "acciones (A₀, A₁, …), con enlaces de exclusión mutua. Es optimista "
           "(ignora parte de las interacciones negativas), así que el nivel en que "
           "aparece un literal es una cota inferior de la dificultad: sirve como "
           "heurística. GRAPHPLAN extrae la solución directamente del grafo.",
           w=5.7, kind="unit", fs=7.6)
    d.edge("a1", "gp")
    d.edge("a2", "gp")
    d.edge("a3", "gp")

    d.caption(3.15, 0.44,
              "Lo que gana la planificación frente a la búsqueda clásica: al ver la "
              "estructura lógica del objetivo puede descartar acciones irrelevantes, "
              "derivar sola una heurística (cuántas conjunciones faltan) y descomponer "
              "el problema en subproblemas casi independientes.", fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d09_planificacion.png"))


def d10_incertidumbre():
    d = Diagram(6.3, 5.35)
    d.title("Razonamiento bajo incertidumbre: dos respuestas distintas", y=5.18,
            fs=10.5)

    d.node("root", 3.15, 4.75,
           "El agente no tiene acceso a toda la verdad sobre su ambiente",
           w=5.7, kind="root", fs=8.4)

    d.node("fz", 1.55, 4.02,
           "LÓGICA DIFUSA\nlos eventos son verdaderos o falsos EN CIERTO GRADO; "
           "las reglas usan adjetivos que modifican ese grado de certeza",
           w=2.75, kind="accent", fs=7.4)
    d.node("pb", 4.75, 4.02,
           "PROBABILIDAD\nlos eventos son verdaderos o falsos CON CIERTA "
           "PROBABILIDAD; el grado es de creencia, no de verdad",
           w=2.75, kind="accent", fs=7.4)
    d.edge("root", "fz")
    d.edge("root", "pb")

    ch = [
        (3.30, "P(a) a priori · P(a|b) = P(a∧b)/P(b) condicional · regla del "
               "producto P(a∧b) = P(a|b)·P(b)", "topic"),
        (2.67, "REGLA DE BAYES   P(b|a) = P(a|b)·P(b) / P(a)\ninvierte el sentido "
               "del condicional: de P(síntoma|enfermedad) a P(enfermedad|síntoma)", "good"),
        (2.00, "Distribución conjunta completa: contiene toda la información, pero "
               "su tamaño crece exponencialmente y es inmanejable", "bad"),
        (1.33, "INDEPENDENCIA CONDICIONAL → RED BAYESIANA\ngrafo acíclico dirigido "
               "+ una tabla P(Xᵢ | Padres(Xᵢ)) por nodo", "unit"),
        (0.63, "Inferencia por enumeración:  P(X|e) = α · Σ P(X, e, y)\nsumando sobre "
               "las variables ocultas y ; α = 1/P(e) normaliza el resultado", "good"),
    ]
    prev = "pb"
    for i, (y, t, k) in enumerate(ch):
        d.node(f"c{i}", 3.15, y, t, w=5.2, kind=k, fs=7.5)
        d.edge(prev, f"c{i}")
        prev = f"c{i}"

    return d.save(os.path.join(OUT, "d10_incertidumbre.png"))


if __name__ == "__main__":
    for f in (d06_busqueda, d07_metaheuristicas, d08_logica,
              d09_planificacion, d10_incertidumbre):
        print(f())
