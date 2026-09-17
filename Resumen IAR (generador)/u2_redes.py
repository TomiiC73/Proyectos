# -*- coding: utf-8 -*-
"""Seccion 2.10 (redes neuronales) en modulo propio: es la que mas crecio al
incorporar los notebooks de la carpeta Collabs, y editarla dentro de build.py
en el lugar era fragil."""


def escribir(doc, h, para, bullets, box, fig, ejemplo, code, salida):
    h(doc, 2, "2.10 Redes neuronales artificiales", "u2_9")
    box(doc, "Cómo hay que pensarlas",
        "Al intentar construir máquinas inteligentes surge de forma natural un modelo: la "
        "mente humana. Pero desde la perspectiva de las aplicaciones prácticas del "
        "reconocimiento de patrones, **el «realismo biológico» impondría restricciones "
        "completamente innecesarias**. Si bien las redes neuronales están inspiradas en el "
        "modelo biológico, hay que pensarlas como **modelos que extraen combinaciones "
        "lineales de las entradas, las convierten en características derivadas y después "
        "modelan la salida como una función no lineal de esas características** — no como "
        "una simulación del cerebro.")
    h(doc, 3, "El perceptrón", "u2_9a")
    para(doc,
         "Ideado por **Frank Rosenblatt en 1958**, es el primer modelo de neurona artificial: "
         "un método de aprendizaje supervisado que realiza clasificación binaria mediante una "
         "transformación lineal, igual que el clasificador lineal. Representa una neurona "
         "biológica donde **las dendritas son las entradas, el axón es la salida y las "
         "sinapsis son los coeficientes de la función de decisión**; el comportamiento se "
         "replica acumulando la intensidad de los impulsos recibidos que, al superar cierto "
         "umbral, «activan» la neurona.")
    para(doc,
         "Dicho en términos operativos: es un **algoritmo de aprendizaje supervisado que "
         "toma varias entradas y produce una única salida**, y su función es resolver "
         "problemas de clasificación **binaria** donde los datos son **linealmente "
         "separables**. El ejemplo típico de la cátedra es decidir si un correo es spam o "
         "no a partir de la frecuencia de ciertas palabras.")
    para(doc,
         "**El objetivo concreto del entrenamiento es encontrar una frontera de decisión "
         "lineal** —una recta en dos dimensiones, un plano en tres, un hiperplano en más— "
         "que separe correctamente las dos clases. Y conviene separar el papel de cada "
         "parámetro, porque se confunden:")
    bullets(doc, [
        "Los **pesos (w)** controlan la **inclinación** de la frontera de decisión.",
        "El **sesgo (b, o w₀)** controla la **posición**: la desplaza sin cambiarle la orientación, para que se ajuste mejor a los datos.",
    ])
    para(doc,
         "Estructuralmente el perceptrón tiene **cuatro partes**: las **neuronas de "
         "entrada** (una por cada característica del conjunto de datos), los **pesos** (uno "
         "por entrada, que son lo que se ajusta durante el entrenamiento), el **sumador** "
         "(que forma la suma ponderada) y la **función de activación** (típicamente el "
         "escalón, que convierte esa suma en una salida binaria 0 o 1).")
    fig("e29_perceptron_arq.png",
        "Arquitectura del perceptrón simple: las cuatro partes y el truco del sesgo "
        "como peso w₀ sobre una entrada fija en 1.")
    bullets(doc, [
        "Se llama **Net** a la suma ponderada de las entradas, Σ wᵢxᵢ. La salida es y′ = f(Net − θ), con f la función escalón (*hard-lim*): 0 si Net − θ < 0, y 1 si Net − θ ≥ 0.",
        "Para simplificar se incluye el umbral dentro de Net agregando un peso **w₀ = −θ** con entrada fija en 1; el vector de entrada se redefine como x = [1, x₁, …, x_N].",
        "**Ley de aprendizaje**: Δwᵢ = α (y − y′) xᵢ, donde y es la salida esperada y α la tasa de aprendizaje.",
        "**Proceso**: inicializar los pesos al azar; mientras el error sea > 0 para algún vector de entradas, ejecutar un ciclo completo (*epoch*) tomando cada par entrada/salida, calcular y′, calcular el error y = y − y′, calcular Δwᵢ y modificar los pesos. Tal como está declarado, **el entrenamiento termina sólo cuando todos los vectores están bien clasificados**, salvo que se defina un máximo de ciclos.",
    ])
    box(doc, "Por qué el sesgo se escribe como una entrada más",
        "El sesgo **no se calcula aparte: se aprende durante el entrenamiento igual que "
        "los pesos**. Es un peso más que el modelo tiene que ajustar, un parámetro libre "
        "que la red optimiza para minimizar el error.\n"
        "La técnica habitual para simplificar los cálculos es tratarlo como el peso de "
        "una neurona de entrada **que siempre vale 1**. Por eso a cada vector de entrada "
        "se le agrega una componente x₀ = 1, y el peso asociado w₀ funciona exactamente "
        "como el sesgo. Para la compuerta AND, los cuatro vectores [0,0], [0,1], [1,0] y "
        "[1,1] se convierten en los **vectores aumentados** [0,0,1], [0,1,1], [1,0,1] y "
        "[1,1,1].")
    ejemplo("Ejemplo · el perceptrón aprendiendo la compuerta OR",
            "Cuatro ejemplos de entrenamiento —(0,0)→0, (0,1)→1, (1,0)→1, (1,1)→1—, pesos "
            "iniciales todos en cero y α = 0,5.\n"
            "**Primera fila**: (0,0) da Net = 0, y como el escalón devuelve 1 cuando "
            "Net ≥ 0, predice 1 cuando debía predecir 0. Error −1, así que w₀ baja a −0,5. "
            "**Segunda**: (0,1) da Net = −0,5 y predice 0 cuando debía predecir 1; error "
            "+1, y los pesos quedan en (0 ; 0 ; 0,5). **Tercera y cuarta**: las dos "
            "aciertan, no se toca nada.\n"
            "Al terminar la primera época **todavía quedan errores**, así que el recorrido "
            "se repite. Recién en la **cuarta época** el perceptrón pasa las cuatro filas "
            "sin equivocarse, con w = (−0,5 ; 0,5 ; 0,5) — o sea la recta "
            "0,5x₁ + 0,5x₂ − 0,5 = 0.\n"
            "Con XOR el mismo procedimiento **no termina nunca**: como no existe recta que "
            "lo separe, siempre queda alguna fila mal y los pesos siguen corrigiéndose "
            "indefinidamente.")
    fig("e07_perceptron.png",
        "Traza de entrenamiento del perceptrón sobre la compuerta OR.")

    para(doc,
         "**En la práctica.** El notebook __Perceptrón Monocapa Simple__ (Clase 3) "
         "resuelve el mismo problema para la compuerta **AND** de tres maneras: a mano, "
         "con scikit-learn y con Keras. Con scikit-learn alcanzan cuatro líneas:")
    code(doc, '''from sklearn.linear_model import Perceptron

# Datos de entrenamiento para la función AND
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([0, 0, 0, 1])

clf = Perceptron(max_iter=1000, tol=1e-3, random_state=42)
clf.fit(X, y)

print("Predicciones para la compuerta AND:", clf.predict(X))
print("Precisión:", clf.score(X, y))
print(clf.coef_)
print(clf.intercept_)''')
    salida(doc, '''Predicciones para la compuerta AND: [0 0 0 1]
Precisión: 1.0
[[2. 2.]]
[-3.]''')
    para(doc,
         "Los pesos aprendidos son w₁ = 2, w₂ = 2 y el sesgo −3, o sea la recta "
         "**2x₁ + 2x₂ − 3 = 0**. Se puede verificar a mano que clasifica bien las cuatro "
         "filas: sólo (1,1) llega a 2 + 2 − 3 = 1 ≥ 0, y las otras tres dan negativo.")
    para(doc,
         "Lo más instructivo del notebook es **abrir el entrenamiento época por época** "
         "con `partial_fit`, que ejecuta un solo paso por llamada, para ver cómo se mueven "
         "los pesos y cuándo deja de haber error:")
    code(doc, '''perceptron = Perceptron(max_iter=1, tol=None, eta0=0.1, random_state=0)
pesos, errores = [], []

# Entrenar el perceptrón y guardar los pesos y el error en cada iteración
for _ in range(10):
    perceptron.partial_fit(X, y, classes=np.unique(y))
    pesos.append(perceptron.coef_.copy())

    # Calcular el número de errores (predicciones incorrectas)
    y_pred = perceptron.predict(X)
    error = np.sum(y != y_pred)
    errores.append(error)

    print(f'Pesos en la iteración {_+1}: {perceptron.coef_}, Error: {error}')''')
    salida(doc, '''Pesos en la iteración 1: [[0. 0.]], Error: 1
Pesos en la iteración 2: [[0. 0.]], Error: 1
Pesos en la iteración 3: [[0.1 0. ]], Error: 1
Pesos en la iteración 4: [[0.1 0. ]], Error: 1
Pesos en la iteración 5: [[0.2 0.1]], Error: 0
Pesos en la iteración 6: [[0.2 0.1]], Error: 0
Pesos en la iteración 7: [[0.2 0.1]], Error: 0''')
    para(doc,
         "Se ve el comportamiento que describe la teoría: **los pesos sólo cambian en las "
         "épocas en que hubo error**, y desde la quinta —cuando el error llega a cero— "
         "quedan congelados en (0,2 ; 0,1). Ésa es exactamente la condición de corte del "
         "algoritmo. Notar además que la solución **no es única**: acá converge a "
         "(0,2 ; 0,1) con sesgo −0,2 y antes había convergido a (2 ; 2) con sesgo −3; "
         "ambas rectas separan igual de bien, y cuál sale depende de la tasa de "
         "aprendizaje y del orden de los ejemplos.")

    ejemplo("Ejemplo · cuando el problema está bien pero el entrenamiento sale mal",
            "El notebook __Ejemplo con Perceptrón Monocapa__ aplica el mismo modelo a un "
            "problema realista: predecir si un cliente va a abandonar el servicio a "
            "partir de **cuántas quejas hizo** y **qué porcentaje del servicio usa**. Son "
            "ocho clientes etiquetados a mano. El resultado es **62,5 % de precisión**: "
            "de ocho clientes, acierta cinco.\n"
            "La lectura fácil sería «no es linealmente separable, como XOR». **Y es "
            "falsa.** Mirando los datos, los cuatro clientes que abandonan tienen 2, 3, 2 "
            "y 4 quejas, y los cuatro que se quedan tienen 0, 1, 0 y 1: la recta "
            "**quejas = 1,5** los separa perfectamente, ignorando la otra variable. El "
            "problema es separable y el teorema de convergencia garantiza que el "
            "perceptrón clásico lo resuelve — de hecho converge en la **época 42**.\n"
            "Lo que falla es el entrenamiento, y el motivo está en los pesos que quedan, "
            "w = (62 ; −20) con sesgo 16. Al calcular Net para cada cliente da "
            "−1984, −460, −1522, −198, −1784, −860, −1322 y 64: **siete de los ocho dan "
            "negativo**, así que el modelo contesta «no abandona» casi siempre y acierta "
            "sólo por los cuatro que efectivamente no abandonan, más el único positivo.\n"
            "La causa es la **diferencia de escalas**: el porcentaje de uso va de 10 a "
            "100 y las quejas de 0 a 4, así que el término del uso pesa unas veinticinco "
            "veces más y aplasta a la variable que de verdad decide. Normalizando ambas "
            "variables, el mismo algoritmo converge en la **época 2** en vez de la 42.\n"
            "Moraleja: un mal resultado no siempre acusa al modelo. Acá acusa a la "
            "**preparación de los datos** — y es el argumento concreto a favor de "
            "normalizar antes de entrenar (ver [[u2_2|sección 2.2]]).")
    code(doc, '''# Características: [Número de quejas, Porcentaje de uso]
X = np.array([[0, 100], [2, 30], [1, 80], [3, 20],
              [0,  90], [2, 50], [1, 70], [4, 10]])

# Etiquetas: 0 = No Abandono, 1 = Abandono
y = np.array([0, 1, 0, 1, 0, 1, 0, 1])

model = Perceptron(max_iter=1000, tol=1e-3, random_state=0)
model.fit(X, y)

print(f"Puntaje de precisión del modelo: {model.score(X, y) * 100}%")
print(f"Pesos (w1, w2): {model.coef_[0]}")
print(f"Sesgo (w0): {model.intercept_[0]}")''')
    salida(doc, '''El entrenamiento ha finalizado.
Puntaje de precisión del modelo: 62.5%
Pesos (w1, w2): [ 62. -20.]
Sesgo (w0): 16.0''')

    para(doc, "**Dónde se usa y dónde no.** Resumiendo lo anterior:")
    bullets(doc, [
        "**Sirve para** clasificación binaria sobre problemas **linealmente separables**, y como pieza básica: los perceptrones multicapa que resuelven problemas no lineales se construyen sobre esta misma idea.",
        "**No sirve para** problemas que no sean linealmente separables: XOR es el caso canónico. Tampoco puede aprender relaciones no lineales complejas entre las características de entrada y la salida: su capacidad está limitada por su estructura.",
        "**Y conviene no confundir las dos cosas**: que el entrenamiento dé mal no prueba que el problema sea no separable. El ejemplo de arriba es separable y aun así el modelo entrenado acierta el 62,5 %. Antes de concluir que hace falta una red multicapa, hay que descartar que el problema sean las escalas, la tasa de aprendizaje o el criterio de parada.",
    ])

    h(doc, 3, "El problema XOR y por qué importa", "u2_9b")
    para(doc,
         "El perceptrón tiene **la misma desventaja que el clasificador lineal**. El ejemplo "
         "clásico es la compuerta **XOR**: resulta obvio que una línea recta no puede separar "
         "los puntos (0,0) y (1,1) de los puntos (0,1) y (1,0).")
    para(doc,
         "El análisis de XOR es interesante porque **deja ver la solución**. Una XOR se puede "
         "construir con otras compuertas. Si tres perceptrones P1, P2 y P3 se entrenan por "
         "separado para funcionar como cada compuerta del circuito y después se conectan, se "
         "puede predecir el comportamiento de la XOR: P1 y P2 implementan AND con una entrada "
         "negada (fáciles, porque para cada compuerta sólo una combinación pertenece a la "
         "clase «1») y P3 implementa un OR. P3 no podría predecir la salida de XOR a partir "
         "de x₁ y x₂, **pero sí lo puede hacer en el nuevo espacio c₁–c₂ formado por las "
         "salidas intermedias**. La función de activación escalón introduce una no linealidad "
         "que evita que las transformaciones lineales sucesivas se conviertan en una sola.")
    box(doc, "El desafío real que esto plantea",
        "La conclusión anterior es cierta, pero **no implica que una red de perceptrones "
        "resuelva estos problemas en casos reales, porque no es posible entrenarla**. Si se "
        "cuenta con conocimiento del dominio, sencillamente no tiene sentido usar una red "
        "neuronal. Si no se cuenta con él, tampoco se conoce la salida esperada para P1 y "
        "P2, así que no se pueden ajustar sus pesos. **El desafío es encontrar un método que "
        "permita ajustar los parámetros a pesar de no conocer los valores esperados de las "
        "salidas intermedias** — y ese método es la retropropagación.\n"
        "Nota terminológica: «perceptrón multicapa» es un nombre inapropiado, porque el "
        "modelo está compuesto por múltiples capas de **regresión logística** (no "
        "linealidades continuas) y no de perceptrones (no linealidades discontinuas).")
    ejemplo("Ejemplo · por qué XOR necesita dos rectas y no una",
            "Los cuatro puntos de XOR: (0,0)→0, (0,1)→1, (1,0)→1, (1,1)→0. Los que valen 1 "
            "están en dos esquinas **opuestas**, así que ninguna recta los deja de un lado "
            "y a los otros dos del otro. Con **dos** rectas sí alcanza: una que separe "
            "«al menos uno» (OR) y otra que separe «los dos» (AND); la respuesta es la "
            "franja que queda entre ambas.\n"
            "Eso es literalmente lo que hace la red: la neurona oculta h₁ aprende el OR, la "
            "h₂ aprende el AND, y la de salida calcula «h₁ y no h₂». Cada neurona sigue "
            "trazando **una** recta; lo que resuelve el problema es combinarlas.\n"
            "Y acá se ve por qué la activación tiene que ser no lineal: si h₁ y h₂ fueran "
            "lineales, la salida sería una combinación lineal de combinaciones lineales — "
            "otra recta — y volveríamos al punto de partida.")
    fig("e08_red_xor.png",
        "XOR resuelto con una capa oculta: dos fronteras en lugar de una.")

    para(doc,
         "**En la práctica.** El notebook __Perceptrón Multicapa – XOR__ implementa la red "
         "2-2-1 **sin librerías**, con la retropropagación escrita a mano. Es el mejor "
         "lugar del material para ver el algoritmo completo en veinte líneas, porque no "
         "hay nada oculto detrás de un `.fit()`:")
    code(doc, '''# Función de activación Sigmoide y su derivada
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def sigmoid_derivative(x):
    return x * (1 - x)

X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y = np.array([[0], [1], [1], [0]])

np.random.seed(42)
pesos_entrada_oculta = 2 * np.random.random((2, 2)) - 1
pesos_oculta_salida  = 2 * np.random.random((2, 1)) - 1

n_epocas = 1000
for epoca in range(n_epocas):
    # Propagación hacia adelante
    capa_entrada = X
    salida_capa_oculta = sigmoid(np.dot(capa_entrada, pesos_entrada_oculta))
    salida             = sigmoid(np.dot(salida_capa_oculta, pesos_oculta_salida))

    # Cálculo del error
    error_salida = y - salida

    # Retropropagación
    delta_salida = error_salida * sigmoid_derivative(salida)
    error_oculta = delta_salida.dot(pesos_oculta_salida.T)
    delta_oculta = error_oculta * sigmoid_derivative(salida_capa_oculta)

    # Actualización de pesos
    pesos_oculta_salida += salida_capa_oculta.T.dot(delta_salida)
    pesos_entrada_oculta += capa_entrada.T.dot(delta_oculta)''')
    salida(doc, '''Error en la época 0: 0.5005462290941706
Salida después del entrenamiento:
Entrada: [0 0] - Salida esperada: [0] - Salida de la red: [0.27016397]
Entrada: [0 1] - Salida esperada: [1] - Salida de la red: [0.68237822]
Entrada: [1 0] - Salida esperada: [1] - Salida de la red: [0.68249765]
Entrada: [1 1] - Salida esperada: [0] - Salida de la red: [0.40947681]''')
    para(doc,
         "Se ven las dos fases que describe la teoría: primero la propagación hacia "
         "adelante hasta `salida`, después el cálculo de `delta_salida` y su propagación "
         "hacia atrás para obtener `delta_oculta` — **el error de la capa oculta se "
         "obtiene del error de la capa siguiente ponderado por los pesos que las "
         "conectan**, que es exactamente `delta_salida.dot(pesos_oculta_salida.T)`.")
    box(doc, "Este entrenamiento quedó a mitad de camino, y vale la pena entender por qué",
        "Las salidas deberían acercarse a 0, 1, 1, 0 y quedaron en **0,27 / 0,68 / 0,68 / "
        "0,41**. La red aprendió la tendencia correcta —las dos del medio son las más "
        "altas— pero no llegó a separar las clases con claridad.\n"
        "El motivo **no** es que la arquitectura esté mal: dos neuronas ocultas alcanzan "
        "para XOR. Son dos detalles de implementación. Primero, **no hay término de "
        "sesgo**: las capas calculan `np.dot(entrada, pesos)` sin sumar nada, y sin sesgo "
        "la entrada (0,0) produce siempre `sigmoid(0) = 0,5` en la capa oculta, sin "
        "importar cuánto se ajusten los pesos. Segundo, **mil épocas son pocas** para "
        "esta configuración.\n"
        "Reejecutando el mismo código con las dos variantes se ve el efecto de cada una: "
        "**agregando el sesgo**, con las mismas mil épocas la red llega a 0,10 / 0,89 / "
        "0,89 / 0,09; **dejándolo como está pero entrenando veinte mil épocas**, llega a "
        "0,02 / 0,95 / 0,95 / 0,06. O sea que el sesgo no es imprescindible acá, pero "
        "acelera la convergencia en un orden de magnitud. Es una buena ilustración de la "
        "advertencia sobre hiperparámetros: **no hay recetas generales**, y un resultado "
        "mediocre puede venir de un detalle del código y no del modelo.")

    h(doc, 3, "Adaline", "u2_9c")
    para(doc,
         "**ADAptative LINear Element** tiene dos diferencias con el perceptrón:")
    bullets(doc, [
        "**Función de activación lineal**: la salida es directamente y′ = Net, lo que le permite hacer regresión (imposible para el perceptrón). Para clasificar hace falta una función escalón en algún momento; hay dos criterios en la bibliografía y **la cátedra de IAR usa el primero**: la activación de Adaline es lineal y, *fuera del modelo*, se aplica una función umbral para determinar la clase.",
        "**Ley de aprendizaje: la regla delta**, basada en el mínimo error cuadrático medio (LMS). Los pesos se ajustan mediante una búsqueda guiada por el **gradiente descendente** de la función del error: Δwᵢ = −α ∂E/∂wᵢ. Aplicando la regla de la cadena se llega a Δwᵢ = α (y_k − O_k) xᵢ — **la misma expresión que la del perceptrón**, salvo que en Adaline el error puede tomar cualquier valor real.",
    ])
    para(doc,
         "Como el error nunca es cero, hace falta otra condición de corte: típicamente se "
         "corta al llegar a un umbral de error definido de antemano. Adaline **sólo clasifica "
         "problemas linealmente separables**, y conectar Adalines en capas no tiene sentido: "
         "como no hay no linealidades, las transformaciones lineales sucesivas se resumen en "
         "una sola.")
    para(doc,
         "**En la práctica.** El notebook __Perceptrón y Adaline – Ejemplo 2__ usa Adaline "
         "para algo que el perceptrón no puede hacer: **una regresión**. El problema es "
         "aprender la conversión de grados Fahrenheit a Celsius a partir de quince pares "
         "de valores, sin decirle la fórmula. La solución exacta es "
         "C = (5/9)·F − 160/9, o sea **w = 0,5556 y b = −17,7778**; el interés está en si "
         "la regla delta llega sola hasta ahí.")
    code(doc, '''# 1. Definir los datos de entrenamiento (Fahrenheit a Celsius)
datos_entrenamiento = [(68, 20), (86, 30), (104, 40), (32, 0), (50, 10),
                       (212, 100), (0, -17.778), (10, -12.222), (75, 23.889),
                       (120, 48.889), (40, 4.444), (95, 35), (150, 65.556),
                       (200, 93.333), (-4, -20)]

# 2. Parámetros iniciales
w, b = 0.5, -15.0
alpha = 0.0001
epocas = 100
historial_mse = []

# 3. Entrenamiento por épocas
for epoca in range(epocas):
    error_cuadratico_total = 0

    for x, y in datos_entrenamiento:
        # Predicción y error lineal
        y_pred = w * x + b
        error = y - y_pred
        error_cuadratico_total += error**2

        # Actualización de pesos (Regla Delta)
        w += (alpha * error * x)
        b += (alpha * error)

    mse = error_cuadratico_total / len(datos_entrenamiento)
    historial_mse.append(mse)''')
    salida(doc, '''Resultados tras 100 épocas:
Peso final (w): 0.5142 (El valor ideal es ~0.5555)
Bias final (b): -15.1689 (El valor ideal es ~-17.7777)''')
    para(doc,
         "Después de cien épocas el peso está muy cerca del valor exacto (0,5142 contra "
         "0,5556) pero **el sesgo se quedó a mitad de camino** (−15,17 contra −17,78). Es "
         "un comportamiento característico de la regla delta sobre datos sin centrar: "
         "como las entradas van de −4 a 212, el término α·error·x mueve mucho más a w que "
         "a b, y el sesgo converge mucho más lento. La cátedra insiste en el punto: **el "
         "error nunca llega a cero**, así que hace falta un criterio de corte definido de "
         "antemano.")
    ejemplo("Ejemplo · qué pasa si la tasa de aprendizaje es demasiado alta",
            "El mismo notebook corre antes ese entrenamiento con **α = 0,001** en vez de "
            "0,0001 —diez veces más grande— y registra la tabla iteración por iteración. "
            "El resultado no es «converge peor»: **es que explota**.\n"
            "Los pesos van 0,568 → 0,237 → 3,394 → 0,398 → … y para la iteración 13 ya "
            "valen 28.966, en la 14 valen −1.129.697 y en la 15 el error cuadrático llega "
            "a 2×10¹³. Y eso ocurre **dentro de la primera pasada por los quince datos**, "
            "sin haber completado una sola época.\n"
            "El mecanismo es fácil de ver: si el paso α·error·x es tan grande que pasa "
            "de largo el mínimo, el error del paso siguiente es mayor, y como el paso es "
            "proporcional al error, el siguiente salto es todavía más grande. Se "
            "realimenta. Es el motivo por el cual la tasa de aprendizaje es el "
            "hiperparámetro que más conviene mirar primero cuando un entrenamiento no "
            "anda: **α demasiado chico hace que tarde, α demasiado grande hace que no "
            "converja nunca**.")
    para(doc,
         "El notebook cierra comparando ambos modelos sobre el mismo problema de "
         "clasificación —detectar motores con falla a partir de vibración y "
         "temperatura— y la diferencia entre las dos curvas de error resume la distinción "
         "teórica: la del perceptrón es **escalonada y llega a cero** (cuenta errores de "
         "clasificación, que son un número entero), mientras que la de Adaline es "
         "**suave y se estabiliza por encima de cero** (mide el error cuadrático medio, "
         "que es continuo). Son dos definiciones distintas de «error», no dos versiones "
         "del mismo gráfico.")
    h(doc, 3, "Redes con conexiones hacia adelante y retropropagación", "u2_9d")
    para(doc, "Una red **feed-forward** dispone las neuronas en capas y cumple:")
    bullets(doc, [
        "Todas las neuronas de una capa conectan su salida a una entrada de **cada una** de las neuronas de la capa siguiente (se dice que están **densamente conectadas**).",
        "No hay conexiones hacia neuronas de capas anteriores.",
        "No hay conexiones con neuronas de la misma capa.",
    ])
    para(doc,
         "Los nodos xᵢ de la capa de entrada no ejecutan ningún cálculo ni tienen parámetros: "
         "sus salidas son directamente los valores del vector de entradas. Los nodos hᵢ "
         "forman las capas ocultas y los nodos Oᵢ la capa de salida. **En clasificación, la "
         "cantidad de neuronas de salida es la cantidad de clases**; en regresión, la capa de "
         "salida suele tener una sola neurona con activación lineal.")
    para(doc,
         "Todas las neuronas de una capa comparten función de activación, que debe ser "
         "**continua, derivable y no decreciente**. La más utilizada —al menos hasta el "
         "aprendizaje profundo— es la **sigmoidal** f(z) = 1/(1+e^−z), con derivada "
         "f(z)(1−f(z)). Junto con la tangente hiperbólica se usa mucho por tener forma de "
         "**escalón suavizado**: la tanh varía entre −1 y 1, la sigmoidal entre 0 y 1.")
    para(doc,
         "El ajuste se hace con la **regla delta generalizada o retropropagación "
         "(*backpropagation*)**. Cada ciclo tiene dos fases:")
    bullets(doc, [
        "**Hacia adelante**: se toma un vector de entrada y se lo propaga a través de todas las capas hasta calcular la salida.",
        "**Hacia atrás**: se calcula el error de la capa de salida y se lo propaga hacia atrás, **calculando el error de las neuronas de las capas ocultas en base al error cometido por las neuronas de la capa siguiente ponderado por los pesos que las conectan**. Recién entonces se modifican los pesos.",
    ])
    para(doc,
         "Con activación sigmoidal, el error de la capa de salida es "
         "δ₂ⱼ = Oⱼ(1 − Oⱼ)(yⱼ − Oⱼ) y el de la capa oculta "
         "δ₁ⱼ = hⱼ(1 − hⱼ) · Σ δ₂ᵢ w₂ⱼᵢ; los ajustes son Δw = −α δ · entrada.")
    box(doc, "No hay recetas generales",
        "Las decisiones de diseño de las redes —cantidad de capas ocultas, cantidad de "
        "neuronas por capa, funciones de activación, distribución de los valores aleatorios "
        "de inicialización, tasa de aprendizaje— **no tienen recomendaciones generales que "
        "funcionen en todos los casos**. Existen enfoques de diseño basados en búsquedas en "
        "el espacio de los hiperparámetros: algunos comienzan con modelos simples que crecen "
        "en complejidad hasta lograr resultados aceptables, y otros siguen el orden inverso. "
        "Esa búsqueda es, literalmente, un problema de los de la [[u3|Unidad 3]].")
    h(doc, 3, "Aprendizaje y topología (presentación de la cátedra)", "u2_9e")
    bullets(doc, [
        "**Ventajas de las RNA**: aprendizaje adaptativo (la red modifica sus pesos a partir de la experiencia), autoorganización, **tolerancia a fallos** (puede seguir funcionando aunque parte de la información sea incompleta o ruidosa) y operación en tiempo real una vez entrenada.",
        "**Topologías**: redes monocapa (entrada → salida), multicapa (entrada → capa oculta → salida) y conexiones *feedforward* y *feedback*.",
        "**Criterios de parada**: estabilidad (los pesos ya casi no cambian), ciclos (se alcanzó el máximo de iteraciones) o error mínimo (el error bajó hasta un valor aceptable).",
        "**Mecanismos supervisados**: corrección de error (perceptrón, Adaline, backpropagation); **por refuerzo** (no recibe la respuesta correcta exacta sino una señal de recompensa o penalización); **estocástico** (los pesos se actualizan con un solo ejemplo por vez — en SGD la red procesa un ejemplo, calcula el error y actualiza inmediatamente).",
        "**Mecanismos no supervisados**: autoorganización (la red aprende a organizar los datos por sí misma, quedando más próximos los datos parecidos), **clusterización**, codificación (representación interna más compacta) y mapeo de características.",
        "**Según la asociación**: **heteroasociativas** (relacionan un patrón de entrada con un patrón de salida diferente) y **autoasociativas** (permiten recuperar la entrada aunque esté incompleta o alterada).",
    ])
