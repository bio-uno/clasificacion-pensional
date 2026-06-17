"""
=============================================================================
         Sistema de Análisis y Clasificación Automática de Expedientes
         Pensionales
=============================================================================
Archivo : generador_dataset.py
Autores : Juan Pablo Guevara Rendón
          Nancy Johanna Calderón Manjarrez
Programa: Máster Universitario en Análisis y Visualización de Datos Masivos
          / Visual Analytics and Big Data - UNIR
Fecha   : 2026
-----------------------------------------------------------------------------
Descripción:
    Genera un dataset sintético de expedientes prestacionales colombianos
    aplicando las reglas de negocio formalizadas en el modelo de
    clasificación progresiva (Tablas 5, 6 y 7 del TFM).

    El dataset resultante contiene tres columnas clave para la validación:
      - ClasificacionModelo   : clasificación asignada por el motor de reglas
      - ClasificacionEsperada : referencia del evaluador experto (ground truth)
      - ResultadoValidacion   : CORRECTO / INCORRECTO

    Salida: dataset_pensional_sintetico.csv
=============================================================================
"""

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Parámetros configurables
# ---------------------------------------------------------------------------
SEMILLA         = 42       # Semilla para reproducibilidad
N_EXPEDIENTES   = 1000     # Número de expedientes a generar
TASA_COMPLEJOS  = 0.35     # Proporción de expedientes con perfil complejo
TASA_ERROR      = 0.05     # Tasa de discrepancia del evaluador experto (5%)

# ---------------------------------------------------------------------------
# Constantes del dominio pensional colombiano
# ---------------------------------------------------------------------------
PRESTACIONES_LINEA_MANUAL = [
    "Sobrevivientes",
    "Convenio Internacional",
    "Invalidez Especial"
]

PRESTACIONES_LINEA_AUTO = [
    "Vejez",
    "Sustitucion",
    "Auxilio Funerario"
]

LABELS = ["Automatico", "Mixto", "Manual"]

# ---------------------------------------------------------------------------
# Motor de reglas de negocio
# Implementa la clasificación progresiva definida en las Tablas 5, 6 y 7
# del TFM. El orden de evaluación es crítico: primero se detectan
# condiciones de línea Manual, luego condiciones de línea Mixta.
# Si ninguna condición aplica, el expediente es Automático.
# ---------------------------------------------------------------------------
def aplicar_reglas(expediente: dict) -> str:
    """
    Aplica el motor de reglas de negocio sobre un expediente y retorna
    la clasificación correspondiente: 'Manual', 'Mixto' o 'Automático'.

    Parámetros
    ----------
    expediente : dict
        Diccionario con las variables del expediente.

    Retorna
    -------
    str
        Clasificación asignada por el motor de reglas.
    """

    # --- ETAPA 1: Reglas de exclusión automática (dirección a línea Manual) ---
    if expediente["TipoPrestacion"] in PRESTACIONES_LINEA_MANUAL:
        return "Manual"
    if expediente["TipoRecurso"] in ["Reposicion", "Apelacion"]:
        return "Manual"
    if expediente["TieneSentencia"] == "Si":
        return "Manual"
    if expediente["CruceISSHistorico"] == "Si":
        return "Manual"

    # --- ETAPA 2: Reglas de procesamiento supervisado (dirección a línea Mixta) ---
    if expediente["ResultadoValIndicios"] == "Si":
        return "Mixto"
    if expediente["ResultadoValNomina"] == "Si":
        return "Mixto"
    if expediente["TieneDocumentosAdicionales"] == "Si":
        return "Mixto"
    if expediente["TienePQRSPendiente"] == "Si":
        return "Mixto"
    if expediente["ExisteRegistroEmbargo"] == "Si":
        return "Mixto"
    if expediente["RequiereRevisionHL"] == "Si":
        return "Mixto"
    if expediente["TieneTiemposNoISS"] == "Si":
        return "Mixto"
    if expediente["RecibePensionActual"] == "Si":
        return "Mixto"
    if expediente["UltimoEmpleadorPublico"] == "Si":
        return "Mixto"
    if expediente["TieneRequerimientoExterno"] == "Si":
        return "Mixto"
    if expediente["EstadoRequerimientoInterno"] == "Abierto":
        return "Mixto"

    # --- ETAPA 3: Validación final - procesamiento automático ---
    return "Automatico"


def introducir_discrepancia(clasificacion: str, tasa_error: float) -> str:
    """
    Simula la clasificación de un evaluador experto humano introduciendo
    una tasa controlada de discrepancia respecto al motor de reglas.
    Esto permite construir el ground truth necesario para calcular
    las métricas de evaluación del modelo.

    Parámetros
    ----------
    clasificacion : str
        Clasificación asignada por el motor de reglas.
    tasa_error : float
        Probabilidad de que el evaluador difiera del modelo (0.0 - 1.0).

    Retorna
    -------
    str
        Clasificación del evaluador experto.
    """
    if np.random.random() >= tasa_error:
        return clasificacion
    alternativas = [label for label in LABELS if label != clasificacion]
    return np.random.choice(alternativas)


def generar_expediente(id_expediente: int, tasa_complejos: float,
                        tasa_error: float) -> dict:
    """
    Genera un expediente sintético con variables derivadas y clasificación.

    Parámetros
    ----------
    id_expediente : int
        Identificador secuencial del expediente.
    tasa_complejos : float
        Probabilidad de que el expediente tenga perfil complejo.
    tasa_error : float
        Tasa de discrepancia del evaluador experto.

    Retorna
    -------
    dict
        Expediente con todas sus variables y columnas de validación.
    """
    es_complejo = np.random.random() < tasa_complejos
    p = 0.35 if es_complejo else 0.08

    pool_prestaciones = (PRESTACIONES_LINEA_MANUAL + PRESTACIONES_LINEA_AUTO
                         if es_complejo else PRESTACIONES_LINEA_AUTO)
    pool_recursos = (["Reposicion", "Apelacion", "Ninguno", "Ninguno"]
                     if es_complejo else ["Ninguno", "Ninguno", "Ninguno"])

    expediente = {
        # ---- Identificación ------------------------------------------------
        "ID_Expediente"              : f"EXP-{id_expediente:06d}",

        # ---- Variables de clasificación base (Tabla 5 - Etapa 1) -----------
        "TipoPrestacion"             : np.random.choice(pool_prestaciones),
        "TipoRecurso"                : np.random.choice(pool_recursos),
        "TieneSentencia"             : "Si" if np.random.random() < (0.15 if es_complejo else 0.02) else "No",
        "CruceISSHistorico"          : "Si" if np.random.random() < (0.18 if es_complejo else 0.03) else "No",

        # ---- Variables de validación cruzada (Tabla 6 - Etapa 2) -----------
        "ResultadoValIndicios"       : "Si" if np.random.random() < p * 1.2 else "No",
        "ResultadoValNomina"         : "Si" if np.random.random() < p       else "No",
        "ResultadoValHL"             : "Si" if np.random.random() < p * 0.8 else "No",
        "TieneDocumentosAdicionales" : "Si" if np.random.random() < p * 1.5 else "No",
        "ExisteRegistroEmbargo"      : "Si" if np.random.random() < p * 0.5 else "No",
        "RequiereRevisionHL"         : "Si" if np.random.random() < p * 1.1 else "No",
        "UltimoEmpleadorPublico"     : "Si" if np.random.random() < (0.25 if es_complejo else 0.10) else "No",
        "RecibePensionActual"        : "Si" if np.random.random() < p * 0.9 else "No",
        "TienePQRSPendiente"         : "Si" if np.random.random() < p * 1.3 else "No",
        "TieneRequerimientoExterno"  : "Si" if np.random.random() < p * 0.7 else "No",
        "EstadoRequerimientoInterno" : "Abierto" if np.random.random() < p * 0.8 else "Cerrado",
        "TieneTiemposNoISS"          : "Si" if np.random.random() < (0.20 if es_complejo else 0.05) else "No",

        # ---- Variables de validación final (Tabla 7 - Etapa 3) -------------
        "EstadoVinculacionBEPS"      : np.random.choice(
                                           ["Vinculado", "Prospecto", "No aplica"],
                                           p=[0.06, 0.06, 0.88]
                                       ),
        "AsignarBancoBEPS"           : "Si" if np.random.random() < 0.08 else "No",
    }

    # ---- Columnas de validación del modelo ----------------------------------
    expediente["ClasificacionModelo"]   = aplicar_reglas(expediente)
    expediente["ClasificacionEsperada"] = introducir_discrepancia(
                                              expediente["ClasificacionModelo"],
                                              tasa_error
                                          )
    expediente["ResultadoValidacion"]   = (
        "CORRECTO"
        if expediente["ClasificacionModelo"] == expediente["ClasificacionEsperada"]
        else "INCORRECTO"
    )

    return expediente


# ---------------------------------------------------------------------------
# Ejecución principal
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    np.random.seed(SEMILLA)

    print("=" * 60)
    print("  Generador de Dataset Sintético Pensional")
    print("=" * 60)
    print(f"  Expedientes a generar : {N_EXPEDIENTES}")
    print(f"  Tasa de complejos     : {TASA_COMPLEJOS * 100:.0f}%")
    print(f"  Tasa de error experto : {TASA_ERROR * 100:.0f}%")
    print(f"  Semilla               : {SEMILLA}")
    print("-" * 60)

    registros = []
    for i in range(1, N_EXPEDIENTES + 1):
        registros.append(
            generar_expediente(i, TASA_COMPLEJOS, TASA_ERROR)
        )

    df = pd.DataFrame(registros)

    # Guardar CSV
    archivo_salida = "dataset_pensional_sintetico.csv"
    df.to_csv(archivo_salida, index=False, encoding="utf-8-sig")

    # Resumen de distribución
    distribucion = df["ClasificacionModelo"].value_counts()
    correctos    = (df["ResultadoValidacion"] == "CORRECTO").sum()

    print("\n  Distribución de clasificaciones (ClasificacionModelo):")
    for label in LABELS:
        n   = distribucion.get(label, 0)
        pct = n / N_EXPEDIENTES * 100
        print(f"    {label:<14}: {n:>5} expedientes  ({pct:.1f}%)")

    print(f"\n  Validación con evaluador experto:")
    print(f"    Correctos   : {correctos} ({correctos / N_EXPEDIENTES * 100:.1f}%)")
    print(f"    Incorrectos : {N_EXPEDIENTES - correctos} "
          f"({(N_EXPEDIENTES - correctos) / N_EXPEDIENTES * 100:.1f}%)")
    print(f"\n  Dataset guardado en: {archivo_salida}")
    print("=" * 60)
