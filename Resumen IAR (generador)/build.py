# -*- coding: utf-8 -*-
"""Arma el resumen completo de Inteligencia Artificial (IAR - UTN FRC) en .docx."""
import os
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor
from docbuild import (new_doc, add_toc, h, para, bullets, box, figure,
                      page_break, rule, footer_pagenum, add_rich, _fmt,
                      code, salida, MORADO, MORADO_OSC, GRIS)

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img")
OUT = r"C:\Users\Usuario\Desktop\Resumenes\IA\Resumen Integral - Inteligencia Artificial (IAR).docx"


def img(n):
    return os.path.join(IMG, n)


_FIG = [0]


def fig(nombre, epigrafe, width_in=6.30):
    """Inserta una figura numerándola sola, para no renumerar a mano."""
    _FIG[0] += 1
    figure(doc, img(nombre), _FIG[0], epigrafe, width_in=width_in)


def ejemplo(titulo, texto):
    """Caja de ejemplo, con el color de acento (ámbar) para distinguirla
    de las cajas de aclaración (moradas)."""
    return box(doc, titulo, texto, fill="FFF8E6", color="C9962A")


doc = new_doc()
footer_pagenum(doc)

# ===================================================================== PORTADA
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(90)
_fmt(p.add_run("INTELIGENCIA ARTIFICIAL"), bold=True, size=30, color=MORADO)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
_fmt(p.add_run("Resumen integral de la materia"), size=15, color=MORADO_OSC)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(30)
_fmt(p.add_run("Las 6 unidades del programa analítico · Plan 2023 · con mapas "
               "conceptuales"), size=11.5, color=GRIS)
rule(doc)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
_fmt(p.add_run("Universidad Tecnológica Nacional · Facultad Regional Córdoba\n"
               "Ingeniería en Sistemas de Información"), size=11, color=MORADO_OSC)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(40)
_fmt(p.add_run("Cátedra IAR"), size=10.5, color=GRIS)

box(doc, "Sobre qué está construido este resumen",
    "La estructura sigue el **programa analítico oficial** de la asignatura "
    "(__Planificación IAR 2026 – modalidad académica__, Plan 2023): seis unidades, con "
    "los contenidos y la carga horaria que fija ese documento.\n"
    "El contenido sale del material real de la cátedra convertido a texto en la carpeta "
    "__IA/PDFS EN .MD/__: el apunte de cátedra __Inteligencia Artificial – UTN FRC__ "
    "(Mario Alejandro García, versión del 07/11/2025), __Inteligencia artificial: un "
    "enfoque moderno__ de Russell y Norvig (2.ª edición, 2004), la 4.ª edición en "
    "inglés (2021) y las presentaciones teóricas de la cátedra. Cuando un tema del "
    "programa no está cubierto con profundidad por ese material, se lo dice "
    "explícitamente en lugar de rellenarlo (ver [[apA|Apéndice A]]).\n"
    "Cada concepto cierra con un **ejemplo concreto** en caja ámbar, y con su diagrama "
    "propio cuando verlo ayuda más que leerlo. Todos los diagramas fueron generados "
    "para este documento.\n"
    "En la Unidad 2, además, los ejemplos incluyen el **código real de los notebooks de "
    "Google Colab** de las clases prácticas (carpeta __IA/Collabs/__), con sus salidas "
    "tal como fueron ejecutadas — no reescrito ni sustituido por código genérico. El "
    "[[apA_notebooks|Apéndice A.4]] detalla qué notebook alimenta cada sección y hasta "
    "dónde llega esa cobertura.")

page_break(doc)

# ============================================================= CÓMO ESTÁ ARMADO
h(doc, 1, "Cómo está organizado este documento", "intro")
para(doc,
     "El orden de las unidades y los temas de cada una **no son una interpretación**: "
     "salen del punto 10, *Programa analítico*, de la planificación oficial de la "
     "asignatura a partir del ciclo lectivo 2026. Son seis unidades:")
bullets(doc, [
    "**Unidad 1 · Inteligencia artificial y agentes inteligentes** (4 hs) — definición, objetivos y alcances, fundamentos, historia, enfoques, tipos de problema del mundo real, estado del arte; agentes: comportamiento esperado, ambientes, estructura.",
    "**Unidad 2 · Aprendizaje automático** (28 hs) — reconocimiento de patrones (sensado, extracción de características, clasificación y regresión); aprendizaje supervisado: regresión lineal, logística y polinomial, redes neuronales artificiales y aprendizaje profundo, máquinas de vectores de soporte.",
    "**Unidad 3 · Razonamiento en ambientes deterministas 1** (24 hs) — problemas, espacios problema y búsqueda; sistemas de producción y estrategias de control; búsqueda no informada, informada y local; planificación; metaheurísticas y algoritmos genéticos.",
    "**Unidad 4 · Razonamiento en ambientes deterministas 2** (16 hs) — sistemas expertos (tipos de problema, características del dominio, componentes); lógica: representación del conocimiento, lógica proposicional y de predicados, conversión a forma clausal, método de resolución.",
    "**Unidad 5 · Razonamiento bajo incertidumbre** (12 hs) — manejo del conocimiento incierto; modelos bayesianos: probabilidad condicional, regla de Bayes, redes de creencia, modelos ocultos de Markov.",
    "**Unidad 6 · Procesamiento del lenguaje natural** (12 hs) — conceptos básicos; enfoque clásico (modelos de lenguaje, gramática, análisis gramatical, gramáticas aumentadas); aportes del aprendizaje profundo (word embeddings, redes recurrentes y LSTM, modelos secuencia-a-secuencia, Transformers).",
])
para(doc,
     "El apunte de cátedra usa una numeración de unidades **distinta** de la del "
     "programa: agrupa planificación con lógica y no llega a cubrir PLN. Cuando hay "
     "diferencia, **manda el programa analítico**, y este documento lo sigue. La "
     "correspondencia con los capítulos del apunte es esta:")
bullets(doc, [
    "Capítulos 2 y 3 del apunte (*Conceptos básicos* y *Agentes inteligentes*) → [[u1|Unidad 1]].",
    "Capítulo 4 (*Aprendizaje automático*) → [[u2|Unidad 2]].",
    "Capítulos 5 (*Búsqueda*), 7 (*Planificación*) y 9 (*Metaheurísticas*) → [[u3|Unidad 3]]. El apunte ubica la planificación junto a la lógica; el programa la pone acá, con la búsqueda.",
    "Capítulo 6 (*Agentes lógicos*) → [[u4|Unidad 4]], junto con los sistemas expertos, que el apunte no desarrolla como tema propio.",
    "Capítulos 8 (*Lógica difusa*) y 10 (*Modelos bayesianos*) → [[u5|Unidad 5]]. La lógica difusa **no figura en el programa analítico**, así que va al final de la unidad marcada como tema complementario.",
    "**Ningún capítulo del apunte cubre la Unidad 6.** Esa unidad está desarrollada sobre Russell y Norvig, capítulos 22-23 de la edición en español y 24-25 de la 4.ª edición en inglés, que es de donde el programa toma literalmente los títulos de sus temas.",
])
para(doc,
     "Dentro de cada unidad los temas van con **definición primero, desarrollo después "
     "y ejemplo concreto al final**. Los ejemplos están en cajas ámbar y son deliberadamente "
     "chicos: un tablero, cuatro filas de una tabla, dos cuentas hechas. Los conceptos "
     "que aparecen en más de una unidad llevan un enlace interno (en morado y subrayado): "
     "al hacerle clic, Word salta a la sección correspondiente. Por ejemplo, "
     "[[u3_4|Heurística y búsqueda informada]].")

rule(doc)
h(doc, 2, "Índice", "toc")
add_toc(doc)
page_break(doc)

# ================================================================ MAPA GENERAL
h(doc, 1, "Mapa general de la materia", "mapa")
para(doc,
     "Las seis unidades no son seis temas sueltos: son **seis respuestas a la misma "
     "pregunta**. Un agente tiene que elegir qué hacer, y lo que cambia de una unidad a "
     "otra es qué información tiene disponible y qué garantías puede dar sobre su "
     "elección.")
fig("d00_mapa_general.png",
    "Cómo se encadenan las seis unidades del programa analítico.")
bullets(doc, [
    "Si el agente **tiene datos etiquetados** y el problema es reconocer un patrón, aprende una función a partir de ellos: [[u2|Unidad 2]].",
    "Si **no hay datos pero sí un espacio de estados** bien definido, explora ese espacio y arma un plan: [[u3|Unidad 3]].",
    "Si puede **representar explícitamente lo que sabe** y el ambiente es determinista, razona con reglas y con lógica: [[u4|Unidad 4]].",
    "Si el conocimiento es **incierto**, necesita grados de creencia y probabilidad: [[u5|Unidad 5]].",
    "Y si el problema es el **lenguaje humano**, hacen falta las cuatro cosas a la vez: [[u6|Unidad 6]].",
])
para(doc,
     "La [[u1|Unidad 1]] es transversal a todas: define qué es un agente, cómo se mide "
     "su rendimiento y qué propiedades del entorno obligan a usar una técnica u otra. "
     "Las horas del programa también cuentan una historia: la Unidad 2 se lleva 28 de "
     "las 96 horas, más del doble que cualquier otra.")

page_break(doc)

# =================================================================== UNIDAD 1
h(doc, 1, "Unidad 1 · Inteligencia artificial y agentes inteligentes", "u1")
para(doc,
     "Cuatro horas de programa para fijar el vocabulario de toda la materia: qué se "
     "entiende por inteligencia artificial, de dónde viene, qué problemas le "
     "corresponden y qué es exactamente un agente.")

h(doc, 2, "1.1 Definición, objetivos y alcances", "u1_1")
para(doc,
     "La cátedra presenta las definiciones de IA cruzando **dos ejes**: si lo que se "
     "quiere reproducir son los *procesos mentales* o la *conducta*, y si el patrón de "
     "referencia es el *ser humano* o la *racionalidad*. De ahí salen dos nociones que "
     "conviene no confundir:")
bullets(doc, [
    "**Comportamiento inteligente**: capacidad de un sistema para resolver problemas y realizar tareas de manera efectiva, eficiente y adaptativa.",
    "**Comportamiento racional**: capacidad de un sistema para tomar decisiones que maximicen un objetivo o meta específica en función de la información disponible.",
])
para(doc,
     "El enfoque que terminó prevaleciendo en el campo es el del **agente racional**: "
     "aquel que actúa con el objetivo de alcanzar el mejor resultado. Por lo generalizado "
     "de este paradigma se lo llama **modelo estándar**. En pocas palabras, la IA se ha "
     "enfocado en el estudio y la construcción de agentes que *hagan lo correcto*, donde "
     "lo que cuenta como correcto es el objetivo definido al agente.")
ejemplo("Ejemplo · inteligente y racional no son sinónimos",
        "Un GPS tiene que llevarte de tu casa a la facultad. El objetivo que le "
        "definieron es **minimizar el tiempo de viaje**.\n"
        "Es **racional** si, con la información que tiene —el mapa, el tránsito "
        "reportado—, elige la ruta que maximiza ese objetivo. Notar que la racionalidad "
        "**se juzga contra la información disponible, no contra el resultado**: si elige "
        "bien y aun así aparece un corte imprevisto que lo demora, siguió siendo "
        "racional. Y al revés, acertar por casualidad no lo vuelve racional.\n"
        "Es **inteligente**, además, si se adapta: si recalcula cuando te desviás, si "
        "aprende que los martes a las 8 esa avenida está tapada, si funciona igual "
        "cuando el GPS pierde señal un rato.\n"
        "La diferencia se ve mejor cuando el objetivo está mal puesto. Si sólo le piden "
        "minimizar tiempo, la ruta racional puede meterte por una calle peligrosa a las "
        "3 de la mañana: **el agente es perfectamente racional respecto del objetivo que "
        "le dieron, y aun así hace algo que nadie quería**. Ése es exactamente el "
        "problema del modelo estándar que reaparece en [[u1_6|sección 1.8]].")
para(doc,
     "Sobre los **alcances**, conviene fijar qué queda adentro y qué no. La IA no es un "
     "algoritmo ni una tecnología puntual: es un **campo** que abarca desde tareas "
     "generales —razonar, percibir, aprender, usar el lenguaje— hasta tareas formales y "
     "especializadas ([[u1_tipos|sección 1.6]]). Y hay dos delimitaciones que suelen hacer "
     "falta:")
bullets(doc, [
    "**No todo sistema automático es IA.** Un programa de sueldos hace miles de cálculos por segundo y no es inteligente en ningún sentido útil: aplica reglas fijas que alguien escribió, sin percibir el entorno ni ajustar su comportamiento. Lo que define al agente es **percibir, decidir y actuar sobre un entorno** ([[u1_7|sección 1.9]]).",
    "**No toda IA es aprendizaje automático.** El aprendizaje automático es la [[u2|Unidad 2]] y hoy domina la práctica, pero las unidades 3 a 6 tratan búsqueda, lógica, planificación, razonamiento probabilístico y lenguaje — problemas de IA que en su mayoría **no se resuelven entrenando un modelo con datos**. Confundir las dos cosas es el error más común al entrar en la materia.",
])

h(doc, 2, "1.2 Los cuatro enfoques", "u1_enf")
para(doc,
     "Cruzando los dos ejes anteriores —procesos mentales frente a conducta, humano "
     "frente a racional— quedan **cuatro casilleros**, y a lo largo de la historia se "
     "siguieron los cuatro. Conviene tenerlos separados porque cada uno define un "
     "criterio de éxito distinto:")
bullets(doc, [
    "**Actuar como humano — la Prueba de Turing.** Propuesta por Alan Turing en 1950 como definición *operacional* de inteligencia: en vez de discutir qué cualidades hacen falta, la máquina aprueba si un evaluador humano no puede distinguir sus respuestas de las de una persona. Para superarla haría falta procesamiento de lenguaje natural, representación del conocimiento, razonamiento automático y aprendizaje automático; la **Prueba Global de Turing** agrega una señal de vídeo y objetos físicos, y con ellos visión computacional y robótica. Esas seis disciplinas cubren casi toda la IA.",
    "**Pensar como humano — el modelo cognitivo.** Requiere primero una teoría de cómo piensan las personas, obtenida por introspección o por experimentos psicológicos, y después expresarla como programa. Si las entradas y salidas *y los tiempos de reacción* se parecen a los humanos, hay evidencia de que los mecanismos coinciden. Es el terreno de la **ciencia cognitiva**.",
    "**Pensar racionalmente — las «leyes del pensamiento».** Arranca en los silogismos de Aristóteles: esquemas de argumentación que llevan siempre a conclusiones correctas si las premisas lo son. Deriva en la **lógica** ([[u4|Unidad 4]]) y en la tradición *logista*. Tiene dos obstáculos: pasar conocimiento informal a notación lógica es difícil cuando no se está seguro al 100 %, y hay una distancia enorme entre resolver un problema «en principio» y resolverlo en la práctica.",
    "**Actuar racionalmente — el agente racional.** Un **agente racional** es el que actúa para alcanzar el mejor resultado o, cuando hay incertidumbre, el mejor resultado esperado. Este enfoque es más general que el de las leyes del pensamiento (hacer inferencias correctas es sólo *uno* de los caminos para actuar bien) y más apto para el avance científico, porque el criterio de racionalidad está bien definido. Es el que adopta la materia.",
])
box(doc, "Por qué no se persigue la Prueba de Turing",
    "Los investigadores le dedicaron poco esfuerzo a evaluar sistemas con la Prueba de "
    "Turing, por considerar más importante estudiar los principios de la inteligencia "
    "que duplicar un ejemplar. La analogía del libro es directa: el vuelo artificial "
    "tuvo éxito cuando los hermanos Wright dejaron de imitar pájaros y entendieron la "
    "aerodinámica; los textos de ingeniería aeronáutica no definen su objetivo como "
    "construir «máquinas que vuelen como palomas de forma que puedan incluso confundir "
    "a otras palomas».\n"
    "Hay además un límite práctico: la **racionalidad perfecta** —hacer siempre lo "
    "correcto— no es alcanzable en entornos complejos, porque la demanda de cómputo es "
    "demasiado grande. De ahí el concepto de **racionalidad limitada**: actuar "
    "adecuadamente cuando no hay tiempo para hacer todos los cálculos deseables.")
ejemplo("Ejemplo · el mismo programa juzgado con los cuatro criterios",
        "Pensemos en un programa de ajedrez. **¿Actúa como humano?** No: juega mucho "
        "mejor que casi cualquier persona y comete errores que ningún humano cometería, "
        "así que fallaría una prueba de indistinguibilidad. **¿Piensa como humano?** "
        "Tampoco: evalúa millones de posiciones por segundo, mientras que un gran "
        "maestro considera unas pocas decenas. **¿Piensa racionalmente?** Sólo en "
        "parte: no deriva sus jugadas de un sistema de axiomas. **¿Actúa "
        "racionalmente?** Sí — y es el único de los cuatro criterios que aprueba. Por "
        "eso el programa es un buen sistema de IA aunque no se parezca en nada a un "
        "jugador humano.")

h(doc, 2, "1.3 De qué disciplinas viene la IA", "u1_2")
para(doc, "Las presentaciones de la cátedra listan los aportes concretos de cada campo:")
bullets(doc, [
    "**Filosofía** (desde el 400 a.C.): concebir la idea de que la mente funciona, de alguna manera, como una máquina que opera sobre conocimiento codificado en un lenguaje interno, y que el pensamiento sirve para seleccionar la acción a llevar a cabo.",
    "**Matemáticas**: herramientas para manipular tanto aseveraciones de certeza lógica como aseveraciones inciertas de tipo probabilista; y el terreno para entender el cálculo y el razonamiento con algoritmos.",
    "**Economía**: formalización del problema de la toma de decisiones para maximizar los resultados esperados.",
    "**Psicología**: la idea de que humanos y animales pueden considerarse máquinas de procesamiento de información.",
    "**Lingüística**: demostrar que el uso del lenguaje se ajusta a ese modelo.",
    "**Informática**: los artefactos que hicieron posible la aplicación de la IA — los programas de IA son extensos y no podrían funcionar sin los avances en velocidad y memoria.",
    "**Teoría de control**: el diseño de dispositivos que actúan de forma óptima con base en la retroalimentación que reciben del entorno. Inicialmente sus herramientas matemáticas eran bastante distintas de las de la IA, pero ambos campos se están acercando.",
])
box(doc, "Actualización que hace el apunte sobre las neurociencias",
    "El libro de 2004 comparaba la capacidad de cálculo de computadoras y cerebro y "
    "anticipaba, con optimismo, que hacia 2020 podrían igualarse. El apunte agrega dos "
    "aclaraciones: (1) los grandes avances de las últimas décadas se lograron gracias a "
    "las redes neuronales artificiales —las neurociencias fueron uno de los fundamentos "
    "más valiosos—, pero los modelos recientes de aprendizaje profundo son "
    "principalmente producto de la ingeniería, no de la biología; (2) citando al propio "
    "Russell: «incluso con una computadora de capacidad virtualmente ilimitada, todavía "
    "necesitamos nuevos avances conceptuales… sin la teoría correcta, las máquinas más "
    "rápidas solo dan la respuesta incorrecta más rápidamente».")

h(doc, 2, "1.4 Las dos corrientes históricas: simbólica y conexionista", "u1_3")
para(doc,
     "Desde los inicios de la IA se plantearon **dos enfoques diferentes**, uno por parte "
     "de los investigadores de Carnegie-Mellon y otro por los del MIT.")
bullets(doc, [
    "**Corriente conexionista — subsimbólica — ascendente** (Carnegie-Mellon): propuso modelos del comportamiento humano inspirados en el cerebro, con un enfoque cognitivo y subsimbólico. Su modelo «ascendente» parte del procesamiento básico de señales y avanza hacia niveles superiores de inteligencia, replicando pasos evolutivos. De aquí surgieron los modelos conexionistas, incluyendo las **redes neuronales** ([[u2_9|sección 2.10]]).",
    "**Corriente tradicional — simbólica — descendente** (MIT, liderada por Minsky y McCarthy): propuso desarrollar inteligencia artificial sin imitar estructuras biológicas, usando sentencias declarativas y reglas de inferencia. Fue dominante en los primeros 20 años. Sus modelos se mostraron ineficaces frente a problemas reales y complejos, porque la creciente cantidad de programación necesaria superaba la capacidad de los sistemas. Es la línea que desemboca en los **agentes lógicos** ([[u4|Unidad 4]]).",
])

h(doc, 2, "1.5 Historia de la inteligencia artificial", "u1_4")
para(doc,
     "El programa pide la **historia** como contenido propio de la unidad. Russell y "
     "Norvig la organizan en períodos, y el rasgo que conviene retener no son las fechas "
     "sino el **patrón**: dos veces el campo prometió más de lo que podía entregar y dos "
     "veces se quedó sin financiamiento. Los llamados **inviernos de la IA** no fueron "
     "fallas técnicas aisladas, sino la corrección de expectativas infladas.")
fig("e32_historia.png",
    "Los períodos de la historia de la IA, con los dos inviernos marcados en rojo "
    "y las etapas de recuperación en verde.")

h(doc, 3, "De la génesis al taller de Dartmouth (1943 – 1956)", "u1_4h1")
bullets(doc, [
    "**1943 — McCulloch y Pitts.** Reconocidos como los autores del primer trabajo de IA. Partieron de tres fuentes: la fisiología de las neuronas, el análisis formal de la lógica proposicional de Russell y Whitehead, y la teoría de la computación de Turing. Su neurona artificial está «activada» o «desactivada» según la estimulación de una cantidad suficiente de neuronas vecinas. Mostraron que **cualquier función computable puede calcularse con alguna red de neuronas interconectadas** y que todos los conectores lógicos se implementan con redes sencillas. Es el antecedente directo del perceptrón ([[u2_9a|sección 2.10]]).",
    "**1949 — Hebb.** Propuso una regla sencilla para modificar la intensidad de las conexiones entre neuronas. El **aprendizaje hebbiano** sigue vigente.",
    "**1950 — Turing.** En *Computing Machinery and Intelligence* introdujo la prueba de Turing, y de paso el aprendizaje automático, los algoritmos genéticos ([[u3_7|sección 3.9]]) y el aprendizaje por refuerzo. Ya entonces consideraba poco práctico programar la inteligencia a mano y sugería construir máquinas que aprendan.",
    "**1951 — Minsky y Edmonds** construyen el SNARC, el primer computador basado en una red neuronal: 3.000 válvulas de vacío simulando 40 neuronas.",
    "**1956 — el taller de Dartmouth.** McCarthy convence a Minsky, Shannon y Rochester de organizar un taller de dos meses con diez asistentes. Newell y Simon presentan el **Teórico Lógico**, capaz de demostrar buena parte de los teoremas del capítulo 2 de los *Principia Mathematica* —y en un caso con una demostración más corta que la original—. El taller no produjo ningún avance notable, pero fijó el nombre propuesto por McCarthy: **inteligencia artificial**.",
])
box(doc, "Por qué la IA tuvo que ser un campo separado",
    "Russell y Norvig se hacen la pregunta explícitamente: si la teoría de control, la "
    "investigación operativa y la teoría de la decisión persiguen objetivos similares, "
    "¿por qué hizo falta un campo nuevo? Dan dos razones. Primero, la IA abarcó desde el "
    "inicio la idea de **duplicar facultades humanas** como la creatividad, la automejora "
    "y el uso del lenguaje, que ninguno de los otros campos consideraba. Segundo, es el "
    "único de esos campos que es claramente una **rama de la informática**.")

h(doc, 3, "Entusiasmo, inviernos y sistemas expertos (1956 – 1988)", "u1_4h2")
bullets(doc, [
    "**Entusiasmo (1952 – 1969).** Los primeros sistemas funcionaban bien en problemas de juguete. Simon predijo en 1957 que en **diez años** una máquina sería campeona mundial de ajedrez y demostraría un teorema matemático importante. Se cumplió, pero en **cuarenta**.",
    "**Dosis de realidad (1966 – 1973) — primer invierno.** Los programas fallaban al pasar a problemas variados o difíciles, porque tenían poco o ningún conocimiento del dominio y obtenían resultados con manipulaciones sintácticas simples. En 1969 **Minsky y Papert** publican *Perceptrons*, que prueba que el perceptrón de una sola capa sólo representa conceptos **linealmente separables** y señala la falta de algoritmos de aprendizaje para redes multicapa: el resultado que explica el problema XOR ([[u2_9b|sección 2.10]]). En el Reino Unido el informe Lighthill corta el financiamiento.",
    "**Sistemas basados en conocimiento (1969 – 1979).** La lección del período anterior invertida: lo que resuelve no es el método general sino el **conocimiento del dominio**. DENDRAL y MYCIN ([[u4_exp|sección 4.1]]) son los casos testigo. En comprensión del lenguaje, SHRDLU funcionaba sólo porque estaba diseñado para el mundo de los bloques.",
    "**La IA se vuelve industria (1980 – 1988) — segundo invierno.** R1, el primer sistema experto comercial exitoso, le ahorraba a DEC unos **40 millones de dólares al año** en 1986; en 1988 DEC tenía 40 sistemas expertos distribuidos y Du Pont, 100 en uso y 500 en desarrollo. La industria pasó de unos pocos millones de dólares en 1980 a miles de millones en 1988, y enseguida llegó el **invierno de la IA**, que se llevó puestas a las empresas que no pudieron entregar lo prometido. Tanto se evitó el nombre que en el Reino Unido se acuñó una etiqueta nueva —*sistemas inteligentes basados en conocimiento*— porque la inteligencia artificial había sido oficialmente cancelada.",
    "**Regreso de las redes neuronales (desde 1986).** El trabajo siguió fuera de la informática: Hopfield (1982) analizó las redes con mecánica estadística y Rumelhart y Hinton estudiaron modelos de memoria. A mediados de los 80 **al menos cuatro grupos distintos reinventaron la retropropagación** ([[u2_9c|sección 2.10]]).",
])
box(doc, "Lo que hay que llevarse de la historia",
    "El eje de los dos inviernos es el mismo y se repite: **los métodos generales sin "
    "conocimiento del dominio fallan cuando el problema se agranda**. Primero fue la "
    "traducción automática por manipulación sintáctica, después los sistemas expertos "
    "cuyo costo de mantener las reglas crecía más rápido que su utilidad. Esa tensión es "
    "exactamente la que separa a las dos corrientes de la sección anterior, y es la razón "
    "de fondo por la que el aprendizaje automático —que extrae el conocimiento de los "
    "datos en vez de que alguien lo cargue a mano— terminó siendo el enfoque dominante.")

h(doc, 3, "Big data (2001 – presente)", "u1_4a")
para(doc,
     "Los avances en capacidad de cómputo y la World Wide Web facilitaron la creación de "
     "conjuntos de datos muy grandes. Esto llevó al desarrollo de algoritmos de "
     "aprendizaje diseñados especialmente para aprovecharlos. Dos hallazgos del apunte "
     "que conviene retener:")
bullets(doc, [
    "En el trabajo de Yarowsky (1995) sobre desambiguación del sentido de las palabras, los ejemplos **no estaban etiquetados**; sin embargo, con conjuntos suficientemente grandes los algoritmos alcanzaron más del **96 % de precisión**.",
    "Banko y Brill (2001) argumentaron que **aumentar el tamaño del conjunto de datos en dos o tres órdenes de magnitud supera cualquier mejora obtenida retocando el algoritmo**.",
    "Hays y Efros (2007), rellenando huecos en fotografías, encontraron que la técnica funcionaba mal con miles de imágenes pero cruzaba un umbral de calidad con millones. Poco después ImageNet provocó la revolución de la visión por computadora.",
    "El big data fue factor crucial en la victoria de **Watson** (IBM) en *Jeopardy!* en 2011.",
])
h(doc, 3, "Aprendizaje profundo (2011 – presente)", "u1_4b")
para(doc,
     "**Aprendizaje profundo** se refiere al aprendizaje automático que utiliza redes con "
     "múltiples capas de elementos computacionales simples y ajustables. Se experimentó "
     "con esas redes desde los años 70 y las convolucionales tuvieron cierto éxito "
     "reconociendo dígitos manuscritos en los 90, pero recién en 2011 despegaron: primero "
     "en reconocimiento de voz y luego en reconocimiento de objetos visuales. En la "
     "competencia **ImageNet 2012** el sistema del grupo de Geoffrey Hinton (Universidad "
     "de Toronto) mostró una mejora dramática sobre los sistemas previos, que dependían "
     "de extracción de características definidas a mano.")
para(doc,
     "El aprendizaje profundo depende fuertemente del hardware: mientras una CPU estándar "
     "realiza 10⁹–10¹⁰ operaciones por segundo, un algoritmo de deep learning sobre "
     "hardware especializado (GPU, TPU, FPGA) puede consumir entre 10¹⁴ y 10¹⁷, "
     "principalmente en forma de operaciones matriciales y vectoriales paralelizables. "
     "El detalle técnico está en [[u2_10|la sección de aprendizaje profundo]].")

h(doc, 2, "1.6 Tipos de problema del mundo real", "u1_tipos")
para(doc,
     "El programa pide distinguir qué problemas caen dentro del dominio de la IA. El "
     "criterio que usa la cátedra es el de la **solución algorítmica**:")
bullets(doc, [
    "Un problema tiene **solución algorítmica directa** cuando se conoce de antemano una secuencia de pasos que lo resuelve siempre y con el mismo resultado: ordenar una lista, calcular el sueldo neto a partir del bruto, liquidar el IVA de una factura. Ahí **no hace falta IA**, y usarla sería peor: más lento, más caro y menos confiable que el algoritmo exacto.",
    "Un problema pertenece al **dominio de la IA** cuando no se conoce ese algoritmo directo, y en cambio hay que *buscar* la respuesta, *aprenderla* de ejemplos, *inferirla* de conocimiento representado, o *estimarla* bajo incertidumbre.",
])
para(doc,
     "Las presentaciones de la cátedra recorren, como muestra del alcance real, los "
     "mismos campos de aplicación que el libro:")
bullets(doc, [
    "**Planificación autónoma**: el Agente Remoto de la NASA, pionero en planificación a bordo, gestionando operaciones espaciales sin intervención humana directa. Hoy misiones como Mars 2020 y Artemis integran razonamiento probabilístico y aprendizaje automático.",
    "**Juegos**: Deep Blue vence a Kasparov en 1997; después AlphaGo derrota a campeones de Go combinando redes neuronales y búsqueda; MuZero y OpenAI Five llegan a jugar sin conocer previamente las reglas.",
    "**Conducción autónoma**: ALVINN guiaba un vehículo con redes neuronales e imágenes de videocámara; hoy Tesla y Waymo integran visión por computador, aprendizaje profundo y sensores avanzados.",
    "**Diagnóstico**: en los años 90 los sistemas de diagnóstico probabilístico ya igualaban a médicos expertos; hoy herramientas como Med-PaLM o Watson Health analizan datos clínicos y justifican diagnósticos.",
    "**Planificación logística**: DART automatizó en 1991 la planificación logística de miles de vehículos, personal y rutas durante la Guerra del Golfo, reduciendo drásticamente el tiempo de planificación.",
    "**Robótica**: HipNav introdujo la cirugía asistida por robot con modelos 3D y navegación para implantes; hoy da Vinci y MAKO integran visión y navegación en tiempo real.",
    "**Lenguaje y resolución de problemas**: PROVERB resolvía crucigramas en 1999 con bases de datos y reglas de restricción; los modelos actuales interpretan metáforas y juegos de palabras ([[u6|Unidad 6]]).",
])
ejemplo("Ejemplo · tres problemas de una empresa, y cuál es de IA",
        "Una empresa de logística tiene tres pedidos. **(1) Calcular el total de cada "
        "factura con IVA.** Hay fórmula exacta: es un algoritmo directo, no es IA. "
        "**(2) Decidir en qué orden visitar 40 clientes minimizando kilómetros.** No "
        "hay algoritmo directo que lo resuelva en tiempo razonable, pero sí un espacio "
        "de soluciones bien definido y una función de costo: es un problema de "
        "[[u3|búsqueda y metaheurísticas]]. **(3) Predecir qué clientes van a cancelar "
        "el servicio el mes que viene.** No hay ni fórmula ni espacio de estados: hay "
        "datos históricos de clientes que se fueron y clientes que se quedaron. Es "
        "[[u2|aprendizaje automático]].\n"
        "El error caro es tratar el problema (1) con una red neuronal, o el (3) con "
        "reglas escritas a mano.")

h(doc, 2, "1.7 Estado del arte", "u1_5")
para(doc,
     "El estudio AI100 de Stanford y el AI Index dan indicadores concretos (datos de los "
     "informes 2018-2019 comparados con el año 2000, salvo indicación):")
bullets(doc, [
    "**Publicaciones**: los artículos de IA se multiplicaron por 20 entre 2010 y 2019, hasta unos 20.000 al año. La categoría más popular es el aprendizaje automático, seguida por visión por computadora y procesamiento del lenguaje natural.",
    "**Estudiantes**: la inscripción en cursos se multiplicó por cinco en EE.UU. y por dieciséis a nivel internacional respecto de 2010. La IA es la especialización más popular en Ciencias de la Computación.",
    "**Diversidad**: los profesores de IA en el mundo son aproximadamente 80 % hombres y 20 % mujeres; números similares para doctorandos y contrataciones en la industria.",
    "**Visión**: la tasa de error en detección de objetos (LSVRC) pasó del 28 % en 2010 al 2 % en 2017, superando el rendimiento humano. La respuesta a preguntas visuales abiertas (VQA) mejoró del 55 % al 68 % desde 2015, todavía por detrás del 83 % humano.",
    "**Velocidad**: el tiempo de entrenamiento para reconocimiento de imágenes se redujo en un factor de 100 en dos años; la energía de cómputo usada en las principales aplicaciones se duplica cada 3,4 meses.",
    "**Lenguaje**: el F1 en SQuAD pasó de 60 a 95 entre 2015 y 2019; en SQuAD 2, de 62 a 90 en un solo año. Ambos superan el nivel humano.",
])
para(doc,
     "Sobre cuándo la IA alcanzará nivel humano en una amplia variedad de tareas, Ford "
     "(2018) obtuvo de expertos un rango que va de 2029 a 2200, con media en 2099; en "
     "otra encuesta el 50 % lo situó hacia 2066. El propio texto advierte no tomar "
     "demasiado en serio esas predicciones: como muestra Tetlock, en predicción de "
     "eventos mundiales **los expertos no son mejores que los aficionados**.")

h(doc, 2, "1.8 Riesgos, ética y máquinas beneficiosas", "u1_6")
para(doc,
     "El apunte agrega una sección entera que no está en el libro de 2004. El problema de "
     "fondo es el **problema de alineación de valores**: los valores u objetivos "
     "introducidos en la máquina deben estar alineados con los de los seres humanos. En "
     "el laboratorio un objetivo mal especificado se arregla reiniciando; en un sistema "
     "desplegado en el mundo real no, y **cuanto más inteligente es el sistema, más "
     "negativas son las consecuencias**.")
bullets(doc, [
    "**Armas autónomas letales**: definidas por la ONU como armas que localizan, seleccionan y eliminan objetivos humanos sin intervención humana. La preocupación central es su *escalabilidad*: sin supervisión humana, un grupo pequeño puede desplegar un número arbitrariamente grande de armas.",
    "**Vigilancia y persuasión**: reconocimiento de voz, visión computarizada y comprensión del lenguaje permiten vigilancia masiva escalable; personalizando flujos de información en redes sociales, el comportamiento político puede modificarse.",
    "**Toma de decisiones sesgadas**: usar aprendizaje automático para evaluar libertad condicional o préstamos puede producir decisiones sesgadas por raza, género u otras categorías protegidas. A menudo **los propios datos reflejan prejuicios de la sociedad**.",
    "**Impacto en el empleo**: las máquinas hacen a las personas más productivas y a las empresas más rentables, pero **tienden a desplazar la riqueza del trabajo al capital**, agravando la desigualdad.",
    "**Aplicaciones críticas de seguridad**: ya hubo accidentes mortales que muestran la dificultad de la verificación formal y el análisis de riesgos en sistemas desarrollados con aprendizaje automático.",
    "**Ciberseguridad**: la IA sirve para defender, pero también potencia el malware; se han usado métodos de aprendizaje por refuerzo para crear herramientas de phishing y chantaje personalizado.",
])
box(doc, "Las dos metáforas del apunte",
    "**Problema del gorila**: hace siete millones de años un primate evolucionó en dos "
    "ramas, una hacia los gorilas y otra hacia los humanos. Hoy los gorilas no están "
    "contentos con la rama humana: esencialmente no tienen control sobre su futuro. Si "
    "ese fuera el resultado de crear IA superhumana, tal vez habría que dejar de "
    "trabajar en IA.\n"
    "**Problema del rey Midas**: Midas pidió que todo lo que tocara se convirtiera en "
    "oro, y se arrepintió al tocar su comida, su bebida y a su familia. Wiener lo dijo "
    "en términos técnicos: si usamos una máquina automática en cuya operación no podemos "
    "interferir, «mejor deberíamos estar bastante seguros de que el propósito puesto en "
    "la máquina es el que realmente deseamos».\n"
    "La salida propuesta son las **máquinas beneficiosas**: no poner un objetivo fijo, "
    "sino máquinas que persigan objetivos humanos **sabiendo que no saben con certeza "
    "cuáles son**. Una máquina que sabe que no conoce el objetivo completo tiene "
    "incentivo para actuar con cautela, pedir permiso, aprender de la observación y "
    "ceder al control humano.")

h(doc, 2, "1.9 Agentes inteligentes: comportamiento esperado", "u1_7")
para(doc,
     "**Un agente es cualquier cosa capaz de percibir su medioambiente con la ayuda de "
     "sensores y actuar en ese medio mediante actuadores.** Toma una decisión en un "
     "momento dado dependiendo de la **secuencia completa de percepciones** hasta ese "
     "instante.")
fig("d01_agente.png",
    "El agente, su entorno de trabajo y la medida de rendimiento.")
para(doc,
     "**Definición de agente racional:** un agente es racional si, en cada posible "
     "secuencia de percepciones, emprende aquella acción que **maximice su medida de "
     "rendimiento**, basándose en las evidencias aportadas por la secuencia de "
     "percepciones y en el conocimiento que el agente mantiene almacenado. Su "
     "racionalidad depende de cuatro factores:")
bullets(doc, [
    "La **medida de rendimiento**, que define el criterio de éxito.",
    "El **conocimiento del medio** que el agente ha acumulado.",
    "Las **acciones** que el agente puede llevar a cabo.",
    "La **secuencia de percepciones** del agente hasta ese momento.",
])
para(doc,
     "Un agente además debe ser **autónomo**: saber aprender a compensar el conocimiento "
     "incompleto o parcial inicial. Después de suficientes experiencias interactuando con "
     "el entorno, su comportamiento será efectivamente independiente del conocimiento "
     "inicial.")
para(doc,
     "Para especificar un agente se usa el acrónimo **REAS** — **R**endimiento, "
     "**E**ntorno, **A**ctuadores, **S**ensores. En el diseño de un agente, *el primer "
     "paso debe ser siempre especificar el entorno de trabajo de la forma más completa "
     "posible*. Estructuralmente, **agente = arquitectura + programa**: el programa debe "
     "ser apropiado para la arquitectura (si recomienda caminar, la arquitectura tiene "
     "que tener piernas).")

ejemplo("Ejemplo · la aspiradora, el agente determinista más chico posible",
        "Una aspiradora robot en una grilla de 2×2 celdas (A, B, C, D). Sus sensores le "
        "dicen **dos cosas y nada más**: en qué celda está y si esa celda está sucia. "
        "Sus acciones son cinco: aspirar, arriba, abajo, izquierda, derecha.\n"
        "Con eso alcanza para escribir la **función del agente completa**: una tabla de "
        "ocho filas, una por cada percepción posible. Ante la misma percepción hace "
        "siempre lo mismo — no hay azar, no hay empates, no hay nada que decidir en "
        "tiempo de ejecución. Eso es exactamente lo que significa que el agente sea "
        "**determinista**.\n"
        "La figura siguiente muestra el mundo, el REAS y la tabla entera. Vale la pena "
        "mirarla con cuidado porque este mismo ejemplo reaparece en la "
        "[[u3|Unidad 3]] como espacio de estados y en la [[u3_prod|Unidad 3, sistemas "
        "de producción]] escrito como reglas.")
fig("e01_aspiradora.png",
    "El mundo de la aspiradora, su especificación REAS y su función de agente completa.")

h(doc, 2, "1.10 Ambientes: propiedades del entorno de trabajo", "u1_8")
para(doc,
     "Estas propiedades no son un catálogo decorativo: **determinan qué técnica de las "
     "unidades siguientes es aplicable**.")
bullets(doc, [
    "**Totalmente vs. parcialmente observable**: si los sensores dan acceso al estado completo del medio en cada momento. Puede ser parcialmente observable por ruido, sensores poco exactos, o porque los sensores no reciben información de alguna parte del sistema.",
    "**Determinista vs. estocástico**: es determinista si el siguiente estado está totalmente determinado por el estado actual y la acción ejecutada.",
    "**Episódico vs. secuencial**: en entornos episódicos la experiencia se divide en episodios separados y el siguiente no depende de las acciones previas; en los secuenciales la decisión presente afecta decisiones futuras.",
    "**Estático vs. dinámico**: es dinámico si el entorno puede cambiar mientras el agente delibera.",
    "**Discreto vs. continuo**: la distinción se aplica al estado del medio, al manejo del tiempo y a las percepciones y acciones del agente.",
    "**Individual vs. multiagente**: hay que analizar caso por caso — un agente resolviendo un crucigrama es individual; uno jugando al ajedrez está en un entorno multiagente.",
    "**Conocido vs. desconocido** (agregado por la 4.ª edición): no se refiere al ambiente en sí, sino al estado de conocimiento del agente sobre las «leyes de la física» del ambiente. En un ambiente conocido se conocen los resultados —o las probabilidades de resultado— de todas las acciones.",
])
box(doc, "Conocido ≠ observable",
    "No es la misma distinción. Un ambiente **conocido** puede ser **parcialmente "
    "observable**: en el solitario se conocen las reglas pero no se ven las cartas sin "
    "voltear. Y un ambiente **desconocido** puede ser **completamente observable**: en un "
    "videojuego nuevo la pantalla muestra todo el estado, pero hasta probarlos no se sabe "
    "qué hacen los botones.\n"
    "Con esta dimensión agregada, el caso más difícil se actualiza a: **parcialmente "
    "observable, multiagente, no determinista, secuencial, dinámico, continuo y "
    "desconocido**. Conducir un taxi es difícil en todos esos sentidos salvo en que el "
    "entorno es en su mayoría conocido; conducir un auto alquilado en un país nuevo, con "
    "geografía desconocida y leyes de tránsito diferentes, «es mucho más emocionante».")
ejemplo("Ejemplo · las siete propiedades aplicadas a la misma aspiradora",
        "**Totalmente observable**: depende del sensor. Si sólo detecta la celda donde "
        "está, es *parcialmente* observable — no sabe si D quedó sucia. "
        "**Determinista**: sí, aspirar siempre limpia y moverse siempre mueve. "
        "**Episódico o secuencial**: secuencial, porque si aspira ahora esa celda queda "
        "limpia después. **Estático**: sí, la suciedad no aparece sola mientras el "
        "agente piensa. **Discreto**: sí, cuatro celdas y cinco acciones. "
        "**Individual**: sí, hay una sola aspiradora. **Conocido**: sí, las reglas del "
        "mundo están dadas.\n"
        "Cambiando **una sola** de esas respuestas cambia la técnica necesaria. Si la "
        "suciedad reapareciera sola, el ambiente pasaría a ser dinámico y estocástico, "
        "y la tabla de ocho filas dejaría de alcanzar: haría falta razonar bajo "
        "incertidumbre ([[u5|Unidad 5]]). Por eso estas propiedades se analizan "
        "**antes** de elegir el algoritmo, no después.")

h(doc, 2, "1.11 Estructura: tipos de programa de agente", "u1_9")
fig("d02_tipos_agente.png",
    "Los cinco tipos de programa de agente y qué agrega cada uno al anterior.")
bullets(doc, [
    "**Agentes reactivos simples**: seleccionan las acciones sobre la base de las percepciones actuales, ignorando el resto de las percepciones históricas. Sólo funcionan si se puede tomar la decisión correcta con la percepción actual, lo cual **sólo es posible si el entorno es totalmente observable**.",
    "**Agentes reactivos basados en modelos**: para manejar la visibilidad parcial, mantienen un **estado interno** que depende de la historia percibida. Esto requiere codificar dos tipos de conocimiento: cómo evoluciona el mundo independientemente del agente, y cómo afectan al mundo las acciones del agente. A ese conocimiento se lo llama **modelo del mundo**.",
    "**Agentes basados en objetivos**: el estado actual no siempre alcanza para decidir; además de la descripción del estado actual el agente necesita información sobre su **meta**, que describa situaciones deseables. Es el punto de contacto con la [[u3|búsqueda]] y la [[u3_plan|planificación]].",
    "**Agentes basados en utilidad**: usan una **función de utilidad** que proyecta un estado en un número real. Permite decidir racionalmente en dos casos donde las metas son inadecuadas: (a) cuando hay objetivos conflictivos y sólo se pueden alcanzar algunos —la utilidad determina el equilibrio—; (b) cuando hay varios objetivos y ninguno se puede alcanzar con certeza —la utilidad permite ponderar la probabilidad de éxito según la importancia de cada objetivo—.",
    "**Agentes que aprenden**: tienen un **elemento de aprendizaje** (responsable de hacer mejoras), un **elemento de actuación** (selecciona acciones externas), una **crítica** (realimenta al elemento de aprendizaje sobre la actuación) y un **generador de problemas** (sugiere acciones que lleven a experiencias nuevas e informativas). Es la puerta de entrada a la [[u2|Unidad 2]].",
])
box(doc, "Agentes clásicos vs. agentes actuales (comparación de la cátedra)",
    "**Enfoque clásico**: perciben el entorno con sensores y actúan con actuadores; "
    "diseñados para entornos específicos, físicos o simulados; conocimiento limitado al "
    "entorno definido.\n"
    "**Enfoque actual**: interactúan con datos digitales, reconocen lenguaje natural y "
    "archivos cargados por el usuario; el entorno es digital y conversacional, sin "
    "interacción física; combinan un modelo de IA generativa con capacidades de "
    "razonamiento y **aprendizaje en contexto** (*in-context learning*), adaptando la "
    "respuesta a la situación; optimizan su «utilidad» mediante la retroalimentación del "
    "usuario y tienen objetivos implícitos: responder de forma correcta, clara y útil.")
ejemplo("Ejemplo · los cinco tipos resolviendo la misma aspiradora",
        "La forma más rápida de ver la diferencia es dejar el problema fijo y cambiar "
        "sólo el agente. Un **reactivo simple** aplica «si sucio, aspirar; si no, "
        "moverme» y con sensor limitado puede quedar yendo de A a B para siempre. Uno "
        "**basado en modelo** anota qué celdas ya limpió y por eso no se repite. Uno "
        "**basado en objetivos** se fija la meta «las cuatro limpias» y planifica la "
        "ruta antes de moverse. Uno **basado en utilidad** compara planes que cumplen la "
        "meta y elige el que gasta menos batería. Y uno **que aprende** descubre solo "
        "que la celda B se ensucia todos los días a la misma hora.\n"
        "Cada tipo agrega **exactamente una cosa** al anterior: memoria, meta, "
        "preferencia entre metas y capacidad de mejorar.")
fig("e02_tipos_aspiradora.png",
    "El mismo problema resuelto por los cinco tipos de agente.")

page_break(doc)

# =================================================================== UNIDAD 2
h(doc, 1, "Unidad 2 · Aprendizaje automático", "u2")
para(doc,
     "La idea del aprendizaje consiste en **utilizar las percepciones no sólo para "
     "actuar, sino también para mejorar la habilidad del agente para actuar en el "
     "futuro**. Entra en juego cuando el agente observa sus interacciones con el mundo y "
     "sus procesos de toma de decisiones.")
box(doc, "Una aclaración que hace el apunte sobre el libro",
    "Russell y Norvig dicen que, entre múltiples hipótesis consistentes, la mejor es la "
    "más simple. Es correcto, pero el apunte remarca **por qué**: porque la función más "
    "simple es la que mejor generaliza, y las funciones complejas tienden a "
    "**sobreajustarse** a los datos de entrenamiento. Ver [[u2_3|la sección de "
    "evaluación en regresión]].")
para(doc,
     "Es la unidad más larga del programa —**28 de las 96 horas**, más del doble que "
     "cualquier otra— y también la que más se apoya en las presentaciones de la "
     "cátedra.")
para(doc,
     "Lo primero que hay que fijar es **qué tipo de realimentación recibe el agente del "
     "entorno**, porque de eso —y no del algoritmo— salen los tres grandes paradigmas "
     "del aprendizaje automático:")
bullets(doc, [
    "**Aprendizaje supervisado.** El algoritmo aprende a partir de **ejemplos etiquetados**: un «profesor» suministra el valor correcto de la salida para cada ejemplo, y el objetivo es minimizar el error entre la predicción y la etiqueta real. Sus dos aplicaciones son la **regresión** (predecir valores continuos, como la distancia de frenado) y la **clasificación** (predecir categorías discretas, como si una imagen contiene un autobús). **Es el paradigma de toda esta unidad.**",
    "**Aprendizaje no supervisado.** El algoritmo aprende a partir de **patrones intrínsecos, sin etiquetas ni salidas especificadas**: no hay profesor indicando qué es correcto. Su aplicación principal es el **agrupamiento** (*clustering*): discernir categorías naturales dentro de conjuntos complejos — segmentación de clientes, taxonomía biológica.",
    "**Aprendizaje por refuerzo.** El agente aprende **interactuando con el entorno**, no sobre un conjunto de datos estático. Ejecuta una acción, recibe el estado resultante y una **recompensa** —positiva o negativa—, y debe descubrir qué acciones producen la mayor recompensa acumulada a lo largo del tiempo, forjando una política óptima de comportamiento.",
])
box(doc, "Por qué la diferencia está en la realimentación y no en el algoritmo",
    "Un mismo modelo —una red neuronal, por ejemplo— puede usarse en los tres "
    "paradigmas. Lo que cambia es **qué información devuelve el entorno**: la respuesta "
    "correcta (supervisado), nada (no supervisado) o una señal de premio o castigo "
    "(refuerzo). Por eso conviene preguntarse primero qué datos hay disponibles y recién "
    "después qué algoritmo usar.\n"
    "El **aprendizaje por refuerzo no figura en el programa analítico** como tema propio "
    "y por eso no se desarrolla acá; se lo incluye porque la presentación de la cátedra "
    "lo presenta como uno de los tres tipos y omitirlo dejaría la clasificación coja.")
para(doc,
     "Con eso fijado, conviene tener el **mapa del proceso completo**, porque casi todo "
     "lo que sigue es una pieza de alguna de estas tres etapas. La presentación de la "
     "cátedra lo organiza así:")
fig("e31_etapas_ml.png",
    "El flujo de trabajo de un proyecto de aprendizaje supervisado, y en qué etapa "
    "entra cada tema de la unidad.")
para(doc,
     "Es útil volver a este esquema cuando un tema parece suelto. El "
     "[[u2_1|reconocimiento de patrones]] y la extracción de características son la "
     "etapa 1; las [[u2_reg|regresiones]], las [[u2_8|SVM]] y las "
     "[[u2_9|redes neuronales]] son la etapa 2; y la "
     "[[u2_4|matriz de confusión]], las métricas y la "
     "[[u2_5|validación cruzada]] son la etapa 3. Dos detalles del esquema que después "
     "se repiten: el entrenamiento ajusta los parámetros **exclusivamente sobre el "
     "conjunto de entrenamiento**, y la evaluación mide el rendimiento **frente a "
     "observaciones completamente nuevas** — separar esas dos cosas es la disciplina "
     "central de toda la unidad.")

h(doc, 2, "2.1 Reconocimiento de patrones", "u2_1")
para(doc,
     "Es el enfoque complementario al de los agentes inteligentes, más cercano a un "
     "proyecto típico de Ciencia de Datos. Cuando una persona percibe un patrón realiza "
     "una **inferencia inductiva** y asocia esa percepción con conceptos generales "
     "derivados de su experiencia pasada. Así, el problema del reconocimiento se concibe "
     "como el de discriminar, clasificar o categorizar la información de entrada, **no "
     "entre patrones individuales sino entre poblaciones**, buscando características o "
     "atributos invariantes entre los miembros de una población.")
para(doc, "El diseño de un sistema de reconocimiento automático involucra tres tareas:")
bullets(doc, [
    "**Sensado** — ¿cómo obtengo los datos del objeto? Consiste en representar la información obtenida mediante algún sensor. En el ejemplo de reconocer caracteres, la imagen se transforma en una grilla donde cada celda vale 1 si forma parte del carácter y 0 si no.",
    "**Extracción de características** — ¿qué información relevante selecciono? Busca **reducir la dimensión** de los vectores de patrones sin perder información significativa. Aquí entra **PCA** (Análisis de Componentes Principales), que encuentra nuevas variables que resumen la información más importante.",
    "**Clasificación** — ¿a qué clase pertenece el patrón? Se resuelve con funciones discriminantes ([[u2_6|sección 2.7]]).",
])
para(doc,
     "Toda la información medida sobre un patrón se guarda en un **vector de patrón** "
     "x = (x₁, x₂, …, xₙ). Cuando los vectores están formados por números reales es útil "
     "interpretarlos como **puntos en el espacio euclidiano n-dimensional**: dos personas "
     "con peso y altura parecidos quedan cerca. Cuando muchos puntos de una misma clase "
     "aparecen agrupados en una región del espacio, ese agrupamiento se llama **clúster**.")
box(doc, "El ejemplo de la cátedra",
    "Patrones de jugadores de básquet y de fútbol descriptos por peso (eje x₁) y altura "
    "(eje x₂). Los de básquet aparecen agrupados en un clúster porque se espera que sean "
    "muy altos, y los de fútbol en otro porque son de menor altura. Si aparece un punto "
    "nuevo con mucha altura y peso alto, parece de básquet; **si aparece un punto en el "
    "medio de ambos clústeres, la clasificación es más dudosa**. Y sobre convertir una "
    "imagen en una grilla de 0 y 1: se gana una representación computable y se simplifica "
    "el problema, pero se pierden los detalles finos de la forma.")
ejemplo("Ejemplo · reconocer monedas de $100 y de $500",
        "Un clasificador de monedas para una máquina expendedora. **Sensado**: una "
        "balanza y un calibre. **Extracción de características**: de toda la moneda "
        "—material, dibujo, canto, brillo— se conservan sólo dos números, peso y "
        "diámetro. **Vector de patrón**: x = (23,9 mm ; 7,2 g). **Clasificación**: una "
        "recta parte el plano en dos regiones, y ese punto cae del lado de $500.\n"
        "Lo importante es la segunda etapa: elegir *esas* dos características y no "
        "otras es la decisión que define si el problema se vuelve fácil o imposible. Si "
        "las dos monedas pesaran y midieran igual, ningún clasificador del mundo podría "
        "separarlas con esos datos.")
fig("e03_patrones.png",
    "Las cuatro etapas del reconocimiento de patrones sobre un caso concreto.")

h(doc, 2, "2.2 Aprendizaje supervisado: el marco formal", "u2_2")
para(doc,
     "Se asume que existe una relación entre la salida escalar y ∈ ℝ y el vector de "
     "entradas x = (x₁, …, xₙ) que puede escribirse como")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
_fmt(p.add_run("y = f(x) + ε"), bold=True, size=13, color=MORADO_OSC)
para(doc,
     "donde **f** es una función fija pero desconocida y **ε** un término de error "
     "aleatorio, independiente de x y de media cero. En esencia, el aprendizaje "
     "automático se refiere a **un conjunto de enfoques para estimar f**. La motivación "
     "más común es la predicción: como el error se promedia a cero, se predice "
     "ŷ = f̂(x), donde f̂ es la estimación de f.")
fig("d03_pipeline_ml.png",
       "El circuito completo: del objeto real a la predicción, y cómo se reparten "
       "los datos para poder confiar en ella.")
h(doc, 3, "Error reducible y error irreducible", "u2_2a")
bullets(doc, [
    "**Error reducible**: f̂ no será un estimador perfecto de f, y esa falta de exactitud introduce error. Es *reducible* porque podríamos mejorar f̂ usando la técnica de aprendizaje más apropiada.",
    "**Error irreducible**: aun con una estimación perfecta (ŷ = f(x)) quedaría error, porque y también es función de ε, que por definición no se puede predecir usando x. **Var(ε) es el piso que ningún modelo puede bajar.** ¿Por qué es mayor que cero? Porque ε puede contener variables no medidas útiles para predecir y, o variaciones no medibles —por ejemplo, derivadas de la subjetividad de un evaluador humano—.",
])
h(doc, 3, "Datos de entrenamiento y métodos paramétricos", "u2_2b")
para(doc,
     "El conjunto de m instancias observadas {(x₁,y₁), …, (xₘ,yₘ)} se llama **datos de "
     "entrenamiento** porque se usa para ajustar el método. Los métodos se dividen en "
     "**paramétricos** y no paramétricos; **la cátedra se enfoca en los paramétricos**, "
     "que constan de dos pasos:")
bullets(doc, [
    "**Suponer la forma de f.** El caso más simple es asumirla lineal: f(x) = w₁x₁ + w₂x₂ + … + wₙxₙ + wₙ₊₁. Una vez asumido esto, en lugar de estimar una función arbitraria de dimensión n sólo hay que estimar **n+1 coeficientes**.",
    "**Ajustar el modelo** con los datos de entrenamiento. El método más común para el modelo lineal es el de **mínimos cuadrados**.",
])
para(doc,
     "La ventaja es clara: es mucho más fácil estimar un conjunto de parámetros que "
     "ajustar una función completamente arbitraria. La **desventaja** es que el modelo "
     "elegido por lo general no coincidirá con la verdadera forma de f; si está demasiado "
     "lejos, la estimación será pobre. Se puede elegir un modelo más flexible, pero eso "
     "requiere estimar más parámetros y **conduce al sobreajuste**.")

h(doc, 2, "2.3 Evaluación del rendimiento: el caso de la regresión", "u2_3")
para(doc,
     "En regresión la medida más utilizada es el **error cuadrático medio (MSE)**: el "
     "promedio de (yᵢ − f̂(xᵢ))². Calculado sobre los datos de entrenamiento se lo llama "
     "**MSE de entrenamiento**; pero *lo que interesa es el MSE de test*, sobre datos no "
     "vistos.")
box(doc, "La propiedad fundamental del aprendizaje automático",
    "A medida que aumenta la flexibilidad del modelo, el **MSE de entrenamiento "
    "disminuye monótonamente**, mientras que el **MSE de test dibuja una forma de "
    "«U»**: primero baja, se nivela y después vuelve a subir. Esta propiedad se mantiene "
    "independientemente de los datos y del método elegido.\n"
    "Cuando un método produce un MSE de entrenamiento pequeño pero un MSE de test "
    "grande, decimos que estamos **sobreajustando**. Pasa porque el método encuentra "
    "patrones causados por el azar en lugar de verdaderas propiedades de f; esos "
    "patrones simplemente no existen en los datos de test.\n"
    "Ojo con el matiz: **casi siempre** el MSE de entrenamiento será menor que el de "
    "test, porque los métodos buscan minimizarlo. Sobreajuste se refiere "
    "específicamente al caso en que **un modelo menos flexible habría dado un MSE de "
    "test más pequeño**. La línea horizontal por debajo de la cual no se puede bajar es "
    "Var(ε), el error irreducible.")
ejemplo("Ejemplo · diez puntos y tres modelos",
        "Diez mediciones que siguen aproximadamente una recta, con algo de ruido. Se "
        "las ajusta con un polinomio de **grado 1**, uno de **grado 3** y uno de "
        "**grado 9**.\n"
        "El de grado 9 pasa **exactamente por los diez puntos**: su MSE de "
        "entrenamiento es prácticamente cero, el mejor de los tres. Y sin embargo es el "
        "peor con datos nuevos, porque entre punto y punto la curva se dispara. El de "
        "grado 1 es demasiado rígido y no llega a seguir la forma. El de grado 3 es el "
        "que menos error de test comete, aunque su error de entrenamiento sea mayor que "
        "el del grado 9.\n"
        "Ésa es la «U» del MSE de test, vista en un caso concreto: **elegir el modelo "
        "por su error de entrenamiento lleva sistemáticamente a la peor opción**.")
fig("e04_sobreajuste.png",
    "Subajuste, buen ajuste y sobreajuste sobre el mismo conjunto de datos.")

h(doc, 2, "2.4 Evaluación en clasificación: matriz de confusión y métricas", "u2_4")
para(doc,
     "En clasificación y ya no es cuantitativa. El enfoque más común para cuantificar el "
     "error es la **tasa de error**: la proporción de clasificaciones incorrectas. Pero "
     "en la práctica se usa menos que otras herramientas, y la más útil —porque además "
     "facilita el cálculo de las demás— es la **matriz de confusión**: una tabla de "
     "contingencia donde se acumulan las ocurrencias de las etiquetas reales y predichas. "
     "**Todas las clasificaciones correctas se ubican sobre la diagonal principal**; las "
     "incorrectas, fuera de ella.")
fig("d05_metricas.png",
       "De la matriz de confusión salen todas las métricas de clasificación.")
para(doc,
     "En clasificación binaria las clases se llaman «positivo» (P) y «negativo» (N), "
     "indicando si se está o no en presencia de la situación que se pretende detectar "
     "—por ejemplo, una patología—. Las cuatro regiones son verdaderos positivos (VP), "
     "falsos positivos (FP), falsos negativos (FN) y verdaderos negativos (VN).")
h(doc, 3, "Por qué ninguna métrica alcanza sola", "u2_4a")
para(doc,
     "La **sensibilidad** (recall) es una cualidad muy importante, pero si sólo miramos "
     "sensibilidad podríamos calificar como bueno a un clasificador que responde «P» en "
     "todos los casos. Por eso hay que incorporar otra métrica y buscar un equilibrio: la "
     "**razón de falsos positivos (FPR)**, que indica qué proporción de los negativos se "
     "etiqueta como positivos. FPR vale 0 cuando no hay falsos positivos y 1 cuando todos "
     "los negativos se clasifican como positivos: **es la única métrica en la que el "
     "óptimo es 0 y no 1**, lo cual es poco intuitivo. La **especificidad** = 1 − FPR "
     "tiene la misma utilidad pero con el óptimo en 1.")
para(doc,
     "**En la práctica.** El notebook __Clasificación – Parte 4__ (Clase 3) entrena una "
     "SVM sobre el conjunto de datos de **diabetes** (768 pacientes, ocho características "
     "clínicas) y evalúa sobre 384 casos de prueba. Sirve para ver el argumento anterior "
     "con números reales:")
code(doc, '''from sklearn.metrics import classification_report, confusion_matrix

y_predict = svc_model.predict(x_test)

print("\\n--- Matriz de Confusión ---")
cm = confusion_matrix(y_test, y_predict)
print(cm)

print("\\n--- Reporte de Clasificación ---")
print(classification_report(y_test, y_predict))''')
salida(doc, '''--- Matriz de Confusión ---
[[221  27]
 [ 70  66]]

--- Reporte de Clasificación ---
              precision    recall  f1-score   support

           0       0.76      0.89      0.82       248
           1       0.71      0.49      0.58       136

    accuracy                           0.75       384
   macro avg       0.73      0.69      0.70       384
weighted avg       0.74      0.75      0.73       384''')
para(doc,
     "Leída como corresponde, la matriz dice: **221 verdaderos negativos, 27 falsos "
     "positivos, 70 falsos negativos y 66 verdaderos positivos**. La exactitud es "
     "(221 + 66)/384 = **75 %**, que suena aceptable. Pero mirando sólo la clase que "
     "importa —los pacientes con diabetes— la **sensibilidad es 0,49**: de 136 enfermos "
     "el modelo detecta 66 y **se le escapan 70**, más de la mitad.")
box(doc, "Éste es exactamente el caso que justifica la sección",
    "El mismo modelo se describe como «75 % de acierto» o como «se le escapa la mitad de "
    "los enfermos», y ambas afirmaciones salen de la misma tabla. La diferencia aparece "
    "porque las clases están **desbalanceadas** (248 sanos contra 136 enfermos): "
    "contestar «sano» siempre ya daría 65 % de exactitud sin haber aprendido nada.\n"
    "Y en un problema de diagnóstico los dos errores no cuestan lo mismo: un falso "
    "positivo cuesta un estudio de más, un falso negativo cuesta un enfermo sin tratar. "
    "Con la **precisión de 0,71** y la **sensibilidad de 0,49** enfrentadas, el "
    "**F1 = 0,58** de esa clase describe el modelo mucho mejor que la exactitud global.")
h(doc, 3, "Curva ROC y AUC", "u2_4b")
para(doc,
     "Tanto los FP como los FN son errores y, salvo indicación, se busca minimizar "
     "FP + FN. Pero **en los problemas reales el costo de cada tipo de error no es el "
     "mismo**: al detectar una enfermedad suele ser menos grave un FP que un FN, y en ese "
     "caso queremos un modelo más sensible aunque perdamos especificidad y exactitud.")
para(doc,
     "La mayoría de los modelos de clasificación binaria produce un **escalar**; cuando "
     "supera cierto **umbral** se asigna «P». Desplazando el umbral varían sensibilidad y "
     "especificidad: si se reduce el umbral hay más muestras clasificadas como positivas "
     "y el clasificador es más sensible. La **curva ROC** grafica simultáneamente los dos "
     "tipos de error para todos los umbrales posibles; cada punto corresponde a un valor "
     "de umbral. Los extremos de la curva siempre caen en el vértice inferior izquierdo "
     "(umbral alto: sensibilidad muy mala, FPR muy buena) y en el superior derecho "
     "(umbral bajo: al revés).")
para(doc,
     "El rendimiento general resumido en todos los umbrales es el **área bajo la curva "
     "(AUC)**: cuanto más se acerque la curva a la esquina superior izquierda, mayor el "
     "AUC y mejor el clasificador. Un AUC de 0,95 se considera muy bueno. La diagonal "
     "marca el comportamiento de un clasificador sin capacidad discriminante.")
ejemplo("Ejemplo · el test con 91 % de aciertos que igual es malo",
        "Un test sobre **100 personas**, de las cuales 10 están enfermas. Resultado: "
        "detecta 6 enfermos (VP = 6), se le escapan 4 (FN = 4), da alarma falsa en 5 "
        "sanos (FP = 5) y acierta en 85 sanos (VN = 85).\n"
        "**Accuracy** = (6 + 85) / 100 = **0,91**. Suena excelente. Pero:\n"
        "**Recall** = 6 / 10 = **0,60** — se pierde 4 de cada 10 enfermos.\n"
        "**Precision** = 6 / 11 = **0,55** — casi la mitad de sus alarmas son falsas.\n"
        "**Especificidad** = 85 / 90 = **0,94**.  **F₁** = **0,57**.\n"
        "El detalle que lo define todo: un test que dijera «sano» a todo el mundo "
        "tendría **90 % de accuracy y recall cero**. Con clases desbalanceadas la "
        "accuracy sola no dice nada, y por eso hay que mirar la matriz completa.")
fig("e10_metricas.png",
    "Las cinco métricas calculadas sobre una misma matriz de confusión.")

h(doc, 2, "2.5 Esquemas de evaluación y validación cruzada", "u2_5")
para(doc,
     "El nivel de generalización de un clasificador está relacionado con su capacidad de "
     "predicción sobre un conjunto de datos independiente. Hay que tener en mente **dos "
     "objetivos distintos**:")
bullets(doc, [
    "**Selección del modelo**: estimar el rendimiento de distintos modelos (distintos conjuntos de hiperparámetros) para elegir el mejor.",
    "**Evaluación del modelo**: estimar el rendimiento del modelo ya elegido sobre datos nuevos.",
])
box(doc, "Por qué la separación tiene que ser aleatoria",
    "Al partir el conjunto original en entrenamiento y prueba, lo que se busca es que "
    "**ambos subconjuntos provengan de la misma distribución poblacional**: su "
    "dispersión estadística, su varianza y su media deben ser prácticamente idénticas, y "
    "lo único que debe variar entre uno y otro es la **cantidad de observaciones**. El "
    "muestreo aleatorio es lo que garantiza eso.\n"
    "Si la partición no es aleatoria —por ejemplo, si se toma el 80 % inicial de un "
    "archivo que venía ordenado por clase— los dos conjuntos dejan de representar la "
    "misma población, y entonces **el error de prueba ya no estima el error de "
    "generalización**: mide otra cosa. Es una de las formas más frecuentes de obtener "
    "resultados que no se sostienen en producción.")
para(doc,
     "El mejor enfoque para ambos es dividir los datos aleatoriamente en **tres** "
     "conjuntos: entrenamiento (ajusta parámetros), validación (estima el rendimiento de "
     "cada modelo y elige el mejor) y test (evalúa el modelo final). **El conjunto de "
     "test se debe mantener separado y usar sólo al final**: en caso contrario se produce "
     "una adaptación de los hiperparámetros a los datos de test.")
para(doc,
     "Como los datos suelen ser limitados aparece un dilema: se quiere usar la mayor "
     "cantidad posible para entrenar, pero un conjunto de validación pequeño da una "
     "estimación poco confiable. La solución es la **validación cruzada (k-fold)**: los "
     "datos se dividen aleatoriamente en k subconjuntos (*folds*) del mismo tamaño; en "
     "cada una de las k iteraciones se elige un fold para validación y el resto para "
     "entrenamiento, y **el rendimiento se calcula como la media de los k rendimientos**.")
ejemplo("Ejemplo · 5-fold sobre 100 muestras",
        "Con sólo 100 muestras, apartar 20 para validación deja 80 para entrenar y una "
        "estimación de rendimiento basada en apenas 20 casos — demasiado ruidosa. Con "
        "**k = 5**: se parten las 100 en cinco bloques de 20; se entrena cinco veces, "
        "cada una con 80 muestras y validando sobre el bloque que quedó afuera. Las "
        "cinco precisiones dan, por ejemplo, 0,84 · 0,79 · 0,86 · 0,81 · 0,85, y el "
        "rendimiento estimado es su media, **0,83**.\n"
        "Se aprovecharon las 100 muestras para validar y las 100 para entrenar, sin que "
        "ninguna se validara consigo misma. El test se sigue reservando aparte y se usa "
        "una sola vez, al final.")

h(doc, 2, "2.6 Regresión lineal, logística y polinomial", "u2_reg")
para(doc,
     "Las tres regresiones que nombra el programa son **el mismo modelo con tres "
     "variantes**, y conviene verlo así en vez de memorizarlas por separado. La base "
     "común es una combinación lineal de las entradas, h(x) = w · x = w₀ + w₁x₁ + … + "
     "wₙxₙ. Lo que cambia entre ellas es qué se hace con ese número y qué se le "
     "entrega como entrada.")
h(doc, 3, "Regresión lineal", "u2_reg_a")
para(doc,
     "La salida es directamente h(x) = w · x, un número real cualquiera. Se usa cuando "
     "**lo que se predice es una cantidad**. El ajuste de los pesos se hace minimizando "
     "el error cuadrático —el MSE de [[u2_3|la sección anterior]]—, y en el caso "
     "univariable ese mínimo tiene **solución cerrada**: se despeja con las derivadas "
     "parciales igualadas a cero, sin necesidad de iterar. En el caso general se usa "
     "**descenso por gradiente**, ajustando los pesos en la dirección que más reduce el "
     "error.")
para(doc,
     "**En la práctica.** El notebook __Clasificación – Parte 2__ (Clase 2) hace una "
     "regresión lineal sobre datos oceanográficos reales: **451 muestras** de agua de "
     "mar, prediciendo la temperatura a partir de la salinidad. El flujo completo son "
     "seis líneas, y son las mismas seis de cualquier problema supervisado:")
code(doc, '''salinitys    = data_salinity[["sal"]]
temperatures = data_salinity[["temp"]]

sal_train, sal_test, temp_train, temp_test = train_test_split(
    salinitys, temperatures, test_size=0.5, random_state=50)

LN = LinearRegression()
LN.fit(sal_train, temp_train)
print(LN.score(sal_test, temp_test))''')
salida(doc, '''Tamaño del set de entrenamiento: 225 - Tamaño del set de testing: 226 -> TOTAL = 451
0.8547139708334874''')
para(doc,
     "El **0,85** es el coeficiente de determinación R², e importa **dónde** está medido: "
     "sobre `sal_test`, es decir sobre las 226 muestras que el modelo **no vio durante el "
     "entrenamiento**. Ésa es la cifra que sirve para estimar el error de generalización; "
     "medida sobre los datos de entrenamiento sólo diría cuánto memorizó "
     "([[u2_5|sección 2.5]]).")
box(doc, "Qué significa y qué no significa ese 0,85",
    "R² = 0,85 quiere decir que el modelo **explica el 85 % de la variabilidad** de la "
    "temperatura a partir de la salinidad, y que el 15 % restante queda fuera de su "
    "alcance. Parte de ese resto es **error irreducible** ([[u2_2a|sección 2.2]]): la "
    "temperatura del agua depende de la profundidad, la estación y la corriente, y "
    "ninguna de esas variables está en el modelo.\n"
    "Tampoco significa que la salinidad **cause** la temperatura. Las dos varían juntas "
    "porque comparten causas físicas —evaporación, mezcla de masas de agua—, y una "
    "regresión mide asociación, no causalidad. Es el mismo cuidado que hay que tener con "
    "cualquier modelo predictivo entrenado sobre datos observacionales.")
h(doc, 3, "Regresión logística", "u2_reg_b")
para(doc,
     "Sirve para **clasificar**, no para predecir un número. El problema del "
     "clasificador de umbral duro (el escalón del [[u2_9a|perceptrón]]) es que **no es "
     "derivable en cero** y salta bruscamente de 0 a 1, lo que impide usar descenso por "
     "gradiente y hace que el aprendizaje sea impredecible cuando los datos no son "
     "separables. La solución es reemplazar el escalón por su versión suave, la "
     "**función logística** —también llamada sigmoide—:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
_fmt(p.add_run("h(x) = Logistic(w · x) = 1 / (1 + e^(−w · x))"), bold=True,
     size=12, color=MORADO_OSC)
para(doc,
     "La salida queda **entre 0 y 1**, y por eso puede leerse como la probabilidad de "
     "pertenecer a la clase etiquetada como 1. La frontera deja de ser una línea dura y "
     "pasa a ser una **frontera blanda**: vale 0,5 justo en el centro de la región de "
     "decisión y se acerca a 0 o a 1 a medida que uno se aleja. No hay solución cerrada "
     "para los pesos óptimos, pero el gradiente es directo, y como la derivada de la "
     "logística cumple g′(z) = g(z)(1 − g(z)), la regla de actualización queda:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
_fmt(p.add_run("wᵢ ← wᵢ + α (y − h(x)) · h(x)(1 − h(x)) · xᵢ"), bold=True,
     size=11.5, color=MORADO_OSC)
box(doc, "Por qué la logística le gana al umbral duro",
    "Repitiendo los mismos experimentos con las dos versiones, en el caso **linealmente "
    "separable** la regresión logística converge algo más lento pero de forma mucho más "
    "predecible. Y en los casos **ruidosos y no separables** —que son los reales— "
    "converge bastante más rápido y de manera más confiable que el clasificador de "
    "umbral. Esas ventajas se trasladan a las aplicaciones prácticas: la regresión "
    "logística es hoy una de las técnicas de clasificación más usadas en medicina, "
    "marketing, análisis de encuestas, scoring crediticio y salud pública.")
h(doc, 3, "Regresión polinomial", "u2_reg_c")
para(doc,
     "No cambia el modelo: cambia la **entrada**. En lugar de alimentarlo con x se lo "
     "alimenta con (x, x², x³, …), y con eso una recta en el espacio ampliado se "
     "convierte en una curva en el espacio original. Es exactamente la misma idea que "
     "la **función de decisión generalizada** de [[u2_7|la sección siguiente]]: "
     "transformar las entradas para que un modelo lineal resuelva un problema que no lo "
     "es.\n"
     "El modelo sigue siendo **lineal en los parámetros w**, así que se ajusta con los "
     "mismos métodos. Y por eso mismo hereda el riesgo: subir el grado baja el sesgo "
     "pero sube la varianza, y ahí vuelve a aparecer el sobreajuste.")
fig("d14_regresion.png",
    "Las tres regresiones del programa y qué cambia exactamente entre una y otra.")
ejemplo("Ejemplo · precio de una casa frente a aprobar un examen",
        "**Lineal**: con ocho casas de las que se conocen superficie y precio, el "
        "modelo ajustado da aproximadamente h(x) = 0,95·x − 6 (precio en miles de "
        "dólares, superficie en m²). Para una casa de 90 m² predice unos 79.500 "
        "dólares. La salida es un número y tiene sentido que lo sea.\n"
        "**Logística**: con diez alumnos de los que se sabe cuántas horas estudiaron y "
        "si aprobaron, el modelo devuelve para 6 horas de estudio un valor de ≈ 0,69. "
        "Como supera el umbral de 0,5, predice «aprueba» — pero además informa que la "
        "confianza es moderada, no del 100 %. Un umbral duro habría dicho «aprueba» y "
        "nada más.\n"
        "**Polinomial**: si el precio de las casas subiera más que proporcionalmente "
        "con la superficie, la recta se quedaría corta; agregando x² el mismo "
        "maquinaria ajusta una parábola.")
fig("e05_regresiones.png",
    "Predecir un número (regresión lineal) frente a predecir una clase (logística).")
para(doc,
     "**En la práctica.** El notebook __Clasificación – Parte 4__ arma esa transformación "
     "de entradas de forma explícita, encadenando los dos pasos en un `Pipeline`: primero "
     "expande las características a grado 3, después aplica un clasificador lineal sobre "
     "las características expandidas. El conjunto de prueba es `make_moons`, dos "
     "medialunas entrelazadas que ninguna recta separa:")
code(doc, '''from sklearn.pipeline import Pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression

# make_moons crea datos con forma de dos lunas entrelazadas.
# Un clasificador lineal simple no podría separar estas clases.
X, y = make_moons(n_samples=100, noise=0.15, random_state=42)

degree = 3
polynomial_classifier = Pipeline([
    # Paso 1: crea combinaciones polinómicas de grado 3 (x², y², x*y, ...)
    ("poly_features", PolynomialFeatures(degree=degree)),
    # Paso 2: un clasificador lineal sobre las nuevas características
    ("log_reg", LogisticRegression())
])
polynomial_classifier.fit(X, y)''')
para(doc,
     "El `Pipeline` deja ver la idea con una claridad que el texto no consigue: **el "
     "clasificador del segundo paso sigue siendo lineal**. Lo único que cambió es que ya "
     "no ve (x₁, x₂) sino (x₁, x₂, x₁², x₁x₂, x₂², x₁³, …). La frontera curva que "
     "aparece en el espacio original es una **frontera recta en el espacio expandido** — "
     "que es exactamente lo que hace también el kernel de una SVM ([[u2_8|sección 2.9]]), sólo "
     "que la SVM se ahorra construir esas columnas de forma explícita.")

h(doc, 2, "2.7 Clasificación y funciones discriminantes", "u2_6")
para(doc,
     "En un problema de c clases ω₁, …, ω_c el espacio de las entradas se considera "
     "compuesto por c regiones, cada una con los elementos de una clase. La solución se "
     "interpreta como **la generación de límites de decisión entre las regiones**. Esos "
     "límites están dados por **funciones discriminantes** d₁(x), …, d_c(x), que son "
     "funciones escalares de los vectores de entrada. La regla multiclase es:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
_fmt(p.add_run("x ∈ ωᵢ   si   dᵢ(x) = máx_j dⱼ(x)"), bold=True, size=12,
     color=MORADO_OSC)
para(doc,
     "En clasificación binaria basta una única función d(x): si d(x) > 0 pertenece a una "
     "clase, si d(x) < 0 a la otra, y si d(x) = 0 el patrón está **sobre el límite de "
     "decisión**.")
box(doc, "Ejemplo numérico de la cátedra (tres clases, dos características)",
    "d₁(x) = 2x₁ + 1x₂ − 1 · d₂(x) = 1x₁ + 3x₂ − 2 · d₃(x) = −1x₁ + 2x₂ + 1\n"
    "Para el patrón x = (2, 3): d₁ = 4 + 3 − 1 = **6**; d₂ = 2 + 9 − 2 = **9**; "
    "d₃ = −2 + 6 + 1 = **5**. El mayor valor lo produce d₂, así que **x ∈ ω₂**.\n"
    "Interpretación de los subíndices: en wᵢⱼ el primero indica a qué clase pertenece el "
    "peso y el segundo qué característica multiplica. Y los pesos indican cuánto influye "
    "cada característica: en d₂ el peso de x₂ es 3 contra 1 de x₁, así que x₂ pesa más "
    "dentro de esa función; en d₁ pasa lo contrario.")
para(doc,
     "**En la práctica.** El notebook __Clasificación – Parte 3__ (Clase 3) construye un "
     "problema de **tres clases** —riesgo crediticio bajo, medio y alto, a partir de "
     "ingresos y deudas— y lo resuelve con un clasificador lineal multiclase. Lo "
     "interesante es la estrategia que usa por debajo:")
code(doc, '''# Definimos las clases según una regla simple:
#  - Bajo riesgo: ingresos altos y deudas bajas
#  - Alto riesgo: ingresos bajos y deudas altas
y = []
for inc, deu in zip(ingresos, deudas):
    if inc > 80 and deu < 30:
        y.append(0)      # Bajo riesgo
    elif inc < 50 and deu > 50:
        y.append(2)      # Alto riesgo
    else:
        y.append(1)      # Riesgo medio

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3,
                                                    random_state=57)
# La Regresión Logística, por defecto, maneja problemas multiclase
# con la estrategia "Uno contra todos" (One-vs-Rest):
# esto significa que entrenará 3 clasificadores lineales binarios.''')
para(doc,
     "Ahí está la conexión con la teoría de arriba: **«uno contra todos» entrena tres "
     "clasificadores binarios, uno por clase**, y cada uno aporta su función "
     "discriminante dᵢ(x). La predicción final aplica exactamente la regla "
     "x ∈ ωᵢ si dᵢ(x) = máx dⱼ(x) — se queda con la clase cuyo clasificador responde con "
     "más confianza. Las tres regiones del espacio de entrada no se definen de una vez, "
     "sino que **emergen de comparar tres funciones**.")
box(doc, "Un resultado que conviene no leer mal",
    "El mismo notebook repite el ejercicio sobre el conjunto **Iris** (150 flores, tres "
    "especies, cuatro medidas) y reporta **83,33 % de precisión sobre los datos de "
    "entrenamiento**.\n"
    "Es un número que hay que leer con cuidado por dos motivos. Primero, está medido "
    "**sobre los datos de entrenamiento**, así que no dice nada sobre la capacidad de "
    "generalización: es el error de entrenamiento, no el de prueba ([[u2_5|sección 2.5]]). "
    "Segundo, en Iris el resultado es esperable — *setosa* se separa linealmente de las "
    "otras dos sin esfuerzo, pero *versicolor* y *virginica* se solapan, y esa frontera "
    "es la que ningún clasificador lineal resuelve del todo. El 17 % de error está "
    "concentrado ahí.")

h(doc, 2, "2.8 Clasificador lineal y función de decisión generalizada", "u2_7")
fig("d04_modelos.png",
       "Todos los modelos de clasificación de la unidad son variaciones sobre "
       "un mismo problema: cómo trazar la frontera.")
para(doc,
     "El caso más simple de función de decisión es la **lineal**: "
     "d(x) = w₁x₁ + … + wₙxₙ + wₙ₊₁, donde los coeficientes wᵢ ∈ ℝ son los parámetros del "
     "clasificador. Es útil calcular d(x) como un producto entre vectores; para eso se "
     "redefine x como **vector de entradas aumentado** xᵀ = [x₁, …, xₙ, 1], con lo cual "
     "d(x) = w·x. El **bias** o término independiente permite desplazar el hiperplano "
     "respecto del origen: sin él, el límite queda obligado a pasar por el origen.")
para(doc,
     "El entrenamiento ajusta w minimizando el error cuadrático medio. Partiendo de la "
     "derivada del MSE respecto de los parámetros se obtiene la solución cerrada")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
_fmt(p.add_run("w = (X Xᵀ)⁻¹ X y     (ecuaciones normales)"), bold=True, size=12,
     color=MORADO_OSC)
para(doc,
     "donde X es la matriz formada por los vectores de entrada. Un sistema de "
     "clasificación lineal para dos clases separables **puede calcularse "
     "matemáticamente en forma precisa**. Para dimensión 2, la frontera d(x) = 0 es una "
     "recta; para 3 características un plano; para n, un hiperplano.")
para(doc,
     "**En la práctica.** El notebook __Clasificador – Parte 1__ (Clase 2) resuelve esa "
     "fórmula **paso a paso con NumPy**, sin llamar a ninguna librería de aprendizaje "
     "automático, sobre cuatro puntos etiquetados (0,0)→1, (0,1)→1, (1,0)→−1 y (1,1)→−1. "
     "Vale la pena seguirlo porque cada línea es un factor de las ecuaciones normales:")
code(doc, '''mat_entrada = np.array([[0,0], [0,1], [1,0], [1,1]])
y = np.array([1, 1, -1, -1])

X = np.hstack((mat_entrada, np.ones((mat_entrada.shape[0],1))))  # entrada aumentada
XT = np.transpose(X)
XP = np.matmul(XT, X)        # XᵀX
XI = np.linalg.inv(XP)       # (XᵀX)⁻¹
XP2 = np.matmul(XI, XT)      # (XᵀX)⁻¹Xᵀ  <- la pseudoinversa
w = np.matmul(XP2, y)
print(w)

y_r = np.matmul(X, w)        # verificacion
print(y_r)''')
salida(doc, '''[-2.  0.  1.]
[ 1.  1. -1. -1.]''')
para(doc,
     "El resultado es exacto: `y_r` reproduce las cuatro etiquetas sin error. Y los "
     "coeficientes dicen algo interesante — **w₂ = 0**, o sea que la función de decisión "
     "queda d(x) = −2x₁ + 1 y **la segunda característica no interviene**. La frontera es "
     "la recta vertical x₁ = 0,5. Tiene sentido: en esos datos la clase depende sólo de "
     "x₁, y el método lo descubre solo, poniendo en cero el peso de la variable inútil.")
box(doc, "El detalle de implementación que esto obliga a mirar",
    "Cuando w₂ = 0 la fórmula habitual para dibujar la frontera, "
    "x₂ = −(w₁x₁ + w₃)/w₂, **divide por cero**. Por eso el código del notebook "
    "pregunta antes:\n"
    "si el coeficiente es distinto de cero traza la recta como función de x₁, y si es "
    "cero dibuja una **recta vertical** en x₁ = −w₃/w₁. Es un buen recordatorio de que la "
    "frontera de decisión no siempre se puede escribir como «x₂ en función de x₁»: la "
    "forma general d(x) = 0 sí cubre todos los casos.")
para(doc,
     "El mismo notebook encapsula después esas cinco líneas en una clase con la interfaz "
     "de scikit-learn, y comprueba que `LinearRegression` de la librería llega **al mismo "
     "resultado** — coeficientes [−2, 0] e intercepto 1,0, con precisión 1.0. Es la "
     "confirmación de que la librería no hace magia: resuelve las mismas ecuaciones "
     "normales.")
code(doc, '''class ClasificadorLineal:
    def __init__(self):
        self.w = np.zeros(1)

    def fit(self, X, y):
        X_a = np.hstack((X, np.ones((X.shape[0],1))))   # vector de entradas aumentado
        aux = np.matmul(np.transpose(X_a), X_a)
        aux = np.linalg.inv(aux)
        aux = np.matmul(aux, np.transpose(X_a))
        self.w = np.matmul(aux, y)

    def get_w(self):
        return(self.w)''')
box(doc, "La gran limitación",
    "Como la frontera entre las clases es una recta (o un hiperplano), **este "
    "clasificador sólo puede separar clases linealmente separables**, y la mayoría de "
    "los problemas reales no lo son. Un caso todavía más complejo y muy frecuente es "
    "cuando los patrones de cada clase están, a su vez, distribuidos en múltiples "
    "clústeres.")
para(doc,
     "El enfoque que se deriva directamente del clasificador lineal para resolverlo es la "
     "**función de decisión generalizada**: d(x) = w₁f₁(x) + … + w_q f_q(x) + w_{q+1}, "
     "donde cada fᵢ(x) es una función real simple del vector de entradas completo. Si "
     "x = (x₁, x₂) se puede elegir f₁ = 1, f₂ = x₁, f₃ = x₂, f₄ = x₁², f₅ = x₂², "
     "f₆ = x₁x₂, y la función de decisión queda "
     "d(x) = w₁ + w₂x₁ + w₃x₂ + w₄x₁² + w₅x₂² + w₆x₁x₂: **ya no es lineal respecto de las "
     "características originales y puede producir una frontera curva**. A este caso "
     "particular se lo llama **clasificador polinomial**.")
para(doc,
     "Lo elegante del truco es que, para calcular los coeficientes, primero se transforma "
     "el vector de entradas en x* = [f₁(x), …, f_q(x), 1]ᵀ y entonces **el cálculo se "
     "reduce a la misma expresión que la del clasificador lineal**. ¿Por qué no usar "
     "siempre fronteras muy complejas? Porque pueden sobreajustar los datos, ser más "
     "costosas computacionalmente o perder capacidad de generalización.")
box(doc, "Parámetros vs. hiperparámetros",
    "Los coeficientes w son los **parámetros**, que se ajustan durante el aprendizaje "
    "(en redes neuronales, los pesos sinápticos). Existe además un conjunto de "
    "decisiones de mayor nivel que afecta el rendimiento: los **hiperparámetros**, que "
    "son las decisiones de diseño del modelo — qué funciones y cuántos términos usa un "
    "clasificador generalizado; en redes neuronales, la cantidad y tipo de capas, la "
    "cantidad de neuronas por capa, las funciones de activación, la tasa de aprendizaje. "
    "Se eligen con el conjunto de validación ([[u2_5|sección 2.5]]).")

h(doc, 2, "2.9 Máquinas de vectores de soporte (SVM)", "u2_8")
para(doc,
     "SVM es un método de clasificación/regresión desarrollado originalmente como método "
     "de clasificación binaria, cuya aplicación se extendió a clasificación múltiple y "
     "regresión. Es considerado **uno de los mejores clasificadores para un amplio "
     "abanico de situaciones**.")
bullets(doc, [
    "**Idea central**: entre todas las fronteras posibles, la SVM busca aquella **recta que quede lo más alejada posible de los puntos más cercanos de ambas clases**. De ahí se define el **margen**: la distancia entre la frontera de decisión y los puntos más cercanos de cada clase. En dos dimensiones es una recta, en tres un plano y en el caso N-dimensional un hiperplano.",
    "**Tolerancia a errores**: cuando las clases no son perfectamente separables hay puntos del lado equivocado y puntos dentro de la zona del margen. La SVM **no mueve la recta para clasificar bien esos puntos** porque hacerlo podría empeorar la separación global: no busca clasificar correctamente absolutamente todos los puntos, sino **un equilibrio entre margen grande y pocos errores**.",
    "**Funciones kernel**: si el problema no es lineal, se trasladan los datos a un espacio donde el hiperplano solución sí lo es. Un kernel K es una función que devuelve el resultado del producto punto entre dos vectores realizado **en un espacio dimensional distinto al original**. Dos grupos cuya separación en dos dimensiones no es lineal sí lo son al añadir una tercera dimensión.",
])
h(doc, 3, "Los kernels más usados", "u2_8a")
bullets(doc, [
    "**Kernel lineal**: K(x, x′) = x·x′. Con dos clases, la SVM compara x con el vector soporte positivo A y con el negativo B, combina esas comparaciones y decide qué clase tiene mayor influencia sobre x.",
    "**Kernel polinómico**: K(x, x′) = (x·x′ + c)^d. Con d = 1 y c = 0 el resultado es el mismo que el del kernel lineal. Con d > 1 se generan límites de decisión no lineales, y la no linealidad aumenta con d. **No suele ser recomendable usar valores de d mayores que 5 por problemas de sobreajuste.** Al ser polinómica, la función de decisión puede generar dos curvas y por lo tanto dos márgenes.",
    "**Kernel gaussiano o RBF** (*Radial Basis Function*): K(x, x′) = exp(−γ‖x − x′‖²). El valor de **γ** controla el comportamiento: cuando es muy pequeño el modelo final equivale al del kernel lineal, y a medida que aumenta también aumenta la flexibilidad del modelo. El RBF da mayor influencia a los puntos cercanos y una influencia cada vez menor a los lejanos, por lo que **puede construir una frontera cerrada alrededor de una región local**.",
])
para(doc,
     "Cada kernel tiene hiperparámetros cuyo valor óptimo se encuentra mediante "
     "**validación cruzada** ([[u2_5|sección 2.5]]), reservando el conjunto de test para la "
     "evaluación final. **No puede decirse que haya un kernel que supere al resto**: "
     "depende en gran medida de la naturaleza del problema.")
para(doc,
     "**En la práctica.** El notebook __Clasificación – Parte 4__ elige el caso más "
     "claro posible para mostrar qué hace un kernel: `make_circles` genera **dos "
     "círculos concéntricos**, uno dentro del otro. Ninguna recta puede separarlos —no "
     "por ruido, sino por geometría—, y sin embargo la SVM con kernel RBF los separa "
     "sin dificultad:")
code(doc, '''from sklearn.datasets import make_circles
from sklearn.svm import SVC   # Support Vector Classifier

# Usamos make_circles para crear dos círculos de datos, uno dentro del otro.
# Este es un caso clásico donde un clasificador lineal fallaría por completo.
X, y = make_circles(n_samples=100, factor=0.5, noise=0.1, random_state=42)

# 'rbf' (Radial Basis Function) es un kernel muy potente
# para capturar patrones no lineales complejos.
svm_model = SVC(kernel='rbf', gamma=2)
svm_model.fit(X, y)''')
para(doc,
     "Es la ilustración exacta de lo que dice la teoría sobre el RBF: al dar mucha "
     "influencia a los puntos cercanos y poca a los lejanos, **construye una frontera "
     "cerrada alrededor de una región local** — acá, una circunferencia alrededor del "
     "grupo interno, que es justamente la forma que el problema pide.\n"
     "Un kernel lineal sobre estos mismos datos está condenado de entrada: **cualquier "
     "recta que se trace deja de un mismo lado una parte del círculo interior y una "
     "parte del exterior**, así que necesariamente clasifica mal a una fracción "
     "importante de los puntos. No es cuestión de entrenar más tiempo ni de ajustar "
     "mejor la tasa de aprendizaje — es que la familia de fronteras que el modelo puede "
     "representar no contiene la solución.")
para(doc,
     "Para **regresión** valen los mismos principios: en lugar de una etiqueta se busca "
     "la curva que modele la tendencia de los datos —minimizando el error, como las SVM "
     "garantizan— y según ella se predice cualquier otro dato futuro. En problemas de "
     "regresión no lineales siempre es posible usar un kernel, donde la no linealidad "
     "aparece como una curva de predicción no lineal.")

ejemplo("Ejemplo · dos clases separables y una sola recta correcta",
        "Diez puntos en el plano, cinco de cada clase, claramente separables. Hay "
        "**infinitas rectas** que los separan sin cometer ningún error: todas tienen "
        "exactamente la misma precisión de entrenamiento, así que ningún criterio "
        "basado en errores puede elegir entre ellas.\n"
        "La SVM sí elige: se queda con la que **maximiza el margen**, es decir la que "
        "pasa lo más lejos posible de los puntos de ambas clases. Los tres puntos que "
        "quedan tocando el borde de ese margen son los **vectores de soporte**, y son "
        "los únicos que importan: si se corre cualquiera de los otros siete, la "
        "frontera no se mueve; si se corre uno de esos tres, sí.\n"
        "Ésa es la razón práctica de preferirla: entre dos clasificadores igual de "
        "buenos con los datos que tengo, el de margen más ancho es el que menos "
        "probablemente se equivoque con un dato nuevo que caiga cerca del límite.")
fig("e06_svm.png",
    "Muchas rectas separan; la SVM elige la del margen máximo.")

import u2_redes
u2_redes.escribir(doc, h, para, bullets, box, fig, ejemplo, code, salida)

h(doc, 2, "2.11 Aprendizaje profundo", "u2_10")
para(doc,
     "Es **la evolución de las redes neuronales artificiales**. El término enfatiza que "
     "ahora es posible entrenar redes con mayor cantidad de capas y pone el foco en la "
     "importancia de esa profundidad; va más allá de la perspectiva neurocientífica y "
     "apela a un principio más general de **aprendizaje compuesto de múltiples niveles**. "
     "Hoy la neurociencia se considera una fuente importante de inspiración, pero ya no "
     "es la guía predominante.")
box(doc, "Qué lo distingue de verdad",
    "Una de las particularidades que lo distinguen, y probablemente una de las causas de "
    "su buen desempeño, es la capacidad de **aprender representaciones complejas de "
    "características y ajustar los parámetros del clasificador al mismo tiempo**. Es "
    "decir: mientras en el esquema clásico de [[u2_1|reconocimiento de patrones]] la "
    "extracción de características es una etapa previa y separada, **en aprendizaje "
    "profundo la extracción de características ocurre dentro del mismo modelo que la "
    "clasificación**.\n"
    "El **neocognitrón**, creado por Fukushima en 1982, es considerado por muchos autores "
    "el primer modelo de aprendizaje profundo: reconoce caracteres manuscritos, se "
    "inspira en la naturaleza jerárquica del procesamiento en la corteza visual de los "
    "mamíferos y está formado por capas «simples» y «complejas» similares a las de "
    "convolución y pooling actuales. Recién en 1989 LeCun aplica retropropagación a un "
    "modelo muy parecido y comienza la nueva era.")
h(doc, 3, "Funciones de activación: el gradiente que se desvanece", "u2_10a")
para(doc,
     "Una de las complicaciones para entrenar redes con muchas capas es que **el "
     "gradiente de la función del error se desvanece a medida que se propaga**. La causa "
     "son las regiones de derivada casi nula de la sigmoidal y la tangente hiperbólica; "
     "el problema fue descubierto en los años 90. En 2011 Glorot et al. demostraron que "
     "la función **ReLU** (*Rectified Linear Unit*), f(z) = máx(0, z), reduce ese efecto, "
     "y con ella los modelos típicamente aprenden mucho más rápido. **A pesar de la gran "
     "cantidad de variantes, ReLU es la función de activación más popular.**")
bullets(doc, [
    "**Sigmoidal** — f(z) = 1/(1+e^−z); derivada f(z)(1−f(z)); rango [0, 1].",
    "**Tangente hiperbólica** — tanh(z); derivada 1 − tanh(z)²; rango [−1, 1].",
    "**ReLU** — máx(0, z); derivada 0 si f(z) ≤ 0 y 1 si f(z) > 0; rango [0, ∞).",
    "**Leaky ReLU** — 0,01z si z ≤ 0, z si z > 0. Mejora: derivada no nula para z < 0.",
    "**PReLU** (*parametric*) — αz si z ≤ 0, z si z > 0.",
    "**ELU** (*exponential*) — α(e^z − 1) si z ≤ 0, z si z > 0. Mejora: transición suave en z = 0; rango [−α, ∞).",
])
h(doc, 3, "Redes neuronales convolucionales (CNN)", "u2_10b")
para(doc,
     "Son un caso particular de red feed-forward **cuyas neuronas no están densamente "
     "conectadas**. Fueron diseñadas para procesar datos en forma de arreglos donde **la "
     "ubicación de los elementos es parte de la información** —los píxeles de una imagen, "
     "o un audio sin procesar (arreglo 1D) o su espectrograma (2D)—. Sobre este tipo de "
     "datos son mucho más fáciles de entrenar y generalizan mucho mejor que las redes "
     "sólo con capas densas.")
para(doc,
     "Hay **cuatro conceptos fundamentales** detrás de las CNN, que aprovechan las "
     "propiedades de las señales naturales: **conexiones locales, pesos compartidos, "
     "pooling y el uso de muchas capas**.")
bullets(doc, [
    "**Capas de convolución**: cada neurona hace una transformación lineal de sus entradas antes de la activación. Las neuronas se organizan en **mapas de características** (*feature maps*), dentro de los cuales cada unidad se conecta a regiones determinadas de los mapas de la capa anterior a través de un conjunto de pesos llamado **kernel** o *filter bank*. **Todas las neuronas del mismo mapa comparten el mismo kernel**; mapas distintos usan kernels diferentes. Cada neurona no se conecta a todo, sino que tiene un **campo receptivo** acotado.",
    "**Por qué esta arquitectura**: primero, en un arreglo los grupos locales de valores frecuentemente forman patrones fácilmente detectables; segundo, **las distribuciones estadísticas locales de las imágenes son invariantes a la ubicación** — si un patrón puede aparecer en una parte del arreglo, puede aparecer en cualquiera. De ahí la idea de que neuronas en distintas ubicaciones compartan los mismos pesos.",
    "**Hiperparámetros de la convolución**: además del tamaño del kernel hay que definir los **strides** (pasos de desplazamiento vertical y horizontal) y qué pasa con los bordes. Como la máscara no puede tener elementos fuera del espacio de la entrada, es común agregar elementos nulos alrededor: **padding**. Las librerías manejan dos tipos: *valid* (la máscara sólo se posiciona en lugares válidos de la entrada original) y *same* (se agregan tantos ceros como sean necesarios para que el mapa de salida tenga el mismo tamaño que la entrada).",
    "**Capas de pooling**: mecánica similar, pero **no se ajustan, no tienen pesos y no cambian durante el entrenamiento**. La salida de cada elemento es el máximo (*max pooling*) o el promedio (*average pooling*) de su campo receptivo. Mientras la convolución detecta conjunciones locales de características, **el pooling fusiona varias características semánticamente similares en una**: hace un «granulado grueso» de la posición, reduce la dimensión de la representación y aporta invariancia a pequeños cambios y distorsiones.",
])
para(doc,
     "En las CNN es común combinar capas de convolución intercaladas con capas de pooling "
     "(extracción de características) y **capas densas al final** (clasificación). "
     "Retropropagar el gradiente a través de una CNN es tan simple como a través de una "
     "red densa. El ejemplo canónico es **LeNet-5** (LeCun et al., 1998), para "
     "reconocimiento de caracteres: dos capas de convolución (la primera con 6 mapas y la "
     "segunda con 16), dos de pooling y tres densas.")
ejemplo("Ejemplo · una convolución 3×3 calculada a mano",
        "Una imagen de 5×5 donde las dos columnas de la izquierda valen 0 (oscuro) y "
        "las tres de la derecha valen 9 (claro): o sea, un **borde vertical** justo en "
        "el medio. El filtro es la matriz 3×3 con las columnas [1, 0, −1] repetidas en "
        "las tres filas.\n"
        "En la primera posición el filtro cubre el bloque superior izquierdo, donde las "
        "dos primeras columnas son 0 y la tercera es 9. La cuenta es "
        "(1·0)+(0·0)+(−1·9) repetido tres veces = **−27**. Un valor grande en módulo: "
        "ahí hay un borde. Cuando el filtro se corre hasta quedar íntegramente sobre la "
        "zona clara, todos los términos se cancelan y la salida es **0**: no hay borde.\n"
        "Dos cosas para retener. Primera: la salida es 3×3, no 5×5 — sin **padding** la "
        "imagen se achica en cada convolución, y ése es justamente el problema que el "
        "padding resuelve. Segunda: **estos nueve pesos no se programan**, se aprenden; "
        "nadie le dice a la red «buscá bordes verticales».")
fig("e09_convolucion.png",
    "Una convolución 3×3 detectando un borde vertical, calculada paso a paso.")

h(doc, 3, "Regularización", "u2_10c")
para(doc,
     "Las redes profundas son modelos complejos, con muchos parámetros, lo que las hace "
     "**propensas al sobreajuste**. Goodfellow et al. definen regularización como "
     "«cualquier modificación que podemos hacer sobre un algoritmo de aprendizaje con el "
     "objetivo de reducir su error de generalización pero no su error de entrenamiento». "
     "El foco no está en mejorar el resultado sobre los datos de entrenamiento, **sino en "
     "reducir la brecha entre entrenamiento y validación**.")
bullets(doc, [
    "**Early stop**: después de cierto punto el error de entrenamiento sigue bajando pero el de validación empieza a subir. En lugar de tomar la configuración final de los pesos, cada vez que mejora el error de validación se almacena una copia de los parámetros; al terminar se devuelven **esos** y no los últimos. El algoritmo finaliza cuando no hubo mejora durante un número preestablecido de iteraciones.",
    "**Penalización**: se agregan restricciones a los valores de los parámetros como términos adicionales en la función objetivo, llamados **regularizadores** Ω(w). Las más usadas son **L1** (Ω = β Σ|wᵢ|), **L2** (Ω = β √(Σ|wᵢ|²)) y la combinación de ambas. Importante: **se regularizan los pesos pero no el bias**, porque el bias requiere menos datos para ajustarse (controla una sola variable, no la interacción entre dos) y regularizarlo podría inducir infra-ajuste.",
    "**Dropout**: durante el entrenamiento **se eliminan al azar algunas neuronas de las capas ocultas**; en cada ciclo, con una probabilidad definida por capa, se eligen ciertas neuronas y se anulan sus salidas. Srivastava et al. demostraron que es más efectivo que otras estrategias de regularización de bajo costo, como la penalización, y puede combinarse con ellas reforzando la mejora.",
    "**Aumentación de datos**: la mejor manera de mejorar la generalización es entrenar con más datos; como en la práctica son limitados, se crean datos nuevos. La tarea principal de un clasificador es **ser invariante ante una amplia variedad de transformaciones**, así que se generan nuevos pares (x, y) aplicando a x exactamente las transformaciones frente a las cuales se pretende ser invariante. En imágenes: rotación, *flipping*, cambios de color, cambio de escala, *cropping*, traslación y adición de ruido. En audio: cambios de tono, *time stretching*, filtrado de frecuencias o transformaciones que simulan variaciones de la longitud del tracto vocal.",
])

page_break(doc)

# =================================================================== UNIDAD 3
h(doc, 1, "Unidad 3 · Razonamiento en ambientes deterministas 1", "u3")
para(doc,
     "Veinticuatro horas de programa para el caso en que **no hay datos etiquetados "
     "pero sí un espacio de estados bien definido**. Cubre problemas y espacios "
     "problema, sistemas de producción y estrategias de control, las tres familias de "
     "búsqueda (no informada, informada y local), la planificación y las "
     "metaheurísticas.")
box(doc, "Una diferencia de ordenamiento con el apunte",
    "El apunte de cátedra pone la **planificación** en la misma unidad que la lógica, "
    "argumentando que conviene definir antes los predicados de primer orden. El "
    "**programa analítico la ubica acá**, junto con la búsqueda, y este documento "
    "sigue el programa. La razón de fondo del programa es sólida: planificar es buscar "
    "en un espacio de estados: lo que cambia es que el estado y las acciones están "
    "descriptos en un lenguaje explícito en vez de ser una caja negra.")

h(doc, 2, "3.1 El problema de búsqueda: nodos, frontera y criterios", "u3_1")
para(doc,
     "Resolver un problema por búsqueda es recorrer el **espacio de estados** mediante un "
     "**árbol de búsqueda** generado por el estado inicial y la función sucesor. La raíz "
     "es el nodo de búsqueda correspondiente al estado inicial; **expandir** un estado es "
     "aplicarle la función sucesor y generar un nuevo conjunto de estados. La esencia de "
     "la búsqueda es **llevar a cabo una opción y dejar de lado las demás para más "
     "tarde**, por si la primera no conduce a una solución. Qué estado se expande lo "
     "determina la **estrategia de búsqueda**.")
box(doc, "Nodo no es lo mismo que estado",
    "Un **nodo** es una estructura de datos usada para representar el árbol de búsqueda, "
    "con cinco componentes: ESTADO, NODO-PADRE, ACCIÓN, COSTO-DEL-CAMINO g(n) y "
    "PROFUNDIDAD. Un **estado** corresponde a una configuración del mundo. Los nodos "
    "están en caminos particulares; los estados no. Por eso, en la búsqueda de ruta en "
    "Rumanía **hay sólo 20 estados —uno por ciudad— pero infinitos caminos**, así que el "
    "árbol de búsqueda tiene infinitos nodos.\n"
    "La colección de nodos generados pero todavía no expandidos se llama **frontera**; "
    "cada elemento de la frontera es un **nodo hoja**. Se implementa como una **cola**, y "
    "el tipo de cola es lo que define la estrategia.")
para(doc, "El rendimiento de una estrategia se evalúa de cuatro formas:")
bullets(doc, [
    "**Completitud**: ¿está garantizado que encuentre una solución cuando exista?",
    "**Optimalidad**: ¿encuentra la solución óptima?",
    "**Complejidad en tiempo**: ¿cuánto tarda? Se mide en número de nodos generados.",
    "**Complejidad en espacio**: ¿cuánta memoria necesita? Se mide en máximo número de nodos almacenados.",
])
para(doc,
     "La complejidad se expresa con tres cantidades: **b**, el factor de ramificación; "
     "**d**, la profundidad del nodo objetivo más superficial; y **m**, la longitud "
     "máxima de cualquier camino en el espacio de estados.")
box(doc, "Dos correcciones que el apunte hace al libro",
    "1. Donde el libro dice «los algoritmos son no informados, en el sentido que no dan "
    "información sobre el problema salvo su definición», **debería decir «…en el sentido "
    "que no *usan* información sobre el problema salvo su definición»**.\n"
    "2. En la sección 3.3 el libro define el factor de ramificación como «el máximo "
    "número de sucesores de cualquier nodo», pero **debería decir «la cantidad media de "
    "sucesores»**.")
ejemplo("Ejemplo · el espacio de estados de la aspiradora, completo",
        "Volvamos al agente de la [[u1_7|Unidad 1]], ahora en su versión de **dos "
        "celdas** (A y B), que es la del libro. Un estado queda determinado por tres "
        "cosas: si A está sucia, si B está sucia y dónde está el agente. Eso da "
        "2 × 2 × 2 = **ocho estados**, y sólo tres acciones: aspirar, izquierda y "
        "derecha.\n"
        "El espacio de estados entero entra en una figura. Buscar una solución es "
        "encontrar un camino desde el estado inicial hasta cualquiera de los dos "
        "estados donde ambas celdas están limpias.\n"
        "Y acá se ve, en un caso mínimo, la distinción entre **estado** y **nodo**: "
        "hay ocho estados, pero infinitos nodos, porque el agente puede ir y volver de "
        "A a B para siempre generando caminos cada vez más largos sobre los mismos "
        "ocho estados. Ése es exactamente el problema que resuelve la lista cerrada de "
        "[[u3_3|la sección sobre estados repetidos]].")
fig("e11_espacio_estados.png",
    "Los ocho estados de la aspiradora de dos celdas y las transiciones entre ellos.")

h(doc, 2, "3.2 Sistemas de producción y estrategias de control", "u3_prod")
para(doc,
     "El programa nombra los **sistemas de producción** junto a los espacios problema, "
     "y con razón: son la otra manera de escribir lo mismo. En vez de definir el "
     "problema con una función sucesor opaca, se lo define con un conjunto de **reglas "
     "de producción** —reglas condición-acción— que operan sobre una memoria.")
bullets(doc, [
    "**Base de reglas** (memoria a largo plazo): el conjunto de reglas «SI ⟨condición⟩ ENTONCES ⟨acción⟩». La palabra *producción* denota justamente una regla de condición-acción.",
    "**Memoria de trabajo** (memoria a corto plazo): los hechos que se conocen del caso actual. Las reglas se emparejan contra estos hechos.",
    "**Ciclo de ejecución**: en cada paso se emparejan las producciones con los hechos de la memoria de trabajo; una producción cuyas condiciones se satisfacen puede **añadir o eliminar hechos** de esa memoria. Se repite hasta que ninguna regla aplica o se alcanza la meta.",
])
para(doc,
     "A diferencia de una base de datos típica, los sistemas de producción suelen tener "
     "**muchas reglas y relativamente pocos hechos**. Con la tecnología de "
     "emparejamiento adecuadamente optimizada —las **redes rete**, que capturan en su "
     "estado todos los emparejamientos parciales y evitan recalcularlos— algunos "
     "sistemas modernos operan sobre **un millón de reglas en tiempo real**.")
para(doc,
     "Cuando **más de una regla** puede dispararse a la vez, ese conjunto se llama "
     "**conjunto conflicto**, y hace falta un criterio para desempatar: eso es la "
     "**estrategia de control**. Su papel es exactamente el mismo que el del tipo de "
     "cola en un algoritmo de búsqueda —FIFO da anchura, LIFO da profundidad—: decide "
     "el orden en que se explora el espacio, y por lo tanto decide si el sistema "
     "encuentra la solución rápido, lento o nunca. Criterios habituales son la "
     "prioridad explícita, preferir la regla más específica, o preferir la que usa los "
     "hechos agregados más recientemente.")
box(doc, "Dónde se usaron de verdad",
    "Los sistemas de producción fueron **el tipo de sistema de encadenamiento hacia "
    "adelante de uso más generalizado**. **XCON** —originalmente R1— se construyó con "
    "una arquitectura de sistema de producción y contenía varios miles de reglas para "
    "configurar computadores a los clientes de Digital Equipment Corporation; fue uno "
    "de los primeros éxitos comerciales claros de los [[u4_exp|sistemas expertos]] "
    "([[u4|Unidad 4]]). Muchos sistemas similares se implementaron sobre el lenguaje "
    "**OPS-5**.\n"
    "También son populares en las **arquitecturas cognitivas** —modelos del "
    "razonamiento humano como **ACT** y **SOAR**—, donde la memoria de trabajo modela "
    "la memoria a corto plazo y las reglas la memoria a largo plazo.")
ejemplo("Ejemplo · la aspiradora escrita como sistema de producción",
        "Las mismas ocho filas de la tabla de la [[u1_7|Unidad 1]], ahora como tres "
        "reglas generales:\n"
        "**R1**: SI En(x) ∧ Sucio(x) ENTONCES Aspirar.\n"
        "**R2**: SI En(x) ∧ ¬Sucio(x) ∧ Sucio(y) ENTONCES Ir(y).\n"
        "**R3**: SI ninguna celda está sucia ENTONCES Detenerse.\n"
        "Con la memoria de trabajo {En(A), Sucio(A), Sucio(B)}, **R1 y R2 tienen las "
        "condiciones satisfechas al mismo tiempo**: ése es el conjunto conflicto. La "
        "estrategia de control desempata; si el criterio es «la regla más específica "
        "primero», gana R1 y el agente aspira. Con el criterio contrario, el agente se "
        "iría a B dejando A sucia — y con el mismo conjunto de reglas obtendríamos un "
        "agente peor.\n"
        "Tres reglas cubren lo que antes eran ocho filas, y siguen cubriéndolo si la "
        "grilla pasa a ser de 3×3. Ésa es la ventaja de las reglas sobre la tabla.")
fig("e12_produccion.png",
    "Reglas, memoria de trabajo, conjunto conflicto y estrategia de control.")

h(doc, 2, "3.3 Estrategias de búsqueda no informada", "u3_2")
para(doc,
     "**No informada** —o *a ciegas*— significa que no se tiene información adicional "
     "sobre los estados más allá de la que da la definición del problema: sólo se pueden "
     "generar sucesores y distinguir un estado objetivo de uno que no lo es. **Todas las "
     "estrategias se distinguen por el orden de expansión de los nodos.**")
fig("d06_busqueda.png",
       "Las estrategias de búsqueda y las garantías de cada una.")
bullets(doc, [
    "**Primero en anchura**: expande el nodo raíz, luego todos sus sucesores, luego los sucesores de éstos. Se implementa con una **cola FIFO**. Es **completa** si b es finito y **óptima si el costo del camino es una función no decreciente de la profundidad** (por ejemplo, si todas las acciones cuestan lo mismo). Tiempo y espacio O(b^(d+1)).",
    "**Costo uniforme**: en vez del nodo más superficial, expande el nodo n con **el camino de costo más pequeño g(n)**. Si todos los costos son iguales es idéntica a primero en anchura. Es **óptima con cualquier función de costo**, siempre que cada paso cueste al menos una constante positiva ε (esa condición también garantiza completitud, y evita el bucle infinito de una acción de costo cero que devuelva al mismo estado).",
    "**Primero en profundidad**: expande siempre el nodo más profundo de la frontera; se implementa con una **pila LIFO** o recursivamente. Necesita almacenar sólo un camino de la raíz a una hoja más los hermanos no expandidos: **O(b·m)**. Su inconveniente es que puede hacer una elección equivocada y seguir un camino muy largo o infinito: **no es óptima ni completa**. En el peor caso genera O(b^m) nodos, y m puede ser mucho mayor que d.",
    "**Profundidad limitada**: primero en profundidad con un límite ℓ predeterminado. Resuelve el problema del camino infinito, pero **introduce incompletitud si ℓ < d** y deja de ser óptima si ℓ > d. A veces el límite sale del conocimiento del problema: en el mapa de Rumanía hay 20 ciudades, pero cualquier ciudad se alcanza desde otra en nueve pasos como mucho — ese número es el **diámetro** del espacio de estados.",
    "**Profundidad iterativa**: aplica repetidamente profundidad limitada aumentando el límite (0, 1, 2, …) hasta encontrar el objetivo. **Combina las ventajas de las dos primeras**: memoria O(b·d) y tiempo O(b^d).",
    "**Bidireccional**: ejecuta dos búsquedas simultáneas, una hacia delante desde el inicio y otra hacia atrás desde el objetivo, parando cuando se encuentran. Tiempo y espacio O(b^(d/2)). **El requerimiento de espacio es su debilidad más significativa**, porque al menos uno de los árboles debe mantenerse en memoria para comprobar la pertenencia.",
])
box(doc, "Por qué la profundidad iterativa no es tan derrochadora como parece",
    "Regenera estados, sí, pero en un árbol con factor de ramificación parecido en cada "
    "nivel **la mayor parte de los nodos está en el nivel inferior**, así que no importa "
    "mucho que los niveles superiores se generen varias veces. Con b = 10 y d = 5:\n"
    "N(profundidad iterativa) = 50 + 400 + 3.000 + 20.000 + 100.000 = **123.450**\n"
    "N(primero en anchura) = 10 + 100 + 1.000 + 10.000 + 100.000 + 999.990 = **1.111.100**\n"
    "Resulta que la profundidad iterativa es en realidad **más rápida** que la primero en "
    "anchura, porque ésta genera además los nodos del nivel d+1. Por eso es **el método "
    "no informado preferido cuando el espacio es grande y no se conoce la profundidad de "
    "la solución**.")
ejemplo("Ejemplo · el mismo árbol, dos órdenes de expansión",
        "Un árbol binario de tres niveles: la raíz A, sus hijos B y C, y los nietos D, "
        "E, F, G.\n"
        "**Primero en anchura** (cola FIFO) los expande por niveles: "
        "A → B → C → D → E → F → G. Si la solución estuviera en C, la encuentra en el "
        "tercer paso.\n"
        "**Primero en profundidad** (pila LIFO) baja hasta el fondo antes de volver: "
        "A → B → D → E → C → F → G. A C recién llega en el quinto paso, pero en ningún "
        "momento tuvo más de tres nodos guardados, mientras que anchura llegó a tener "
        "cuatro hojas simultáneas.\n"
        "El árbol es idéntico y el algoritmo es el mismo: **lo único que cambia es el "
        "tipo de cola**. Toda la diferencia de garantías y de consumo de memoria sale "
        "de ese único detalle.")
fig("e13_arbol_busqueda.png",
    "El mismo árbol expandido en anchura y en profundidad.")

h(doc, 2, "3.4 Evitar estados repetidos", "u3_3")
para(doc,
     "Para algunos problemas la repetición de estados es inevitable: todos aquellos donde "
     "**las acciones son reversibles**, como la búsqueda de rutas y los puzles de piezas "
     "deslizantes. Sus árboles de búsqueda son infinitos, pero podando estados repetidos "
     "se los recorta a un tamaño finito. La diferencia es brutal: en una **rejilla "
     "rectangular** cada estado tiene cuatro sucesores, así que el árbol con repeticiones "
     "tiene 4^d hojas, pero **hay sólo 2d² estados distintos a d pasos**. Para d = 20 eso "
     "es aproximadamente un billón de nodos contra unos 800 estados distintos.")
para(doc,
     "El algoritmo **BÚSQUEDA-GRAFOS** agrega una estructura llamada **lista cerrada** "
     "que almacena cada nodo expandido (a la frontera se la llama entonces *lista "
     "abierta*); si el nodo actual coincide con uno de la lista cerrada se elimina en vez "
     "de expandirlo. La frase del libro que resume el problema: **«los algoritmos que "
     "olvidan su historia están condenados a repetirla»** — pero hay una compensación "
     "fundamental entre espacio y tiempo.")

h(doc, 2, "3.5 Heurística y búsqueda informada", "u3_4")
para(doc,
     "La palabra «heurística» deriva del verbo griego *heuriskein*, que significa "
     "«encontrar» o «descubrir». **En el contexto de búsqueda en IA, una heurística es "
     "una técnica que aumenta la eficiencia de un proceso de búsqueda, posiblemente "
     "sacrificando demandas de completitud.** Se implementa como una función que recibe "
     "un estado del problema y devuelve una estimación del grado de bondad de dicho "
     "estado. En términos generales las funciones heurísticas **no garantizan la solución "
     "óptima, pero frecuentemente ayudan a llegar a una buena solución**.")
para(doc,
     "El marco general es la **búsqueda primero el mejor**: se selecciona para expansión "
     "el nodo con menor valor de una **función de evaluación** f(n), usando una cola con "
     "prioridad. El componente clave es la **función heurística h(n)** = costo estimado "
     "del camino más barato desde n hasta un nodo objetivo, con la única restricción de "
     "que h(n) = 0 si n es objetivo.")
bullets(doc, [
    "**Voraz primero el mejor**: f(n) = h(n). Expande el nodo que *parece* más cercano al objetivo. En el mapa de Rumanía con la distancia en línea recta encuentra la solución sin expandir nodos fuera del camino, **pero no es óptima**: el camino vía Sibiu y Fagaras es 32 km más largo que el vía Rimnicu Vilcea y Pitesti. Además **es incompleta**: puede irse por un camino infinito. Complejidad O(b^m) en el peor caso.",
    "**Búsqueda A-estrella (A*)**: f(n) = g(n) + h(n) — el costo real hasta n más el costo estimado desde n al objetivo, es decir, **el costo más barato estimado de la solución a través de n**.",
])
h(doc, 3, "Cuándo A* es óptima", "u3_4a")
bullets(doc, [
    "Con **BÚSQUEDA-ÁRBOLES**, A* es óptima si h es **admisible**, es decir, **si nunca sobrestima el costo de alcanzar el objetivo**. Las heurísticas admisibles son por naturaleza optimistas. La distancia en línea recta es admisible porque el camino más corto entre dos puntos es una recta.",
    "Con **BÚSQUEDA-GRAFOS** hace falta más: **consistencia** (o *monotonía*). h es consistente si para cada nodo n y cada sucesor n′ generado por una acción a se cumple **h(n) ≤ c(n, a, n′) + h(n′)** — una forma de la desigualdad triangular. Toda heurística consistente es también admisible, y hay que trabajar bastante para inventar una que sea admisible pero no consistente.",
])
para(doc,
     "La consecuencia clave de la consistencia es que **los valores de f(n) no disminuyen "
     "a lo largo de ningún camino**, de modo que A* expande los nodos en orden no "
     "decreciente de f y el primer nodo objetivo seleccionado es la solución óptima. Eso "
     "permite dibujar **curvas de nivel** en el espacio de estados: A* busca hacia afuera "
     "desde el nodo inicial añadiendo nodos en bandas concéntricas de f creciente. Con "
     "h = 0 (costo uniforme) las bandas son circulares; con heurísticas más precisas se "
     "estiran hacia el objetivo. Si C* es el costo óptimo: A* expande todos los nodos con "
     "f(n) < C* y podría expandir algunos con f(n) = C* antes de seleccionar el objetivo. "
     "Los nodos con f(n) > C* quedan **podados**.")
box(doc, "El techo de A*",
    "A* es completa, óptima y **óptimamente eficiente**: ningún otro algoritmo óptimo "
    "garantiza expandir menos nodos. Y sin embargo no resuelve todo. Para la mayoría de "
    "los problemas el número de nodos dentro de la curva de nivel del objetivo sigue "
    "siendo exponencial en la longitud de la solución, salvo que el error de la "
    "heurística no crezca más rápido que el logaritmo del costo real del camino — "
    "condición que en la práctica casi nunca se cumple.\n"
    "Pero el tiempo no es su desventaja principal: como mantiene en memoria todos los "
    "nodos generados, **A* por lo general se queda sin espacio antes que sin tiempo**. De "
    "ahí las variantes de memoria acotada: **A*PI** (profundidad iterativa donde el corte "
    "es el f-costo en lugar de la profundidad) y **BRPM** (búsqueda recursiva del primero "
    "mejor, que usa espacio lineal recordando el f-valor del mejor camino alternativo "
    "disponible desde cualquier antepasado del nodo actual).")
ejemplo("Ejemplo · A* sobre un grafo de cinco nodos",
        "Un grafo con S (inicio), G (meta) y tres intermedios. Costos reales: "
        "S→A = 1, A→C = 2, C→G = 2 (total 5) y S→B = 4, B→G = 3 (total 7). "
        "Heurísticas: h(S) = 5, h(A) = 4, h(B) = 3, h(C) = 2, h(G) = 0.\n"
        "A* expande siempre el menor f = g + h:\n"
        "**1º S** — g = 0, h = 5, **f = 5**.\n"
        "**2º A** — g = 1, h = 4, **f = 5**.  (B queda en la frontera con g = 4, h = 3, "
        "**f = 7**.)\n"
        "**3º C** — g = 3, h = 2, **f = 5**.\n"
        "**4º G** — g = 5, h = 0, **f = 5** → solución encontrada, costo 5.\n"
        "**B nunca se expande.** Su f de 7 siempre fue mayor que el de los nodos del "
        "camino bueno, así que quedó podado sin que el algoritmo tuviera que explorar "
        "qué hay más allá. Eso es lo que ahorra la heurística — y como h nunca "
        "sobrestimó el costo real, el ahorro no costó la optimalidad.")
fig("e14_astar.png",
    "A* expandiendo por f creciente: el nodo B queda podado.")

h(doc, 2, "3.6 Cómo se inventan heurísticas admisibles", "u3_5")
para(doc,
     "El ejemplo canónico es el **8-puzle**, uno de los primeros problemas de búsqueda "
     "heurística. El costo medio de solución para casos generados al azar es de unos 22 "
     "pasos y el factor de ramificación es aproximadamente 3, de modo que una búsqueda "
     "exhaustiva a profundidad 22 miraría unos 3,1 × 10¹⁰ estados (reducibles a 181.440 "
     "estados distintos alcanzables si se controlan los repetidos). Dos heurísticas "
     "clásicas:")
bullets(doc, [
    "**h₁ = número de piezas mal colocadas.** Es admisible porque cualquier pieza fuera de lugar debe moverse por lo menos una vez.",
    "**h₂ = suma de las distancias de las piezas a sus posiciones objetivo** (*distancia de Manhattan* o «distancia en la ciudad», porque las piezas no se mueven en diagonal). También es admisible, porque cualquier movimiento acerca una pieza un solo paso a su destino.",
])
para(doc,
     "**h₂ domina a h₁**: para cualquier nodo n, h₂(n) ≥ h₁(n). La dominación se traslada "
     "directamente a la eficiencia — A* con h₂ nunca expandirá más nodos que con h₁. En "
     "los experimentos del libro, con soluciones de longitud 14, **A* con h₂ es 30.000 "
     "veces más eficiente que la búsqueda de profundidad iterativa**. La conclusión "
     "general es que **siempre es mejor usar una heurística con valores más altos, a "
     "condición de que no sobrestime y de que calcularla no sea demasiado caro**.")
ejemplo("Ejemplo · h₁ y h₂ contadas sobre el mismo tablero",
        "Tablero actual (de arriba a abajo y de izquierda a derecha): "
        "**7 2 4 / 5 _ 6 / 8 3 1**. Objetivo: **_ 1 2 / 3 4 5 / 6 7 8**.\n"
        "**h₁ — fichas mal colocadas.** Se recorren las ocho fichas y ninguna está en "
        "su casilla objetivo, así que **h₁ = 8**.\n"
        "**h₂ — distancia Manhattan.** Se cuenta, ficha por ficha, cuántas casillas "
        "horizontales y verticales le faltan recorrer: la 1 está en la esquina inferior "
        "derecha y va arriba al medio, 3 pasos; la 2 necesita 1; la 3 necesita 2; la 4, "
        "2; la 5, 2; la 6, 3; la 7, 3; la 8, 2. Total: 3+1+2+2+2+3+3+2 = **h₂ = 18**.\n"
        "Las dos son admisibles: la solución real de este tablero son 26 movimientos, y "
        "ni 8 ni 18 lo sobrestiman. Pero **18 está mucho más cerca de 26 que 8**, y por "
        "eso h₂ poda muchísimos más nodos. Ésa es la dominación, vista en un caso "
        "concreto: entre dos heurísticas admisibles, siempre conviene la más grande.")
fig("e15_8puzzle.png",
    "Las dos heurísticas del 8-puzle contadas sobre el mismo tablero.")
box(doc, "El método: relajar el problema",
    "h₁ y h₂ son estimaciones para el 8-puzle, pero son **longitudes de camino "
    "exactas para versiones simplificadas** del puzle. Un problema con menos "
    "restricciones en las acciones se llama **problema relajado**, y el costo de la "
    "solución óptima de un problema relajado es una heurística admisible para el "
    "original — y además consistente, porque cumple la desigualdad triangular.\n"
    "Si las acciones se describen como «una ficha puede moverse de A a B si A es "
    "adyacente a B **y** B está vacío», quitando condiciones se obtienen tres problemas "
    "relajados. De «A es adyacente a B» sale **h₂**; de «una ficha puede moverse a "
    "cualquier lado» sale **h₁**. Es crucial que el problema relajado se resuelva "
    "esencialmente sin búsqueda: si es difícil de resolver, calcular la heurística sale "
    "caro.\n"
    "Otras dos fuentes: el costo de la solución de un **subproblema** (colocar sólo las "
    "fichas 1-2-3-4 en su lugar) almacenado en un **modelo de bases de datos**; y si se "
    "dispone de varias heurísticas admisibles sin que ninguna domine, "
    "**h(n) = máx{h₁(n), …, h_m(n)}** es admisible, consistente y domina a todas.")

h(doc, 2, "3.7 Planificación", "u3_plan")
para(doc,
     "La planificación clásica trabaja en ambientes **deterministas, completamente "
     "observables, finitos, estáticos y discretos**. Nace de tres limitaciones concretas "
     "que tiene un agente solucionador de problemas puro cuando se enfrenta a entornos "
     "reales:")
bullets(doc, [
    "**Acciones irrelevantes.** Con una acción de compra por cada ISBN de 10 dígitos hay 10 billones de acciones, y el algoritmo de búsqueda tendría que examinar los resultados de todas para encontrar la que satisface el objetivo. Un planificador que trabaja con expresiones de objetivos explícitas —*Tener(ISBN…)*— genera la acción *Comprar(ISBN…)* directamente, con sólo saber que «Comprar(x) se reduce a Tener(x)».",
    "**Falta de heurística.** Para comprar cuatro libros hay 10⁴⁰ planes de cuatro etapas. Un humano estimaría el costo como «cuántos libros faltan comprar», pero esa idea no es obvia para un agente que evalúa el objetivo como una caja negra. Un planificador con acceso a la representación explícita del objetivo puede usar una heurística independiente de dominio: **el número de conjunciones insatisfechas**.",
    "**Imposibilidad de descomponer.** Repartir maletas por toda Australia se resuelve mejor dividiendo por aeropuerto. En el peor caso, entregar n paquetes es O(n!), pero **sólo O((n/k)! · k) si el problema se descompone en k partes iguales**. Los problemas perfectamente descomponibles no son frecuentes, así que los planificadores se apoyan en que la mayoría sea **prácticamente descomponible**: se puede trabajar en subobjetivos de forma independiente, aunque haga falta trabajo adicional para combinar los subplanes.",
])
fig("d09_planificacion.png",
       "El problema de planificación y las cuatro maneras de atacarlo.")
h(doc, 3, "El lenguaje STRIPS", "u3_plan_a")
bullets(doc, [
    "**Representación de estados**: un estado es una conjunción de **literales positivos**, sin variables y sin dependencias funcionales (no se permite *En(x, y)* ni *En(Padre(Fred), Sydney)*). Se asume la **hipótesis de mundo cerrado**: todo lo que no se menciona en un estado se asume falso.",
    "**Representación de objetivos**: un objetivo es un **estado parcialmente especificado**, una conjunción de literales positivos y simples. Un estado s **satisface** un objetivo g si s contiene todos los elementos de g (y posiblemente otros): *Rico ∧ Famoso ∧ Miserable* satisface *Rico ∧ Famoso*.",
    "**Representación de acciones**: un **esquema de acción** tiene tres partes — el nombre con su lista de parámetros, la **precondición** (conjunción de literales positivos que debe ser verdad antes de ejecutarla) y el **efecto** (conjunción de literales que describe cómo cambia el estado; los positivos van a la *lista Añadir* y los negativos a la *lista Borrar*). Todas las variables de precondición y efecto deben aparecer en la lista de parámetros.",
])
para(doc,
     "Una acción es **aplicable** en cualquier estado que satisfaga sus precondiciones. "
     "El resultado de ejecutarla es el mismo estado salvo que se agregan los literales "
     "positivos del efecto y se eliminan los negativos. Esto expresa la **hipótesis "
     "STRIPS**: *cada literal no mencionado en el efecto permanece sin modificar* — que "
     "es exactamente cómo STRIPS evita el problema del marco.")
para(doc,
     "La **solución** es, en su forma más sencilla, una secuencia de acciones que, "
     "ejecutada desde el estado inicial, da un estado final que satisface el objetivo. "
     "Existen extensiones más expresivas: **ADL** (permite literales negativos, hipótesis "
     "de mundo abierto, variables cuantificadas y disyunciones en los objetivos, efectos "
     "condicionales, igualdad y tipos) y **PDDL**, la sintaxis estándar que permite "
     "intercambiar problemas y resultados entre investigadores.")
h(doc, 3, "Progresión, regresión y orden parcial", "u3_plan_b")
bullets(doc, [
    "**Progresión** (búsqueda hacia delante): parte del estado inicial. Una única función sucesor sirve para todos los problemas de planificación, y **sin símbolos funcionales el espacio de estados es finito**, así que cualquier algoritmo de búsqueda en grafos completo (A*, por ejemplo) es un planificador completo. Pero es **ineficaz en la práctica**: no puede tratar las acciones irrelevantes y se empantana sin buena heurística. En el problema de carga aérea con 10 aeropuertos, 50 aviones y 200 paquetes hay unas 1.000 acciones posibles en promedio, y el árbol para la solución obvia tiene del orden de 1.000⁴¹ nodos.",
    "**Regresión** (búsqueda hacia atrás): su principal ventaja es que **permite considerar sólo acciones relevantes** — aquellas que alcanzan alguno de los objetivos. En el mismo problema de carga aérea hay unas 1.000 acciones hacia delante desde el estado inicial, pero **sólo 20 acciones hacia atrás desde el objetivo**. Una búsqueda hacia atrás que permitiera acciones irrelevantes sería completa pero mucho menos eficiente.",
    "**Planificación de orden parcial (POP)**: las dos anteriores exploran secuencias estrictamente lineales, así que no aprovechan la descomposición. POP aplica una **estrategia de mínimo compromiso**: aplaza las decisiones de orden y trabaja primero en las decisiones obvias o importantes. Un plan tiene cuatro componentes: un conjunto de **acciones** (el plan vacío contiene sólo *Iniciar* y *Finalizar*), un conjunto de **restricciones ordenadas** A ≺ B («A antes de B», no necesariamente inmediatamente antes; cualquier ciclo es una contradicción), un conjunto de **relaciones causales** A →p B («A alcanza B a través de p») y las precondiciones abiertas. La solución **se representa como un grafo de acciones, no como una secuencia**; cada orden total compatible es una **linealización**. El ejemplo mínimo son los zapatos y calcetines: una solución de orden parcial que corresponde a seis planes de orden total.",
])
h(doc, 3, "Grafos de planificación y GRAPHPLAN", "u3_plan_c")
para(doc,
     "Todas las heurísticas anteriores pueden sufrir imprecisiones. Un **grafo de "
     "planificación** da mejores estimaciones, y además permite **extraer una solución "
     "directamente** con el algoritmo GRAPHPLAN. Consiste en una secuencia de **niveles** "
     "que corresponden a escalones de tiempo, con el nivel 0 en el estado inicial. Cada "
     "nivel contiene un conjunto de literales y un conjunto de acciones:")
bullets(doc, [
    "Los **literales** son todos aquellos que *pueden* ser ciertos en esa etapa, dependiendo de las acciones ejecutadas antes.",
    "Las **acciones** son todas aquellas que *pueden* tener sus precondiciones satisfechas en esa etapa.",
    "Se dice «pueden» porque el grafo **sólo registra un subconjunto restringido de las posibles interacciones negativas** entre acciones. Por eso es **optimista** sobre el número mínimo de etapas necesarias, y por eso el nivel en que aparece un literal es una **cota inferior** de la dificultad de alcanzarlo — buena estimación heurística. Lo importante es que se construye **muy eficientemente**: su complejidad es de orden polinomial bajo, mientras que el espacio de estados es exponencial en el número de literales.",
])
para(doc,
     "Para representar la ausencia de acción se agregan **acciones persistentes**: para "
     "cada literal C, una acción con precondición C y efecto C (el equivalente a los "
     "axiomas del marco). Los **enlaces de exclusión mutua** registran qué pares no pueden "
     "darse juntos. Entre dos **acciones** hay exclusión mutua si se cumple alguna de "
     "estas condiciones: **efectos inconsistentes** (una niega el efecto de la otra), "
     "**interferencia** (un efecto de una es la negación de una precondición de la otra) "
     "o necesidades en competencia. El grafo se expande alternando niveles S y A hasta "
     "que dos niveles consecutivos son idénticos: entonces se dice que **está "
     "estabilizado**. Los grafos de planificación funcionan sólo sobre problemas "
     "proposicionales, pero tanto STRIPS como ADL pueden proposicionalizarse.")
box(doc, "Precisión sobre la fuente de esta sección",
    "El apunte indica leer, para planificación, el capítulo 11 de Russell y Norvig "
    "**hasta la página 439** y el capítulo 13 de Rich, Knight y González Calero, "
    "*Inteligencia artificial* (McGraw-Hill, 1994) **hasta la página 379**, y aclara que "
    "**en caso de conflicto entre los libros hay que usar las definiciones y "
    "nomenclatura de Rich y Knight**. Ese segundo libro no está entre el material "
    "convertido de este vault, así que toda esta sección está desarrollada sobre Russell "
    "y Norvig. Ver [[apA|Apéndice A]].")
ejemplo("Ejemplo · tres bloques sobre una mesa",
        "El mundo de los bloques, que es el ejemplo mínimo de planificación. Estado "
        "inicial: **A sobre C**, C sobre la mesa, B sobre la mesa. Objetivo: la torre "
        "**A sobre B sobre C**.\n"
        "En STRIPS el estado inicial se escribe como conjunción de literales positivos: "
        "Sobre(A, C) ∧ SobreMesa(C) ∧ SobreMesa(B) ∧ Libre(A) ∧ Libre(B). El objetivo "
        "es un estado *parcialmente* especificado: Sobre(A, B) ∧ Sobre(B, C) — no dice "
        "nada de qué hay sobre la mesa, y no hace falta.\n"
        "Hay un solo esquema de acción, **Mover(b, x, y)**, con precondición "
        "Sobre(b, x) ∧ Libre(b) ∧ Libre(y) y efecto Sobre(b, y) ∧ Libre(x) ∧ "
        "¬Sobre(b, x) ∧ ¬Libre(y).\n"
        "El plan tiene tres pasos: **Mover(A, C, Mesa)** — hay que sacar A de encima "
        "para poder usar C; **Mover(B, Mesa, C)**; **Mover(A, Mesa, B)**.\n"
        "El primer paso es el que muestra por qué planificar no es trivial: **hay que "
        "deshacer algo que ya estaba** (A ya estaba apilado) para poder construir el "
        "objetivo. Y notar la hipótesis STRIPS en acción: después de mover A nadie tuvo "
        "que declarar que B sigue sobre la mesa — todo lo que la acción no menciona "
        "queda igual, y eso es lo que evita el problema del marco.")
fig("e18_bloques.png",
    "Estado inicial, objetivo, esquema de acción y plan en el mundo de los bloques.")

h(doc, 2, "3.8 Metaheurísticas", "u3_6")
para(doc,
     "A menudo resulta **imposible calcular soluciones óptimas** para problemas de "
     "optimización con importancia industrial o científica. Como ya se vio en esta unidad, "
     "muchas veces un agente inteligente puede estar satisfecho con soluciones buenas que "
     "no son óptimas o de las que no se puede comprobar que lo sean. **Las metaheurísticas "
     "son una familia de técnicas de optimización aproximada que proporcionan soluciones "
     "aceptables en un tiempo razonable para problemas complejos.**")
para(doc,
     "El sufijo «meta» es una palabra griega que significa «después» o «más allá», y se "
     "usa para hacer referencia a una abstracción de nivel superior: indica que hay un "
     "procedimiento heurístico que **hace uso de otra heurística**. Se las puede pensar "
     "como **métodos de búsqueda de nivel superior o metodologías generales (*templates*) "
     "que sirven de estrategia guía en el diseño de las heurísticas subyacentes**.")
fig("d07_metaheuristicas.png",
       "Los dos criterios en tensión y los cinco ejes de clasificación.")
para(doc, "Al diseñar una metaheurística hay que tener en cuenta **dos criterios "
          "contradictorios**:")
bullets(doc, [
    "**Diversificación (exploración)**: visitar regiones no exploradas para asegurarse de que todas las regiones del espacio se exploren de manera equitativa y la búsqueda no se limite a una zona reducida.",
    "**Intensificación (explotación)**: explorar más a fondo las regiones prometedoras —determinadas a partir de las buenas soluciones ya obtenidas— con la esperanza de encontrar mejores soluciones.",
])
h(doc, 3, "Los cinco ejes de clasificación", "u3_6a")
bullets(doc, [
    "**Inspiradas en la naturaleza vs. no inspiradas**: algoritmos evolutivos y sistemas inmunitarios artificiales (biología); colonias de hormigas, colonias de abejas y enjambres de partículas (ciencias sociales); enfriamiento o recocido simulado (física).",
    "**Con memoria vs. sin memoria**: algunas no usan información extraída durante la búsqueda —búsqueda local, **GRASP** y enfriamiento simulado—; otras sí, como la **búsqueda tabú**, que recuerda movimientos recientes y los prohíbe temporalmente.",
    "**Deterministas vs. estocásticas**: en las deterministas (búsqueda local, búsqueda tabú) el mismo punto de partida lleva siempre a la misma solución final. Las estocásticas (enfriamiento simulado, algoritmos evolutivos) pueden tomar decisiones distintas ante la misma situación, lo que da mayor variabilidad en los caminos de búsqueda.",
    "**Basadas en población vs. basadas en una solución**: las de una sola solución (búsqueda local, enfriamiento simulado) manipulan y transforman una única solución y **están orientadas a la explotación**; las basadas en población (enjambre de partículas, algoritmos evolutivos) adaptan todo un conjunto y **están orientadas a la exploración**. Son características complementarias.",
    "**Iterativas vs. voraces (*greedy*)**: las iterativas comienzan con una solución completa (o población) y la transforman en cada iteración; las voraces parten de una solución vacía y en cada paso asignan una variable de decisión hasta obtener una solución completa. **La mayoría de las metaheurísticas son iterativas.**",
])
box(doc, "Cuándo NO usar una metaheurística",
    "La respuesta depende de la complejidad del problema —O(g(n))— y del tamaño de las "
    "instancias. Incluso si un problema es NP-duro, **instancias pequeñas pueden "
    "resolverse con un método exacto**, y algunas instancias medianas o grandes con "
    "estructura específica también.\n"
    "**No es prudente usar metaheurísticas para resolver problemas que tienen algoritmos "
    "exactos eficientes (clase P).** Por ejemplo, no se debe usar una metaheurística para "
    "encontrar un árbol de expansión mínimo o el camino más corto en un grafo, porque "
    "existen algoritmos exactos polinómicos conocidos. El apunte es explícito: "
    "«desafortunadamente, se puede ver a muchos profesionales resolviendo problemas de "
    "optimización de complejidad polinómica con metaheurísticas y otros métodos de IA».\n"
    "**La primera guía es siempre analizar la complejidad del problema.** Si se puede "
    "reducir a un problema clásico ya resuelto en la literatura, conviene usar el "
    "algoritmo conocido.")

h(doc, 2, "3.9 Búsqueda local y algoritmos genéticos", "u3_7")
para(doc,
     "En muchos problemas **el camino al objetivo es irrelevante**: en las 8 reinas lo que "
     "importa es la configuración final, no el orden en que se colocaron. Esta clase "
     "incluye diseño de circuitos integrados, disposición del suelo de una fábrica, "
     "programación de trabajo, optimización de redes de telecomunicaciones y gestión de "
     "carteras. Los **algoritmos de búsqueda local** trabajan con un solo estado actual y "
     "se mueven sólo a sus vecinos, sin retener los caminos. No son sistemáticos, pero "
     "tienen dos ventajas clave: **usan muy poca memoria** (por lo general una cantidad "
     "constante) y **encuentran soluciones razonables en espacios grandes o infinitos** "
     "donde los algoritmos sistemáticos son inadecuados.")
bullets(doc, [
    "**Ascensión de colinas** (*hill climbing*): se mueve siempre al vecino de mejor valor; se la llama también **búsqueda local voraz**. Hace progreso muy rápido pero **se atasca** en máximos locales, mesetas y crestas. Variantes: ascensión estocástica, de primera opción, y **de reinicio aleatorio** (una serie de búsquedas desde estados iniciales aleatorios; si cada una tiene probabilidad p de éxito, se necesitan en promedio 1/p reinicios).",
    "**Recocido o temple simulado** (*simulated annealing*): una ascensión de colinas que nunca baja se atasca; una que sólo se mueve al azar es completa pero ineficiente. El temple simulado combina ambas. En metalurgia, templar es calentar un metal y enfriarlo gradualmente para que alcance un estado cristalino de energía baja. **En vez de escoger el mejor movimiento se escoge uno al azar, y se lo acepta con una probabilidad que decrece según un parámetro de «temperatura»**. A principios de los 80 se lo usó ampliamente para el diseño de circuitos VLSI.",
])
ejemplo("Ejemplo · el paisaje donde la ascensión de colinas se equivoca",
        "Imaginemos el valor de cada solución dibujado como la altura de un terreno: "
        "una loma chica a la izquierda y una montaña más alta a la derecha. El agente "
        "arranca al pie de la loma chica.\n"
        "La **ascensión de colinas** sólo acepta vecinos mejores, así que sube la loma "
        "y **ahí se queda**: desde la cima, cualquier movimiento —hacia la izquierda o "
        "hacia la derecha— la empeora. El algoritmo termina anunciando una solución que "
        "es un **máximo local**, sin enterarse nunca de que existía la montaña.\n"
        "El **temple simulado** acepta a veces un movimiento que empeora, con "
        "probabilidad e^(−ΔE/T). Con T alta se mueve casi al azar y puede bajar de la "
        "loma y cruzar el valle (**diversificación**); a medida que T baja se vuelve "
        "cada vez más exigente y termina comportándose como la ascensión de colinas, "
        "afinando la mejor zona que encontró (**intensificación**).\n"
        "Ese es el sentido concreto de los dos criterios en tensión: no son una "
        "abstracción, son literalmente cuánto se está dispuesto a empeorar antes de "
        "mejorar.")
fig("e16_colinas.png",
    "Máximo local frente a máximo global, y cómo escapa el temple simulado.")

h(doc, 3, "Algoritmos genéticos", "u3_7a")
para(doc,
     "Un **algoritmo genético (AG)** es una variante de la búsqueda de haz estocástica en "
     "la que **los estados sucesores se generan combinando dos estados padres** en lugar "
     "de modificar un solo estado: la analogía es con la reproducción sexual en vez de la "
     "asexual. El ciclo, con el ejemplo de las 8 reinas del libro:")
bullets(doc, [
    "**Población inicial**: k estados generados aleatoriamente. Cada estado o **individuo** se representa como una cadena sobre un alfabeto finito (lo más común, cadenas de 0 y 1). Un estado de las 8 reinas requiere 8 × log₂8 = 24 bits, o bien 8 dígitos en el rango 1–8. *La codificación importa: no se comportan igual.*",
    "**Función de idoneidad** (*fitness*): tasa cada estado y **debe devolver valores más altos para estados mejores**. Para las 8 reinas se usa el número de pares de reinas no atacadas, que vale 28 en una solución. En el ejemplo del libro los cuatro estados valen 24, 23, 20 y 11.",
    "**Selección**: se eligen pares de manera aleatoria para la reproducción, **con probabilidad directamente proporcional al resultado de idoneidad** (en el ejemplo, 31 %, 29 %, 26 % y 14 %). Un individuo puede ser seleccionado dos veces y otro ninguna.",
    "**Cruce** (*crossover*): se elige aleatoriamente un punto de cruce y cada hijo toma los primeros dígitos de un padre y el resto del otro. Cuando los padres son bastante diferentes el cruce **puede producir un estado lejos de cualquiera de los dos**: al principio, con población diversa, da pasos grandes en el espacio de estados, y pasos más pequeños después, cuando los individuos se parecen.",
    "**Mutación**: cada posición está sujeta a mutación aleatoria con una pequeña probabilidad independiente. En las 8 reinas equivale a elegir una reina al azar y moverla a un cuadrado al azar de su columna.",
])
para(doc,
     "**De dónde viene la ventaja**: si las posiciones del código genético se permutan al "
     "principio en un orden aleatorio, puede demostrarse matemáticamente que **el cruce "
     "no comunica ninguna ventaja**. Intuitivamente, la ventaja viene de la capacidad del "
     "cruce para **combinar bloques grandes de letras que han evolucionado "
     "independientemente** y que realizan funciones útiles, aumentando el nivel de "
     "granularidad al que funciona la búsqueda. La teoría lo formaliza con la idea de "
     "**esquema**: una subcadena en la cual algunas posiciones quedan sin especificar "
     "(por ejemplo, poner las tres primeras reinas en las posiciones 2, 4 y 6, donde no "
     "se atacan, es un bloque útil).")
box(doc, "La advertencia",
    "El apunte cierra la sección remitiendo al comentario de Russell y Norvig sobre **la "
    "tendencia, a veces exagerada, a aplicar algoritmos genéticos**. El libro es claro: "
    "no está claro si lo solicitado de los algoritmos genéticos proviene de su "
    "rendimiento o de sus orígenes estéticamente agradables, y **su uso acertado requiere "
    "una ingeniería cuidadosa de la representación**. Conviene leerlo junto con «cuándo "
    "no usar una metaheurística» en [[u3_6|la sección de metaheurísticas]].")
ejemplo("Ejemplo · una generación completa maximizando f(x) = x²",
        "Buscamos el x entre 0 y 31 que maximiza x². Cada individuo es una cadena de "
        "**5 bits**, y la idoneidad es directamente f(x) = x². Población inicial de "
        "cuatro:\n"
        "01101 → x = 13 → f = **169** (14,4 % del total)\n"
        "11000 → x = 24 → f = **576** (49,2 %)\n"
        "01000 → x = 8 → f = **64** (5,5 %)\n"
        "10011 → x = 19 → f = **361** (30,9 %)\n"
        "Total 1170, promedio 292,5, máximo 576.\n"
        "**Selección** proporcional a la idoneidad: el segundo individuo se lleva dos "
        "copias, el tercero ninguna, los otros una cada uno. **Cruce** en dos pares: "
        "0110|1 con 1100|0 da 01100 (12) y 11001 (25); 11|000 con 10|011 da 11011 (27) "
        "y 10000 (16).\n"
        "Nueva generación: f = 144, 625, 729, 256. **Total 1754, promedio 438,5, máximo "
        "729.** En una sola generación el promedio subió un 50 % y apareció un "
        "individuo mejor que todos los iniciales — sin que nadie le explique al "
        "algoritmo qué significa «x grande». Eso es todo el mecanismo: la selección "
        "premia lo bueno y el cruce recombina las piezas que funcionan.")
fig("e17_genetico.png",
    "Selección, cruce y resultado de una generación de un algoritmo genético.")

page_break(doc)

# =================================================================== UNIDAD 4
h(doc, 1, "Unidad 4 · Razonamiento en ambientes deterministas 2", "u4")
para(doc,
     "Dieciséis horas para la otra mitad del razonamiento determinista: los **sistemas "
     "expertos** —cómo se construye un sistema que razona en un dominio acotado usando "
     "conocimiento humano codificado— y la **lógica** como formalismo de representación "
     "y como método de inferencia.")
para(doc,
     "Es la continuación natural de los [[u3_prod|sistemas de producción]] de la "
     "unidad anterior: allí las reglas condición-acción resolvían problemas de "
     "búsqueda; acá el mismo mecanismo se usa para **representar conocimiento y "
     "derivar conclusiones nuevas**.")

h(doc, 2, "4.1 Sistemas expertos", "u4_exp")
para(doc,
     "Un **sistema experto** es un programa que resuelve problemas en un dominio "
     "específico y acotado aplicando conocimiento obtenido de expertos humanos, "
     "codificado de forma explícita y **separado del mecanismo que razona sobre él**. "
     "Esa separación entre conocimiento y razonamiento es la lección central del "
     "primer sistema del género.")
h(doc, 3, "Tipos de problema y características del dominio", "u4_exp_a")
para(doc,
     "No cualquier problema se presta. Del recorrido histórico y de la práctica de la "
     "ingeniería del conocimiento salen las condiciones que debe cumplir el dominio:")
bullets(doc, [
    "**Debe existir un experto humano que resuelva el problema bien** y esté disponible para ser entrevistado. Si nadie sabe resolverlo, no hay conocimiento que extraer — y ése es el caso donde corresponde el [[u2|aprendizaje automático]] a partir de datos.",
    "**El dominio tiene que estar acotado y su rango de preguntas conocido de antemano.** El enfoque sirve para bases de conocimiento de propósito específico; las de propósito general, que pretenden cubrir todo el conocimiento humano, son un problema distinto y mucho más difícil.",
    "**El conocimiento debe poder expresarse como reglas.** DENDRAL funcionaba porque toda la información teórica necesaria se había podido proyectar desde su forma general a formas eficientes especiales — el propio Feigenbaum las llamó «recetas de cocina».",
    "**Los problemas típicos son de diagnóstico, clasificación, configuración e interpretación**: entrada un conjunto de observaciones, salida una categoría o una recomendación. DENDRAL infería la estructura molecular a partir de un espectro de masas; MYCIN diagnosticaba infecciones sanguíneas; R1/XCON configuraba pedidos de equipos informáticos.",
    "**Debe poder convivir con la incertidumbre**, porque el conocimiento experto rara vez es categórico. MYCIN incorporó los **factores de certeza** justamente porque las reglas tenían que reflejar la incertidumbre inherente al conocimiento médico. Los sistemas posteriores reemplazaron ese mecanismo por [[u5_5|redes bayesianas]].",
])
h(doc, 3, "Componentes", "u4_exp_b")
bullets(doc, [
    "**Base de conocimiento**: las reglas y los hechos generales del dominio. En MYCIN eran unas **450 reglas**; en XCON, varios miles.",
    "**Memoria de trabajo**: los hechos del caso concreto que se está resolviendo.",
    "**Motor de inferencia**: el mecanismo que aplica las reglas sobre los hechos, por [[u4_4a|encadenamiento hacia adelante]] o [[u4_4b|hacia atrás]].",
    "**Subsistema de explicación**: la capacidad de responder «por qué llegaste a esa conclusión» mostrando la cadena de reglas aplicadas. Es una de las ventajas de la codificación explícita frente a un modelo aprendido.",
    "**Subsistema de adquisición del conocimiento**: la interfaz por la que el ingeniero del conocimiento carga y depura las reglas.",
])
h(doc, 3, "El proceso de ingeniería del conocimiento", "u4_exp_c")
para(doc,
     "Construir la base de conocimiento es un proceso con nombre propio. Un **ingeniero "
     "del conocimiento** investiga el dominio, aprende qué conceptos importan y crea "
     "una representación formal de los objetos y relaciones. Russell y Norvig lo "
     "descomponen en siete pasos:")
bullets(doc, [
    "**1. Identificar la tarea.** Delimitar qué preguntas debe soportar la base y qué hechos estarán disponibles en cada instancia. *Este paso es análogo al proceso REAS del diseño de agentes* ([[u1_7|Unidad 1]]).",
    "**2. Recopilar el conocimiento relevante** — la **adquisición del conocimiento**. Acá el conocimiento todavía no se representa formalmente: se trata de entender el alcance y cómo funciona realmente el dominio. En dominios reales decidir qué es relevante puede ser bastante difícil.",
    "**3. Decidir el vocabulario** de predicados, funciones y constantes: traducir los conceptos del dominio a nombres del nivel lógico. El resultado es la **ontología** del dominio, que establece qué tipo de cosas existen (pero no sus propiedades específicas). Es una decisión de estilo con impacto significativo en el éxito del proyecto.",
    "**4. Codificar el conocimiento general** del dominio: escribir los axiomas de todos los términos del vocabulario. Esta fase suele revelar ideas equivocadas o lagunas, y obliga a volver al paso 3.",
    "**5. Codificar la instancia específica** del problema: sentencias atómicas simples sobre casos concretos. Si la ontología está bien pensada, es fácil.",
    "**6. Plantear las consultas** al procedimiento de inferencia y obtener respuestas. Es la fase donde se obtiene la recompensa.",
    "**7. Depurar la base de conocimiento.** Rara vez las respuestas son correctas al primer intento. Los **axiomas ausentes o demasiado débiles** se detectan mirando dónde se detiene inesperadamente la cadena de razonamiento; los **axiomas incorrectos** se detectan porque son enunciados falsos sobre el mundo, y —a diferencia de un error de programación típico— **se pueden identificar independientemente del resto de la base**.",
])
box(doc, "La ventaja de depurar conocimiento en vez de código",
    "Russell y Norvig marcan la diferencia con un ejemplo. La sentencia "
    "∀x NumPatas(x, 4) ⇒ Mamífero(x) es **falsa** —vale para reptiles, anfibios y, más "
    "importante, para las mesas— y eso puede determinarse sin mirar nada más. En "
    "cambio, para saber si la línea `offset = posición + 1` es correcta hay que revisar "
    "el resto del programa. Ésa es una de las razones prácticas para representar "
    "conocimiento declarativamente.")
fig("d11_expertos.png",
    "De dónde sale el conocimiento y qué componentes tiene un sistema experto.")
h(doc, 3, "Auge, límites y qué quedó", "u4_exp_d")
para(doc,
     "**DENDRAL** (1971) fue el primer sistema de conocimiento intenso que tuvo éxito: "
     "su base estaba formada por grandes cantidades de reglas de propósito particular. "
     "Su aporte duradero fue **la nítida separación del conocimiento —en forma de "
     "reglas— de la parte correspondiente al razonamiento**. **MYCIN** mostró que se "
     "podía diagnosticar tan bien como un experto, con reglas obtenidas de entrevistas "
     "extensas porque no había un modelo teórico del que deducirlas. **R1/XCON**, el "
     "primer sistema experto comercial exitoso, le ahorraba a Digital Equipment "
     "Corporation unos **40 millones de dólares al año** en 1986; para 1988 DEC tenía "
     "40 sistemas expertos desplegados y Du Pont un centenar.")
para(doc,
     "El límite es estructural: **un sistema experto no aprende de datos**. Todo lo que "
     "sabe hay que ponérselo a mano y mantenerlo a mano, y ese costo crece con el "
     "dominio. Es la misma pared con la que chocó la corriente simbólica "
     "([[u1_3|sección 1.4]]): la cantidad de programación necesaria terminaba superando la "
     "capacidad práctica de mantenimiento. La generación siguiente reemplazó los "
     "factores de certeza por **redes bayesianas**, y con **redes de decisión** los "
     "sistemas pasaron de responder preguntas a **recomendar decisiones** que ponderan "
     "probabilidad y utilidad.")
box(doc, "Probabilidad no es lo mismo que importancia",
    "Una estrategia corriente de los primeros sistemas expertos médicos era ordenar los "
    "diagnósticos por probabilidad y considerar el más probable. Eso puede dar "
    "resultados desastrosos: los dos diagnósticos más probables para la mayoría de los "
    "pacientes son «no tiene nada serio» o «tiene un resfriado», pero **si el tercero "
    "más probable es un cáncer de pulmón, se trata de un asunto grave**. Una prueba o "
    "un tratamiento debe depender tanto de la probabilidad como de la utilidad.")
ejemplo("Ejemplo · un sistema experto de tres reglas",
        "Dominio: por qué no arranca un auto. Base de conocimiento:\n"
        "**R1**: SI luces_apagadas ∧ arranque_mudo ENTONCES batería_descargada.\n"
        "**R2**: SI batería_descargada ENTONCES no_arranca.\n"
        "**R3**: SI tanque_vacío ENTONCES no_arranca.\n"
        "Hechos observados: luces_apagadas, arranque_mudo.\n"
        "**Hacia adelante**: se dispara R1 y se agrega batería_descargada a la memoria "
        "de trabajo; con ese hecho nuevo se dispara R2 y se concluye no_arranca. Se "
        "parte de los datos y se ve a dónde llevan.\n"
        "**Hacia atrás**: se parte de la hipótesis no_arranca y se busca qué reglas la "
        "concluyen — R2 y R3. R3 exige tanque_vacío: se pregunta, hay nafta, se "
        "descarta. R2 exige batería_descargada, que no es un hecho observado pero sí la "
        "conclusión de R1, cuyas dos premisas sí lo son. Confirmado.\n"
        "Y acá está la ventaja de tener el conocimiento explícito: el sistema puede "
        "**explicar** su respuesta — «no arranca porque la batería está descargada, y "
        "sé que está descargada porque las luces no encienden y el arranque no suena». "
        "Un modelo aprendido de datos daría la misma conclusión sin poder decir eso.")
fig("e19_experto_reglas.png",
    "Encadenamiento hacia adelante y hacia atrás sobre la misma base de reglas.")

h(doc, 2, "4.2 Agentes lógicos: sintaxis, semántica, implicación e inferencia", "u4_1")
fig("d08_logica.png",
       "El recorrido completo, de la base de conocimiento a la conclusión.")
bullets(doc, [
    "**Sintaxis**: especifica qué sentencias están bien formadas. En aritmética, «x + y = 4» lo está y «x2y+ =» no. Las sentencias de la base de conocimiento del agente son **configuraciones físicas reales** de sus partes, y el razonamiento consiste en generar y manipular esas configuraciones.",
    "**Semántica**: define el **valor de verdad** de cada sentencia respecto de cada **mundo posible**. Cuando hace falta ser preciso se usa el término **modelo** en lugar de mundo posible: los modelos son abstracciones matemáticas que permiten definir la verdad o falsedad de cada sentencia relevante. Se dice «m es un modelo de α» para indicar que α es verdadera en m.",
    "**Implicación (BC ⊨ α)**: α se sigue lógicamente de BC. Definición formal: **BC ⊨ α si y sólo si en cada modelo en el que BC es verdadera, α también lo es**. Informalmente, el valor de verdad de α «está contenido» en el de BC.",
    "**Inferencia (BC ⊢ᵢ α)**: el algoritmo i deriva α de BC. Si la implicación es la aguja que está en el pajar, **la inferencia es encontrarla**.",
])
para(doc, "A un algoritmo de inferencia se le piden dos propiedades:")
bullets(doc, [
    "**Solidez** (o mantenimiento de la verdad): deriva **sólo** sentencias implicadas. Un procedimiento no sólido «anunciaría el descubrimiento de agujas que no existen».",
    "**Completitud**: puede derivar **cualquier** sentencia que esté implicada. En pajares finitos parece obvio, pero en muchas bases de conocimiento el pajar de las consecuencias es infinito y la completitud pasa a ser una cuestión importante.",
])
para(doc,
     "El primer algoritmo, la **comprobación de modelos**, enumera todos los modelos "
     "posibles y verifica si α es verdadera en todos aquellos donde BC lo es. Es sólido, "
     "pero funciona bien sólo cuando **el espacio de modelos es finito** — en aritmética "
     "es infinito.")
box(doc, "La denotación: ¿cómo sabemos que la BC es verdadera en el mundo real?",
    "Después de todo, la BC sólo es «sintaxis» dentro de la cabeza del agente. La "
    "respuesta sencilla es que **los sensores crean la conexión**: el programa del agente "
    "crea una sentencia adecuada siempre que hay una percepción, y por lo tanto esa "
    "sentencia es verdadera en el mundo real. ¿Y el resto del conocimiento, como la regla "
    "general de que el wumpus causa mal hedor en las casillas adyacentes? Esas reglas se "
    "generan mediante un proceso de construcción de sentencias llamado **aprendizaje** "
    "([[u2|Unidad 2]]) — y **el aprendizaje es falible**.")

h(doc, 2, "4.3 Lógica proposicional", "u4_2")
bullets(doc, [
    "**Sentencias atómicas**: un único **símbolo proposicional** (P, Q, R…) que representa una proposición que puede ser verdadera o falsa. Hay dos con significado fijado: *Verdadero* y *Falso*. Un símbolo como W₁,₃ es atómico: W, 1 y 3 no son partes significantes.",
    "**Sentencias complejas**: se construyen con cinco **conectivas lógicas** — ¬ (negación), ∧ (conjunción), ∨ (disyunción), ⇒ (implicación) y ⇔ (bicondicional).",
    "**Literal**: una sentencia atómica (literal positivo) o una sentencia atómica negada (literal negativo).",
])
para(doc,
     "Ésa es la **sintaxis**: qué sentencias se pueden escribir. Falta la **semántica**, "
     "que son las reglas para determinar el **valor de verdad de una sentencia respecto "
     "de un modelo concreto**. En lógica proposicional un modelo es simplemente una "
     "asignación de verdadero o falso a cada símbolo. Si la base de conocimiento usa los "
     "símbolos H₁,₂, H₂,₂ y H₃,₁, un modelo posible es "
     "m₁ = {H₁,₂ = falso, H₂,₂ = falso, H₃,₁ = verdadero}. Con tres símbolos hay "
     "**2³ = 8 modelos posibles**, y con n símbolos hay 2ⁿ — un detalle que después "
     "explica por qué la inferencia por enumeración es cara.")
box(doc, "Los símbolos no significan nada por sí solos",
    "Una vez fijada la sintaxis, **los modelos son objetos puramente matemáticos, sin "
    "conexión necesaria con el mundo**. H₁,₂ es sólo un símbolo: puede denotar «hay un "
    "hoyo en la casilla [1,2]» o «estaré en París hoy y mañana». El significado se lo "
    "pone quien construye la base de conocimiento, no la lógica.")
para(doc,
     "El valor de verdad de una sentencia compleja se obtiene de forma **recursiva**: "
     "*Verdadero* es verdadero en todos los modelos, *Falso* es falso en todos, el valor "
     "de cada símbolo lo fija el modelo, y las conectivas se resuelven con la **tabla de "
     "verdad**, que reduce el cálculo de una sentencia compleja al de sus componentes.")
fig("e30_tabla_verdad.png",
    "Las cinco conectivas lógicas y su tabla de verdad.")
box(doc, "La implicación no significa lo que parece",
    "La fila que más confunde es la de ⇒. **P ⇒ Q es verdadera siempre que P sea "
    "falsa**, sin importar qué diga Q. Así, «si 5 es par, entonces Napoleón sigue vivo» "
    "es una sentencia **verdadera** en lógica proposicional.\n"
    "La razón es que P ⇒ Q **no afirma causalidad ni relevancia** entre P y Q, como sí "
    "hace el «si… entonces» del castellano. Sólo afirma que *no se da el caso de que P "
    "sea verdadera y Q falsa* — de hecho P ⇒ Q es lógicamente equivalente a ¬P ∨ Q. Con "
    "esa lectura la tabla deja de ser rara: la única forma de que la promesa se rompa es "
    "que P se cumpla y Q no.")
para(doc,
     "Con la semántica definida aparecen tres conceptos que se usan todo el tiempo y "
     "conviene no mezclar:")
bullets(doc, [
    "**Equivalencia lógica**: dos sentencias son equivalentes si tienen los mismos valores de verdad en el mismo conjunto de modelos (α ⇔ β). Por ejemplo P ∧ Q y Q ∧ P. Las equivalencias —conmutatividad, asociatividad, distributividad, De Morgan, doble negación— **juegan en la lógica el mismo papel que las igualdades en el álgebra**, y son las que permiten transformar una sentencia en forma normal conjuntiva ([[u4_3a|sección 4.4]]).",
    "**Validez**: una sentencia es válida si es verdadera en **todos** los modelos. Se las llama también **tautologías**; P ∨ ¬P es el ejemplo típico. Son necesariamente verdaderas y por lo tanto vacías de contenido informativo. Toda sentencia válida es equivalente a *Verdadero*.",
    "**Satisfacibilidad**: una sentencia es satisfacible si es verdadera **en algún** modelo. Se determina enumerando modelos hasta encontrar uno que la satisfaga. Si α es verdadera en m, se dice que *m satisface α* o que *m es un modelo de α*.",
])
box(doc, "Dos consecuencias que valen la pena",
    "**El teorema de la deducción** conecta implicación y validez: α ⊨ β si y sólo si la "
    "sentencia (α ⇒ β) es **válida**. Dicho de otro modo, preguntar si algo se deduce de "
    "la base de conocimiento es lo mismo que preguntar si (BC ⇒ α) es una tautología — y "
    "eso es exactamente lo que hace el algoritmo de inferencia por enumeración de "
    "modelos.\n"
    "**Validez y satisfacibilidad son dos caras de lo mismo**: α es válida si y sólo si "
    "¬α es insatisfacible. De ahí sale la demostración por refutación o *reducción al "
    "absurdo*, que es la base del método de resolución de la sección siguiente.\n"
    "Dato no menor: **determinar la satisfacibilidad en lógica proposicional fue el "
    "primer problema que se demostró NP-completo**. Muchos problemas de computación "
    "—entre ellos los de satisfacción de restricciones— son en el fondo problemas de "
    "satisfacibilidad.")
ejemplo("Ejemplo · verificar una inferencia con una tabla de verdad",
        "Sea la base de conocimiento **BC = {P ⇒ Q, P}** y la pregunta: ¿se deduce Q?\n"
        "Con dos símbolos hay cuatro modelos. Sólo hace falta mirar aquéllos en los que "
        "**toda** la BC es verdadera: (P=F, Q=F) hace P falsa, descartado; (P=F, Q=V) "
        "ídem; (P=V, Q=F) hace P ⇒ Q falsa, descartado; queda **(P=V, Q=V)**, el único "
        "modelo que satisface la BC entera. En ese modelo Q es verdadera, así que "
        "**BC ⊨ Q**.\n"
        "Ése es todo el algoritmo de inferencia por enumeración: recorrer los 2ⁿ modelos, "
        "quedarse con los que hacen verdadera la base de conocimiento y verificar que la "
        "conclusión valga en todos ellos. Es **correcto y completo**, y su problema es "
        "sólo el costo: con 30 símbolos ya son más de mil millones de modelos.")
box(doc, "Correcciones del apunte al libro (secciones 7.2, 7.4 y 7.5)",
    "· Pág. 222: donde dice «si el agente percibe un mal hedor **una** pequeña brisa» "
    "debería decir «un mal hedor **y** una pequeña brisa».\n"
    "· Pág. 230: dice que la notación BNF se explica en la página 984, pero en realidad "
    "se lo hace en la **1117**.\n"
    "· Pág. 236: donde dice «una sentencia es **satisfactoria** si es verdadera para "
    "algún modelo» debería decir **satisfacible**.\n"
    "· Pág. 238: donde dice «una característica denominada **monótono**» debería decir "
    "**monotonicidad**.")

h(doc, 2, "4.4 Reglas de inferencia y resolución", "u4_3")
para(doc,
     "Las **reglas de inferencia** son patrones estándar que permiten derivar cadenas de "
     "conclusiones. La más conocida es el **Modus Ponens**: de α ⇒ β y α se infiere β. "
     "Otra útil es la **Eliminación-∧**: de una conjunción se infiere cualquiera de sus "
     "conjuntores. Ambas son sólidas y **se pueden aplicar sin necesidad de enumerar "
     "todos los modelos**. Todas las equivalencias lógicas sirven también como reglas de "
     "inferencia, aunque **no todas se pueden usar en ambas direcciones**: no se puede "
     "aplicar Modus Ponens al revés para obtener α ⇒ β y α a partir de β.")
para(doc,
     "A una secuencia de aplicaciones de reglas de inferencia se la llama **prueba** o "
     "demostración. Obtener una prueba es muy parecido a encontrar una solución en un "
     "problema de búsqueda: si la función sucesor genera todas las aplicaciones posibles "
     "de las reglas, **todos los algoritmos de la [[u3|Unidad 3]] sirven para obtener una "
     "prueba**, hacia delante desde la BC o hacia atrás desde la sentencia objetivo.")
para(doc,
     "La inferencia proposicional es **NP-completa**, así que en el peor caso buscar una "
     "prueba no es mucho mejor que enumerar modelos. Pero en muchos casos prácticos es "
     "altamente eficiente, **simplemente porque el proceso puede ignorar las "
     "proposiciones irrelevantes, sin importar cuántas haya**: aunque se agregara un "
     "millón de sentencias a la base de conocimiento, la prueba no cambiaría; el "
     "algoritmo de la tabla de verdad, en cambio, quedaría saturado por la explosión "
     "exponencial de modelos.")
box(doc, "Monotonía",
    "Esa propiedad proviene de una característica más fundamental: la lógica clásica es "
    "**monótona**. El conjunto de sentencias implicadas **sólo puede aumentar**, nunca "
    "cambiar, al añadir información: si BC ⊨ α, entonces BC ∧ β ⊨ α. Conocimiento "
    "adicional puede ayudar a obtener conclusiones nuevas, pero **no puede invalidar "
    "ninguna conclusión ya inferida**. Eso es lo que permite aplicar una regla en cuanto "
    "sus premisas están en la BC, sin revisar todo lo demás.\n"
    "(Las lógicas **no monótonas**, que violan esta propiedad, modelan una característica "
    "muy humana: cambiar de opinión.)")
h(doc, 3, "Resolución y forma normal conjuntiva", "u4_3a")
para(doc,
     "Las reglas anteriores son sólidas, pero nada garantiza que un algoritmo que las use "
     "sea **completo**: si suprimimos una regla, la prueba puede volverse inalcanzable. "
     "La **resolución** es una regla de inferencia sencilla que, emparejada con un "
     "algoritmo de búsqueda completo, da un algoritmo de inferencia completo.")
para(doc,
     "La **resolución unitaria** toma una **cláusula** (una disyunción de literales) y un "
     "literal, y produce una nueva cláusula eliminando los **literales complementarios** "
     "(uno es la negación del otro). La **regla general de resolución** hace lo mismo con "
     "dos cláusulas: genera una cláusula nueva con los literales de las dos originales "
     "menos los complementarios. Ejemplo del mundo de wumpus: de H₁,₁ ∨ H₂,₂ ∨ H₃,₁ y "
     "¬H₂,₂ se obtiene H₁,₁ ∨ H₃,₁; y de ahí con ¬H₁,₁ se obtiene H₃,₁. Al proceso de "
     "eliminar copias múltiples de un literal se lo llama **factorización**: resolver "
     "(A ∨ B) con (A ∨ ¬B) da (A ∨ A), que se reduce a A.")
para(doc,
     "Como la resolución sólo se aplica a disyunciones de literales, hace falta que toda "
     "la BC esté en **forma normal conjuntiva (FNC)**: una conjunción de disyunciones de "
     "literales. Toda sentencia de la lógica proposicional es lógicamente equivalente a "
     "una FNC, y de hecho **cada sentencia se puede transformar en una 3-FNC** con un "
     "conjunto de modelos equivalente.")
box(doc, "En qué sentido «completa»",
    "La resolución es completa **en un sentido muy especializado**. Dado que A es "
    "verdadero, no se puede usar resolución para generar automáticamente la consecuencia "
    "A ∨ B; **sí se puede usar para responder si A ∨ B es verdadero**. Eso se llama "
    "**completitud de la resolución**: sirve siempre para *confirmar o refutar* una "
    "sentencia, pero no para *enumerar* sentencias verdaderas. De ahí que se la use por "
    "refutación: se agrega la negación de la consulta y se busca derivar la cláusula "
    "vacía (la contradicción).")

ejemplo("Ejemplo · una refutación por resolución, completa",
        "Base de conocimiento: «si llueve y Juan sale, Juan se moja»; «llueve»; «Juan "
        "sale». Queremos probar **M** (Juan se moja).\n"
        "**Paso 1 — pasar todo a forma clausal.** La implicación (Ll ∧ S) ⇒ M se "
        "reescribe como **¬Ll ∨ ¬S ∨ M**. Los otros dos hechos ya son cláusulas: **Ll** "
        "y **S**.\n"
        "**Paso 2 — negar lo que se quiere probar** y agregarlo: **¬M**.\n"
        "**Paso 3 — resolver.** ¬Ll ∨ ¬S ∨ M con Ll → **¬S ∨ M**. Eso con S → **M**. "
        "Y M con ¬M → **□**, la cláusula vacía.\n"
        "Llegar a la cláusula vacía significa que el conjunto es **insatisfacible**: no "
        "hay ningún modelo donde la base sea verdadera y M falsa. Por lo tanto la base "
        "implica M.\n"
        "Lo contraintuitivo del método es que **nunca demuestra M directamente**: "
        "demuestra que suponer lo contrario lleva a una contradicción. Por eso se lo "
        "llama *refutación*, y por eso el primer paso siempre es negar la conclusión.")
fig("e20_resolucion.png",
    "Refutación por resolución paso a paso hasta la cláusula vacía.")

h(doc, 2, "4.5 Cláusulas de Horn y encadenamiento", "u4_4")
para(doc,
     "Restringir la BC a **cláusulas de Horn** parece un tecnicismo, pero es muy "
     "importante por tres razones:")
bullets(doc, [
    "**Se leen como implicaciones.** Cada cláusula de Horn se escribe como una implicación cuya premisa es una conjunción de literales positivos y cuya conclusión es un único literal positivo: (¬L₁,₁ ∨ ¬Brisa ∨ B₁,₁) se reescribe como (L₁,₁ ∧ Brisa) ⇒ B₁,₁. Las cláusulas con **exactamente un** literal positivo se llaman **cláusulas positivas**; el literal positivo es la **cabeza** y la disyunción de literales negativos, el **cuerpo**. Una cláusula positiva sin literales negativos es un **hecho**.",
    "**Permiten encadenamiento**, hacia adelante y hacia atrás — dos algoritmos muy naturales, «en el sentido de que los pasos de inferencia son obvios y fáciles de seguir por las personas».",
    "**Averiguar si hay implicación se hace en tiempo lineal** respecto del tamaño de la base de conocimiento. El libro lo llama «una grata sorpresa»: significa que la inferencia lógica es un proceso barato para muchas bases de conocimiento del mundo real.",
])
h(doc, 3, "Encadenamiento hacia adelante", "u4_4a")
para(doc,
     "Determina si un símbolo q se deduce de una BC de cláusulas de Horn. **Comienza a "
     "partir de los hechos conocidos**: si todas las premisas de una implicación son "
     "conocidas, la conclusión se añade al conjunto de hechos. El proceso continúa hasta "
     "que se añade q o hasta que no se pueden hacer más inferencias. Se lo representa "
     "cómodamente con un **grafo Y-O**, donde múltiples enlaces se juntan mediante un arco "
     "para indicar conjunción: la propagación se detiene hasta que todos los conjuntores "
     "sean conocidos.")
para(doc,
     "Es **sólido** (cada inferencia es una aplicación de Modus Ponens) y **completo**: "
     "toda sentencia atómica implicada será derivada. La demostración pasa por el estado "
     "final de la tabla de inferidos, después de que el algoritmo alcanza un **punto "
     "fijo** a partir del cual no es posible realizar nuevas inferencias; ese conjunto "
     "define un modelo de la BC original.")
para(doc,
     "Es un ejemplo del **razonamiento dirigido por los datos**: el foco parte de los "
     "datos conocidos y se derivan conclusiones sin necesidad de una petición concreta. "
     "El ejemplo del libro es transparente: «si estoy en casa y oigo que comienza a "
     "llover, podría sucederme que la merienda quede cancelada; no será muy probable que "
     "el pétalo decimoséptimo de la rosa más alta del jardín de mi vecino se haya "
     "mojado». **Las personas llevan a cabo encadenamiento hacia adelante con un control "
     "cuidadoso, a fin de no hundirse en consecuencias irrelevantes.**")
h(doc, 3, "Encadenamiento hacia atrás", "u4_4b")
para(doc,
     "Trabaja **hacia atrás a partir de la petición**. Si q ya se sabe verdadera, no hay "
     "trabajo que hacer; si no, el algoritmo encuentra las implicaciones de las que se "
     "concluye q y, si puede probar que todas las premisas de alguna de ellas son "
     "verdaderas (recursivamente, hacia atrás), entonces q es verdadera. Es un tipo de "
     "**razonamiento dirigido por el objetivo**, útil para preguntas como «¿qué debo "
     "hacer ahora?» o «¿dónde están mis llaves?». **A menudo su costo es mucho menor que "
     "el orden lineal**, porque sólo trabaja con los hechos relevantes.")
para(doc,
     "En general, un agente debería repartir el trabajo: limitar el razonamiento hacia "
     "adelante a generar los hechos que probablemente sean relevantes, y resolver las "
     "peticiones mediante encadenamiento hacia atrás.")

h(doc, 2, "4.6 Lógica de predicados (primer orden)", "u4_5")
para(doc,
     "Los modelos de la lógica proposicional son sólo conjuntos de valores de verdad. "
     "**Los de la lógica de primer orden contienen objetos.** El **dominio** de un modelo "
     "es el conjunto de objetos que contiene. Los objetos se relacionan de diversas "
     "formas, y formalmente **una relación es sólo un conjunto de tuplas de objetos que "
     "están relacionados**. Hay relaciones binarias (hermano, sobre-la-cabeza), unitarias "
     "o **propiedades** (ser persona, ser rey), y ciertos casos que conviene tratar como "
     "**funciones**, donde un objeto dado se relaciona exactamente con otro (la pierna "
     "izquierda de cada persona).")
para(doc, "Los elementos sintácticos básicos son tres tipos de símbolos:")
bullets(doc, [
    "**Símbolos de constante**, que representan objetos (*Ricardo*, *Juan*).",
    "**Símbolos de predicado**, que representan relaciones (*Hermano*, *SobreCabeza*, *Persona*, *Rey*, *Corona*).",
    "**Símbolos de función**, que representan funciones (*PiernaIzquierda*).",
])
para(doc,
     "Cada símbolo de predicado y de función tiene una **aridad**, que establece su "
     "número de argumentos. La gramática agrega los **cuantificadores** ∀ y ∃ y las "
     "**variables**, lo que permite escribir sentencias generales en lugar de enumerar "
     "casos. Estos predicados son los que después usan los esquemas de acción de la "
     "planificación ([[u3_plan|la sección de planificación]]).")
para(doc,
     "Una **sentencia atómica** es un símbolo de predicado seguido de una lista de "
     "términos entre paréntesis: *Hermano(Ricardo, Juan)*. Los términos pueden ser "
     "complejos, es decir, contener funciones: *CasadoCon(Padre(Ricardo), Madre(Juan))* "
     "afirma que el padre de Ricardo está casado con la madre de Juan. Una sentencia "
     "atómica es verdadera, en un modelo y bajo una interpretación dadas, **si la "
     "relación que nombra el predicado se da efectivamente entre los objetos que nombran "
     "sus argumentos**. Un término sin variables se llama **término base**.")
para(doc,
     "Las **sentencias compuestas** se arman con las mismas cinco conectivas de la lógica "
     "proposicional, y **su semántica es idéntica** — la tabla de verdad de "
     "[[u4_2|sección 4.3]] se aplica sin cambios. Lo genuinamente nuevo son los "
     "**cuantificadores**, que permiten hablar de colecciones enteras de objetos sin "
     "enumerarlos:")
bullets(doc, [
    "**Universal ∀** («para todo»). «Todos los reyes son personas» se escribe **∀x Rey(x) ⇒ Persona(x)**: para todo x, si x es un rey entonces x es una persona. Equivale a afirmar la conjunción de la implicación aplicada a **cada** objeto del dominio.",
    "**Existencial ∃** («existe un x tal que», «para algún x»). «El rey Juan tiene una corona sobre su cabeza» se escribe **∃x Corona(x) ∧ SobreCabeza(x, Juan)**. Equivale a afirmar la disyunción sobre todos los objetos: basta que **una** de las instancias sea verdadera.",
])
box(doc, "Los dos errores de cuantificación que todo el mundo comete",
    "Russell y Norvig lo señalan como **«un error común»**, y aclaran que lo siguen "
    "cometiendo incluso quienes ya leyeron la advertencia varias veces. Son dos errores "
    "simétricos y conviene memorizarlos juntos:\n"
    "**∀ va con ⇒, no con ∧.** Escribir ∀x Rey(x) ∧ Persona(x) afirma que *todo objeto "
    "del dominio es un rey y además es una persona* — o sea que la pierna izquierda de "
    "Ricardo es un rey. La implicación funciona porque, al ser verdadera cuando la "
    "premisa es falsa, **no dice nada sobre los objetos que no son reyes**; y eso es "
    "exactamente lo que se quiere de una regla general.\n"
    "**∃ va con ∧, no con ⇒.** Escribir ∃x Corona(x) ⇒ SobreCabeza(x, Juan) da una "
    "sentencia **trivialmente verdadera**: alcanza con encontrar un objeto que no sea "
    "una corona —la pierna de Ricardo, por ejemplo— para que la implicación se cumpla "
    "con premisa falsa, sin que ninguna corona esté sobre ninguna cabeza.\n"
    "La regla práctica sale de la tabla de verdad: **⇒ es débil** (se satisface sola "
    "cuando la premisa falla), lo cual sirve para «todos» y arruina «existe»; **∧ es "
    "fuerte** (exige las dos partes), lo cual sirve para «existe» y arruina «todos».")
para(doc,
     "Los dos cuantificadores están conectados por la negación, con la misma forma que "
     "las leyes de De Morgan: **∀x ¬P equivale a ¬∃x P**, y **¬∀x P equivale a ∃x ¬P**. "
     "«Todos no lo hacen» es lo mismo que «no hay ninguno que lo haga», y «no todos lo "
     "hacen» es lo mismo que «hay alguno que no lo hace». Por eso, en rigor, **un solo "
     "cuantificador alcanza**: el otro se define como su negación.")
ejemplo("Ejemplo · el mismo enunciado en las dos lógicas",
        "Para ver qué se gana, tomemos «todos los alumnos de la comisión aprobaron».\n"
        "**En lógica proposicional** hay que inventar un símbolo por alumno —A₁, A₂, …, "
        "A₃₀— y escribir A₁ ∧ A₂ ∧ … ∧ A₃₀. Si entra un alumno nuevo **hay que reescribir "
        "la sentencia**, y no existe forma de expresar la regla en general.\n"
        "**En lógica de primer orden** se escribe una sola vez: "
        "∀x Alumno(x) ∧ CursaEn(x, Comision1) ⇒ Aprobo(x). Vale para los treinta alumnos "
        "y para los que se agreguen después, porque **cuantifica sobre el dominio en "
        "lugar de enumerarlo**.\n"
        "Ésa es toda la ventaja de la lógica de predicados, y también el motivo de su "
        "costo: la inferencia ya no se puede resolver enumerando 2ⁿ modelos, porque el "
        "dominio puede ser infinito.")

page_break(doc)

# =================================================================== UNIDAD 5
h(doc, 1, "Unidad 5 · Razonamiento bajo incertidumbre", "u5")
para(doc,
     "Cuando se habla de incertidumbre en IA se hace referencia a situaciones donde **el "
     "agente no tiene acceso a toda la verdad sobre su ambiente**. Doce horas de "
     "programa para el manejo del conocimiento incierto y los modelos bayesianos: "
     "probabilidad condicional, regla de Bayes, redes de creencia y modelos ocultos de "
     "Markov.")
para(doc,
     "La **lógica difusa** que desarrolla el apunte de cátedra **no figura en el "
     "programa analítico**; por eso va al final de la unidad, marcada como tema "
     "complementario ([[u5_1|sección 5.7]]). Conviene igual conocerla, porque la distinción "
     "entre *grado de verdad* y *grado de creencia* aclara qué es exactamente lo que "
     "hace la probabilidad.")
fig("d10_incertidumbre.png",
       "Grado de verdad frente a grado de creencia, y el camino hasta la inferencia "
       "en redes bayesianas.")

h(doc, 2, "5.1 Manejo del conocimiento incierto: los conceptos de base", "u5_2")
para(doc,
     "Antes de los conceptos conviene entender **por qué hace falta esta unidad**. Todo "
     "lo de las unidades 3 y 4 supone que el agente sabe con certeza en qué estado está y "
     "qué produce cada acción. Casi ningún dominio real cumple eso. El argumento de "
     "Russell y Norvig es directo: **intentar escribir las reglas de un diagnóstico "
     "dental en lógica de predicados para ver cómo fracasa**.")
para(doc,
     "El primer intento sería ∀p Síntoma(p, DolorDeMuelas) ⇒ Enfermedad(p, Caries). Pero "
     "**es falso**: no todo el que tiene dolor de muelas tiene caries — puede tener "
     "dolencia de encías, un absceso, u otra cosa. Para salvarla habría que agregar una "
     "disyunción con **una lista casi ilimitada de causas posibles**. Se puede probar al "
     "revés, como regla causal: ∀p Enfermedad(p, Caries) ⇒ Síntoma(p, DolorDeMuelas). "
     "**Tampoco es cierta**: no todas las caries duelen. Habría que agregar del lado "
     "izquierdo todas las condiciones necesarias para que una caries efectivamente "
     "duela — y aun así quedaría el caso del paciente que tiene dolor de muelas y una "
     "caries **sin relación entre sí**.")
box(doc, "Las tres razones por las que la lógica no alcanza",
    "El fracaso no es un defecto de la notación: es estructural, y tiene tres causas "
    "distintas que conviene no confundir.\n"
    "**Pereza.** Enumerar el conjunto completo de antecedentes y consecuentes que harían "
    "una regla sin excepciones es demasiado trabajo, y las reglas resultantes serían "
    "impracticables de usar.\n"
    "**Ignorancia teórica.** La ciencia médica sencillamente **no tiene una teoría "
    "completa del dominio**. No es que no la hayamos escrito: no existe.\n"
    "**Ignorancia práctica.** Aunque conociéramos todas las reglas, sobre un paciente "
    "concreto puede haber incertidumbre porque **no se le hicieron todos los estudios**, "
    "o porque no se le pueden hacer.\n"
    "Las dos primeras son limitaciones del conocimiento general; la tercera, del caso "
    "particular. La probabilidad sirve para las tres porque **resume en un número la "
    "incertidumbre que viene de la pereza y de la ignorancia**.")
para(doc,
     "La conclusión es que la conexión entre dolor de muelas y caries **no es una "
     "consecuencia lógica en ninguna de las dos direcciones**, y que eso es lo típico en "
     "medicina, derecho, negocios, diseño o reparación de automóviles. Lo máximo que el "
     "conocimiento del agente puede dar es un **grado de creencia** en cada sentencia, y "
     "la herramienta para manejar grados de creencia es la **teoría de la probabilidad**, "
     "que asigna a cada oración un número entre 0 y 1.")
box(doc, "Probabilidad no es lo mismo que lógica difusa",
    "Un grado de creencia de 0,8 **no** significa «el paciente tiene un 80 % de caries», "
    "ni que la proposición sea verdadera en un 80 %. La proposición «tiene caries» es "
    "verdadera o falsa; lo que vale 0,8 es **la confianza del agente en ella dada la "
    "evidencia disponible**. Por eso las probabilidades cambian cuando llega evidencia "
    "nueva, mientras el mundo no cambió en absoluto.\n"
    "La distinción importa porque la [[u5_1|lógica difusa]] sí modela lo otro: grados de "
    "pertenencia a un concepto vago —«el agua está tibia»—, donde la vaguedad está en el "
    "predicado y no en el conocimiento del observador.")
bullets(doc, [
    "**Probabilidad a priori o incondicional** P(a): el grado de creencia que se le otorga a una proposición **en ausencia de cualquier otra información**.",
    "**Probabilidad condicional o a posteriori** P(a|b): una vez que el agente obtiene evidencia que afecta a la variable, las probabilidades a priori dejan de aplicarse. Se define como **P(a|b) = P(a ∧ b) / P(b)**, donde P(a ∧ b) es la probabilidad conjunta (la de que a y b ocurran al mismo tiempo).",
    "**Regla del producto**: despejando, **P(a ∧ b) = P(a|b) · P(b)**. Es la forma más intuitiva: la probabilidad de que ocurran a y b es la probabilidad de que ocurra a dado b, por la probabilidad de b.",
])
box(doc, "Una advertencia que el apunte repite",
    "**La probabilidad condicional no indica una relación causa-efecto.** Es una "
    "herramienta muy útil para representar información causal de la forma "
    "P(efecto | causa), pero eso es una elección de modelado, no una propiedad de la "
    "definición. Lo mismo vale para la dependencia: **que dos variables sean "
    "dependientes no implica que una sea causa de la otra**.")

h(doc, 2, "5.2 La regla de Bayes", "u5_3")
para(doc,
     "Como P(a ∧ b) = P(b ∧ a), aplicando la regla del producto en los dos sentidos e "
     "igualando se obtiene:")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
_fmt(p.add_run("P(b|a) = P(a|b) · P(b) / P(a)"), bold=True, size=13, color=MORADO_OSC)
para(doc,
     "Permite calcular la probabilidad condicional de una variable dada otra **cuando se "
     "cuenta con la información en el sentido inverso**. Si una alarma se dispara con "
     "probabilidad P(alarma), los robos ocurren con P(robo) y sabemos "
     "P(alarma | robo), la regla de Bayes permite calcular P(robo | alarma).")
box(doc, "El ejemplo de la radiografía (Juan y Pedro)",
    "Juan se hace una radiografía de tórax como examen preocupacional y hay un hallazgo "
    "compatible con cáncer de pulmón. El test tiene tasa de falsos negativos 0,4 y de "
    "falsos positivos 0,02, de donde P(Rad = pos | Enf = verdadero) = 0,6 y "
    "P(Rad = pos | Enf = falso) = 0,02. **Todavía falta un dato**: P(Enf = verdadero), la "
    "probabilidad a priori. Como Juan pertenece al grupo de gente que se hace un examen "
    "preocupacional —no motivado por síntomas— y sólo 1 de cada 1.000 nuevos empleados "
    "tiene cáncer de pulmón, esa probabilidad es 0,001.\n"
    "P(Enf | Rad=pos) = (0,6 × 0,001) / (0,6 × 0,001 + 0,02 × 0,999) ≈ **0,029**.\n"
    "Pedro recibe exactamente el mismo resultado de radiografía, pero se hizo el estudio "
    "porque trabajó 20 años en minas y cerca del 10 % de esos trabajadores desarrollaron "
    "cáncer de pulmón. Su probabilidad a priori es 0,1, y repitiendo el cálculo: "
    "**P(Enf | Rad=pos) = 0,769**.\n"
    "**Mismo test, mismo resultado, dos conclusiones completamente distintas.** Toda la "
    "diferencia la hace la probabilidad a priori.")

ejemplo("Ejemplo · el test que acierta el 99 % y aun así se equivoca casi siempre",
        "Una enfermedad que afecta a **1 de cada 1.000 personas**. El test detecta al "
        "**99 %** de los enfermos y da positivo en el **5 %** de los sanos. A alguien le "
        "da positivo: ¿qué probabilidad tiene de estar enfermo?\n"
        "La intuición dice «99 %». La cuenta dice otra cosa:\n"
        "P(+) = 0,99 × 0,001 + 0,05 × 0,999 = 0,00099 + 0,04995 = **0,05094**\n"
        "P(enf | +) = 0,00099 / 0,05094 ≈ **0,019** — apenas el **1,9 %**.\n"
        "Contado sobre 100.000 personas se ve por qué: hay 100 enfermos, de los cuales "
        "99 dan positivo; y 99.900 sanos, de los cuales **4.995 también dan positivo**. "
        "De los 5.094 positivos totales, sólo 99 lo son de verdad.\n"
        "El error de la intuición es ignorar la **probabilidad a priori**: como los "
        "sanos son muchísimos más, incluso un porcentaje chico de falsos positivos "
        "genera muchas más alarmas falsas que verdaderas. Es el mismo fenómeno del caso "
        "de Juan y Pedro, y la razón por la que en medicina un test de cribado positivo "
        "se confirma siempre con un segundo estudio.")
fig("e21_bayes.png",
    "La regla de Bayes con números, y el mismo resultado contado sobre 100.000 personas.")

h(doc, 2, "5.3 Distribución conjunta, independencia e independencia condicional", "u5_4")
para(doc,
     "La **distribución conjunta completa** considera el conjunto completo de variables: "
     "contiene la probabilidad de ocurrencia de cada una de las combinaciones posibles de "
     "valores. Las **probabilidades marginales** P(xᵢ) se obtienen sumando la fila o "
     "columna correspondiente, es decir, sumando todas las conjuntas donde esa variable "
     "toma ese valor. Es el método más simple y directo para hacer inferencia sobre el "
     "dominio, pero **almacenar probabilidades conjuntas no es eficiente** y el método "
     "tiene complejidad algorítmica muy alta.")
bullets(doc, [
    "**Independencia**: a y b son independientes si P(a|b) = P(a) —con P(a) ≠ 0 y P(b) ≠ 0—, o si alguna de las dos es nula. Claramente, la probabilidad de a no cambia si ocurre o no b. Sólo si son independientes vale **P(a ∧ b) = P(a) · P(b)**.",
    "**Independencia condicional**: a y b son condicionalmente independientes dado c (con P(c) ≠ 0) si **P(a | b ∧ c) = P(a|c)**.",
])
box(doc, "El ejemplo de los dos vecinos",
    "En un pueblo hay dos vecinos que no interactúan entre sí. Cada uno tiene cierta "
    "probabilidad de salir con paraguas cuando hay pronóstico de lluvia. Cuando uno de "
    "ellos sale con paraguas es más probable que el otro también lo haga, **es decir, p₁ "
    "y p₂ no son independientes**. Eso no significa que se influyan mutuamente: el "
    "comportamiento se debe a que **ambos eventos tienen la misma causa**.\n"
    "Para un observador que no conoce el pronóstico, los eventos son dependientes. Si el "
    "observador conoce el pronóstico, **los eventos se vuelven independientes dado el "
    "pronóstico**: P(p₁ | lluvia ∧ p₂) = P(p₁ | lluvia).\n"
    "La independencia condicional tiene particular importancia en las redes bayesianas "
    "porque **permite representar toda la información necesaria mediante un conjunto "
    "reducido de probabilidades condicionales**.")

h(doc, 2, "5.4 Redes de creencia (redes bayesianas)", "u5_5")
para(doc,
     "Las **redes bayesianas** —también llamadas redes de creencia, redes causales y "
     "diagramas de influencia— son **estructuras gráficas para representar las relaciones "
     "probabilísticas entre un gran número de variables y para realizar inferencias "
     "probabilísticas sobre esas variables**. Muestran una descripción compacta de "
     "cualquier distribución conjunta completa. Su especificación completa es:")
bullets(doc, [
    "Un conjunto de **variables aleatorias** forma los nodos de la red; pueden ser discretas o continuas.",
    "Un conjunto de **arcos dirigidos** conecta pares de nodos. Si hay un arco de X a Y, se dice que X es **padre** de Y.",
    "Cada nodo Xᵢ tiene una **distribución de probabilidad condicionada P(Xᵢ | Padres(Xᵢ))** que cuantifica el efecto de sus padres.",
    "**El grafo no tiene ciclos dirigidos**: es un grafo acíclico dirigido (GAD).",
])
para(doc,
     "**La topología de la red especifica las relaciones de independencia condicional que "
     "existen en el dominio.** El significado intuitivo de un arco de X a Y es, "
     "habitualmente, que X tiene una influencia directa sobre Y, y suele ser sencillo "
     "para un experto del dominio decidir qué influencias directas existen. Una vez "
     "diseñada la topología, sólo hace falta especificar una distribución condicional por "
     "variable: **la combinación de topología y distribuciones condicionales es "
     "suficiente para definir la distribución conjunta completa**.")
ejemplo("Ejemplo · la red de la alarma",
        "Cinco variables booleanas: **Robo** y **Terremoto** pueden disparar la "
        "**Alarma**; y si suena la alarma, los vecinos **Juan** y **María** pueden "
        "llamar. Los arcos van Robo → Alarma ← Terremoto, Alarma → Juan y "
        "Alarma → María.\n"
        "Las probabilidades: P(Robo) = 0,001; P(Terremoto) = 0,002; la tabla de la "
        "alarma tiene cuatro filas (0,95 si hay robo y terremoto, 0,94 si sólo robo, "
        "0,29 si sólo terremoto, 0,001 si ninguno); P(Juan | Alarma) = 0,90 y "
        "P(Juan | ¬Alarma) = 0,05; P(María | Alarma) = 0,70 y "
        "P(María | ¬Alarma) = 0,01.\n"
        "**La cuenta que importa**: con 5 variables booleanas, la distribución conjunta "
        "completa necesitaría 2⁵ − 1 = **31 números**. La red necesita **10**. Y la "
        "diferencia crece de manera brutal: con 30 variables serían más de mil millones "
        "de números contra unas pocas decenas.\n"
        "De dónde sale el ahorro: de la **independencia condicional**. Juan y María no "
        "se escuchan entre sí, sólo reaccionan a la alarma, así que P(Juan | Alarma, "
        "María) = P(Juan | Alarma) y no hace falta guardar ninguna combinación de los "
        "dos. Es exactamente el caso de los dos vecinos con paraguas de la sección "
        "anterior, dibujado como grafo.")
fig("e22_red_bayesiana.png",
    "La red de la alarma: topología, tablas condicionales y el ahorro que producen.")

h(doc, 2, "5.5 Inferencia en redes bayesianas", "u5_6")
para(doc,
     "La tarea básica de cualquier sistema de inferencia probabilista es **calcular la "
     "distribución de probabilidad a posteriori para un conjunto de variables pregunta, "
     "dado algún evento observado**. La notación: X es la variable pregunta, E el conjunto "
     "de variables **evidencia** con un evento observado e, e Y las variables no evidencia "
     "(también llamadas **ocultas**). La pregunta típica pide P(X | e).")
para(doc,
     "Sobre el ejemplo del robo de Russell y Norvig —donde una alarma puede dispararse "
     "por un robo o por un terremoto, y dos vecinos, John y Mary, pueden llamar—, la "
     "pregunta es P(Robo | JohnLlama ∧ MaryLlama). El apunte la resuelve de dos maneras:")
bullets(doc, [
    "**A mano, con la regla de Bayes.** Hay que calcular P(j ∧ m) y P(j ∧ m | r), y para eso primero P(a) y P(a|r), descomponiendo sobre las dos posibilidades de terremoto. El resultado: **P(r | j ∧ m) ≈ 0,284**. La probabilidad de que haya ocurrido un robo, dado que Mary y John llamaron, es cercana a 0,28.",
    "**Inferencia automática por enumeración.** Se parte de **P(X | e) = α · Σ P(X, e, y)**, sumando sobre todos los valores de las variables ocultas y, donde α = 1/P(e) es la constante de normalización. Para el robo, el cálculo se hace en cuatro ciclos, uno por cada combinación de las variables ocultas T (terremoto) y A (alarma). Sumando los cuatro términos y multiplicando por α se obtiene **exactamente el mismo 0,284**, pero **en menos pasos, de forma automática y usando sólo los valores originales de las tablas de probabilidad condicional**.",
])
box(doc, "Un truco de cálculo que el libro apenas insinúa",
    "La forma más simple y eficiente de obtener α no es calcular P(e) por separado, sino "
    "aprovechar que P(r | j,m) + P(¬r | j,m) = 1. Si cᵢ son los términos del cálculo para "
    "P(r|j,m) y c′ᵢ los equivalentes para P(¬r|j,m), entonces\n"
    "**α = 1 / [(c₁+c₂+c₃+c₄) + (c′₁+c′₂+c′₃+c′₄)]**.\n"
    "El apunte aclara que esta forma de calcular el denominador de α «no está clara en el "
    "libro, sólo se insinúa levemente».")
box(doc, "Qué pasa cuando la red es grande (y por qué esto conecta con la Unidad 2)",
    "En redes reales —como la del proyecto Pathfinder, de patologías de ganglios "
    "linfáticos— hay cuatro consecuencias importantes:\n"
    "· Llevar a cabo la deducción a mano, como en el ejemplo anterior, es **prácticamente "
    "imposible**.\n"
    "· Representar las probabilidades conjuntas totales tendría un **tamaño inmanejable**; "
    "por eso se usan las condicionales.\n"
    "· Los mecanismos de inferencia automáticos **deben enfocarse en la eficiencia**, "
    "hasta el punto de que para casos grandes el cálculo exacto es demasiado ambicioso.\n"
    "· **No es posible crear estas redes de forma manual**: ni el conocimiento del "
    "dominio para definir la topología ni las probabilidades conocidas son suficientes. "
    "En esos casos **hay que usar métodos automáticos para aprender las redes** — y ahí "
    "esta unidad se cierra sobre la [[u2|Unidad 2]].")

h(doc, 2, "5.6 Modelos ocultos de Markov", "u5_hmm")
para(doc,
     "Todo lo anterior asume un **mundo estático**: cada variable aleatoria tiene un "
     "valor fijo y la evidencia observada no cambia. Reparando un auto eso es "
     "razonable —si está roto, sigue roto durante el diagnóstico—. Pero muchos "
     "problemas son esencialmente **dinámicos**: monitorear a un paciente diabético, "
     "seguir la actividad económica de un país con estadísticas parciales, o "
     "comprender una secuencia de palabras habladas a partir de mediciones acústicas "
     "ruidosas y ambiguas.")
h(doc, 3, "Estados, observaciones y las dos hipótesis", "u5_hmm_a")
para(doc,
     "El proceso de cambio se ve como una serie de fotos instantáneas, o **cortes de "
     "tiempo**. Cada corte contiene un conjunto de variables: **Xₜ** son las variables "
     "de estado **no observables** y **Eₜ** las variables de evidencia **observables**. "
     "Para que el modelo sea manejable hacen falta dos supuestos:")
bullets(doc, [
    "**Proceso estacionario**: las leyes que gobiernan el cambio no cambian ellas mismas con el tiempo. Ojo con el matiz: *estacionario no es estático* — en un proceso estático el estado no cambia; en uno estacionario cambia, pero según reglas fijas. Gracias a esto basta con especificar las distribuciones de un corte de tiempo «representativo» en vez de infinitos.",
    "**Hipótesis de Markov**: el estado actual depende sólo de un conjunto finito de estados precedentes. En un **proceso de Markov de primer orden** depende sólo del anterior: **P(Xₜ | X₀:ₜ₋₁) = P(Xₜ | Xₜ₋₁)**. Dicho de otra manera, *un estado es la información que se necesita para hacer el futuro independiente del pasado*.",
])
para(doc,
     "Con eso, todo el modelo se define con **tres distribuciones**: la probabilidad a "
     "priori P(X₀); el **modelo de transición** P(Xₜ | Xₜ₋₁), que describe cómo "
     "evoluciona el estado; y el **modelo sensor** P(Eₜ | Xₜ), que describe cómo el "
     "estado del mundo afecta a los sensores. Notar la dirección: la flecha va del "
     "estado a la evidencia porque el estado **causa** los valores de los sensores, "
     "aunque la inferencia después vaya en sentido contrario.")
para(doc,
     "Un **modelo oculto de Markov (MOM)** es el caso en que **cada estado del proceso "
     "está definido por una única variable aleatoria discreta**. Se pueden agregar más "
     "variables de estado y seguir dentro del marco, pero sólo combinándolas en una "
     "«megavariable» cuyos valores son todas las tuplas posibles. Esa estructura "
     "limitada es lo que permite una implementación matricial simple y elegante: el "
     "modelo de transición se vuelve una matriz **T** de S×S con Tᵢⱼ = P(Xₜ = j | Xₜ₋₁ "
     "= i), y el modelo sensor una matriz diagonal **Oₜ** con P(eₜ | Xₜ = i) en la "
     "diagonal.")
fig("d12_markov.png",
    "Estados ocultos, evidencia observada y las cuatro tareas de inferencia.")
h(doc, 3, "Las cuatro tareas de inferencia", "u5_hmm_b")
bullets(doc, [
    "**Filtrado** o monitorización: calcular el **estado de creencia**, P(Xₜ | e₁:ₜ) — la distribución del estado actual dada toda la evidencia hasta ahora. Es lo que un agente racional necesita para mantener la pista del presente y decidir. Un cálculo casi idéntico da además la verosimilitud de la secuencia de evidencia.",
    "**Predicción**: P(Xₜ₊ₖ | e₁:ₜ) para algún k > 0 — la distribución de un estado **futuro**. Sirve para evaluar posibles cursos de acción.",
    "**Suavizado** o retrospectiva: P(Xₖ | e₁:ₜ) con k < t — la distribución de un estado **pasado** a la luz de todo lo observado después. Da una estimación mejor de la que estaba disponible en su momento, porque incorpora más evidencia. Es imprescindible para *aprender* el modelo: el aprendizaje con filtrado puede no converger.",
    "**Explicación más probable**: argmax P(x₁:ₜ | e₁:ₜ) — la secuencia de estados más creíble que generó las observaciones. Se resuelve con el **algoritmo de Viterbi**, que es idéntico al filtrado salvo que reemplaza la sumatoria por una **maximización** y guarda punteros al mejor predecesor de cada estado. Su tiempo es lineal en la longitud de la secuencia, y su espacio también (a diferencia del filtrado), justamente por esos punteros.",
])
para(doc,
     "El algoritmo hacia delante-atrás resuelve las cuatro con complejidad temporal "
     "**O(S²t)** para una secuencia de longitud t con S estados posibles, ya que cada "
     "paso multiplica un vector de S elementos por una matriz S×S. Las aplicaciones "
     "clásicas de la explicación más probable son el **reconocimiento del habla** "
     "—encontrar la secuencia de palabras más probable dada una serie de sonidos— y la "
     "reconstrucción de bits transmitidos por un canal ruidoso.")
ejemplo("Ejemplo · el guardia y el paraguas",
        "El ejemplo canónico. Un guardia de seguridad trabaja en una instalación "
        "subterránea y quiere saber si llueve, pero su única información del exterior "
        "es si el director entra con paraguas o sin él. El estado oculto es "
        "**Lluviaₜ**; la evidencia observable es **Paraguasₜ**.\n"
        "Modelo: P(Lluvia₀) = 0,5. Transición: si ayer llovió, hoy llueve con "
        "probabilidad 0,7; si no llovió, 0,3. Sensor: P(paraguas | lluvia) = 0,9 y "
        "P(paraguas | ¬lluvia) = 0,2.\n"
        "**Día 1, el director llega con paraguas.** *Predecir*: sin mirar nada, "
        "P(Ll₁) = 0,7×0,5 + 0,3×0,5 = 0,5. *Observar*: se pesa con el modelo sensor — "
        "0,9×0,5 = 0,45 para «llueve» y 0,2×0,5 = 0,10 para «no llueve». *Normalizar*: "
        "0,45 / 0,55 ≈ **0,82**.\n"
        "**Día 2, otra vez con paraguas.** Predicción 0,7×0,82 + 0,3×0,18 = 0,627; se "
        "pesa 0,9×0,627 = 0,565 contra 0,2×0,373 = 0,075; normalizando, "
        "P(Lluvia₂) ≈ **0,88**. La creencia se refuerza con cada observación coherente.\n"
        "Siempre es la misma cuenta —predecir, pesar, normalizar— y eso es lo que la "
        "hace barata: es **estimación recursiva**, no hace falta guardar toda la "
        "historia sino sólo la creencia del paso anterior. Notar además que **el "
        "guardia nunca ve la lluvia**: infiere un estado que le está vedado a partir de "
        "un indicio imperfecto. Ése es exactamente el sentido de «oculto» en el nombre "
        "del modelo.")
fig("e23_hmm_paso.png",
    "Un paso de filtrado en el mundo del paraguas, con los números hechos.")

h(doc, 2, "5.7 Lógica difusa (tema complementario)", "u5_1")
para(doc,
     "Es frecuente incluir la lógica difusa dentro de los métodos de razonamiento bajo "
     "incertidumbre, **aunque hay una diferencia** con el resto: mientras en los métodos "
     "probabilísticos se habla de eventos que son verdaderos o falsos **con cierta "
     "probabilidad**, en lógica difusa **los eventos son verdaderos o falsos en cierto "
     "grado**.")
para(doc,
     "Los agentes que utilizan lógica difusa toman decisiones **en base a reglas definidas "
     "de forma difusa**, donde se hacen afirmaciones sobre la ocurrencia de ciertos "
     "eventos, pero esas afirmaciones **se ven afectadas por adjetivos que modifican el "
     "grado de certeza**.")
box(doc, "Vacío en el material disponible — hay que buscar la fuente aparte",
    "El propio apunte de cátedra dice, textualmente, que **«ninguno de los libros "
    "utilizados trata el tema en detalle»**, y que por lo tanto se utilizarán como "
    "material de lectura el apunte de Eduardo Destéfanis *Inferencia y probabilidad. "
    "Lógica difusa* (Aula Virtual de IAR, 2020) y **las presentaciones que se subieron al "
    "aula virtual**.\n"
    "Ninguno de esos dos materiales está entre los PDF convertidos de este vault, y "
    "Russell y Norvig sólo lo mencionan al pasar (en una nota al pie del capítulo 7 "
    "remitiendo al capítulo 14, que trata «otros enfoques al razonamiento con "
    "incertidumbre»). Por eso esta sección se limita a lo que el apunte afirma "
    "explícitamente. **Conjuntos difusos, funciones de pertenencia, operadores difusos, "
    "reglas SI-ENTONCES difusas y el proceso de fusificación / inferencia / "
    "defusificación no se desarrollan acá porque el material fuente no está**: hay que "
    "bajar el apunte de Destéfanis y las presentaciones del aula virtual.")
ejemplo("Ejemplo · «probablemente llueve» frente a «el día está caluroso»",
        "Los dos enunciados llevan un número entre 0 y 1, y sin embargo significan "
        "cosas distintas.\n"
        "**«Hay 70 % de probabilidad de que llueva»** es un **grado de creencia**: el "
        "evento «llover» va a ser verdadero o falso, y el 0,7 mide mi información "
        "incompleta sobre cuál de los dos. Mañana, cuando llueva o no llueva, ese 0,7 "
        "desaparece.\n"
        "**«El día está caluroso en grado 0,7»** es un **grado de verdad**: aunque yo "
        "sepa con total certeza que hay 28 °C, sigue siendo verdad que el día es "
        "caluroso «en cierto grado». No falta información — lo que pasa es que el "
        "predicado «caluroso» no tiene un límite nítido. El grado es parte del "
        "significado del adjetivo, no de mi ignorancia.\n"
        "Ésa es toda la diferencia, y es la que el apunte marca explícitamente. El "
        "desarrollo completo (conjuntos difusos, funciones de pertenencia, reglas "
        "SI-ENTONCES difusas y el ciclo de fusificación / inferencia / defusificación) "
        "**no se puede escribir con el material disponible** — ver [[apA|Apéndice A]].")
fig("e24_difusa.png",
    "Grado de creencia frente a grado de verdad, con el mismo número 0,7.")

page_break(doc)

# =================================================================== UNIDAD 6
h(doc, 1, "Unidad 6 · Procesamiento del lenguaje natural", "u6")
para(doc,
     "Doce horas para la última unidad del programa, y la que cierra el círculo: usa "
     "gramáticas —que son [[u4|lógica]]—, probabilidad —que es la "
     "[[u5|Unidad 5]]— y redes profundas —que son la [[u2|Unidad 2]]—, todo sobre el "
     "mismo problema.")
box(doc, "De dónde sale esta unidad",
    "**Ningún capítulo del apunte de cátedra cubre el procesamiento del lenguaje "
    "natural.** Los títulos de los temas del programa —modelos de lenguaje, gramática, "
    "análisis gramatical, gramáticas aumentadas; word embeddings, redes recurrentes y "
    "LSTM, modelos secuencia-a-secuencia, Transformers— coinciden **literalmente** con "
    "los de los capítulos 24 y 25 de Russell y Norvig, __Artificial Intelligence: A "
    "Modern Approach__, 4.ª edición (2021), que sí está en el material convertido. Toda "
    "esta unidad está desarrollada sobre esa fuente, cotejada con los capítulos 22 y 23 "
    "de la 2.ª edición en español (2004) para la terminología en castellano.")

h(doc, 2, "6.1 Conceptos básicos: por qué el lenguaje es distinto", "u6_1")
para(doc,
     "Turing basó su prueba de inteligencia en el lenguaje, y no por casualidad: el "
     "lenguaje captura buena parte del comportamiento inteligente. Un hablante tiene el "
     "objetivo de comunicar conocimiento, planifica un enunciado que lo representa y "
     "actúa para lograrlo; el oyente percibe el enunciado e infiere el significado "
     "buscado. Hay **tres razones** para que una computadora procese lenguaje natural:")
bullets(doc, [
    "**Para comunicarse con las personas**, que en la mayoría de las situaciones prefieren el lenguaje natural a un lenguaje formal como el cálculo de predicados.",
    "**Para aprender.** Los humanos escribieron muchísimo conocimiento en lenguaje natural — sólo Wikipedia tiene decenas de millones de páginas de hechos —, y casi nada en lógica formal. Un sistema que quiera saber mucho tiene que entender lenguaje natural.",
    "**Para avanzar en la comprensión científica del lenguaje**, combinando las herramientas de la IA con la lingüística, la psicología cognitiva y la neurociencia.",
])
para(doc,
     "El problema de fondo es que **los lenguajes naturales no se dejan caracterizar "
     "como los formales**:")
bullets(doc, [
    "**Los juicios de gramaticalidad varían** entre personas y con el tiempo. Todos aceptan «no ser invitado es triste»; sobre «ser no invitado es triste» hay desacuerdo.",
    "**Son ambiguos y vagos.** «Vi a su pato» puede significar que tiene un ave o que hizo un movimiento evasivo hacia abajo. Y «¡qué bueno!» no precisa cuán bueno ni de qué se habla.",
    "**La correspondencia entre símbolos y objetos no está formalmente definida.** En lógica de primer orden dos usos del símbolo «Ricardo» refieren a la misma persona; en lenguaje natural dos apariciones de la misma palabra pueden referir a cosas distintas.",
])
para(doc,
     "De ahí la salida que adopta el campo: si no se puede trazar una frontera booleana "
     "definitiva entre lo gramatical y lo agramatical, **al menos se puede decir qué "
     "tan probable es cada cadena**. Ésa es la idea de modelo de lenguaje, y explica "
     "por qué la [[u5|probabilidad]] aparece en el corazón de esta unidad. Como decía "
     "el lingüista Edward Sapir, «ninguna lengua es tiránicamente consistente: todas "
     "las gramáticas tienen filtraciones».")

h(doc, 2, "6.2 Modelos de lenguaje", "u6_2")
para(doc,
     "Un **modelo de lenguaje** es una distribución de probabilidad que describe la "
     "verosimilitud de cualquier cadena. Debería decir que «¿me atrevo a perturbar el "
     "universo?» tiene una probabilidad razonable como cadena del español, y que "
     "«universo el atrevo perturbar me a ¿?» es extremadamente improbable.")
para(doc,
     "Con un modelo de lenguaje se puede **predecir qué palabra viene**, y con eso "
     "sugerir el final de un correo; calcular **qué modificación a un texto lo haría "
     "más probable**, y con eso corregir ortografía y gramática; con un par de modelos, "
     "calcular la **traducción más probable** de una oración; y con ejemplos de "
     "pregunta y respuesta, la **respuesta más probable** a una pregunta. Por eso los "
     "modelos de lenguaje están en el centro de casi todas las tareas de PLN, y la "
     "tarea de modelado sirve además como banco de pruebas del progreso del campo.")
h(doc, 3, "Bolsa de palabras", "u6_2a")
para(doc,
     "El modelo más simple aplica **naive Bayes** a cadenas de palabras. Dada una "
     "oración w₁…w_N, se estima P(Clase | w₁:N) = α P(Clase) ∏ P(wⱼ | Clase). Es un "
     "modelo **generativo**: se imagina una bolsa de palabras por cada categoría "
     "—negocios, clima, deportes—, se elige una bolsa y se van sacando palabras al azar "
     "hasta sacar el indicador de fin de oración.")
para(doc,
     "**El modelo está claramente equivocado**: asume que cada palabra es independiente "
     "de las demás, y por eso no genera oraciones coherentes. Pero clasifica con buena "
     "precisión, porque «acciones» y «ganancias» son evidencia clara de la sección de "
     "economía mientras que «lluvia» y «nublado» apuntan a la de clima. Las "
     "probabilidades se estiman contando sobre un **corpus** —un cuerpo de texto "
     "etiquetado, típicamente de al menos un millón de palabras y decenas de miles de "
     "palabras distintas—. Dividir el texto en palabras no es trivial y tiene nombre "
     "propio: **tokenización**.")
h(doc, 3, "Modelos de n-gramas", "u6_2b")
para(doc,
     "La bolsa de palabras pierde el orden, y el orden importa: «cuarto» es común tanto "
     "en economía como en deportes, pero «informe de ganancias del cuarto trimestre» "
     "sólo aparece en economía. Hacer que cada palabra dependa de **todas** las "
     "anteriores sería correcto pero impracticable: con un vocabulario de 100.000 "
     "palabras y oraciones de 40, habría que estimar 10²⁰⁰ parámetros.")
para(doc,
     "El compromiso es una **cadena de Markov** ([[u5_hmm|sección 5.6]]) que considera sólo "
     "las n palabras adyacentes. Eso es un **modelo de n-gramas**: la probabilidad de "
     "cada palabra depende sólo de las n−1 anteriores.")
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_after = Pt(8)
_fmt(p.add_run("P(w₁:N) = ∏ P(wⱼ | wⱼ₋ₙ₊₁ : ⱼ₋₁)"), bold=True, size=12,
     color=MORADO_OSC)
para(doc,
     "Los casos particulares tienen nombre: **unigrama** (n = 1), **bigrama** (n = 2) y "
     "**trigrama** (n = 3). Funcionan bien para clasificar secciones de diario y "
     "también para **detección de spam**, **análisis de sentimiento** (clasificar una "
     "reseña como positiva o negativa) y **atribución de autoría**. Hay dos variantes "
     "útiles: los modelos **a nivel de carácter**, que resuelven bien la "
     "**identificación del idioma** —con textos tan cortos como «Hello, world» superan "
     "el 99 % de acierto— y ayudan con palabras nunca vistas; y los **skip-gramas**, "
     "que cuentan palabras cercanas salteando alguna en el medio, lo que captura "
     "fenómenos como la negación discontinua del francés «ne … pas».")
h(doc, 3, "Suavizado", "u6_2c")
para(doc,
     "Los n-gramas frecuentes tienen conteos altos y estimaciones confiables; los raros "
     "tienen conteos bajos y **mucha varianza**. Peor: siempre puede aparecer una "
     "palabra **fuera del vocabulario**, que nunca estuvo en el corpus, y asignarle "
     "probabilidad cero volvería cero la probabilidad de toda la oración. El "
     "**suavizado** reserva parte de la masa de probabilidad para lo nunca visto:")
bullets(doc, [
    "**Palabras desconocidas**: se reemplazan las palabras infrecuentes del corpus por un símbolo especial `<UNK>` y se lo trata como una palabra más. Variantes: `<NUM>` para cifras, `<EMAIL>` para direcciones. También conviene un símbolo `<S>` que marque el inicio, para que la fórmula del bigrama tenga qué contestar ante la primera palabra.",
    "**Suavizado de Laplace** (o *add-one*): sumar 1 a todos los conteos. Es un paso en la dirección correcta pero rinde pobremente en muchas aplicaciones reales.",
    "**Modelos de retroceso** (*backoff*): si una secuencia tiene conteo bajo o nulo, se retrocede a los (n−1)-gramas. El **suavizado por interpolación lineal** combina trigramas, bigramas y unigramas con pesos λ₃ + λ₂ + λ₁ = 1, que pueden fijarse o entrenarse.",
])
para(doc,
     "Hay dos escuelas: una desarrolla técnicas de suavizado cada vez más sofisticadas "
     "—Witten-Bell, Kneser-Ney—; la otra sostiene que conviene juntar un corpus más "
     "grande para que alcance con técnicas simples. **Las dos apuntan al mismo "
     "objetivo: reducir la varianza del modelo.**")
ejemplo("Ejemplo · un modelo de bigramas sobre tres oraciones",
        "Corpus: «el gato duerme», «el gato come», «el perro duerme».\n"
        "**Conteos**: «el gato» aparece 2 veces, «el perro» 1, «gato duerme» 1, «gato "
        "come» 1, «perro duerme» 1.\n"
        "**Probabilidades**: P(gato | el) = 2/3 ≈ 0,67; P(perro | el) = 1/3 ≈ 0,33; "
        "P(duerme | gato) = 1/2; P(come | gato) = 1/2.\n"
        "Con eso, P(«el gato duerme») ≈ 1 × 0,67 × 0,50 = **0,33**.\n"
        "**Y acá aparece el problema**: P(come | perro) = 0/1 = **cero**, porque ese "
        "bigrama no apareció. Pero «el perro come» es una oración perfectamente válida "
        "del español, y el modelo le asigna probabilidad nula — con lo cual la "
        "descartaría por completo en una traducción o en un corrector.\n"
        "Ése es exactamente el agujero que tapa el suavizado. Con add-one, "
        "P(come | perro) pasaría de 0 a un valor chico pero positivo, y la oración deja "
        "de ser imposible.")
fig("e25_ngramas.png",
    "Conteos de bigramas, probabilidades estimadas y el problema del conteo cero.")

h(doc, 2, "6.3 Gramática", "u6_3")
para(doc,
     "Una **gramática** es un conjunto de reglas que define la estructura de árbol de "
     "las frases admisibles, y un **lenguaje** es el conjunto de oraciones que siguen "
     "esas reglas. Los lenguajes naturales no tienen una frontera dura entre lo "
     "admisible y lo inadmisible, ni un único árbol definitivo por oración — pero la "
     "**estructura jerárquica** igual es importante. En «Las acciones subieron el "
     "lunes», «acciones» no es sólo una palabra ni sólo un sustantivo: es el "
     "**sintagma nominal** que hace de sujeto del sintagma verbal que sigue.")
para(doc,
     "Las **categorías sintácticas** —sintagma nominal, sintagma verbal— restringen "
     "qué palabras son probables en cada punto, y la **estructura de frase** da el "
     "andamiaje sobre el que se construye el significado.")
para(doc,
     "El modelo que desarrolla el libro es la **gramática independiente del contexto "
     "probabilística (PCFG)**. *Probabilística* porque asigna una probabilidad a cada "
     "cadena; *independiente del contexto* porque cualquier regla puede usarse en "
     "cualquier posición: las reglas para un sintagma nominal al principio de la "
     "oración son las mismas que para uno más adelante. Una regla como "
     "**Adjs → Adjetivo [0,80] | Adjetivo Adjs [0,20]** dice que una lista de "
     "adjetivos es un adjetivo solo con probabilidad 0,80, o un adjetivo seguido de "
     "otra lista con probabilidad 0,20.")
para(doc,
     "El **léxico** es la lista de palabras admisibles con su categoría. Se divide en "
     "**clases abiertas** —sustantivos, nombres propios, verbos, adjetivos y "
     "adverbios—, que tienen decenas de miles de miembros y a las que se agregan "
     "palabras constantemente, y **clases cerradas** —pronombres, pronombres "
     "relativos, artículos, preposiciones y conjunciones—, con una docena de miembros "
     "que cambian en el curso de siglos, no de meses.")
box(doc, "Sobregeneración y subgeneración",
    "Una gramática chica siempre falla en las dos direcciones. **Sobregenera**: acepta "
    "cadenas que no son gramaticales, como «Mí voy yo». Y **subgenera**: rechaza "
    "oraciones perfectamente válidas que no previó. No es un defecto de una gramática "
    "en particular sino la condición normal de cualquier gramática formal frente a un "
    "lenguaje natural — y la razón por la que después se recurre a aprenderlas de "
    "datos en vez de escribirlas a mano.")

h(doc, 2, "6.4 Análisis gramatical", "u6_4")
para(doc,
     "**Analizar** (*parsear*) es el proceso de examinar una cadena de palabras para "
     "descubrir su estructura de frase de acuerdo con las reglas de una gramática. Se "
     "lo puede pensar como **una búsqueda** ([[u3|Unidad 3]]) de un árbol de análisis "
     "válido cuyas hojas sean las palabras de la cadena: se puede buscar **de arriba "
     "hacia abajo**, partiendo del símbolo inicial, o **de abajo hacia arriba**, "
     "partiendo de las palabras.")
para(doc,
     "Las dos estrategias puras son ineficientes, porque repiten trabajo en zonas del "
     "espacio de búsqueda que terminan en callejones sin salida. El ejemplo del libro "
     "es contundente: dos oraciones en inglés que comparten sus primeras diez palabras "
     "tienen análisis completamente distintos —una es una orden y la otra una "
     "pregunta—, y un analizador de izquierda a derecha no puede saber cuál es hasta la "
     "palabra número once. Si adivinó mal, tiene que **retroceder hasta la primera "
     "palabra** y reanalizar todo.")
para(doc,
     "La solución es **programación dinámica**: cada vez que se analiza una subcadena "
     "se guarda el resultado para no volver a analizarla. Esa estructura se llama "
     "**tabla** (*chart*), y un algoritmo que la usa, **analizador de tabla** (*chart "
     "parser*). Como la gramática es independiente del contexto, un sintagma "
     "encontrado en una rama del árbol de búsqueda sirve igual en cualquier otra. El "
     "algoritmo que desarrolla el libro es el **CYK**, un analizador de tabla "
     "probabilístico de abajo hacia arriba.")
ejemplo("Ejemplo · el árbol de «el gato come pescado»",
        "Con una gramática mínima: **O → SN SV**, **SN → Det N**, **SV → V N**, y el "
        "léxico Det → «el», N → «gato» | «pescado», V → «come».\n"
        "El análisis arma este árbol: la oración **O** se parte en un sintagma nominal "
        "**SN** y uno verbal **SV**. El SN se parte en el determinante «el» y el "
        "sustantivo «gato». El SV se parte en el verbo «come» y el sustantivo "
        "«pescado».\n"
        "Cuatro palabras, siete nodos y ninguna ambigüedad. Con la oración «vi al "
        "hombre con el telescopio» habría **dos** árboles válidos —el telescopio puede "
        "colgar del verbo o del sustantivo— y ahí es donde las probabilidades de la "
        "PCFG hacen falta: el analizador devuelve el árbol más probable en vez de "
        "quedarse trabado entre los dos.")
fig("e26_arbol_sintactico.png",
    "Árbol de análisis de una oración de cuatro palabras.")

h(doc, 2, "6.5 Gramáticas aumentadas", "u6_5")
para(doc,
     "Una gramática independiente del contexto trata a todos los pronombres por igual, "
     "y eso no alcanza. «Yo comí una banana» está bien; «Mí comí una banana» es "
     "agramatical, aunque «yo» y «mí» sean los dos pronombres. Y «comí una bandana» es "
     "gramatical pero improbable, aunque «banana» y «bandana» sean los dos "
     "sustantivos.")
para(doc,
     "Los lingüistas dicen que «yo» está en **caso sujeto** y «mí» en **caso objeto**; "
     "que «yo» es de **primera persona** y **singular**. Una categoría enriquecida con "
     "rasgos así —«caso sujeto, primera persona singular»— se llama **subcategoría**. "
     "Una **gramática aumentada** es aquella en la que los no terminales dejan de ser "
     "símbolos atómicos y pasan a ser **representaciones estructuradas**: el sintagma "
     "«yo» se escribe SN(Suj, 1S, Hablante) y «mí», SN(Obj, 1S, Hablante).")
para(doc,
     "Con eso se pueden imponer **concordancias** —de caso, de número, de persona, "
     "entre sujeto y verbo— que la gramática plana no podía expresar, y construir "
     "además una representación del significado de forma composicional.")
para(doc,
     "La otra variante es la **PCFG lexicalizada**, que asigna probabilidades según las "
     "palabras concretas y no sólo las categorías. Para que los datos no queden "
     "demasiado dispersos se introduce la noción de **núcleo** (*head*) de un "
     "sintagma: la palabra más importante. «Banana» es el núcleo del SN «una banana» y "
     "«comer» el del SV «comer una banana». Así se puede establecer que "
     "P₁(comer, banana) > P₁(comer, bandana) y preferir el análisis correcto.")
box(doc, "El costo de lexicalizar",
    "P₁ es conceptualmente una tabla enorme: con 5.000 verbos y 10.000 sustantivos "
    "haría falta almacenar 50 millones de entradas. En la práctica la mayoría no se "
    "guarda explícitamente, sino que se deriva por **suavizado y retroceso** — las "
    "mismas técnicas de [[u6_2c|los modelos de n-gramas]]. Notar también el límite: "
    "como sólo se consideran los núcleos, la distinción entre «comer una banana» y "
    "«comer una banana podrida» **no la captura** P₁.")

h(doc, 2, "6.6 Aportes del aprendizaje profundo: word embeddings", "u6_6")
para(doc,
     "Hasta acá todo lo que el modelo sabe lo aprendió **contando secuencias "
     "específicas**. Un hablante nativo contaría otra historia: «un gato negro» es "
     "válido porque sigue un patrón familiar —artículo, adjetivo, sustantivo—, y "
     "reconocería la cercanía sintáctica entre «un» y «el» y la semántica entre «gato» "
     "y «gatito». Lo que hace falta es una **representación de las palabras** que "
     "permita generalizar entre palabras relacionadas sin diseñar rasgos a mano.")
para(doc,
     "La codificación obvia, el vector **one-hot** —un 1 en la posición de la palabra y "
     "0 en el resto—, no sirve: no captura ninguna similitud, porque dos palabras "
     "cualesquiera están a la misma distancia. Siguiendo la máxima del lingüista John "
     "Firth, **«se conoce una palabra por la compañía que mantiene»**, se podría "
     "representar cada palabra por sus conteos de n-gramas — pero con 100.000 palabras "
     "eso da vectores de dimensión astronómica y casi todos ceros.")
para(doc,
     "Un **word embedding** es la versión reducida y densa de esa idea: un vector de "
     "unas pocas centenas de dimensiones, **aprendido automáticamente de los datos**. "
     "Ninguna dimensión suelta tiene un significado discernible, pero el espacio "
     "resultante tiene la propiedad de que **palabras similares quedan cerca**: se "
     "forman grupos separados de países, de parentescos, de medios de transporte y de "
     "comidas. Los diccionarios preentrenados de uso común son **WORD2VEC**, **GloVe** "
     "y **FASTTEXT**, este último con vectores para 157 idiomas.")
para(doc,
     "También se pueden entrenar vectores propios, normalmente al mismo tiempo que la "
     "red que resuelve la tarea. A diferencia de los preentrenados genéricos, los "
     "vectores hechos a medida se entrenan sobre un corpus elegido y tienden a "
     "enfatizar los aspectos de las palabras que sirven para esa tarea concreta.")
ejemplo("Ejemplo · «Atenas es a Grecia como Oslo es a…»",
        "Tomando los vectores de Atenas (A) y Grecia (B), la **resta B − A** parece "
        "codificar la relación «capital de». Y lo notable es que los pares "
        "Francia-París, Rusia-Moscú y Zambia-Lusaka tienen esencialmente **la misma "
        "diferencia vectorial**.\n"
        "Eso permite resolver analogías con aritmética: llamando C al vector de Oslo y "
        "D a la incógnita, se supone B − A = D − C, o sea **D = C + (B − A)**. Al "
        "calcular ese vector, la palabra más cercana resulta ser **Noruega**.\n"
        "El mismo truco funciona para monedas (Angola-kwanza → Irán-rial), símbolos "
        "químicos (cobre-Cu → oro-Au), gentilicios, plurales, superlativos y tiempos "
        "verbales.\n"
        "Con una advertencia importante que el libro subraya: **nada garantiza** que un "
        "algoritmo de embedding sobre un corpus dado capture una relación semántica "
        "determinada. Los embeddings se usan porque **funcionan bien como entrada de "
        "otras tareas** —traducción, respuesta a preguntas, resumen—, no porque "
        "resuelvan analogías. La analogía es una consecuencia agradable, no el "
        "objetivo.")
fig("e27_embeddings.png",
    "Palabras cercanas en el espacio de embeddings y la aritmética de la analogía.")

h(doc, 2, "6.7 Redes recurrentes y LSTM para PLN", "u6_7")
para(doc,
     "Los embeddings resuelven la representación de palabras **aisladas**, pero el "
     "lenguaje es una secuencia ordenada donde el contexto importa. Para el etiquetado "
     "morfosintáctico alcanza con una ventana chica de unas cinco palabras; para "
     "responder preguntas o resolver a qué refiere un pronombre pueden hacer falta "
     "decenas. En «Eduardo me dijo que Miguel estaba muy enfermo así que lo llevé al "
     "hospital», saber que «lo» es Miguel y no Eduardo exige abarcar la oración de "
     "punta a punta.")
para(doc,
     "Una ventana fija tiene dos problemas. **El contexto necesario puede exceder la "
     "ventana**, o el modelo termina con demasiados parámetros. Y hay un problema de "
     "**asimetría**: lo que la red aprenda sobre la palabra «lo» apareciendo en la "
     "posición 12 tiene que volver a aprenderlo para la posición 3, porque los pesos "
     "son distintos en cada posición.")
para(doc,
     "Una **red neuronal recurrente (RNN)** procesa la secuencia **de a un elemento por "
     "vez**, manteniendo una capa oculta z que se pasa de un paso al siguiente. Eso "
     "resuelve las tres cosas:")
bullets(doc, [
    "**Parámetros**: el número de pesos es **O(1)**, constante e independiente del largo de la secuencia — frente a O(n) de una red con ventana fija y O(vⁿ) de un modelo de n-gramas, con v el tamaño del vocabulario.",
    "**Asimetría**: los pesos son **los mismos para todas las posiciones**, así que lo aprendido en una posición vale en todas.",
    "**Contexto**: en teoría no hay límite de cuán atrás puede mirar el modelo, porque cada actualización de z tiene acceso a la palabra actual y al z anterior; la información puede copiarse indefinidamente. En la práctica z tiene capacidad limitada y no puede recordar todo.",
])
para(doc,
     "Se entrena con **retropropagación a través del tiempo**, cuidando que los pesos "
     "se mantengan iguales en todos los pasos. Un uso directo: entrenada para predecir "
     "la palabra siguiente, la red puede **generar texto** — se le da una palabra "
     "inicial, se muestrea la siguiente de la distribución softmax de salida, se la "
     "realimenta como entrada y se repite. Cuánto se favorece a las palabras probables "
     "frente a las improbables es un hiperparámetro del muestreo.")
para(doc,
     "Las **LSTM** son la variante que mitiga el olvido de contexto lejano; aun así, el "
     "libro es explícito en que **incluso las LSTM tienen dificultades** con las "
     "dependencias realmente largas — y ése es el problema que motiva lo que sigue.")

h(doc, 2, "6.8 Modelos secuencia-a-secuencia y atención", "u6_8")
para(doc,
     "La tarea más estudiada del PLN es la **traducción automática**: pasar una oración "
     "de un idioma origen a uno destino, entrenando con un corpus grande de pares de "
     "oraciones. Si hubiera correspondencia uno a uno entre palabras, bastaría con "
     "etiquetar. Pero no la hay: «caballo de mar» son tres palabras en español y una "
     "sola en inglés (*seahorse*), y «perro grande» se traduce invirtiendo el orden "
     "(*big dog*). En fiyiano el sujeto va al final de la oración.")
para(doc,
     "El **modelo secuencia-a-secuencia básico** usa **dos RNN**: una recorre la "
     "oración origen y su estado oculto final se usa como estado inicial de la "
     "segunda, que genera la oración destino. Así cada palabra generada queda "
     "condicionada tanto por toda la oración origen como por las palabras ya "
     "generadas. Fue un avance decisivo: según Wu y otros (2016), redujo el error un "
     "**60 %** respecto de los métodos anteriores. Pero tiene tres defectos:")
bullets(doc, [
    "**Sesgo hacia el contexto cercano**: cada actualización del vector oculto reemplaza parte de la información vieja por información nueva, así que en la palabra 57 de una secuencia de 70 el estado contiene más información de la palabra 56 que de la 5.",
    "**Tamaño de contexto fijo**: toda la oración origen se comprime en un único vector de estado de dimensión fija. Una LSTM del estado del arte ronda las 1.024 dimensiones; para una oración de 64 palabras eso deja 16 dimensiones por palabra, insuficiente para oraciones complejas. Agrandar el vector trae entrenamiento lento y sobreajuste.",
    "**Procesamiento secuencial lento**: las redes ganan mucha eficiencia procesando lotes con aritmética matricial, pero una RNN parece obligada a operar de a una palabra por vez.",
])
para(doc,
     "La **atención** resuelve los dos primeros. En vez de condicionar la RNN destino "
     "sólo al último vector oculto de la origen, se la condiciona a **todos**. "
     "Concatenarlos aumentaría muchísimo los pesos; en cambio se aprovecha que, al "
     "generar cada palabra destino, **sólo una parte chica del origen es relevante**. "
     "Se calcula un puntaje crudo rᵢⱼ entre el estado destino actual y cada estado "
     "origen, se normalizan con un softmax en probabilidades aᵢⱼ, y con ellas se arma "
     "un promedio ponderado cᵢ —el **vector de contexto**— que entra como entrada "
     "adicional a la RNN destino.")
box(doc, "Tres detalles de la atención que conviene retener",
    "· El componente de atención **no tiene pesos aprendidos propios** y admite "
    "secuencias de largo variable en ambos lados.\n"
    "· La atención es enteramente **latente**: el programador no dicta qué información "
    "se usa en cada momento, **el modelo aprende qué mirar**.\n"
    "· La formulación con softmax cumple tres funciones a la vez: hace la atención "
    "**derivable** (condición necesaria para entrenarla con retropropagación), la "
    "normaliza y la convierte en una distribución interpretable.")
ejemplo("Ejemplo · traducir «The front door is red»",
        "La traducción es «La puerta de entrada es roja». Notar el desajuste: **cinco "
        "palabras en inglés, seis en español**, y «front door» se convierte en «puerta "
        "de entrada» con el orden invertido.\n"
        "Si se dibuja la matriz de pesos de atención —una fila por palabra generada, "
        "una columna por palabra origen— se ve exactamente qué mira el modelo en cada "
        "paso. Al generar «La» presta atención sobre todo a *The*; al generar «puerta», "
        "a *door*; al generar «entrada», a *front*; al generar «roja», a *red*. Cada "
        "fila suma 1.\n"
        "Lo importante: **nadie escribió esa alineación**. No hay ninguna regla que "
        "diga «front door se traduce puerta de entrada invirtiendo el orden». Los pesos "
        "salen del entrenamiento, y la matriz es simplemente una forma de mirar por "
        "dentro qué aprendió el modelo.")
fig("e28_atencion.png",
    "Matriz de pesos de atención en una traducción con reordenamiento.")

h(doc, 2, "6.9 La arquitectura Transformer", "u6_9")
para(doc,
     "El artículo *Attention is all you need* (Vaswani y otros, 2018) introdujo el "
     "**Transformer**, que usa un mecanismo de **autoatención** capaz de modelar "
     "contexto a larga distancia **sin dependencia secuencial** — con lo que ataca "
     "también el tercer defecto de los modelos secuencia-a-secuencia.")
h(doc, 3, "Autoatención: consulta, clave y valor", "u6_9a")
para(doc,
     "Mientras la atención clásica iba de la RNN destino a la origen, la "
     "**autoatención** hace que cada secuencia se atienda **a sí misma**: el origen al "
     "origen y el destino al destino. Así captura contexto lejano y cercano dentro de "
     "una misma secuencia.")
para(doc,
     "Aplicarla directamente como producto punto de los vectores de entrada consigo "
     "mismos no funciona: el producto de un vector consigo mismo siempre es alto, así "
     "que cada palabra tendería a atenderse sólo a sí misma. El Transformer lo resuelve "
     "proyectando la entrada en **tres representaciones distintas** con tres matrices "
     "de pesos:")
bullets(doc, [
    "**Vector de consulta** (*query*) qᵢ = W_q xᵢ — el que atiende, análogo al destino en la atención clásica.",
    "**Vector de clave** (*key*) kᵢ = W_k xᵢ — el que es atendido, análogo al origen.",
    "**Vector de valor** (*value*) vᵢ = W_v xᵢ — el contexto que efectivamente se genera.",
])
para(doc,
     "El puntaje es rᵢⱼ = (qᵢ · kⱼ) / √d, con d la dimensión de las claves; el divisor "
     "está para **estabilidad numérica**. Los puntajes se normalizan con softmax y se "
     "usan para promediar los vectores de valor. Tres consecuencias: la autoatención "
     "es **asimétrica** (rᵢⱼ ≠ rⱼᵢ); la codificación de **todas** las palabras de la "
     "oración puede calcularse **simultáneamente**, porque todo se expresa como "
     "operaciones matriciales paralelizables en hardware especializado; y el contexto "
     "que se usa se aprende, no se prescribe.")
para(doc,
     "Como cᵢ es una suma sobre todas las posiciones, a veces se pierde información "
     "importante «promediada» con el resto. La **atención multicabeza** parte la "
     "oración en m trozos, aplica atención a cada uno con sus propios pesos y "
     "**concatena** —en vez de sumar— los resultados, lo que permite que un fragmento "
     "importante se destaque.")
h(doc, 3, "De la autoatención al Transformer", "u6_9b")
para(doc,
     "La autoatención es **sólo un componente**. Cada capa del Transformer aplica "
     "primero autoatención; la salida pasa por capas *feedforward* cuyos pesos se "
     "aplican de forma independiente en cada posición, con una activación no lineal "
     "—típicamente **ReLU**— después de la primera. Se agregan **dos conexiones "
     "residuales** para atacar el problema del gradiente que se desvanece. Los modelos "
     "en la práctica apilan seis o más de estas capas, y la salida de la capa i es la "
     "entrada de la i+1.")
box(doc, "El detalle que falta: la posición",
    "El Transformer **no captura el orden de las palabras**, porque el contexto se "
    "modela sólo con autoatención y la autoatención es indiferente al orden. La "
    "solución es el **embedding posicional**: si la secuencia tiene largo máximo n, se "
    "aprenden n vectores nuevos, uno por posición, y la entrada de la primera capa es "
    "la **suma** del embedding de la palabra más el embedding de su posición.\n"
    "Sin eso, el modelo vería «el perro mordió al hombre» y «el hombre mordió al perro» "
    "exactamente igual.")
para(doc,
     "Lo descripto es el **codificador** del Transformer, que es lo que sirve para "
     "clasificación de texto. La arquitectura completa fue diseñada como un modelo "
     "secuencia-a-secuencia para traducción, así que incluye además un "
     "**descodificador**, casi idéntico salvo por dos diferencias: usa una versión de "
     "autoatención en la que **cada palabra sólo puede atender a las anteriores** "
     "—porque el texto se genera de izquierda a derecha— y tiene en cada capa un "
     "**segundo módulo de atención** que atiende a la salida del codificador.")
para(doc,
     "Sobre esa base se monta el **preentrenamiento y la transferencia**: entrenar un "
     "modelo grande sobre enormes cantidades de texto sin etiquetar y después "
     "adaptarlo a una tarea concreta. Es el esquema de los modelos de lenguaje "
     "actuales, y el puente directo con la IA generativa que menciona la "
     "[[u1_4b|Unidad 1]].")
fig("d13_pln.png",
    "Los dos enfoques del PLN que pide el programa, y qué resuelve cada uno.")

page_break(doc)

# ================================================================= APÉNDICE A
import apendice
apendice.escribir(
    lambda n, t, bm: h(doc, n, t, bm),
    lambda t: para(doc, t),
    lambda items: bullets(doc, items),
    lambda t, c: box(doc, t, c))

doc.save(OUT)
print(OUT)
