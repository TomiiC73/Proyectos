# -*- coding: utf-8 -*-
import os
from dlib import Diagram

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "img")


def d03_pipeline_ml():
    d = Diagram(6.3, 4.35)
    d.title("Del objeto real a la predicción: el circuito del aprendizaje supervisado",
            y=4.18, fs=10.5)

    xs = [0.72, 1.93, 3.15, 4.37, 5.58]
    txt = ["Sensado\n¿cómo obtengo los datos?",
           "Extracción de características\n¿qué información relevante conservo?",
           "Vector de patrón\nx = (x₁ … xₙ)",
           "Modelo f̂\najuste de los parámetros w",
           "Predicción\nŷ = f̂(x)"]
    kinds = ["accent", "accent", "topic", "unit", "good"]
    for i, (t, k) in enumerate(zip(txt, kinds)):
        d.node(f"p{i}", xs[i], 3.40, t, w=1.12, kind=k, fs=7.4, minh=0.78)
    for i in range(4):
        d.edge(f"p{i}", f"p{i+1}")

    d.band(0.15, 1.62, 6.15, 2.85, "CÓMO SE REPARTEN LOS DATOS")
    d.node("tr", 1.20, 2.16, "Entrenamiento\najusta los parámetros w",
           w=1.75, kind="topic", fs=7.4)
    d.node("va", 3.15, 2.16, "Validación\nelige los hiperparámetros",
           w=1.75, kind="topic", fs=7.4)
    d.node("te", 5.10, 2.16, "Test\nmide el modelo ya elegido",
           w=1.75, kind="topic", fs=7.4)
    d.edge("tr", "va")
    d.edge("va", "te")
    d.caption(3.15, 1.76,
              "Si hay pocos datos: validación cruzada (k-fold) sobre entrenamiento + "
              "validación; el test se reserva y se usa una sola vez, al final.",
              fs=7.0, maxw=5.7)

    d.node("er", 1.55, 1.24,
           "Error reducible\nse achica eligiendo un mejor f̂",
           w=2.6, kind="good", fs=7.6)
    d.node("ei", 4.60, 1.24,
           "Error irreducible Var(ε)\npiso que ningún modelo baja",
           w=2.6, kind="bad", fs=7.6)

    d.caption(3.15, 0.48,
              "Sobreajuste: cuando aumenta la flexibilidad del modelo, el MSE de "
              "entrenamiento baja de forma monótona pero el MSE de test dibuja una «U» y "
              "vuelve a subir. El modelo memorizó patrones del azar que no existen en los "
              "datos nuevos.", fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d03_pipeline_ml.png"))


def d04_modelos():
    d = Diagram(6.3, 5.65)
    d.title("Cómo se traza la frontera entre clases: una sola familia de ideas",
            y=5.48, fs=10.5)

    d.node("root", 3.15, 5.05,
           "Función de decisión d(x): divide el espacio de patrones en regiones, "
           "una por clase",
           w=5.5, kind="root", fs=8.4)

    d.node("a", 1.20, 4.20, "Clasificador lineal\nd(x)=w·x\nmínimos cuadrados",
           w=1.85, kind="unit", fs=7.8)
    d.node("b", 3.15, 4.20, "Perceptrón (1958)\nescalón\nΔw = α(y−y′)xᵢ",
           w=1.85, kind="unit", fs=7.8)
    d.node("c", 5.10, 4.20, "Adaline\nactivación lineal\nregla delta (LMS)",
           w=1.85, kind="unit", fs=7.8)
    d.edge("root", "a")
    d.edge("root", "b")
    d.edge("root", "c")

    d.node("lim", 3.15, 3.35,
           "TODOS COMPARTEN EL MISMO TECHO: una sola unidad sólo separa clases "
           "linealmente separables (el contraejemplo clásico es la compuerta XOR)",
           w=5.5, kind="bad", fs=7.8)
    d.edge("a", "lim")
    d.edge("b", "lim")
    d.edge("c", "lim")

    d.node("s1", 1.20, 2.42,
           "1 · Transformar las entradas\nfunción de decisión generalizada → "
           "clasificador polinomial",
           w=1.85, kind="topic", fs=7.6)
    d.node("s2", 3.15, 2.42,
           "2 · Maximizar el margen\nSVM + funciones kernel (lineal, polinómico, RBF)",
           w=1.85, kind="topic", fs=7.6)
    d.node("s3", 5.10, 2.42,
           "3 · Apilar capas no lineales\nred feed-forward multicapa",
           w=1.85, kind="topic", fs=7.6)
    d.edge("lim", "s1")
    d.edge("lim", "s2")
    d.edge("lim", "s3")

    d.node("bp", 5.10, 1.50,
           "Retropropagación\n(regla delta generalizada): propaga el error hacia atrás "
           "capa por capa", w=1.85, kind="unit", fs=7.6)
    d.node("dl", 5.10, 0.62,
           "Aprendizaje profundo\nReLU · convolución + pooling · dropout, early stop, "
           "aumentación", w=1.85, kind="root", fs=7.6)
    d.edge("s3", "bp")
    d.edge("bp", "dl")

    d.caption(1.20, 1.50,
              "Las tres salidas resuelven el mismo problema por caminos distintos: "
              "cambiar el espacio, cambiar el criterio de ajuste o cambiar la "
              "arquitectura.", fs=7.4, maxw=1.95)
    d.caption(2.05, 0.68,
              "La no linealidad de la función de activación es lo que impide que las "
              "transformaciones lineales sucesivas se resuman en una sola: sin ella, "
              "apilar capas no agrega nada.", fs=7.4, maxw=3.5)
    return d.save(os.path.join(OUT, "d04_modelos.png"))


def d05_metricas():
    d = Diagram(6.3, 4.45)
    d.title("Matriz de confusión: de dónde sale cada métrica", y=4.28, fs=10.5)

    d.caption(1.10, 3.72, "Predicción P", fs=7.4, weight="bold")
    d.caption(2.10, 3.72, "Predicción N", fs=7.4, weight="bold")
    d.caption(0.28, 3.28, "Real P", fs=7.4, weight="bold")
    d.caption(0.28, 2.72, "Real N", fs=7.4, weight="bold")

    d.node("vp", 1.10, 3.28, "VP", w=0.92, kind="good", fs=9.0,
           weight="bold", minh=0.46)
    d.node("fn", 2.10, 3.28, "FN", w=0.92, kind="bad", fs=9.0,
           weight="bold", minh=0.46)
    d.node("fp", 1.10, 2.72, "FP", w=0.92, kind="bad", fs=9.0,
           weight="bold", minh=0.46)
    d.node("vn", 2.10, 2.72, "VN", w=0.92, kind="good", fs=9.0,
           weight="bold", minh=0.46)

    d.caption(1.60, 2.28,
              "Los aciertos caen en la diagonal principal; los errores, fuera de ella.",
              fs=7.2, maxw=2.5)

    # --- boceto de curva ROC, para llenar el hueco de la izquierda ---
    import numpy as np
    ax = d.ax
    x0, y0, ww, hh = 1.00, 0.98, 1.30, 0.90
    d.caption(x0 + ww / 2, y0 + hh + 0.16, "Curva ROC", fs=7.6,
              weight="bold", color="#2C1758")
    ax.plot([x0, x0, x0 + ww], [y0 + hh, y0, y0], color="#5A6076", lw=1.0, zorder=3)
    ax.plot([x0, x0 + ww], [y0, y0 + hh], ls=(0, (3, 3)), color="#B3B9C9",
            lw=0.9, zorder=3)
    t = np.linspace(0, 1, 80)
    ax.plot(x0 + ww * t, y0 + hh * (t ** 0.27), color="#4C2A85", lw=1.7, zorder=4)
    d.caption(x0 + ww * 0.60, y0 + hh * 0.36, "AUC", fs=7.4, color="#4C2A85",
              weight="bold")
    d.caption(x0 + ww / 2, y0 - 0.15, "FPR  (1 − especificidad)", fs=6.6)
    ax.text(x0 - 0.13, y0 + hh / 2, "sensibilidad", rotation=90, ha="center",
            va="center", fontsize=6.6, fontfamily="DejaVu Sans", color="#5A6076")

    mx, mw = 4.55, 3.15
    mets = [
        ("Accuracy = (VP+VN) / total", "proporción de muestras bien clasificadas", "topic"),
        ("Recall / sensibilidad = VP / (VP+FN)", "capacidad de detectar los casos positivos", "good"),
        ("Especificidad = VN / (FP+VN) = 1 − FPR", "proporción de negativos detectados como negativos", "good"),
        ("Precision = VP / (VP+FP)", "de lo que predije positivo, cuánto lo era de verdad", "topic"),
        ("F₁ = 2·precision·recall / (precision+recall)", "media armónica: castiga los valores extremos", "accent"),
    ]
    ys = [3.72, 3.06, 2.40, 1.74, 1.08]
    for i, ((t, sub, k), y) in enumerate(zip(mets, ys)):
        d.node(f"m{i}", mx, y, t + "\n" + sub, w=mw, kind=k, fs=7.4)

    d.caption(3.15, 0.44,
              "Ninguna métrica alcanza sola: un clasificador que responde siempre «P» "
              "tiene recall perfecto y especificidad nula. La curva ROC recorre todos los "
              "umbrales posibles enfrentando sensibilidad contra FPR; el área bajo la "
              "curva (AUC) resume el rendimiento global —cuanto más cerca de 1, mejor—.",
              fs=7.3, maxw=6.0)
    return d.save(os.path.join(OUT, "d05_metricas.png"))


if __name__ == "__main__":
    for f in (d03_pipeline_ml, d04_modelos, d05_metricas):
        print(f())
