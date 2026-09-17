# -*- coding: utf-8 -*-
"""Cierra los dos huecos reales de las Unidades 1 y 2 frente al programa.

Fuentes:
  - Russell y Norvig 2004, seccion 2.3.1 "Omnisciencia, aprendizaje y autonomia"
  - Catedra, "4- Reconocimiento de patrones" (laminas de extraccion y PCA)
Cada funcion agrega al final del doc; aplicar12.py se encarga de moverlo.
"""
from docbuild import h, para, bullets, box


def _ej(doc, titulo, texto):
    return box(doc, titulo, texto, fill="FFF8E6", color="C9962A")


# =====================================================================  1.9
def omnisciencia(doc):
    """Va dentro de 1.9, antes del ejemplo de la aspiradora."""
    h(doc, 3, "Racionalidad no es omnisciencia", "u1_9_omn")
    para(doc,
         "Un agente **omnisciente** conoce el resultado real de su acción y actúa "
         "de acuerdo con él. En la realidad la omnisciencia no es posible, y la "
         "definición de racionalidad de arriba tampoco la exige: la elección "
         "racional depende **sólo de la secuencia de percepciones hasta el "
         "momento**, no de lo que efectivamente va a pasar después.")

    _ej(doc, "Ejemplo · cruzar la calle en los Campos Elíseos",
        "Voy caminando y veo a un amigo del otro lado de la calle. No hay tránsito "
        "y no tengo ningún compromiso, así que cruzo. Al mismo tiempo, a 33.000 "
        "pies de altura, se desprende la puerta de un avión, y antes de que "
        "termine de cruzar me encuentro aplastado. **¿Fue irracional cruzar la "
        "calle?** No: sería raro que en la necrológica dijera «un idiota "
        "intentando cruzar la calle». El ejemplo separa dos cosas que se confunden "
        "todo el tiempo — **la racionalidad maximiza el rendimiento esperado; la "
        "perfección maximiza el resultado real**. Exigirle perfección a un agente "
        "sería exigirle una bola de cristal, y eso no es un criterio de diseño.")

    para(doc,
         "Aflojar la exigencia de perfección no es hacerle un favor al agente: es "
         "lo único que vuelve al problema diseñable. Pero cuidado con leerlo al "
         "revés, porque de ahí salen **dos obligaciones** que sí son parte de la "
         "racionalidad:")
    bullets(doc, [
        "**Recopilación de información.** Si el agente cruza sin mirar, su "
        "secuencia de percepciones no le avisa del camión que viene — pero la "
        "secuencia quedó incompleta **por culpa suya**. El agente racional elige "
        "primero la acción «mirar», porque mirar maximiza el rendimiento "
        "esperado. Llevar a cabo acciones cuyo valor es modificar las "
        "percepciones futuras se llama recopilación de información; la "
        "**exploración** que hace la aspiradora en un ambiente desconocido es el "
        "otro caso típico.",
        "**Aprendizaje.** El agente racional no sólo recopila información: "
        "aprende lo máximo posible de lo que percibe. La configuración inicial "
        "puede reflejar un conocimiento preliminar del entorno, pero a medida que "
        "adquiere experiencia ese conocimiento se modifica y se amplía. Sólo en "
        "el caso excepcional de un entorno conocido por completo de antemano el "
        "agente puede limitarse a actuar correctamente sin percibir ni aprender.",
    ])
    para(doc,
         "Junto con la **autonomía** que se define más arriba, éstas son las tres "
         "patas que separan al agente racional del que simplemente tuvo suerte.")


# =====================================================================  2.1
def extraccion_pca(doc):
    """Va al final de 2.1, despues del ejemplo de las monedas."""
    h(doc, 3, "Extracción de características y PCA", "u2_1_pca")
    para(doc,
         "De las tres tareas del reconocimiento automático, la extracción de "
         "características es la que menos se explica sola, así que conviene "
         "detallarla. Busca **reducir la dimensión de los vectores de patrones "
         "sin perder información significativa**. Importa porque muchos sistemas "
         "trabajan con grandes cantidades de datos y no siempre conviene "
         "conservar todas las variables originales.")
    para(doc,
         "La herramienta que nombra la cátedra es **PCA — Análisis de Componentes "
         "Principales**, que reduce la dimensión de los datos conservando la mayor "
         "cantidad posible de información significativa. Si tengo 100 "
         "características de una imagen, es probable que algunas sean "
         "**redundantes**; PCA intenta encontrar **nuevas** variables que resuman "
         "la información más importante. El detalle de que las variables son "
         "*nuevas* es lo que distingue extraer de seleccionar: no se queda con un "
         "subconjunto de las columnas que ya había.")
    _ej(doc, "Ejemplo de la cátedra · el reconocedor de rostros",
        "Un sistema que reconoce rostros donde **cada imagen tiene 10.000 "
        "píxeles**: el vector de patrón tiene 10.000 componentes. ¿Por qué puede "
        "ser útil reducir la dimensión? La cátedra da cuatro razones, y conviene "
        "tenerlas separadas porque son de naturaleza distinta — **disminuir el "
        "costo computacional** (menos cuentas), **eliminar información "
        "redundante** (píxeles vecinos dicen casi lo mismo), **facilitar la "
        "clasificación** (menos dimensiones, fronteras más simples) y **reducir "
        "el ruido** (las componentes descartadas suelen ser las de menor "
        "varianza). Las dos primeras son de eficiencia; las dos últimas mejoran "
        "directamente la calidad del clasificador.")
