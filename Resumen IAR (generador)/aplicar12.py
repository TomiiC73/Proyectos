# -*- coding: utf-8 -*-
"""Inserta los dos bloques que faltaban en U1 y U2 sobre el docx del usuario.

Se trabaja sobre una COPIA (trabajo2.docx); recien despues de verificar se
pisa el archivo de la carpeta, y antes se deja respaldo en Archive/.
"""
import os
import sys
import shutil
from insertar import Doc
import add_u12

sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DEST = r"C:\Users\Usuario\Desktop\Resumenes\Ing\IA\Inteligencia Artificial (IAR).docx"
COPIA = os.path.join(HERE, "trabajo2.docx")

shutil.copy2(DEST, COPIA)
d = Doc(COPIA)

antes = len(d.doc.paragraphs)

# --- 1.9 · omnisciencia, justo antes del ejemplo de la aspiradora
ancla = d.parrafo("Ejemplo · la aspiradora, el agente determinista")
n1 = d.insertar_antes(ancla, add_u12.omnisciencia)
print("1.9  Racionalidad no es omnisciencia   -> %3d parrafos" % n1)

# --- 2.1 · extraccion y PCA, al final de la seccion
ancla = d.heading("2.2 Aprendizaje supervisado")[3]
n2 = d.insertar_antes(ancla, add_u12.extraccion_pca)
print("2.1  Extraccion de caracteristicas y PCA -> %3d parrafos" % n2)

nfig = d.renumerar_figuras()
print("figuras: %d (sin cambios esperados)" % nfig)
d.guardar()
print("parrafos: %d -> %d" % (antes, len(d.doc.paragraphs)))
print("guardado:", COPIA)
