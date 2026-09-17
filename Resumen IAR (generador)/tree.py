# -*- coding: utf-8 -*-
import re, sys, docx
sys.stdout.reconfigure(encoding="utf-8")
DOC = r"C:\Users\Usuario\Desktop\Resumenes\Ing\IA\Inteligencia Artificial (IAR).docx"
d = docx.Document(DOC)
rows, cur, buf = [], None, []
for p in d.paragraphs:
    m = re.match(r"Heading (\d)", p.style.name or "")
    if m and p.text.strip():
        if cur: rows.append((cur[0], cur[1], len(" ".join(buf).split())))
        cur, buf = (int(m.group(1)), p.text.strip()), []
    elif p.text.strip(): buf.append(p.text.strip())
if cur: rows.append((cur[0], cur[1], len(" ".join(buf).split())))
on = False
tot = 0
for lvl, t, n in rows:
    if re.match(r"Unidad 1", t): on = True
    if re.match(r"Unidad 3", t): on = False
    if on:
        print("%s%-58s %5d" % ("  " * (lvl - 1), t[:58], n)); tot += n
print("TOTAL U1+U2:", tot)
