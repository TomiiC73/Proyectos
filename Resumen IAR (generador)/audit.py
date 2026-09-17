# -*- coding: utf-8 -*-
"""Extrae el arbol de secciones del Word con el texto de cada una,
para poder cruzarlo contra el temario item por item."""
import docx, json, re, io, sys
sys.stdout.reconfigure(encoding="utf-8")

D = docx.Document(r"C:\Users\Usuario\Desktop\Resumenes\IA\Resumen Integral - Inteligencia Artificial (IAR).docx")

secs = []       # (nivel, titulo, [parrafos])
cur = None
for p in D.paragraphs:
    st = p.style.name or ""
    t = p.text.strip()
    m = re.match(r"Heading (\d)", st)
    if m and t:
        cur = {"lvl": int(m.group(1)), "tit": t, "txt": []}
        secs.append(cur)
    elif cur is not None and t:
        cur["txt"].append(t)

out = []
for s in secs:
    body = " ".join(s["txt"])
    out.append({"lvl": s["lvl"], "tit": s["tit"],
                "pal": len(body.split()), "txt": body})

json.dump(out, open("secciones.json","w",encoding="utf-8"), ensure_ascii=False)
for s in out:
    print(f'{"  "*(s["lvl"]-1)}{s["tit"]}  [{s["pal"]}]')
