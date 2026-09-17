# -*- coding: utf-8 -*-
import json, re, sys, unicodedata
sys.stdout.reconfigure(encoding="utf-8")
S = json.load(open("secciones.json", encoding="utf-8"))

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

TODO = norm(" ".join(s["tit"] + " " + s["txt"] for s in S))

# terminos del temario que hay que confirmar en el texto, no solo en titulos
TERM = ["dartmouth", "invierno de la ia", "mccarthy", "turing", "1956", "perceptron",
        "sensado", "extraccion de caracteristicas", "pila de objetivos",
        "descomposicion", "jerarquic", "htn", "sussman",
        "motor de inferencia", "base de conocimiento", "ingeniero del conocimiento",
        "scikit-learn", "tensorflow", "colab", "gpu", "sesgo algoritmic",
        "costo computacional", "recursos"]
for t in TERM:
    print(f'{TODO.count(norm(t)):4d}  {t}')

print("\n=== secciones donde aparece cada termino critico ===")
for t in ["dartmouth", "pila de objetivos", "sensado", "extraccion de caracteristicas",
          "descomposicion", "motor de inferencia", "tensorflow", "gpu"]:
    hits = [s["tit"] for s in S if norm(t) in norm(s["tit"]+" "+s["txt"])]
    print(f'\n{t}: {hits if hits else "NINGUNA"}')
