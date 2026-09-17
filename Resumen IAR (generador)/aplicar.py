# -*- coding: utf-8 -*-
"""Inserta el contenido nuevo en el .docx que edito el usuario.

NO se reconstruye el documento: se abre el que esta en la carpeta y se le
agregan bloques en los puntos que corresponden, respetando todo lo demas
(el usuario saco la portada, la seccion 'Como esta organizado' y el
Apendice A, y recorto las aperturas de unidad; nada de eso se repone).
"""
import os
import sys
from insertar import Doc
import docbuild
import add_u2
import add_u6

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(HERE, "img")
DEST = r"C:\Users\Usuario\Desktop\Resumenes\Ing\IA\Inteligencia Artificial (IAR).docx"

d = Doc(os.path.join(HERE, "trabajo.docx"))


def hacer_fig(doc):
    """Las figuras se numeran con un marcador; renumerar_figuras() les pone el
    numero definitivo segun el orden final del documento."""
    def fig(nombre, epigrafe, width_in=6.30):
        docbuild.figure(doc, os.path.join(IMG, nombre), 0, epigrafe,
                        width_in=width_in)
    return fig


PLAN = [
    # (descripcion, ancla = parrafo ANTES del cual insertar, funcion)
    ("2.10 · motor del aprendizaje",
     "Aprendizaje y topología",
     lambda doc: (add_u2.motor_del_aprendizaje(doc),
                  add_u2.backprop_pytorch(doc),
                  add_u2.consideraciones(doc))),

    ("2.11 · tipos de capa",
     "Funciones de activación",
     add_u2.tipos_de_capas),

    ("2.11 · codigo de convolucion y pooling",
     "Regularización",
     add_u2.convolucion_codigo),

    ("2.12 · K-means (seccion nueva)",
     "Unidad 3 · Razonamiento",
     add_u2.kmeans),

    ("6.1 · etapas de la comunicacion",
     "6.2 Modelos de lenguaje",
     lambda doc: add_u6.etapas_comunicacion(doc, hacer_fig(doc))),

    ("6.2 · codigo bolsa de palabras, tf-idf y n-gramas",
     "6.3 Gramática",
     add_u6.codigo_modelos_lenguaje),

    ("6.3 · lexico y gramatica e0",
     "6.4 Análisis gramatical",
     add_u6.gramatica_e0),

    ("6.4 · el analisis sintactico como busqueda",
     "6.5 Gramáticas aumentadas",
     lambda doc: add_u6.analisis_sintactico(doc, hacer_fig(doc))),

    ("6.5 · interpretacion semantica y desambiguacion",
     "6.6 Aportes del aprendizaje profundo",
     add_u6.semantica),

    ("6.6 · codigo de word embeddings",
     "6.7 Redes recurrentes",
     add_u6.codigo_embeddings),
]

for desc, ancla_txt, escribir in PLAN:
    _i, _l, tit, ancla = d.heading(ancla_txt)
    n = d.insertar_antes(ancla, escribir)
    print(f"  {desc:52s} -> {n:3d} parrafos, antes de «{tit[:34]}»")

nfig = d.renumerar_figuras()
print(f"\nfiguras renumeradas: {nfig}")
d.guardar()
print("guardado:", d.ruta)
