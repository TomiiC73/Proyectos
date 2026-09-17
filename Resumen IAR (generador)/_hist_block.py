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

