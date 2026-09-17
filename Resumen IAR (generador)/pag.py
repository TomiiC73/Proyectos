import sys, fitz
sys.stdout.reconfigure(encoding="utf-8")
doc = fitz.open("trabajo2.pdf")
for q in ["Racionalidad no es omnisciencia", "Campos Elíseos",
          "Extracción de características y PCA", "reconocedor de rostros"]:
    pgs = [p.number + 1 for p in doc if p.search_for(q)]
    print("%-38s %s" % (q, pgs))
