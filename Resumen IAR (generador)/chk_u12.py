# -*- coding: utf-8 -*-
"""Auditoria hoja-por-hoja del programa analitico, Unidades 1 y 2.

Para cada hoja del programa se definen 'canarios': terminos que TIENEN que
aparecer si el tema esta tratado. Se busca sobre el texto normalizado (sin
tildes) para no depender de como quedo escrito cada acento.
Ademas se reporta en que seccion del documento cae cada aparicion, para
distinguir 'el tema esta desarrollado aca' de 'la palabra aparece de paso'.
"""
import re, sys, unicodedata, docx
sys.stdout.reconfigure(encoding="utf-8")

DOC = r"C:\Users\Usuario\Desktop\Resumenes\Ing\IA\Inteligencia Artificial (IAR).docx"

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

d = docx.Document(DOC)

# texto por seccion: cada parrafo se atribuye al ultimo encabezado visto
secs, actual = [], "(preambulo)"
buf = []
for p in d.paragraphs:
    if re.match(r"Heading \d", p.style.name or "") and p.text.strip():
        secs.append((actual, " ".join(buf)))
        actual, buf = p.text.strip(), []
    else:
        if p.text.strip():
            buf.append(p.text.strip())
secs.append((actual, " ".join(buf)))
# el titulo tambien cuenta como texto de la seccion
secs = [(t, norm(t + " " + c), len(c.split())) for t, c in secs]

HOJAS = {
 "U1": [
  ("IA > Definicion, objetivos y alcances", ["definicion de inteligencia artificial", "actuar racionalmente", "objetivo"]),
  ("IA > Fundamentos",                      ["filosofia", "neurociencia", "linguistica", "cibernetica"]),
  ("IA > Historia",                         ["dartmouth", "invierno de la ia", "1956"]),
  ("IA > Enfoques",                         ["pensar como humano", "actuar racionalmente", "test de turing"]),
  ("IA > Tipos de problema del mundo real", ["espacio de soluciones", "metaheuristica", "tipos de problema"]),
  ("IA > Estado del arte",                  ["estado del arte", "alphago", "vehiculo autonomo"]),
  ("Agentes > Comportamiento esperado",     ["medida de rendimiento", "racionalidad", "omnisciencia"]),
  ("Agentes > Ambientes",                   ["totalmente observable", "estocastico", "episodico", "reps"]),
  ("Agentes > Estructura",                  ["agente reactivo simple", "basado en objetivos", "basado en utilidad"]),
 ],
 "U2": [
  ("Rec. de patrones > Sensado",            ["sensado", "sensor", "adquisicion"]),
  ("Rec. de patrones > Extraccion de caracteristicas", ["extraccion de caracteristicas", "vector de caracteristicas"]),
  ("Rec. de patrones > Clasificacion y regresion", ["clasificacion", "regresion", "variable objetivo"]),
  ("Sup. > Regresion lineal, logistica y polinomial", ["regresion lineal", "regresion logistica", "regresion polinomial", "sigmoide"]),
  ("Sup. > Redes neuronales y aprendizaje profundo", ["perceptron", "retropropagacion", "aprendizaje profundo", "convolucion"]),
  ("Sup. > Maquinas de vectores de soporte", ["vectores de soporte", "margen", "kernel"]),
 ],
}

for uni, hojas in HOJAS.items():
    print("=" * 78)
    print(uni)
    print("=" * 78)
    for hoja, canarios in hojas:
        print("\n* " + hoja)
        for c in canarios:
            cn = norm(c)
            hits = [(t, n) for t, txt, n in secs if cn in txt]
            total = sum(txt.count(cn) for _t, txt, _n in secs)
            if not hits:
                print("    [FALTA] %-38s 0" % c)
            else:
                donde = "; ".join("%s" % t[:44] for t, _ in hits[:3])
                extra = "" if len(hits) <= 3 else " (+%d)" % (len(hits) - 3)
                print("    [ok]    %-38s %2d  -> %s%s" % (c, total, donde, extra))
