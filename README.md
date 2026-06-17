# Sistema de Análisis y Clasificación Automática de Expedientes Pensionales

> Trabajo de Fin de Máster — Máster Universitario en Análisis y Visualización de Datos Masivos / Visual Analytics and Big Data  
> Universidad Internacional de La Rioja (UNIR) — 2026

---

## 👥 Autores

| Nombre | Rol en el proyecto |
|---|---|
| Juan Pablo Guevara Rendón | Diseño del modelo de clasificación, desarrollo del código y validación |
| Nancy Johanna Calderón Manjarrez | Análisis normativo, definición de variables y validación del modelo |

---

## 📋 Descripción del proyecto

Este proyecto es un sistema de análisis y clasificación automática de expedientes prestacionales del sistema pensional colombiano, diseñado en el contexto de la Reforma Pensional (Ley 2381 de 2024).

El sistema implementa un **motor de reglas de negocio basado en normativa** que clasifica expedientes en tres categorías:

- ✅ **Automático** — expedientes que cumplen todos los criterios para procesamiento sin intervención humana
- ⚠️ **Mixto** — expedientes que requieren supervisión humana en alguna etapa del proceso
- 🔴 **Manual** — expedientes que deben ser gestionados íntegramente por un analista

El modelo fue validado sobre un dataset sintético de **1.000 expedientes**, obteniendo las siguientes métricas de desempeño:

| Métrica | Valor |
|---|---|
| Accuracy | 95.5% |
| Precision (macro) | 95.7% |
| Recall (macro) | 95.0% |
| F1-Score (macro) | 95.3% |

---

## 📁 Contenido del repositorio

```
clasificacion-pensional/
│
├── README.md                                      ← Este archivo
├── requirements.txt                               ← Dependencias Python
│
├── generador_dataset.py                           ← Genera el dataset sintético
├── evaluacion_modelo.py                           ← Calcula métricas de desempeño
│
├── dataset_pensional_sintetico.csv                ← Dataset generado (1.000 expedientes)
└── reporte_evaluacion_modelo.txt                  ← Resultado metricas de evaluación
└── validador_modelo_clasificacion_pensional.html  ← Visualización interactiva
```

### Descripción de cada archivo

**`generador_dataset.py`**  
Genera el dataset sintético de expedientes prestacionales aplicando las reglas de negocio formalizadas en el modelo de clasificación progresiva. Produce el archivo `dataset_pensional_sintetico.csv` con 1.000 registros y las columnas `ClasificacionModelo`, `ClasificacionEsperada` y `ResultadoValidacion`.

**`evaluacion_modelo.py`**  
Lee el dataset generado y calcula las métricas de evaluación del modelo: Accuracy, Precision, Recall, F1-Score (por clase y promedio macro) y matriz de confusión. Genera el archivo `reporte_evaluacion_modelo.txt` con los resultados completos.

**`dataset_pensional_sintetico.csv`**  
Dataset de 1.000 expedientes sintéticos generado a partir de las reglas de negocio del sistema pensional colombiano. No contiene datos personales reales. Incluye 21 variables derivadas de los sistemas institucionales de Colpensiones.

**`reporte_evaluacion_modelo.txt`**  
Resultado de la evaluación de las métricas del dataset sintetico. Permite visualizar metricas globales, por categoría de clasificación, Matriz de confusión y distribución de clasificaciones al realizar el análisis y evaluación del dataset.

**`validador_modelo_clasificacion_pensional.html`**  
Visualización interactiva de los resultados de validación. Permite configurar el número de expedientes y la tasa de error del evaluador experto, y muestra en tiempo real las métricas, la matriz de confusión y una vista previa del dataset.

---

## ▶️ Cómo ejecutar el código

### 1. Requisitos previos

Tener instalado Python 3.8 o superior. Verificar con:

```bash
python --version
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Generar el dataset sintético

```bash
python generador_dataset.py
```

Esto genera el archivo `dataset_pensional_sintetico.csv` en el mismo directorio.

### 4. Evaluar el modelo

```bash
python evaluacion_modelo.py
```

Esto lee el CSV generado y muestra en consola las métricas completas. También genera `reporte_evaluacion_modelo.txt`.

### 5. Ver la visualización interactiva

Abrir directamente en el navegador:

🔗 [Visualización interactiva del modelo](https://htmlpreview.github.io/?https://github.com/bio-uno/clasificacion-pensional/blob/main/validador_modelo_clasificacion_pensional.html)

---

## 🔒 Nota sobre confidencialidad de datos

El dataset sintético publicado en este repositorio es suficiente para reproducir los resultados de validación presentados en el TFM, incluyendo la matriz de confusión y las métricas de desempeño del modelo.

---

## 📚 Contexto académico

Este repositorio forma parte del Trabajo de Fin de Máster titulado:

**"Sistema de Análisis y Clasificación Automática de Datos Masivos para la Optimización de Decisiones Administrativas Pensionales"**

Desarrollado en el marco del Máster Universitario en Análisis y Visualización de Datos Masivos / Visual Analytics and Big Data de la Universidad Internacional de La Rioja (UNIR), en el contexto de la Reforma Pensional colombiana establecida por la Ley 2381 de 2024.

---

## 📄 Licencia

Repositorio de uso académico. Todos los derechos reservados por los autores.
