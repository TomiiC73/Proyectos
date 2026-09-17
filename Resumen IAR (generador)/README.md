# Resumen IAR — generador del apunte

Conjunto de scripts que construyen el resumen completo de **Inteligencia Artificial (IAR)** como documento Word, a partir del material de la cátedra: presentaciones en PDF, notebooks de Google Colab y la bibliografía (Russell y Norvig).

No es un proyecto de cursada: es la herramienta con la que se arma y se mantiene el apunte de estudio de la materia.

## Qué hace

- Genera un `.docx` de ~104 páginas y ~44.600 palabras, con índice automático, marcadores, referencias internas y 49 figuras propias.
- Dibuja todas las figuras por código, con un estilo y una paleta únicos, a escala 1:1 respecto del ancho de inserción en Word.
- Permite **insertar contenido nuevo en un documento ya editado a mano**, sin regenerarlo y sin pisar los cambios del autor.
- Audita el documento contra el programa analítico de la materia para detectar temas faltantes.

## Estructura

### Construcción del documento
| Archivo | Rol |
|---|---|
| `docbuild.py` | Primitivas sobre python-docx: encabezados, párrafos con formato inline, viñetas, cajas de ejemplo, bloques de código con su salida, figuras con epígrafe, índice y marcadores. |
| `build.py` | El documento completo, sección por sección. |
| `apendice.py`, `u2_redes.py`, `_hist_block.py` | Bloques extensos separados del build principal. |

### Diagramas
| Archivo | Rol |
|---|---|
| `dlib.py` | Motor de diagramas sobre matplotlib. Trabaja en **pulgadas 1:1**: el ancho del lienzo es el ancho de inserción en Word, así que nada se reescala ni queda ilegible al imprimir. |
| `gen1.py` … `gen10.py` | Las 49 figuras del documento, agrupadas por unidad. |

### Edición sobre el documento ya editado
python-docx sólo sabe agregar al final. Para insertar en el medio, el contenido se crea al final del documento **destino** (así las imágenes conservan una relación `r:embed` válida) y después se mueven los elementos XML a su lugar.

| Archivo | Rol |
|---|---|
| `insertar.py` | La maquinaria: localizar anclas por encabezado o por párrafo, mover el XML nuevo, renumerar las figuras de abajo. |
| `aplicar.py`, `aplicar12.py` | Los planes de inserción concretos: qué bloque va antes de qué ancla. |
| `add_u2.py`, `add_u6.py`, `add_u12.py` | El contenido nuevo de cada unidad. |

> Lo nuevo se identifica **por posición**, no por `id()` de los elementos: los proxies de lxml se crean bajo demanda y su `id` se reutiliza, de modo que un set de `id()` da falsos positivos.

### Auditoría y verificación
| Archivo | Rol |
|---|---|
| `audit.py`, `tree.py` | Árbol de encabezados con conteo de palabras por sección. |
| `chk.py`, `chk_u12.py` | Búsqueda de "canarios": términos que tendrían que aparecer si un tema estuviera tratado. Detecta temas **ausentes**, cosa que un conteo de palabras no hace. |
| `alt.py`, `alt2.py` | Contraprueba con sinónimos, para descartar los falsos positivos del método anterior. |
| `dump.py` | Vuelca el texto de una sección. |
| `verif.py` | Compara dos versiones del `.docx` y verifica que no se haya perdido ningún párrafo. |
| `pag.py` | Ubica un texto en el PDF exportado, para revisar visualmente esa página. |

### Conversión de material fuente
| Archivo | Rol |
|---|---|
| `nb2md.py` | Convierte los notebooks `.ipynb` a Markdown **conservando las salidas de ejecución**, que `markitdown` descarta. |

## Flujo de verificación

El documento no se da por bueno hasta verlo renderizado:

```
build / aplicar  →  .docx
                 →  Word COM (actualizar índice y campos, repaginar, exportar)
                 →  .pdf
                 →  PyMuPDF rasteriza las páginas afectadas
                 →  inspección visual
```

## Dependencias

```
python-docx    escritura del .docx
matplotlib     diagramas
PyMuPDF        rasterizado del PDF para verificar
markitdown     conversión de los PDF de la cátedra
```

Además, la exportación a PDF y la actualización del índice usan **Word vía COM** desde PowerShell, así que esa parte del flujo sólo corre en Windows con Word instalado.

**Tecnologías:** Python, python-docx, matplotlib, PyMuPDF, lxml, markitdown, Word COM (PowerShell)
