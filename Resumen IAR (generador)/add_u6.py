# -*- coding: utf-8 -*-
"""Contenido nuevo de la Unidad 6, a partir del material subido el 17/09/2026:
   - Presentaciones/10- Procesamiento del lenguaje natural CLASICO.pdf (catedra)
   - Collabs/UV/Copia de Procesamiento del lenguaje natural.ipynb
El documento tenia la Unidad 6 armada sobre Russell y Norvig en ingles; la
catedra usa FN/FV y una gramatica e0 en espanol, con un ejemplo trabajado.
"""
from docbuild import h, para, bullets, box, figure, code, salida


def _ej(doc, titulo, texto):
    return box(doc, titulo, texto, fill="FFF8E6", color="C9962A")


# ======================================================================== 6.1
def etapas_comunicacion(doc, fig):
    """Va al final de 6.1 Conceptos basicos."""
    h(doc, 3, "Las etapas de la comunicación", "u6_1_eta")
    para(doc,
         "La cátedra plantea el PLN como un problema **de agentes**: los agentes "
         "emiten señales a otros agentes para informar, pedir ayuda, compartir "
         "conocimiento, preguntar, ordenar o comprometerse. Y por agente se "
         "entiende cualquier sistema que recibe información del medio y actúa "
         "sobre él —un sistema de IA, un control simple, una persona, un pájaro—, "
         "que es exactamente la definición de [[u1_7|sección 1.9]].")
    fig("e33_comunicacion.png",
        "Las nueve etapas de la comunicación sobre el ejemplo de la cátedra. "
        "Tres corresponden al emisor y seis al receptor.")
    para(doc,
         "El ejemplo que recorre toda la presentación es mínimo y conviene "
         "seguirlo entero: el **agente 1** quiere comunicar que el auto está roto "
         "y el **agente 2** termina con `Roto(auto)` incorporado a su base de "
         "conocimiento, junto a lo que ya sabía —`Perro(Tobi)`, "
         "`Perro(x) ∧ ¬Gato(x)`—. Es decir: el resultado del PLN clásico es una "
         "sentencia en **lógica de predicados** ([[u4_5|sección 4.6]]), lista para "
         "razonar con ella.")
    box(doc, "Por qué el enfoque clásico sigue en el programa",
        "La propia cátedra aclara que el enfoque clásico **fue superado en calidad "
        "y eficiencia**, y aun así lo enseña. Las razones que da: enfrenta los "
        "enfoques simbólico y conexionista de [[u1_3|sección 1.4]]; ayuda a "
        "comprender los desafíos que enfrentan los modelos de lenguaje grandes; y "
        "**usa casi todo lo demás de la materia** —agentes inteligentes, sistemas "
        "de producción o basados en reglas ([[u3_prod|sección 3.2]]), búsqueda en "
        "espacio de estados ([[u3_1|sección 3.1]]), sistemas expertos y lógica "
        "([[u4|Unidad 4]]) y razonamiento bajo incertidumbre ([[u5|Unidad 5]])—. "
        "Es, en los hechos, el problema integrador de la materia.")
    para(doc,
         "**Lenguajes formales y lenguajes naturales.** El notebook de la cátedra "
         "marca el contraste que explica toda la dificultad:")
    bullets(doc, [
        "**Formales** —la lógica de predicados, Python—. Los mensajes son un conjunto de cadenas, cada una concatenación de símbolos terminales. **Tienen definiciones estrictas**, asocian un significado a cada cadena válida, y ese significado está determinado **sólo por su forma**.",
        "**Naturales**. Se generan espontáneamente en un grupo de hablantes y **no tienen definiciones estrictas**. El significado específico y contextual de sus componentes interviene en la validez de la frase. No se dejan caracterizar fácilmente porque no hay reglas gramaticales claras —o no se respetan—, hay ambigüedad, y la relación entre símbolos y objetos no está formalmente definida.",
    ])
    _ej(doc, "La cita que resume el problema",
        "«Una confusión común es que el uso del lenguaje tiene que ver "
        "principalmente con las palabras y lo que significan. No es así.» —Herb "
        "Clark, citado por la cátedra—. Tiene que ver con las personas y con lo "
        "que ellas quieren decir. De ahí que exista una etapa de **interpretación "
        "pragmática** separada de la semántica: la semántica da el significado "
        "literal de la oración, la pragmática da el que tiene **dicha en esa "
        "situación**.")


# ======================================================================== 6.3
def gramatica_e0(doc):
    """Va al final de 6.3 Gramatica."""
    h(doc, 3, "El léxico y la gramática ε₀ de la cátedra", "u6_3_e0")
    para(doc,
         "La cátedra trabaja sobre **ε₀**, un fragmento del español, y conviene "
         "usar su nomenclatura porque es la del parcial: **S** para sentencia, "
         "**FN** para frase nominal —hace referencia a objetos del mundo—, **FV** "
         "para frase verbal —indica acciones— y **FP** para frase preposicional. A "
         "esas categorías se las llama **símbolos no terminales**, y la gramática "
         "las define con reglas de reescritura en notación **Backus-Naur (BNF)**.")
    box(doc, "Dos vocabularios para lo mismo",
        "La traducción de Russell y Norvig —y el resto de esta unidad, que está "
        "armada sobre ese libro— habla de **sintagma nominal (SN)** y **sintagma "
        "verbal (SV)**. La cátedra dice **frase nominal (FN)** y **frase verbal "
        "(FV)**. Son exactamente lo mismo: *noun phrase* y *verb phrase*. "
        "Conviene tener presentes las dos formas, porque el apunte y las "
        "presentaciones no coinciden, pero **en el parcial manda la nomenclatura "
        "de la cátedra**.")
    para(doc, "**El léxico**, que como señala la cátedra también está escrito en "
              "forma de reglas:")
    code(doc,
         "Sustantivo   -> auto | casa | ruedas | trabajo | ...\n"
         "Verbo        -> esta | es | volver | comer | salio | ...\n"
         "Adjetivo     -> roto | azul | lenta | apurado | ...\n"
         "Adverbio     -> aca | alla | demasiado | mal | ...\n"
         "Pronombre    -> mi | tu | yo | ello | ...\n"
         "Articulo     -> el | las | lo | un | unas | ...\n"
         "Preposicion  -> a | en | sobre | ...\n"
         "Conjuncion   -> y | o | pero | ...\n"
         "Digito       -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9",
         lang="bnf")
    para(doc, "**Las reglas gramaticales**, con el ejemplo que da la cátedra para "
              "cada una:")
    code(doc,
         "S   ->  FN FV                 Yo + siento calor\n"
         "     |  S Conjuncion S        Yo siento calor + pero + ella siente frio\n"
         "\n"
         "FN  ->  Pronombre             yo\n"
         "     |  Sustantivo            casa\n"
         "     |  Articulo Sustantivo   la + casa\n"
         "     |  Digito                8\n"
         "     |  FN FP                 la casa + sobre la montana\n"
         "\n"
         "FV  ->  Verbo                 comer\n"
         "     |  Verbo Adjetivo        parece + divertido\n"
         "     |  FV FN                 siento + calor\n"
         "     |  FV FP                 gira + al este\n"
         "     |  FV Adverbio           ve + adelante\n"
         "\n"
         "FP  ->  Preposicion FN        sobre + la montana",
         lang="bnf")
    box(doc, "Dónde está la recursión, y por qué importa",
        "Tres reglas se refieren a sí mismas: `S -> S Conjunción S`, `FN -> FN FP` "
        "y `FV -> FV FN`. Son las que hacen que una gramática **finita** —nueve "
        "categorías léxicas y catorce reglas— genere **infinitas** oraciones, que "
        "es la observación con la que abre la unidad: los humanos parecen usar la "
        "gramática para producir infinitos mensajes estructurados. También son las "
        "que hacen que el análisis sintáctico sea un problema de **búsqueda** y no "
        "una simple sustitución: `FN -> FN FP` permite «la casa sobre la montaña "
        "en el valle junto al río…» sin límite.")


# ======================================================================== 6.4
def analisis_sintactico(doc, fig):
    """Va al final de 6.4 Analisis gramatical."""
    h(doc, 3, "El análisis sintáctico como búsqueda: «El auto está roto»",
      "u6_4_arb")
    para(doc,
         "El **análisis sintáctico** es la recuperación de la estructura de la "
         "oración con base en una gramática. El resultado es un **árbol "
         "gramatical** donde los nodos internos son frases o categorías, los arcos "
         "son aplicaciones de reglas y **las hojas son las palabras**.")
    para(doc,
         "La cátedra lo presenta explícitamente como una **búsqueda en un espacio "
         "de estados** ([[u3_1|sección 3.1]]): el estado inicial es el árbol sin "
         "resolver `[S: ?]`, los operadores son las reglas de la gramática y el "
         "objetivo es un árbol cuyas hojas sean exactamente las palabras de la "
         "oración. La traza que se desarrolla en clase:")
    code(doc,
         "[S: ?]\n"
         "                      aplicar  S -> FN FV  |  S Conjuncion S\n"
         "[S: [S: ?][Conj: ?][S: ?]]        [S: [FN: ?][FV: ?]]\n"
         "                      expandir FN, cinco alternativas\n"
         "[S: ...] ... [S: [FN: [Articulo: ?][Sustantivo: ?]][FV: ?]] ... [S: ...]\n"
         "                      unificar con el lexico\n"
         "[S: [FN: [Articulo: el][Sustantivo: ?]][FV: ?]]\n"
         "[S: [FN: [Articulo: el][Sustantivo: auto]][FV: ?]]\n"
         "                      expandir FV\n"
         "[S: [FN: [Articulo: el][Sustantivo: auto]]\n"
         "    [FV: [Verbo: esta][Adjetivo: roto]]]",
         lang="texto")
    _ej(doc, "Por qué es una búsqueda y no un cálculo",
        "En el primer paso ya hay **dos** reglas aplicables para S, y al expandir "
        "FN hay **cinco**. Cada elección abre una rama y la mayoría no lleva a "
        "ningún lado: si el analizador hubiera elegido `S -> S Conjunción S` "
        "tendría que encontrar una conjunción en «El auto está roto», y no la hay. "
        "Por eso hace falta **retroceder** y probar otra rama, igual que en "
        "cualquier búsqueda no informada de [[u3_2|sección 3.3]]. Y por eso el "
        "tamaño de la gramática importa tanto: cada regla nueva multiplica el "
        "factor de ramificación.")
    fig("e34_arbol.png",
        "El árbol gramatical de «El auto está roto» con la gramática ε₀, y sobre "
        "cada nodo el significado que le asigna la gramática aumentada.")


# ======================================================================== 6.5
def semantica(doc):
    """Va al final de 6.5 Gramaticas aumentadas."""
    h(doc, 3, "Interpretación semántica: de la sintaxis al significado",
      "u6_5_sem")
    para(doc,
         "La **interpretación semántica** es la extracción del significado de las "
         "declaraciones. El mecanismo de la cátedra es directo: se **aumenta la "
         "gramática** agregando, para cada regla sintáctica, una regla que produce "
         "el cambio equivalente en el lenguaje formal elegido para representar el "
         "conocimiento —acá, lógica de predicados—. Cada categoría gana un "
         "atributo `.sem`.")
    para(doc, "Las reglas usadas en el ejemplo del auto roto:")
    code(doc,
         "S   -> FN FV                    S.sem   = FV.sem(FN.sem)\n"
         "FN  -> Articulo Sustantivo      FN.sem  = Articulo.sem(Sustantivo.sem)\n"
         "FV  -> Verbo Adjetivo           FV.sem  = λs Verbo.sem(Adjetivo.sem)(s)\n"
         "\n"
         "Articulo   -> el                Articulo.sem   = λx x\n"
         "Sustantivo -> auto              Sustantivo.sem = c_auto\n"
         "Verbo      -> esta              Verbo.sem      = λP λs P(s)\n"
         "Adjetivo   -> roto              Adjetivo.sem   = λx Roto(x)",
         lang="texto")
    para(doc, "El significado se arma **de las hojas hacia la raíz**, aplicando "
              "cada función a su argumento:")
    code(doc,
         "FN.sem = (λx x)(c_auto)                      = c_auto\n"
         "\n"
         "FV.sem = λs (λP λz P(z))(λx Roto(x))(s)\n"
         "       = λs (λz (λx Roto(x))(z))(s)\n"
         "       = λs (λz Roto(z))(s)\n"
         "       = λs Roto(s)\n"
         "\n"
         "S.sem  = FV.sem(FN.sem) = (λs Roto(s))(c_auto) = Roto(c_auto)",
         lang="texto")
    box(doc, "Qué hace cada λ",
        "**λx x** es la función identidad: el artículo «el» no aporta contenido, "
        "sólo deja pasar el significado del sustantivo. **c_auto** es una "
        "constante: el objeto del mundo. **λx Roto(x)** es un predicado a la "
        "espera de un argumento —«ser roto»—. Y **λP λs P(s)** es el verbo "
        "copulativo «está», que toma un predicado *P* y devuelve una función que "
        "se lo aplica a un sujeto: la cópula no agrega significado, **conecta** el "
        "adjetivo con el sujeto. El resultado, `Roto(c_auto)`, es una sentencia de "
        "lógica de predicados como cualquiera de [[u4_5|sección 4.6]], y con ella "
        "el agente 2 ya puede hacer inferencia.")
    _ej(doc, "Esto es semántica denotacional, y tiene un límite",
        "La forma en que la cátedra define el significado de cada palabra es "
        "**símbolo (significante) ↔ significado (idea o cosa)**: la **semántica "
        "denotacional**, el sentido literal y objetivo, tal como aparecería en un "
        "diccionario. Los primeros intentos de PLN se centraron en esto y "
        "construyeron diccionarios enormes, como **WordNet**. El límite es que "
        "asigna a cada símbolo un significado fijo e independiente del contexto, "
        "que es justo lo contrario de lo que hacen los *embeddings* de "
        "[[u6_6|sección 6.6]] —y la razón por la que se los presenta como una "
        "**semántica distribuida**—.")

    h(doc, 3, "Desambiguación", "u6_5_des")
    para(doc,
         "El análisis sintáctico y la interpretación semántica pueden devolver "
         "**más de un** resultado válido. La desambiguación es la etapa que elige "
         "uno. La cátedra lista cuatro fuentes de ambigüedad:")
    bullets(doc, [
        "**Léxica** — palabras con varios significados.",
        "**Sintáctica** — la misma oración admite más de un árbol gramatical.",
        "**Metonimia** — una figura de sustitución: se nombra algo por otra cosa asociada.",
        "**Metáfora**.",
    ])
    _ej(doc, "El ejercicio de la palabra tapada",
        "El notebook de la cátedra propone deducir qué significa una palabra "
        "borrada a partir de tres oraciones: «La XXXX se quedó sin batería en "
        "medio de la clase», «Guardé todas mis fotos en la XXXX nueva», «La XXXX "
        "del laboratorio necesita una actualización urgente». Ninguna de las tres "
        "define la palabra, y sin embargo entre las tres queda claro de qué se "
        "habla. Ese ejercicio es la intuición detrás de la frase del lingüista "
        "**J. R. Firth** que cita la cátedra —«reconocerás una palabra por la "
        "compañía que tiene»— y el puente directo a los *word embeddings*: el "
        "significado está en el **contexto**, no en una entrada de diccionario.")


# ======================================================================== 6.2
def codigo_modelos_lenguaje(doc):
    """Va al final de 6.2 Modelos de lenguaje."""
    para(doc,
         "**El código de tu Colab.** El notebook de PLN muestra cómo se pasa de "
         "texto libre a los vectores que necesitan los modelos de esta sección. "
         "Tres oraciones de prueba:")
    code(doc,
         "texto = [\"Where is the Life we have lost in living?\",\n"
         "         \"Where is the wisdom we have lost in knowledge?\",\n"
         "         \"Where is the knowledge we have lost in information?\"]\n"
         "\n"
         "from sklearn.feature_extraction.text import CountVectorizer\n"
         "vectorizer = CountVectorizer()\n"
         "vectorizer.fit(texto)\n"
         "vectorizer.vocabulary_")
    salida(doc,
           "{'where': 10, 'is': 3, 'the': 8, 'life': 5, 'we': 9, 'have': 0,\n"
           " 'lost': 7, 'in': 1, 'living': 6, 'wisdom': 11, 'knowledge': 4,\n"
           " 'information': 2}")
    para(doc, "Cada oración se vuelve un vector de conteos sobre ese vocabulario "
              "de doce palabras: **eso es la bolsa de palabras**.")
    code(doc, "oh_words = vectorizer.transform(texto)\noh_words.toarray()")
    salida(doc,
           "array([[1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0],\n"
           "       [1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1],\n"
           "       [1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0]])")
    _ej(doc, "Lo que la matriz deja ver",
        "Las columnas 0, 1, 3, 7, 8, 9 y 10 —`have`, `in`, `is`, `lost`, `the`, "
        "`we`, `where`— valen **1 en las tres filas**: aparecen en todas las "
        "oraciones y por lo tanto **no sirven para distinguirlas**. Las únicas que "
        "discriminan son `life`, `living`, `wisdom`, `knowledge` e `information`. "
        "Ese es exactamente el problema que resuelve **tf-idf**, que baja el peso "
        "de lo que aparece en muchos documentos:")
    code(doc,
         "from sklearn.feature_extraction.text import TfidfVectorizer\n"
         "tfidf_vectorizer = TfidfVectorizer()\n"
         "tfidf_vectorizer.fit(texto)\n"
         "print(tfidf_vectorizer.transform(texto).toarray())")
    salida(doc,
           "[[0.28 0.28 0.   0.28 0.   0.47 0.47 0.28 0.28 0.28 0.28 0.  ]\n"
           " [0.29 0.29 0.   0.29 0.38 0.   0.   0.29 0.29 0.29 0.29 0.5 ]\n"
           " [0.29 0.29 0.5  0.29 0.38 0.   0.   0.29 0.29 0.29 0.29 0.  ]]")
    para(doc, "Se ve el efecto directo: las palabras comunes a las tres oraciones "
              "quedan en **0,28–0,29**, mientras que `living` y `life` —exclusivas "
              "de la primera— suben a **0,47**, e `information` y `wisdom` "
              "—exclusivas de una sola cada una— llegan a **0,50**. `knowledge`, "
              "que está en dos de las tres, queda en el medio con **0,38**.")
    para(doc, "Y los **n-gramas**, que recuperan parte del orden que la bolsa de "
              "palabras tira:")
    code(doc,
         "# secuencias de longitud minima 2 y maxima 2\n"
         "bigram_vectorizer = CountVectorizer(ngram_range=(2, 2))\n"
         "bigram_vectorizer.fit(texto)\n"
         "bigram_vectorizer.get_feature_names_out()")
    salida(doc,
           "array(['have lost', 'in information', 'in knowledge', 'in living',\n"
           "       'is the', 'knowledge we', 'life we', 'lost in', 'the knowledge',\n"
           "       'the life', 'the wisdom', 'we have', 'where is', 'wisdom we'])")
    box(doc, "El costo de los n-gramas, en números",
        "Doce unigramas se convierten en **catorce bigramas**, y con "
        "`ngram_range=(1,2)` —unigramas y bigramas juntos— el vocabulario pasa a "
        "**veintiséis**. Con tres oraciones de nueve palabras. Ahí está el "
        "compromiso de [[u6_2b|sección 6.2]]: los n-gramas capturan que «no bueno» "
        "significa lo contrario que «bueno», pero el vocabulario crece y la matriz "
        "se vuelve cada vez más rala. Como dice el propio notebook, el *n* óptimo "
        "depende del algoritmo, del conjunto de datos y de la tarea: **es un "
        "hiperparámetro**, con todo lo que eso implica según "
        "[[u2_10_con|las consideraciones de la sección 2.10]].")


# ======================================================================== 6.6
def codigo_embeddings(doc):
    """Va al final de 6.6 word embeddings."""
    para(doc,
         "**El código de tu Colab.** El notebook carga **GloVe** entrenado sobre "
         "Wikipedia y Gigaword, con vectores de cien dimensiones, y mide cercanía "
         "con **similitud coseno**:")
    code(doc,
         "import gensim.downloader as api\n"
         "model = api.load(\"glove-wiki-gigaword-100\")\n"
         "model['bread'].shape")
    salida(doc, "(100,)")
    para(doc, "El método `most_similar()` calcula la similitud coseno de una "
              "palabra contra todo el vocabulario y devuelve las más cercanas. Los "
              "resultados reales:")
    code(doc, "model.most_similar('peach')")
    salida(doc,
           "[('apricot', 0.772), ('pear', 0.770), ('mango', 0.742),\n"
           " ('raspberry', 0.713), ('pecan', 0.708), ('pumpkin', 0.708),\n"
           " ('watermelon', 0.702), ('blueberry', 0.701), ('plum', 0.692),\n"
           " ('cherry', 0.689)]")
    code(doc, "model.most_similar('argentina')")
    salida(doc,
           "[('uruguay', 0.836), ('brazil', 0.828), ('chile', 0.825),\n"
           " ('paraguay', 0.807), ('spain', 0.776), ('ecuador', 0.753),\n"
           " ('mexico', 0.751), ('portugal', 0.750), ('peru', 0.744),\n"
           " ('argentine', 0.732)]")
    para(doc, "Nadie le dijo al modelo que Uruguay limita con Argentina ni que el "
              "damasco y el durazno son parientes. Todo eso salió de **con qué "
              "otras palabras aparecen** en el corpus. Pero los dos casos "
              "siguientes son más instructivos que los que funcionan bien:")
    code(doc, "model.most_similar('apple')")
    salida(doc,
           "[('microsoft', 0.745), ('ibm', 0.682), ('intel', 0.678),\n"
           " ('software', 0.678), ('dell', 0.674), ('pc', 0.668),\n"
           " ('macintosh', 0.662), ('iphone', 0.660), ('ipod', 0.653),\n"
           " ('hewlett', 0.652)]")
    code(doc, "model.most_similar('orange')")
    salida(doc,
           "[('yellow', 0.736), ('red', 0.714), ('blue', 0.712),\n"
           " ('green', 0.711), ('pink', 0.678), ('purple', 0.677),\n"
           " ('black', 0.671), ('colored', 0.665), ('lemon', 0.625),\n"
           " ('peach', 0.617)]")
    box(doc, "Los dos resultados que hay que saber explicar",
        "**`apple` no devuelve ninguna fruta**: devuelve Microsoft, IBM, Intel y "
        "Dell. **`orange` devuelve casi puros colores**, y la fruta aparece recién "
        "abajo con `lemon` y `peach`. No son errores; son la consecuencia directa "
        "de la semántica distribuida. El corpus es Wikipedia más Gigaword —texto "
        "periodístico—, donde «apple» aparece abrumadoramente como empresa. "
        "De ahí dos límites concretos: **el corpus decide el significado**, y un "
        "*embedding* clásico asigna **un solo vector por palabra**, así que los "
        "sentidos de una palabra polisémica se promedian en un único punto y gana "
        "el más frecuente. Es exactamente la desambiguación léxica de "
        "[[u6_5_des|la sección de desambiguación]], y es lo que resuelven los "
        "modelos contextuales: el mecanismo de atención de "
        "[[u6_9a|sección 6.9]] produce un vector distinto para cada aparición de "
        "la palabra, según su contexto.")
    _ej(doc, "Y el sesgo entra por la misma puerta",
        "Si el significado sale del corpus, **los prejuicios del corpus también "
        "entran al modelo**. Es el mismo mecanismo que hace que `apple` sea una "
        "empresa: no hay un paso donde alguien decida qué significa cada palabra, "
        "sólo un recuento de con qué aparece. Por eso la evaluación de sesgos de "
        "[[u1_6|sección 1.8]] no es un tema aparte del PLN sino parte de su "
        "ingeniería, y por eso el RA6 del programa la pide explícitamente.")
