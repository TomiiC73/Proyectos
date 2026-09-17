# -*- coding: utf-8 -*-
"""Contenido nuevo de la Unidad 2, a partir del material subido el 17/09/2026:
   - Practico/Redes Neuronales.pdf      (catedra)
   - Practico/Aprendizaje Profundo.pdf  (catedra)
   - Collabs/UV/...Backprop con Pytorch, K-means
   - Collabs/Clase 4/Convolucion en imagenes
Cada funcion agrega al final del doc; insertar.py se encarga de moverlo.
"""
from docbuild import h, para, bullets, box, figure, code, salida


def _ej(doc, titulo, texto):
    return box(doc, titulo, texto, fill="FFF8E6", color="C9962A")


# =====================================================================  2.10
def motor_del_aprendizaje(doc):
    """Va despues de 'Redes con conexiones hacia adelante y retropropagacion'."""
    h(doc, 3, "El motor del aprendizaje: pérdida, gradiente y regla de la cadena",
      "u2_10_mot")
    para(doc,
         "La sección anterior describe **qué** hace la retropropagación. La "
         "presentación de la cátedra *Redes Neuronales Artificiales* agrega **con "
         "qué herramientas** lo hace, que es lo que permite entender por qué "
         "funciona y por qué a veces no.")

    para(doc, "**La función de pérdida.** Una vez que la red produce una "
              "predicción, lo primero es medir cuán equivocada estuvo. La "
              "**función de pérdida** (*loss function*) es la fórmula que actúa "
              "de juez: compara la predicción contra la respuesta correcta y "
              "condensa el error en **un único número**. Cuanto más alto, peor el "
              "rendimiento.")
    bullets(doc, [
        "**Regresión** (predecir un número): **error cuadrático medio (MSE)**, que penaliza fuertemente los errores grandes. Es el mismo que se usa en [[u2_3|sección 2.3]].",
        "**Clasificación** (predecir una categoría): **entropía cruzada** (*cross-entropy*), efectiva para medir la diferencia entre la predicción y la categoría real.",
    ])

    para(doc, "**El descenso de gradiente.** Es el algoritmo de optimización que "
              "guía toda la corrección: busca el conjunto de pesos y sesgos que "
              "haga la pérdida lo más chica posible. El **gradiente del error** "
              "dice dos cosas —la dirección en la que los pesos deberían cambiar "
              "para **aumentar** el error, y la magnitud de ese cambio—, así que "
              "el algoritmo da el paso en la dirección **opuesta**.")
    _ej(doc, "La analogía de la cátedra · el excursionista en la niebla",
        "Estás en una montaña con mucha niebla; la montaña es la función de "
        "pérdida y querés llegar al punto más bajo del valle, que es el error "
        "mínimo. No ves el camino. **Mirás a tus pies**: sentís la inclinación del "
        "terreno donde estás parado, y esa inclinación es el gradiente, que "
        "siempre apunta hacia la subida más empinada. **Das un paso** en la "
        "dirección exactamente opuesta. **Repetís**. Dos cosas se leen directo de "
        "la analogía: la **tasa de aprendizaje α** es el tamaño del paso —si es "
        "muy grande te pasás del fondo, si es muy chica tardás una eternidad—, y "
        "como sólo mirás a tus pies, nada garantiza que el valle al que llegues "
        "sea el más profundo de la montaña, sino apenas el más cercano.")

    para(doc, "**La regla de la cadena.** Una red profunda no es otra cosa que "
              "una **función compuesta gigante**: la salida de la primera capa es "
              "la entrada de la segunda, y así hasta el final. Cuando la red se "
              "equivoca hay que saber cuánto aportó cada peso, en cada capa, a ese "
              "error final. La regla de la cadena del cálculo es la herramienta "
              "que permite deshacer esa composición y calcular la influencia de "
              "cada componente. Backpropagation **es** la regla de la cadena "
              "aplicada de la salida hacia la entrada.")
    _ej(doc, "La analogía de la cátedra · el efecto dominó y el reparto de culpa",
        "**Dominó:** una fila larga de fichas. Si empujás la primera —un peso al "
        "principio de la red— empuja a la siguiente, y así hasta que cae la última, "
        "que es la predicción. La regla de la cadena permite calcular cómo un "
        "cambio chico en la primera ficha afecta la posición final de la última, "
        "teniendo en cuenta todas las intermedias. "
        "**Reparto de culpa:** si un producto sale defectuoso de una línea de "
        "montaje, el encargado recorre la línea hacia atrás preguntándole a cada "
        "operario cuánto contribuyó al defecto, hasta llegar al origen y dar "
        "instrucciones nuevas. Eso es exactamente actualizar los pesos.")

    para(doc, "**El algoritmo completo**, tal como lo da la cátedra:")
    bullets(doc, [
        "Definir el valor de **α**.",
        "**Inicializar los pesos** con valores aleatorios.",
        "Mientras el **error medio** sea mayor que el error aceptado, ejecutar un **ciclo completo de entrenamiento (época)**. Dentro de la época, mientras queden vectores de entrenamiento:",
    ])
    bullets(doc, [
        "Tomar un vector entrada/salida del conjunto de datos.",
        "Calcular la salida de cada capa hasta llegar a la capa de salida.",
        "Calcular el error de las neuronas de la capa de salida.",
        "Calcular el error de las neuronas de la última capa oculta.",
        "Repetir el paso anterior para todas las capas ocultas, desde la salida hacia la entrada.",
        "Calcular los **deltas** de cada neurona en función de su propio error.",
        "**Modificar los pesos.**",
    ], level=2)
    box(doc, "Por qué el orden importa",
        "Los errores de **todas** las capas se calculan **antes** de modificar "
        "ningún peso. Si se actualizaran los pesos de la capa de salida antes de "
        "calcular el error de las ocultas, ese error se estaría propagando a "
        "través de pesos que ya cambiaron, y dejaría de corresponder a la red que "
        "produjo la predicción.")


def backprop_pytorch(doc):
    """Codigo real: el mismo XOR a mano y con PyTorch."""
    para(doc,
         "**El código de tu Colab.** El notebook *Redes Neuronales 2 (Backprop con "
         "PyTorch)* resuelve el mismo XOR de [[u2_9b|sección 2.10]] de dos formas, "
         "y la comparación es la mejor ilustración de la regla de la cadena. "
         "Primero, la red entera a mano, procesando los cuatro vectores juntos "
         "(*batch*) en vez de uno por vez:")
    code(doc,
         "A, B, C = 2, 2, 1      # neuronas de entrada, ocultas y de salida\n"
         "lr = 1\n"
         "X = np.array([[0,0],[0,1],[1,0],[1,1]])\n"
         "Y = np.array([[0],[1],[1],[0]])\n"
         "w1 = np.random.uniform(-.1, .1, size=(A+1,B))\n"
         "w2 = np.random.uniform(-.1, .1, size=(B+1,C))\n"
         "\n"
         "def ciclo(X, Y, w1, w2, lr):\n"
         "    X1 = np.hstack((np.ones((X.shape[0],1)), X))   # columna de sesgo\n"
         "    h  = np.apply_along_axis(logistic, 0, np.matmul(X1, w1))\n"
         "    h1 = np.hstack((np.ones((h.shape[0],1)), h))\n"
         "    o  = np.apply_along_axis(logistic, 0, np.matmul(h1, w2))\n"
         "\n"
         "    error2 = (Y - o) * np.apply_along_axis(logistic_d, 0, o)\n"
         "    error1 = np.matmul(error2, np.transpose(w2[1:,:]))\n"
         "    error1 = error1 * np.apply_along_axis(logistic_d, 0, h)\n"
         "\n"
         "    w1 = w1 + lr * np.matmul(np.transpose(X1), error1)\n"
         "    w2 = w2 + lr * np.matmul(np.transpose(h1), error2)\n"
         "    return w1, w2")
    para(doc, "Las dos líneas de `error` son la regla de la cadena escrita a mano: "
              "`error1` es el error de la capa de salida **traído hacia atrás** por "
              "la traspuesta de los pesos (`w2[1:,:]`, salteando la fila del sesgo) "
              "y multiplicado por la derivada de la activación de la capa oculta.")
    para(doc, "Ahora lo mismo con PyTorch. Desaparece todo el cálculo de errores:")
    code(doc,
         "def ciclo_torch(X, Y, w1_torch, w2_torch, lr):\n"
         "    X1 = torch.hstack((unos, X_torch))\n"
         "    h  = torch.sigmoid(torch.matmul(X1, w1_torch))\n"
         "    h1 = torch.hstack((unos, h))\n"
         "    o  = torch.sigmoid(torch.matmul(h1, w2_torch))\n"
         "\n"
         "    errcuad = torch.mean(torch.square(Y_torch - o))\n"
         "    errcuad.backward()          # <-- la regla de la cadena, automatica\n"
         "\n"
         "    w1_torch = w1_torch - lr * w1_torch.grad\n"
         "    w2_torch = w2_torch - lr * w2_torch.grad\n"
         "    return w1_torch, w2_torch")
    para(doc, "Después de 50.000 ciclos, los pesos de la capa de salida:")
    salida(doc,
           "# a mano                    # con PyTorch\n"
           "[[ -5.68060601]             tensor([[  4.8069],\n"
           " [-12.00502577]                     [ 10.6390],\n"
           " [ 11.83421607]]                    [-10.1604]])")
    box(doc, "Qué muestra la comparación",
        "Los dos vectores son **distintos** y sin embargo **los dos resuelven "
        "XOR**. Reejecutando este mismo código con ocho inicializaciones "
        "distintas, las ocho convergen, con salidas en torno a "
        "**0,006 · 0,994 · 0,993 · 0,005**; en seis el patrón de signos es "
        "(+, −, +) y en dos es el espejado. Una de esas corridas reproduce el "
        "resultado del notebook casi dígito por dígito: −5,703 · −12,005 · +11,868 "
        "contra los −5,681 · −12,005 · +11,834 de arriba. "
        "La conclusión práctica: la inicialización aleatoria decide **a cuál de "
        "los mínimos equivalentes** cae cada corrida —el excursionista arranca en "
        "otro punto de la montaña—, así que **comparar pesos entre corridas no "
        "dice nada; comparar el error sí**. "
        "Y la diferencia con el intento manual de [[u2_9b|sección 2.10]], que "
        "quedaba a mitad de camino en 0,27 · 0,68 · 0,68 · 0,41: acá hay **sesgo** "
        "en las dos capas (la columna de unos), se entrena **por lotes** y se dan "
        "50.000 ciclos con α = 1.")


def consideraciones(doc):
    h(doc, 3, "Consideraciones prácticas al entrenar", "u2_10_con")
    para(doc,
         "La cátedra cierra el tema con las decisiones que quedan en manos de "
         "quien diseña la red y que **no** se aprenden durante el entrenamiento.")
    bullets(doc, [
        "**Los hiperparámetros.** Son los ajustes que se configuran *antes* de entrenar: no son los pesos que la red aprende, sino las reglas que guían ese aprendizaje. No hay fórmula para elegirlos; es experimentación y experiencia.",
        "**La arquitectura.** Cuántas capas ocultas y cuántas neuronas por capa. **Demasiado simple**: la red no tiene capacidad para aprender los patrones y cae en **subentrenamiento** (*underfitting*). **Demasiado compleja**: en vez de aprender los patrones generales memoriza los datos de entrenamiento con todo su ruido, y cae en **sobreentrenamiento** (*overfitting*).",
        "**La inicialización de los pesos.** Una mala inicialización puede impedir directamente que la red aprenda —por ejemplo, poner todos los pesos en cero, o usar valores muy grandes—. **Xavier** y **He** son formas sistemáticas de elegir un buen punto de partida.",
        "**La tasa de aprendizaje α.** Probablemente el hiperparámetro más crítico. **Muy alta**: el modelo da saltos grandes, se pasa del punto óptimo y nunca lo encuentra, como una pelota que rebota de un lado al otro del valle sin llegar al fondo —es lo que le pasa al Adaline de [[u2_9c|sección 2.10]] con α = 0,001—. **Muy baja**: aprende, pero puede tardar un tiempo inaceptable.",
    ])
    _ej(doc, "La analogía de la cátedra · la torta",
        "Los ingredientes son los datos y el modelo es la torta. Los "
        "hiperparámetros serían la **temperatura del horno** (la tasa de "
        "aprendizaje), el **tiempo de cocción** (la cantidad de épocas) y el "
        "**tamaño del molde** (la arquitectura de la red). Una mala combinación da "
        "una torta quemada —el modelo no converge—, cruda por dentro "
        "—subentrenamiento— o que se desinfla al sacarla —sobreentrenamiento—.")
    _ej(doc, "Por qué inicializar todos los pesos en cero rompe la red",
        "No es un detalle de implementación. Si todas las neuronas de una capa "
        "arrancan con los mismos pesos, reciben las mismas entradas y producen la "
        "misma salida; al retropropagar reciben **el mismo error** y por lo tanto "
        "**la misma corrección**. Siguen siendo idénticas para siempre: una capa "
        "de veinte neuronas se comporta como si tuviera una sola. La asimetría "
        "inicial es lo que permite que cada neurona se especialice, y por eso los "
        "pesos arrancan aleatorios —en el código de arriba, "
        "`np.random.uniform(-.1, .1, ...)`—.")
    box(doc, "Sobreentrenamiento · la analogía del estudiante",
        "Dos estudiantes preparan un examen de matemática. El que **sobreentrena** "
        "memoriza la solución de los 100 problemas del libro: si le toca uno de "
        "esos, lo resuelve perfecto, pero si le ponen un problema nuevo con los "
        "mismos conceptos y otros números, no sabe qué hacer, porque nunca entendió "
        "la fórmula. El que **generaliza bien** se enfoca en entender los conceptos: "
        "quizá no recuerde todas las soluciones, pero resuelve cualquier problema "
        "nuevo. El segundo es el objetivo. Las contramedidas concretas están en la "
        "sección de regularización, y la forma de **detectarlo** es el esquema de "
        "evaluación de [[u2_5|sección 2.5]]: si el error de entrenamiento baja y el "
        "de prueba sube, es sobreentrenamiento.")


# =====================================================================  2.11
def tipos_de_capas(doc):
    """Va al comienzo de 2.11, antes de 'Funciones de activacion'."""
    h(doc, 3, "Los tipos de capa y para qué sirve cada uno", "u2_11_cap")
    para(doc,
         "La presentación de la cátedra *Aprendizaje Profundo* ordena el tema por "
         "**tipo de capa**, que es la forma práctica de pensar una arquitectura. "
         "El punto de partida es una advertencia: una red suficientemente profunda "
         "de capas densas puede, **sólo en teoría**, resolver cualquier problema. "
         "La arquitectura importa porque *elimina caminos innecesarios*.")
    bullets(doc, [
        "**Densamente conectadas** (*dense*, *fully connected*). Cada neurona recibe una conexión de **todas** las de la capa anterior. Son las que hacen la clasificación final a partir de las características que extrajeron las capas previas. Van bien con datos **sin estructura espacial ni temporal**, como los de una tabla. Ejemplo de la cátedra: en un modelo que predice si un cliente abandona un servicio, la capa final es densa y combina edad, antigüedad y monto de la última factura para dar la probabilidad de abandono —es el caso de [[u2_9a|sección 2.10]]—.",
        "**Convolucionales**. El corazón de las CNN. En vez de mirar todo de una vez, usan **filtros** o *kernels* —lupas chicas— que se deslizan sobre la imagen detectando características locales: bordes, esquinas, texturas. Las primeras capas detectan patrones simples y las profundas los combinan. Ejemplo: en una red que reconoce rostros, las primeras capas detectan los bordes de la nariz y los ojos, las siguientes reconocen «un ojo», y las finales ensamblan «un rostro».",
        "**De pooling** (agrupamiento). Casi siempre siguen a una convolucional y **reducen y resumen**. **MaxPooling** se queda con el valor máximo de una región, y sirve para capturar la característica más prominente; **AveragePooling** promedia, y suaviza. Hacen la red más eficiente —menos datos— y más robusta, porque la vuelven menos sensible a la **posición exacta** de la característica: gracias al pooling el modelo reconoce al gato esté en el centro o en la esquina de la imagen.",
        "**Recurrentes** (RNN). Diseñadas para datos **secuenciales**, donde el orden importa. Tienen una especie de memoria: procesan la secuencia elemento por elemento y en cada paso la salida vuelve a entrar como parte de la entrada del paso siguiente. Ejemplo: predecir la próxima palabra en «El cielo es…» exige recordar las anteriores.",
        "**LSTM** (*Long Short-Term Memory*). Un tipo avanzado de capa recurrente que resuelve el mayor problema de las RNN simples: la dificultad para recordar a largo plazo. Tienen **compuertas** internas que deciden qué guardar, qué olvidar y qué usar en cada paso. Ejemplo: traducir un párrafo entero, donde el género de una palabra al final puede depender de un sustantivo que apareció al principio. El detalle está en [[u6_7|sección 6.7]].",
    ])
    box(doc, "La jerarquía es el concepto, no la cantidad de capas",
        "La palabra «profundo» se refiere a la cantidad de capas —una red simple "
        "puede tener dos o tres; una profunda, cientos—, pero lo que importa es "
        "**qué** habilita esa profundidad: aprender características **por "
        "jerarquías**. Para reconocer un gato, las primeras capas detectan líneas, "
        "bordes y gradientes de color; las intermedias combinan eso en ojos, orejas "
        "y texturas de pelaje; las finales unen esas partes en el concepto «gato». "
        "Construir conocimiento de lo simple a lo complejo **de forma automática** "
        "es lo que distingue al aprendizaje profundo del esquema clásico, donde la "
        "extracción de características era una etapa previa y separada.")


def convolucion_codigo(doc):
    """Va al final de la subseccion de CNN."""
    para(doc,
         "**El código de tu Colab.** El notebook *Convolución en imágenes* "
         "implementa la convolución a mano, sin librerías, y deja a la vista los "
         "dos hiperparámetros: el **paso** (*stride*) y el **relleno** (*padding*).")
    code(doc,
         "def convolution2d(image, kernel, paso=1, relleno=1):\n"
         "    # Rellenar la imagen con 0 en todas las direcciones\n"
         "    image = np.pad(image, [(relleno, relleno), (relleno, relleno)],\n"
         "                   mode='constant', constant_values=0)\n"
         "    kernel_height, kernel_width = kernel.shape\n"
         "    padded_height, padded_width = image.shape\n"
         "    # Tamano de la salida\n"
         "    output_height = (padded_height - kernel_height) // paso + 1\n"
         "    output_width  = (padded_width  - kernel_width)  // paso + 1\n"
         "    new_image = np.zeros((output_height, output_width)).astype(np.float32)\n"
         "\n"
         "    for y in range(0, output_height):\n"
         "        for x in range(0, output_width):\n"
         "            new_image[y][x] = np.sum(\n"
         "                image[y * paso : y * paso + kernel_height,\n"
         "                      x * paso : x * paso + kernel_width] * kernel\n"
         "            ).astype(np.float32)\n"
         "    return new_image")
    para(doc, "La línea del tamaño de salida es la fórmula general de la "
              "convolución: con una imagen de lado *I*, un kernel de lado *K*, "
              "relleno *P* y paso *S*, la salida tiene lado **(I + 2P − K)/S + 1**. "
              "Con la imagen de 24×24 del notebook, kernel 3×3, relleno 1 y paso 1, "
              "da (24 + 2 − 3)/1 + 1 = **24**: el relleno es exactamente el que "
              "hace falta para que la salida conserve el tamaño de la entrada.")
    para(doc, "Los kernels que usa el práctico, todos de 3×3:")
    code(doc,
         "kernel_identity = np.array([[0, 0, 0],\n"
         "                            [0, 1, 0],\n"
         "                            [0, 0, 0]])\n"
         "sharpen         = np.array([[ 0,-1, 0],\n"
         "                            [-1, 5,-1],\n"
         "                            [ 0,-1, 0]])\n"
         "ridge           = np.array([[ 0,-1, 0],\n"
         "                            [-1, 4,-1],\n"
         "                            [ 0,-1, 0]])\n"
         "gaussian_blur   = np.array([[1, 2, 1],\n"
         "                            [2, 4, 2],\n"
         "                            [1, 2, 1]]) / 16")
    _ej(doc, "Leer un kernel sin ejecutarlo",
        "Los cuatro se entienden mirando **la suma de sus coeficientes**. "
        "**Identidad** suma 1 y sólo copia el píxel central. **Desenfoque "
        "gaussiano** suma 16/16 = 1 y todos sus pesos son positivos: promedia con "
        "los vecinos, así que preserva el brillo y suaviza. **Ridge** suma 0 "
        "(4 − 4): donde la zona es uniforme el resultado es cero —negro—, y sólo "
        "sobrevive lo que cambia, es decir los **bordes**. **Sharpen** suma 1 "
        "(5 − 4): es la identidad más el detector de bordes, o sea la imagen "
        "original con sus bordes reforzados. La regla general: **suma 1 preserva "
        "el brillo, suma 0 detecta cambios**.")
    para(doc, "Y el pooling, también a mano:")
    code(doc,
         "def max_pooling(image, pool_size, paso):\n"
         "    output_height = (image.shape[0] - pool_size) // paso + 1\n"
         "    output_width  = (image.shape[1] - pool_size) // paso + 1\n"
         "    pooled_image = np.zeros((output_height, output_width))\n"
         "    for y in range(0, output_height):\n"
         "        for x in range(0, output_width):\n"
         "            region = image[y*paso : y*paso+pool_size,\n"
         "                           x*paso : x*paso+pool_size]\n"
         "            pooled_image[y, x] = np.max(region)\n"
         "    return pooled_image")
    para(doc, "En el notebook el pooling se aplica sobre un dígito manuscrito de "
              "`load_digits`, que son imágenes de **8×8**, ya convolucionado. Con "
              "`pool_size=2` y `paso=2`, la salida real:")
    salida(doc,
           "Output shape: (4, 4)\n"
           "\n"
           "8  15  15  0\n"
           "2  15  13  0\n"
           "0   1  12  8\n"
           "0  13  14  9")
    para(doc, "Con `pool_size = paso`, las regiones **no se superponen** y cada "
              "dimensión se divide por dos: de 8×8 a 4×4, de 64 valores a 16. Ahí "
              "está la reducción de la que habla "
              "la teoría: cuatro píxeles de entrada producen uno de salida, y lo "
              "que se conserva es el máximo de los cuatro —la respuesta más fuerte "
              "del filtro en esa vecindad—, sin importar en cuál de las cuatro "
              "posiciones estaba.")


# ==================================================  2.12 no supervisado
def kmeans(doc):
    """Seccion nueva al final de la Unidad 2."""
    h(doc, 2, "2.12 Aprendizaje no supervisado: K-means", "u2_12")
    para(doc,
         "Los tres paradigmas de aprendizaje se presentan al comienzo de esta "
         "unidad; el **no supervisado** es el único que no se desarrolla después, "
         "y el notebook *Aprendizaje automático 0X (K-means)* lo cubre. El "
         "programa analítico no lo pide explícitamente —la Unidad 2 nombra "
         "reconocimiento de patrones y aprendizaje supervisado—, pero la "
         "presentación de la cátedra lo da como la aplicación principal del "
         "aprendizaje no supervisado y el apunte lo menciona al hablar de "
         "autoorganización.")
    para(doc,
         "**La idea.** No hay etiquetas ni profesor. El algoritmo busca *k* grupos "
         "en los datos alternando dos pasos hasta que los centros dejan de "
         "moverse: **asignar** cada punto al centro más cercano, y **recalcular** "
         "cada centro como el promedio de los puntos que le tocaron. Es el "
         "**clúster** de [[u2_1|sección 2.1]], ahora encontrado por un algoritmo en "
         "vez de a ojo.")
    para(doc, "**El código de tu Colab.** El paso de asignación, en cuatro líneas:")
    code(doc,
         "def kmeans_paso(X, k):\n"
         "    clusters = [[] for i in range(len(k))]\n"
         "    for i in range(X.shape[0]):\n"
         "        distancias = [distance.euclidean(X[i], x) for x in k]\n"
         "        clusters[np.argmin(distancias)].append(X[i])\n"
         "    return clusters")
    para(doc, "Y el paso de actualización, que es el promedio de cada grupo:")
    code(doc,
         "if len(grupos[0]) > 0:\n"
         "    nc1 = np.average(np.array(grupos[0]), axis=0)\n"
         "if len(grupos[1]) > 0:\n"
         "    nc2 = np.average(np.array(grupos[1]), axis=0)\n"
         "if len(grupos[2]) > 0:\n"
         "    nc3 = np.average(np.array(grupos[2]), axis=0)")
    para(doc, "Los datos son tres nubes gaussianas de 50 puntos cada una, "
              "centradas en (2, 2), (8, 2) y (5, 8), y los centros iniciales salen "
              "de `np.random.uniform(0, 10, size=2)`. Tras la **primera** "
              "asignación:")
    salida(doc, "np.array(grupos[0]).shape\n(58, 2)")
    _ej(doc, "Por qué 58 y no 50",
        "El dato delata cómo funciona el algoritmo. Hay exactamente 50 puntos por "
        "nube, pero el primer grupo se queda con **58**: los centros iniciales son "
        "aleatorios y no tienen por qué caer uno en cada nube, así que la primera "
        "partición del plano no coincide con la estructura real de los datos. Ese "
        "es justamente el trabajo de las iteraciones siguientes. "
        "También explica las dos guardas `if len(grupos[i]) > 0` del código: si un "
        "centro queda tan mal ubicado que **no le toca ningún punto**, "
        "`np.average` de un arreglo vacío da `nan` y el centro se pierde para "
        "siempre. Es el mismo problema de sensibilidad al punto de partida que el "
        "descenso de gradiente, y la razón por la que en la práctica K-means se "
        "corre varias veces con inicializaciones distintas.")
