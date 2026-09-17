# -*- coding: utf-8 -*-
import re, sys, docx
sys.stdout.reconfigure(encoding="utf-8")
def secs(p):
    d = docx.Document(p); out = []
    for q in d.paragraphs:
        m = re.match(r"Heading (\d)", q.style.name or "")
        if m and q.text.strip(): out.append((int(m.group(1)), q.text.strip()))
    return out, d
A, dA = secs(r"C:\Users\Usuario\Desktop\Resumenes\Ing\IA\Inteligencia Artificial (IAR).docx")
B, dB = secs("trabajo2.docx")
ta, tb = [t for _l, t in A], [t for _l, t in B]
print("secciones: original %d  nuevo %d" % (len(ta), len(tb)))
print("perdidas :", [t for t in ta if t not in tb])
print("nuevas   :", [t for t in tb if t not in ta])
pa = [q.text.strip() for q in dA.paragraphs if q.text.strip()]
pb = [q.text.strip() for q in dB.paragraphs if q.text.strip()]
faltan = [x for x in pa if x not in pb]
print("parrafos del usuario perdidos: %d" % len(faltan))
for x in faltan[:6]: print("   -", x[:90])
# contexto alrededor de lo nuevo
for marca in ("Racionalidad no es omnisciencia", "Extracción de características y PCA"):
    i = tb.index(marca)
    print("\ncontexto de «%s»:" % marca)
    for l, t in B[max(0, i-2):i+3]:
        print("   %sL%d %s" % ("  " * (l - 1), l, t[:62]))
