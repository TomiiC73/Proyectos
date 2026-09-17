# -*- coding: utf-8 -*-
"""Apendice A: cobertura, vacios y bibliografia. Se mantiene aparte de build.py
porque es la seccion que hay que revisar cada vez que cambia el material."""


def escribir(h, para, bullets, box):
    h(1, "Apéndice A · Qué cubre y qué no cubre este resumen", "apA")
    para("El pedido era no completar con contenido genérico lo que el material real "
         "no cubre. Estos son los puntos donde el material disponible en el vault se "
         "queda corto respecto del **programa analítico oficial**, y qué falta "
         "conseguir en cada caso.")

    h(2, "A.1 Vacíos reales del material", "apA_1")
    bullets([
        "**Sistemas expertos (Unidad 4).** El programa pide «tipos de problema, características del dominio, componentes». **El apunte de cátedra no desarrolla el tema**, y Russell y Norvig lo tratan de forma dispersa: históricamente en el capítulo 1 (DENDRAL, MYCIN, R1/XCON), como proceso de ingeniería del conocimiento en la sección 8.4, y desde la teoría de la decisión en la 16.7. La sección [[u4_exp|4.1]] está armada juntando esas tres fuentes. **La presentación canónica de la arquitectura de un sistema experto —la que suele darse con Rich y Knight o con Destéfanis— no está en el material convertido**, así que los componentes se describen a partir de lo que las fuentes disponibles sí afirman, sin agregar detalle que no puedan respaldar.",
        "**Planificación por pila de objetivos (Unidad 3).** El programa nombra explícitamente «estrategia de descomposición» y «planificación por pila de objetivos», que es terminología de **Rich, Knight y González Calero**, __Inteligencia artificial__ (McGraw-Hill). El apunte manda leer su capítulo 13 hasta la página 379 y aclara que **ante conflicto hay que usar su nomenclatura**. Ese libro no está en el vault. La sección [[u3_plan|3.7]] está desarrollada íntegramente sobre Russell y Norvig capítulo 11: la descomposición aparece ahí como *problema prácticamente descomponible*, y la planificación de orden parcial cubre parte del mismo terreno, **pero el algoritmo de pila de objetivos como tal no está desarrollado**.",
        "**Lógica difusa.** El apunte dice explícitamente que ninguno de los libros utilizados trata el tema en detalle, y remite al apunte de **Eduardo Destéfanis**, __Inferencia y probabilidad. Lógica difusa__ (Aula Virtual, 2020) y a las presentaciones del aula virtual; ninguno de los dos está convertido. **Atenuante importante: la lógica difusa no figura en el programa analítico 2026**, así que este vacío no afecta la cobertura del temario oficial. Queda en [[u5_1|sección 5.7]] como tema complementario, con lo poco que el material afirma.",
        "**Reconocimiento de patrones (Unidad 2).** El apunte remite al apunte de Destéfanis *Reconocimiento de patrones* (Aula Virtual) y a la tesis doctoral de **Mario A. García**, __Clasificación automática del grado general de disfonía__ (UTN FRC, 2021), secciones 2.2 a 2.2.2. Ninguno está convertido; la sección [[u2_1|2.1]] se apoya en la presentación 4 de la cátedra, que sí está y cubre el tema con ejemplos.",
        "**Algoritmos genéticos (Unidad 3).** Además de Russell y Norvig sección 4.3 —que sí está y es la fuente de [[u3_7|sección 3.9]]—, el apunte remite a una presentación del aula virtual de las profesoras **Sandra Olariaga y Nancy Páez**, que no está convertida.",
        "**Metaheurísticas específicas.** El apunte nombra búsqueda tabú, GRASP, colonias de hormigas, colonias de abejas y enjambre de partículas al clasificarlas, pero **no las desarrolla algorítmicamente**. Este resumen mantiene ese mismo nivel —qué las distingue y en qué eje de clasificación cae cada una— sin inventar pseudocódigo que el material no trae.",
        "**Un PDF que la conversión automática no puede leer.** La presentación __Aprendizaje Automático__ (Casatti y Guzmán, 24 páginas) tiene el contenido de las diapositivas **dentro de imágenes rasterizadas**: `markitdown` extrae de ella 1.842 caracteres —los títulos y poco más— sobre 3,6 MB de archivo. Su contenido se recuperó **leyendo las páginas como imagen** y quedó transcripto en __PDFS EN .MD/3- Aprendizaje Automatico ML (completo).md__. De ahí salen la clasificación en tres tipos de aprendizaje y el flujo de tres etapas del comienzo de la [[u2|Unidad 2]]. Conviene tenerlo presente: **si aparecen más presentaciones en ese formato, la conversión automática las va a dejar vacías sin avisar**.",
    ])
    para("Dos aclaraciones sobre unidades que **no** tienen vacío, aunque el apunte no "
         "las cubra: los **modelos ocultos de Markov** ([[u5_hmm|sección 5.6]]) salen del "
         "capítulo 15 de Russell y Norvig en español, que está convertido y trata el "
         "tema completo; y toda la **Unidad 6** sale de los capítulos 24-25 de la 4.ª "
         "edición en inglés y 22-23 de la 2.ª en español, también convertidos. En "
         "ambos casos sólo cambia la fuente, no falta material — pero conviene saber "
         "que ninguna parte de esas secciones está respaldada por el apunte ni por las "
         "presentaciones de la cátedra.")

    h(2, "A.2 Diferencias entre el programa analítico y el apunte", "apA_2")
    para("El apunte de cátedra organiza los temas en unidades **distintas** de las del "
         "programa analítico 2026. Donde hubo conflicto, este documento siguió el "
         "programa. Las diferencias son:")
    bullets([
        "**Planificación**: el apunte la agrupa con la lógica; el programa la pone junto a la búsqueda. Acá está en la [[u3_plan|Unidad 3]].",
        "**Sistemas expertos**: son un tema explícito del programa (Unidad 4) que el apunte no trata como tal.",
        "**Lógica difusa**: es un capítulo entero del apunte que **no aparece en el programa**. Se conservó como tema complementario en vez de sacarlo.",
        "**Unidad 6 completa**: el programa incluye procesamiento del lenguaje natural con doce horas asignadas; el apunte no llega a cubrirla.",
        "**Modelos ocultos de Markov**: están en el programa dentro de modelos bayesianos; el apunte no los desarrolla.",
        "**Regresión lineal, logística y polinomial**: el programa las nombra explícitamente como contenido de aprendizaje supervisado; el apunte toca la regresión sólo al hablar de MSE y flexibilidad, sin desarrollarlas como modelos. La sección [[u2_reg|2.6]] las desarrolla sobre Russell y Norvig 4.ª edición, sección 19.6.",
    ])

    h(2, "A.3 Material del vault que queda fuera del programa", "apA_3")
    para("Al revés, hay material convertido en el vault que **no corresponde a ninguna "
         "unidad del programa analítico**, y por eso no se incluyó:")
    bullets([
        "**Búsqueda entre adversarios y juegos** y **problemas de satisfacción de restricciones (CSP)**. No figuran en el programa; para la Unidad 3 el apunte manda leer sólo las secciones 3.1, 3.3, 3.4 (hasta profundidad limitada), 3.5, 4.1 (hasta A*) y 4.2.",
        "**Aprendizaje por refuerzo**. No aparece en el programa como tema propio.",
        "**Visión por computadora** y **robótica** como capítulos propios. Se las menciona en la [[u1_tipos|Unidad 1]] dentro de los tipos de problema del mundo real y el estado del arte, que es el alcance que les da el programa.",
        "Las **guías de trabajos prácticos** (Jupyter/Colab, NumPy, K-means, convolución, métricas) no se incluyen como tales, porque son consignas de ejercicio y no contenido: los conceptos que ejercitan ya están desarrollados en las unidades correspondientes. **Los notebooks resueltos sí se usan**, y son la fuente de todos los ejemplos con código de la Unidad 2 (ver [[apA_notebooks|A.4]]).",
    ])

    h(2, "A.4 Los notebooks de Colab y hasta dónde llegan", "apA_notebooks")
    para("Los bloques de código que aparecen en la Unidad 2 **no fueron escritos para "
         "este documento**: salen de los notebooks de Google Colab desarrollados en las "
         "clases prácticas, que están en __IA/Collabs/__ y convertidos a Markdown en "
         "__IA/Collabs EN .MD/__. Se transcriben con el código tal como fue escrito y "
         "**los outputs tal como fueron ejecutados**, recortando sólo lo accesorio "
         "(imports repetidos, código de graficación) para dejar la parte que ilustra el "
         "concepto. Son nueve notebooks:")
    bullets([
        "__Clasificador – Parte 1__ (Clase 2): clasificador lineal resuelto por pseudoinversa paso a paso, y encapsulado en una clase propia. Es la fuente del ejemplo de [[u2_7|sección 2.8]].",
        "__Clasificación – Parte 2__ (Clase 2): regresión lineal sobre datos oceanográficos reales, con separación entrenamiento/prueba. Fuente de [[u2_reg_a|sección 2.6]].",
        "__Clasificación – Parte 3__ (Clase 3): clasificación multiclase con la estrategia «uno contra todos», sobre un caso de riesgo crediticio y sobre Iris. Fuente de [[u2_6|sección 2.7]].",
        "__Clasificación – Parte 4__ (Clase 3): clasificador polinomial con `Pipeline`, SVM con kernel RBF, y matriz de confusión sobre el conjunto de diabetes. Fuente de [[u2_reg_c|sección 2.6]], [[u2_8|sección 2.9]] y [[u2_4a|sección 2.4]].",
        "__Clasificadores Ejemplos__ (Clase 3): diferencia entre la línea de decisión y la frontera dibujada por evaluación sobre una malla.",
        "__Ejemplo con Perceptrón Monocapa__ y __Perceptrón Monocapa Simple__ (Clase 3): la compuerta AND resuelta a mano, con scikit-learn y con Keras, la traza de pesos época por época, y el caso de abandono de clientes. Fuente de [[u2_9a|sección 2.10]].",
        "__Perceptrón Multicapa – XOR__ (Clase 3): retropropagación implementada sin librerías. Fuente de [[u2_9b|sección 2.10]].",
        "__Perceptrón y Adaline – Ejemplo 2__ (Clase 3): Adaline sobre la conversión Fahrenheit-Celsius, y la comparación de ambos modelos. Fuente de [[u2_9c|sección 2.10]].",
    ])
    box("Los notebooks cubren la Unidad 2 y nada más",
        "Es la limitación importante de esta fuente: **las nueve prácticas son todas de "
        "aprendizaje automático**. Las unidades 1, 3, 4, 5 y 6 no tienen ningún notebook "
        "asociado, así que sus ejemplos siguen siendo trazas calculadas a mano o casos de "
        "la bibliografía, no código ejecutado.\n"
        "En la Unidad 3 eso se nota especialmente: búsqueda, planificación y algoritmos "
        "genéticos se prestarían a una implementación corta y verificable, y no hay "
        "material práctico de la cátedra que la respalde. **Si aparecen prácticas de esas "
        "unidades, son las que más agregarían.**")
    box("Tres resultados de los notebooks que conviene no leer de más",
        "Varios notebooks terminan con resultados imperfectos, y en los tres casos el "
        "documento explica la causa en vez de disimularla, porque el error enseña más "
        "que el acierto:\n"
        "· El perceptrón sobre el caso de **abandono de clientes** da 62,5 %, pero el "
        "problema **sí es linealmente separable**: falla por la diferencia de escalas "
        "entre las variables, no por el modelo ([[u2_9a|sección 2.10]]).\n"
        "· La red **XOR** implementada a mano queda en 0,27 / 0,68 / 0,68 / 0,41 después "
        "de mil épocas, porque le falta el término de sesgo y le sobran pocas épocas; "
        "reejecutada con sesgo llega a 0,10 / 0,89 / 0,89 / 0,09.\n"
        "· El **Adaline** sobre Fahrenheit-Celsius deja el sesgo a mitad de camino "
        "(−15,17 contra −17,78 ideal), y con una tasa de aprendizaje diez veces mayor "
        "**diverge** hasta 10¹³.\n"
        "Las tres explicaciones fueron **verificadas reejecutando el código**, no "
        "deducidas de la lectura.")

    h(2, "A.5 Sobre los ejemplos y los diagramas", "apA_4")
    para("Todos los **diagramas** de este documento fueron generados específicamente "
         "para él, con la misma paleta y la misma tipografía, y se insertan al ancho "
         "exacto al que fueron dibujados, de manera que no hay reescalado y el texto "
         "interior se imprime a su tamaño real. **Ninguna imagen fue tomada de "
         "internet.**")
    para("Los **ejemplos** en caja ámbar son de dos clases, y conviene distinguirlas:")
    bullets([
        "Los que **vienen del material**: el mundo de la aspiradora, el 8-puzle con h₁ = 8 y h₂ = 18, el mundo del paraguas, la red de la alarma, el caso de Juan y Pedro con la radiografía, las tres funciones discriminantes, la analogía Atenas-Grecia-Oslo-Noruega y la traducción de «The front door is red». Son los ejemplos de la bibliografía, con sus números originales.",
        "Los **construidos para ilustrar** un concepto que el material define pero no ejemplifica: la grilla de 2×2, las monedas de $100 y $500, los diez puntos ajustados con tres polinomios, el test sobre 100 personas, el auto que no arranca, la refutación de «Juan se moja» y el corpus de tres oraciones. Están armados con las definiciones del propio material y no agregan doctrina: **si se borrara cualquiera de ellos no se perdería ningún contenido del programa**, sólo la ilustración.",
    ])
    para("Las trazas numéricas —la del perceptrón sobre OR, la generación del "
         "algoritmo genético, los pasos de filtrado del paraguas y las cuentas de "
         "Bayes— fueron **verificadas ejecutándolas**, no escritas de memoria.")

    h(2, "A.6 Bibliografía efectivamente usada", "apA_5")
    bullets([
        "**Planificación IAR a partir del ciclo lectivo 2026** (modalidad académica, Plan 2023, UTN FRC). Fuente de la estructura en seis unidades, del reparto de temas y de la carga horaria.",
        "**García, Mario Alejandro**, __Inteligencia Artificial – UTN FRC__ (apunte de cátedra, versión del 7 de noviembre de 2025). Fuente de las correcciones al libro, del encuadre de las metaheurísticas y de los capítulos de aprendizaje automático y modelos bayesianos.",
        "**Russell, S. J. y Norvig, P.**, __Inteligencia artificial: un enfoque moderno__, **2.ª edición** (Pearson, 2004). Capítulos 1-3 (enfoques, fundamentos, historia, agentes y búsqueda), 4 (búsqueda informada, búsqueda local y algoritmos genéticos), 7-8 (lógica e ingeniería del conocimiento), 9 (sistemas de producción), 11 (planificación), 13-14 (incertidumbre y redes bayesianas), 15 (modelos ocultos de Markov), 16.7 (sistemas expertos basados en la teoría de la decisión) y 22-23 (lenguaje natural).",
        "**Russell, S., Norvig, P. y Davis, E.**, __Artificial Intelligence: A Modern Approach__, **4.ª edición** (Prentice Hall, 2021). Sección 19.6 (regresión lineal y logística) y capítulos 24-25 (procesamiento del lenguaje natural clásico y con aprendizaje profundo), que son la fuente de la Unidad 6.",
        "**Presentaciones de la cátedra** convertidas en la carpeta __IA/PDFS EN .MD/__: *IA concepto*, *Agentes inteligentes*, *Aprendizaje Automático ML*, *Reconocimiento de patrones*, *SVM*, *Redes neuronales concepto*, *Algoritmos de redes neuronales*, *Métricas*, *Ejemplo de métricas* y **Perceptrón Simple** (Casatti y Guzmán), esta última la fuente de la estructura en cuatro partes, del papel del sesgo y del cuadro de aplicaciones y limitaciones de [[u2_9a|sección 2.10]].",
        "Obras citadas dentro del apunte y usadas por su intermedio: **Talbi (2009)** para metaheurísticas; **James et al.**, __An Introduction to Statistical Learning__, para el marco de aprendizaje supervisado; **Goodfellow, Bengio y Courville**, __Deep Learning__ (2016), y **LeCun, Bengio y Hinton (2015)** para aprendizaje profundo; **Srivastava et al. (2014)** para dropout; **Bishop (2006)** y **Hastie, Tibshirani y Friedman** para el encuadre de las redes neuronales.",
    ])
    box("Bibliografía del programa que NO está en el vault",
        "El programa analítico lista como **obligatoria** a García (versión actualizada "
        "del aula virtual; acá se usó la del 07/11/2025) y a las dos ediciones de "
        "Russell y Norvig, que sí están. Como **optativa** lista a **Destéfanis** "
        "(2014), **Rich y Knight** (2010), **James et al.** (2021), **Goodfellow et "
        "al.** (2016) y **Talbi** (2009): de ésos, a los tres últimos se accedió sólo "
        "de forma indirecta, a través de lo que el apunte cita.\n"
        "Conseguir **Rich y Knight** cerraría el hueco de la planificación por pila de "
        "objetivos y daría la nomenclatura que el apunte pide priorizar; conseguir "
        "**Destéfanis** cerraría los de lógica difusa y reconocimiento de patrones. "
        "Son los dos que más conviene buscar.")
