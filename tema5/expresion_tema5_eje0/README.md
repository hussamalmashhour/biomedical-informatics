# Ejercicio 0 - Análisis de Expresión Génica

## Objetivo
Analizar el experimento de DeRisi sobre el "diauxic shift" en *Saccharomyces cerevisiae* utilizando Python y NumPy.

## Descripción del Ejercicio

### 1) Descarga del experimento de DeRisi
- **URL**: http://vis.usal.es/rodrigo/documentos/bioinfo/expresion/2010diauxic-edited.txt
- El experimento ya está en **log2 fold-change**
- **Origen de los datos**: 
  - Experimento clásico de DeRisi et al. (1997)
  - Publicado en Science, 278(5338), 680-686
  - Puedes encontrar esta matriz en:
    - Stanford Microarray Database (SMD)
    - Gene Expression Omnibus (GEO)

### 2) Carga de la matriz con Python
- Utiliza `numpy.genfromtxt` con los siguientes argumentos:
  - `delimiter='\t'`: separador de tabuladores
  - `skip_header=1`: saltar la primera línea (cabecera)
  - `usecols`: seleccionar solo columnas numéricas
  - `filling_values=0`: rellenar valores perdidos con 0
- **Dimensiones de la matriz**: 6034 genes × 7 tiempos

### 3) Selección de genes diferencialmente expresados
- **Criterio**: Genes con expresión (log2) en valor absoluto > 2.3 para **alguno** de los tiempos
- **Herramientas a utilizar**:
  - `numpy.any`: para verificar si algún valor en cada fila cumple la condición
  - `numpy.where`: para obtener los índices de los genes que cumplen
- **Resultado**: 
  - Los genes seleccionados se llaman `dgenes`
  - Su matriz de expresión se llama `dm`
  - **Número de genes**: 229 (3.8% del total)

## Uso

Ejecuta el script principal:

```bash
python expresion.py
```

## Estructura del Código

El script `expresion.py` incluye las siguientes funciones:

1. **`download_data(url, filename)`**: Descarga el archivo de datos si no existe
2. **`load_expression_data(filename)`**: Carga la matriz de expresión usando numpy
3. **`analyze_dimensions(data)`**: Analiza y muestra las dimensiones de la matriz
4. **`select_differentially_expressed_genes(data, gene_names, threshold)`**: Selecciona genes con expresión diferencial
5. **`show_sample_genes(dgenes, dm, n)`**: Muestra una muestra de los genes seleccionados

## Resultados Esperados

Al ejecutar el script, obtendrás:

```
======================================================================
Ejercicio 0 - Análisis de Expresión Génica
Experimento de DeRisi (Diauxic Shift)
======================================================================

--- Dimensiones de la matriz ---
Forma de la matriz: (6034, 7)
Número de genes: 6034
Número de tiempos/condiciones: 7

--- Selección de genes diferencialmente expresados ---
Umbral: |log2 FC| > 2.3
Número de genes diferencialmente expresados: 229

======================================================================
RESUMEN
======================================================================
✓ Matriz original: 6034 genes × 7 tiempos
✓ Genes diferencialmente expresados (|log2 FC| > 2.3): 229
✓ Porcentaje de genes diferenciales: 3.8%
======================================================================
```

## Conceptos Clave

### Diauxic Shift
El "diauxic shift" es el cambio metabólico que ocurre en levaduras cuando pasan de metabolismo fermentativo (glucosa) a respiratorio (etanol). Este experimento mide la expresión génica durante esta transición.

### Log2 Fold-Change
- Representa el cambio de expresión en escala logarítmica base 2
- **log2 FC = 1**: expresión duplicada (2×)
- **log2 FC = -1**: expresión reducida a la mitad (0.5×)
- **log2 FC = 2.3**: expresión aumentada ~5×
- **log2 FC = -2.3**: expresión reducida a ~0.2×

### NumPy Functions Utilizadas
- `numpy.genfromtxt()`: carga datos desde archivos de texto
- `numpy.abs()`: valor absoluto
- `numpy.any(axis=1)`: verifica si algún valor es True en cada fila
- `numpy.where()`: retorna índices donde la condición es True
- `.shape`: dimensiones del array

## Referencias

- DeRisi, J. L., Iyer, V. R., & Brown, P. O. (1997). Exploring the metabolic and genetic control of gene expression on a genomic scale. *Science*, 278(5338), 680-686.
