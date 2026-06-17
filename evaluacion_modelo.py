"""
=============================================================================
         Sistema de Análisis y Clasificación Automática de Expedientes
         Pensionales
=============================================================================
Archivo : evaluacion_modelo.py
Autores : Juan Pablo Guevara Rendón
          Nancy Johanna Calderón Manjarrez
Programa: Máster Universitario en Análisis y Visualización de Datos Masivos
          / Visual Analytics and Big Data - UNIR
Fecha   : 2026
-----------------------------------------------------------------------------
Descripción:
    Evalúa el desempeño del modelo de clasificación progresiva de expedientes
    pensionales utilizando el dataset generado por generador_dataset.py.

    Calcula y presenta:
      - Accuracy global del modelo
      - Precision, Recall y F1-Score (por clase y promedio macro)
      - Matriz de confusión completa
      - Reporte detallado por categoría de clasificación

    Entrada : dataset_pensional_sintetico.csv
              (generado previamente por generador_dataset.py)
    Salida  : Resultados impresos en consola + reporte_evaluacion_modelo.txt
=============================================================================
"""

import pandas as pd
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# ---------------------------------------------------------------------------
# Parámetros configurables
# ---------------------------------------------------------------------------
ARCHIVO_DATASET = "dataset_pensional_sintetico.csv"
ARCHIVO_REPORTE = "reporte_evaluacion_modelo.txt"
LABELS          = ["Automatico", "Mixto", "Manual"]


# ---------------------------------------------------------------------------
# Funciones de evaluación y presentación
# ---------------------------------------------------------------------------
def cargar_dataset(ruta: str) -> pd.DataFrame:
    """
    Carga el dataset sintético desde el archivo CSV.

    Parámetros
    ----------
    ruta : str
        Ruta al archivo CSV generado por generador_dataset.py.

    Retorna
    -------
    pd.DataFrame
        Dataset con columnas ClasificacionModelo y ClasificacionEsperada.
    """
    try:
        df = pd.read_csv(ruta, encoding="utf-8-sig")
        columnas_requeridas = {"ClasificacionModelo", "ClasificacionEsperada",
                               "ResultadoValidacion"}
        if not columnas_requeridas.issubset(df.columns):
            raise ValueError(
                f"El dataset no contiene las columnas requeridas: "
                f"{columnas_requeridas}"
            )
        return df
    except FileNotFoundError:
        raise FileNotFoundError(
            f"No se encontró el archivo '{ruta}'.\n"
            f"Ejecute primero generador_dataset.py para crear el dataset."
        )


def formatear_matriz_confusion(cm: np.ndarray, labels: list) -> str:
    """
    Formatea la matriz de confusión como tabla de texto.

    Parámetros
    ----------
    cm     : np.ndarray  Matriz de confusión (n_clases x n_clases).
    labels : list        Etiquetas de las clases.

    Retorna
    -------
    str
        Representación textual de la matriz de confusión.
    """
    ancho_col  = 16
    ancho_fila = 18

    # Encabezado
    lineas = []
    lineas.append("\n  Filas = ClasificacionEsperada (real)")
    lineas.append("  Columnas = ClasificacionModelo (predicha)\n")

    encabezado = " " * ancho_fila
    for label in labels:
        encabezado += label.center(ancho_col)
    lineas.append(encabezado)
    lineas.append("-" * (ancho_fila + ancho_col * len(labels)))

    # Filas de datos
    for i, label_fila in enumerate(labels):
        fila = label_fila.ljust(ancho_fila)
        for j in range(len(labels)):
            valor = str(cm[i][j])
            # Resaltar diagonal (predicciones correctas)
            if i == j:
                fila += f"[{valor}]".center(ancho_col)
            else:
                fila += valor.center(ancho_col)
        lineas.append(fila)

    lineas.append("-" * (ancho_fila + ancho_col * len(labels)))
    lineas.append("  Nota: [valor] indica predicciones correctas (diagonal principal)\n")

    return "\n".join(lineas)


def calcular_metricas_por_clase(y_true: pd.Series,
                                 y_pred: pd.Series,
                                 labels: list) -> pd.DataFrame:
    """
    Calcula métricas de desempeño por categoría de clasificación.

    Retorna
    -------
    pd.DataFrame
        Tabla con Precision, Recall, F1-Score y Soporte por clase.
    """
    filas = []
    for label in labels:
        tp = ((y_true == label) & (y_pred == label)).sum()
        fp = ((y_true != label) & (y_pred == label)).sum()
        fn = ((y_true == label) & (y_pred != label)).sum()

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall    = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1        = (2 * precision * recall / (precision + recall)
                     if (precision + recall) > 0 else 0.0)
        soporte   = (y_true == label).sum()

        filas.append({
            "Clase"    : label,
            "Precision": round(precision, 4),
            "Recall"   : round(recall, 4),
            "F1-Score" : round(f1, 4),
            "Soporte"  : soporte
        })

    return pd.DataFrame(filas)


def generar_reporte(df: pd.DataFrame, labels: list) -> str:
    """
    Genera el reporte completo de evaluación del modelo.

    Parámetros
    ----------
    df     : pd.DataFrame  Dataset con columnas de clasificación.
    labels : list          Etiquetas de las clases.

    Retorna
    -------
    str
        Reporte completo como cadena de texto.
    """
    y_true = df["ClasificacionEsperada"]
    y_pred = df["ClasificacionModelo"]
    n      = len(df)

    accuracy  = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average="macro",
                                labels=labels, zero_division=0)
    recall    = recall_score(y_true, y_pred, average="macro",
                             labels=labels, zero_division=0)
    f1        = f1_score(y_true, y_pred, average="macro",
                         labels=labels, zero_division=0)
    cm        = confusion_matrix(y_true, y_pred, labels=labels)

    correctos   = (df["ResultadoValidacion"] == "CORRECTO").sum()
    incorrectos = n - correctos

    df_por_clase = calcular_metricas_por_clase(y_true, y_pred, labels)

    lineas = []
    lineas.append("=" * 62)
    lineas.append("  Reporte de Evaluación del Modelo de")
    lineas.append("  Clasificación de Expedientes Pensionales")
    lineas.append("=" * 62)
    lineas.append(f"  Dataset evaluado    : {ARCHIVO_DATASET}")
    lineas.append(f"  Total de expedientes: {n}")
    lineas.append(f"  Correctamente clas. : {correctos} ({correctos/n*100:.1f}%)")
    lineas.append(f"  Incorrectamente     : {incorrectos} ({incorrectos/n*100:.1f}%)")

    lineas.append("\n" + "-" * 62)
    lineas.append("  MÉTRICAS GLOBALES (promedio macro)")
    lineas.append("-" * 62)
    lineas.append(f"  Accuracy            : {accuracy:.4f}  ({accuracy*100:.2f}%)")
    lineas.append(f"  Precision           : {precision:.4f}  ({precision*100:.2f}%)")
    lineas.append(f"  Recall              : {recall:.4f}  ({recall*100:.2f}%)")
    lineas.append(f"  F1-Score            : {f1:.4f}  ({f1*100:.2f}%)")

    lineas.append("\n" + "-" * 62)
    lineas.append("  MÉTRICAS POR CATEGORÍA DE CLASIFICACIÓN")
    lineas.append("-" * 62)

    # Encabezado tabla por clase
    lineas.append(
        f"  {'Clase':<16} {'Precision':>10} {'Recall':>10} "
        f"{'F1-Score':>10} {'Soporte':>10}"
    )
    lineas.append("  " + "-" * 58)
    for _, row in df_por_clase.iterrows():
        lineas.append(
            f"  {row['Clase']:<16} {row['Precision']:>10.4f} "
            f"{row['Recall']:>10.4f} {row['F1-Score']:>10.4f} "
            f"{row['Soporte']:>10}"
        )
    lineas.append("  " + "-" * 58)

    # Promedios macro
    lineas.append(
        f"  {'Promedio macro':<16} {precision:>10.4f} {recall:>10.4f} "
        f"{f1:>10.4f} {n:>10}"
    )

    lineas.append("\n" + "-" * 62)
    lineas.append("  MATRIZ DE CONFUSIÓN")
    lineas.append("-" * 62)
    lineas.append(formatear_matriz_confusion(cm, labels))

    lineas.append("-" * 62)
    lineas.append("  DISTRIBUCIÓN DE CLASIFICACIONES")
    lineas.append("-" * 62)
    dist_modelo   = df["ClasificacionModelo"].value_counts()
    dist_esperada = df["ClasificacionEsperada"].value_counts()
    lineas.append(
        f"  {'Clase':<16} {'Modelo':>10} {'%':>8} "
        f"{'Esperada':>12} {'%':>8}"
    )
    lineas.append("  " + "-" * 58)
    for label in labels:
        nm = dist_modelo.get(label, 0)
        ne = dist_esperada.get(label, 0)
        lineas.append(
            f"  {label:<16} {nm:>10} {nm/n*100:>7.1f}% "
            f"{ne:>12} {ne/n*100:>7.1f}%"
        )

    lineas.append("\n" + "=" * 62)
    lineas.append("  Reporte generado correctamente.")
    lineas.append("=" * 62)

    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Ejecución principal
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # Cargar dataset
    df = cargar_dataset(ARCHIVO_DATASET)

    # Generar reporte
    reporte = generar_reporte(df, LABELS)

    # Imprimir en consola
    print(reporte)

    # Guardar reporte en archivo de texto
    with open(ARCHIVO_REPORTE, "w", encoding="utf-8") as f:
        f.write(reporte)

    print(f"\n  Reporte guardado en: {ARCHIVO_REPORTE}")
