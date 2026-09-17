# -*- coding: utf-8 -*-
"""Convierte notebooks .ipynb a Markdown conservando codigo Y outputs.
markitdown descarta los outputs; aca son lo mas importante porque son los
resultados reales que obtuvo el alumno."""
import base64
import json
import os
import re
import sys

SRC = r"C:\Users\Usuario\Desktop\Resumenes\Ing\IA\Collabs"
DST = r"C:\Users\Usuario\Desktop\Resumenes\Ing\IA\Collabs EN .MD"
IMG = r"C:\Users\Usuario\AppData\Local\Temp\claude\C--Users-Usuario-Desktop-Resumenes\14217196-23d1-408f-ac59-23e5e5b94d44\scratchpad\nbimg"

ANSI = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")


def txt(x):
    if isinstance(x, list):
        x = "".join(x)
    return ANSI.sub("", x or "")


def convert(path, rel):
    nb = json.load(open(path, encoding="utf-8"))
    stem = os.path.splitext(os.path.basename(path))[0]
    out = ["---", "tags: [ia/tecnologia, colab, material-fuente]", "aliases: []",
           "created: 2026-09-17", "---", "",
           "# " + stem, "",
           "> Notebook original: `Ing/IA/" + rel.replace("\\", "/") + "`. "
           "Conversion automatica: se conserva el codigo tal como fue escrito y "
           "los outputs tal como fueron ejecutados.", ""]
    nimg = 0
    ncode = 0
    for i, c in enumerate(nb["cells"]):
        src = txt(c.get("source"))
        if c["cell_type"] == "markdown":
            # las imagenes embebidas en base64 dentro del markdown ensucian todo
            src = re.sub(r"!\[[^\]]*\]\(data:image/[^)]+\)", "*(imagen embebida)*", src)
            if src.strip():
                out.append(src.rstrip())
                out.append("")
        elif c["cell_type"] == "code":
            if not src.strip():
                continue
            ncode += 1
            out.append("```python")
            out.append(src.rstrip())
            out.append("```")
            out.append("")
            for o in c.get("outputs", []):
                t = o.get("output_type")
                if t == "stream":
                    s = txt(o.get("text")).rstrip()
                    if s:
                        out.append("**Salida:**")
                        out.append("```")
                        out.append(s)
                        out.append("```")
                        out.append("")
                elif t in ("execute_result", "display_data"):
                    d = o.get("data", {})
                    if "image/png" in d:
                        nimg += 1
                        fn = "%s__c%02d_%d.png" % (
                            re.sub(r"[^A-Za-z0-9]+", "_", stem)[:40], i, nimg)
                        try:
                            raw = d["image/png"]
                            if isinstance(raw, list):
                                raw = "".join(raw)
                            open(os.path.join(IMG, fn), "wb").write(
                                base64.b64decode(raw))
                            out.append("**Grafico generado:** `%s`" % fn)
                            out.append("")
                        except Exception as e:
                            out.append("*(grafico no decodificable: %s)*" % e)
                            out.append("")
                    elif "text/plain" in d:
                        s = txt(d["text/plain"]).rstrip()
                        if s:
                            out.append("**Resultado:**")
                            out.append("```")
                            out.append(s)
                            out.append("```")
                            out.append("")
                elif t == "error":
                    s = "\n".join(txt(l) for l in o.get("traceback", []))[:1200]
                    out.append("**Error:**")
                    out.append("```")
                    out.append(s.rstrip())
                    out.append("```")
                    out.append("")
    sub = os.path.dirname(rel).split(os.sep)[1:]   # Clase 2 / Clase 3 / UV
    carpeta = os.path.join(DST, *sub)
    os.makedirs(carpeta, exist_ok=True)
    dest = os.path.join(carpeta, stem + ".md")
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    return dest, ncode, nimg, len("\n".join(out))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    os.makedirs(IMG, exist_ok=True)
    tot = 0
    for root, _, files in os.walk(SRC):
        for f in sorted(files):
            p = os.path.join(root, f)
            try:
                json.load(open(p, encoding="utf-8"))
            except Exception:
                print("  omitido (no es notebook):", f)
                continue
            rel = os.path.relpath(p, os.path.dirname(SRC))
            d, nc, ni, sz = convert(p, rel)
            tot += 1
            print("  %-52s %2d celdas cod, %2d graficos, %6d bytes" % (
                os.path.basename(d), nc, ni, sz))
    print("\nnotebooks convertidos:", tot)
