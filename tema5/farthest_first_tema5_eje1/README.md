# Ejercicio 1 - Farthest First Clustering

## Objetivo
Aplicar el algoritmo de clustering **Farthest First** a la matriz de expresión génica `dm` obtenida del Ejercicio 0.

## Descripción del Algoritmo

### Farthest First Traversal
El algoritmo **Farthest First** es un método heurístico para seleccionar k centros de clusters:

1. **Inicio**: Comenzar con un punto inicial como primer centroide
2. **Iteración**: Para seleccionar el siguiente centroide:
   - Calcular la distancia de cada punto a su centroide más cercano
   - Seleccionar el punto que tiene la mayor distancia mínima
3. **Repetir**: Hasta tener k centroides

**Complejidad**: O(k × n × m) donde k = clusters, n = puntos, m = dimensiones

## Workflow Completo

### PASO 1: Obtener la matriz dm (Ejercicio 0)
- Cargar datos de expresión de DeRisi: `2010diauxic-edited.txt`
- Seleccionar genes con |log2 FC| > 2.3 para algún timepoint
- **Resultado**: dm matriz de 229 genes × 7 timepoints

### PASO 2: Test del Algoritmo
- Verificar con ejemplo 2D simple:
  ```python
  E = [[3,20], [4,22], ..., [14,2]]  # 18 puntos
  k = 3
  init = [3, 20]
  # Resultado esperado: [[3,20], [24,13], [11,2]]
  ```

### PASO 3: Aplicar a dm
- **k = 3** clusters
- **init = [-0.23, -0.09, -0.27, 0.2, 0.56, 1.52, 2.64]**
- Este punto inicial representa el perfil del gen YPR184W

## Uso

```bash
python farthest_first.py
```

## Resultados

### Centroides Encontrados (k=3)

**Centroid 1** (init - UP-REGULATED late):
```
0 hr:    -0.230
9.5 hr:  -0.090
11.5 hr: -0.270
13.5 hr:  0.200
15.5 hr:  0.560
18.5 hr:  1.520
20.5 hr:  2.640
```
- **Gene más cercano**: YPR184W
- **Patrón**: Inducido en fase tardía del diauxic shift

**Centroid 2** (DOWN-REGULATED late):
```
0 hr:     0.080
9.5 hr:  -0.270
11.5 hr: -0.150
13.5 hr: -1.180
15.5 hr: -1.600
18.5 hr: -2.940
20.5 hr: -3.060
```
- **Gene más cercano**: YPL012W
- **Patrón**: Reprimido en fase tardía (~8× reducción)

**Centroid 3** (STRONG UP-REGULATION):
```
0 hr:     -0.120
9.5 hr:    0.200
11.5 hr:   0.970
13.5 hr:   1.560
15.5 hr:   1.360
18.5 hr:   4.320  ← Pico máximo
20.5 hr:   3.470
```
- **Gene más cercano**: YML128C
- **Patrón**: Fuerte inducción (máximo ~20× en 18.5h)

### Interpretación Biológica

Los 3 centroides representan **patrones de expresión distintos** durante el diauxic shift:

1. **Centroide 1**: Genes de adaptación gradual a respiración
   - Incremento sostenido desde 13.5h hasta 20.5h
   
2. **Centroide 2**: Genes de metabolismo fermentativo
   - Reprimidos cuando se agota la glucosa
   - Máxima represión en fase respiratoria
   
3. **Centroide 3**: Genes de respuesta al estrés/respiración
   - Fuerte inducción máxima en 18.5h
   - Posiblemente genes mitocondriales o de metabolismo de etanol

## Archivos Generados

1. **`farthest_first_results.txt`**: Resultados detallados en formato texto
2. **`centroids.npy`**: Centroides en formato NumPy (para uso posterior)

## Conceptos Clave

### Distancia Euclidiana
El algoritmo usa distancia euclidiana en el espacio de expresión de 7 dimensiones:

```
d(gene1, gene2) = √(Σ(expr1[i] - expr2[i])²)
```

### Propiedad de Farthest First
- **Garantía**: Cada nuevo centroide está lo más lejos posible de los existentes
- **Ventaja**: Maximiza la separación inicial de clusters
- **Desventaja**: Sensible a outliers (puntos atípicos)

### Diferencias con K-means
| Farthest First | K-means |
|----------------|---------|
| Selección determinista | Iterativo con asignación |
| Una pasada | Múltiples iteraciones |
| Inicialización | Clustering completo |
| O(k × n × m) | O(iter × k × n × m) |

## Validación

El script incluye un test del algoritmo con el ejemplo 2D:

```
E = 18 puntos en 2D (3 clusters naturales)
k = 3
init = [3, 20]

Resultado esperado: [[3, 20], [24, 13], [11, 2]]
✓ Test PASSED
```

## Dependencias

```python
import numpy as np
import os
```

## Referencias

- DeRisi, J. L., et al. (1997). Exploring the metabolic and genetic control of gene expression on a genomic scale. *Science*, 278(5338), 680-686.
- Gonzalez, T. F. (1985). Clustering to minimize the maximum intercluster distance. *Theoretical Computer Science*, 38, 293-306.

## Extensiones Posibles

1. **Visualización**: Plot de centroides en heatmap
2. **Asignación de genes**: Clasificar todos los genes a clusters
3. **Validación**: Calcular silhouette score
4. **Comparación**: Comparar con K-means++ inicialización
