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
for a in ["pca","componentes principales","reduccion de dimension","dimensionalidad",
          "normalizacion","escalado","preprocesamiento","seleccion de caracteristicas"]:
    an = norm(a)
    hits = [t for t, txt in secs if an in txt]
    print("%-30s %3d  %s" % (a, sum(t.count(an) for _x, t in secs), "; ".join(h[:46] for h in hits[:4])))
