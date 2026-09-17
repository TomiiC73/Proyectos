# -*- coding: utf-8 -*-
import re, sys, docx
sys.stdout.reconfigure(encoding="utf-8")
DOC = r"C:\Users\Usuario\Desktop\Resumenes\Ing\IA\Inteligencia Artificial (IAR).docx"
d = docx.Document(DOC)
secs, actual, buf = [], "(preambulo)", []
for p in d.paragraphs:
    if re.match(r"Heading \d", p.style.name or "") and p.text.strip():
        secs.append((actual, buf)); actual, buf = p.text.strip(), []
    elif p.text.strip(): buf.append(p.text.strip())
secs.append((actual, buf))
q = sys.argv[1:]
for t, b in secs:
    if any(t.startswith(x) for x in q):
        print("#### " + t + "   [%d palabras]" % len(" ".join(b).split()))
        print("\n".join(b)[:2600])
        print()
