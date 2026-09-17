# -*- coding: utf-8 -*-
import re, sys, unicodedata, docx
sys.stdout.reconfigure(encoding="utf-8")
DOC = r"C:\Users\Usuario\Desktop\Resumenes\Ing\IA\Inteligencia Artificial (IAR).docx"
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")
d = docx.Document(DOC)
secs, actual, buf = [], "(preambulo)", []
for p in d.paragraphs:
    if re.match(r"Heading \d", p.style.name or "") and p.text.strip():
        secs.append((actual, " ".join(buf))); actual, buf = p.text.strip(), []
    elif p.text.strip(): buf.append(p.text.strip())
secs.append((actual, " ".join(buf)))
secs = [(t, norm(t + " " + c)) for t, c in secs]

ALT = ["prueba de turing","turing","test de turing","imitacion",
       "cibernetica","teoria de control","control",
       "reflejo simple","reactivo simple","reflejo","tabla de percep",
       "omnisciente","omniscien","no es omnisc",
       "vehiculo autonomo","conduccion autonoma","auto autonomo","vehiculos autonomos","waymo","robotica autonoma",
       "vector de caracteristicas","vector de atributos","vector de rasgos",
       "variable objetivo","etiqueta","variable de salida","target",
       "definicion de inteligencia artificial","que es la inteligencia artificial","que se entiende por"]
for a in ALT:
    an = norm(a)
    hits = [t for t, txt in secs if an in txt]
    tot = sum(txt.count(an) for _t, txt in secs)
    print("%-42s %3d  %s" % (a, tot, "; ".join(h[:40] for h in hits[:3])))
