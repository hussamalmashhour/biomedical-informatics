# Ejercicio 3 - Lloyd's Algorithm (K-means)

## Objetivo
Implementar el **algoritmo de Lloyd** (también conocido como **K-means**), el algoritmo más popular para clustering.

## Descripción del Algoritmo

### Lloyd's Algorithm / K-means
Lloyd's algorithm es un método iterativo para particionar n puntos en k clusters:

1. **Inicialización**: Seleccionar k centroides iniciales
   - Aleatoriamente de los puntos existentes, O
   - Especificados mediante `initCenters` (para reproducibilidad)

2. **Iteración** (hasta convergencia o límite de iteraciones):
   - **Asignación**: Asignar cada punto al centroide más cercano
   - **Actualización**: Recalcular centroides como media de puntos asignados
   - **Convergencia**: Verificar si el movimiento promedio de centroides < threshold

3. **Salida**: Array de asignaciones de cluster para cada punto

### Criterio de Convergencia
```
avg_movement = (1/k) × Σ ||new_center_i - old_center_i||
```

Si `avg_movement ≤ convergence`, el algoritmo termina.

## Especificación de la Función

```python
def lloyd(points, k, convergence, iterations, initCenters=None):
    """
    Ejecuta el algoritmo de Lloyd (K-means clustering).
    
    Args:
        points: array (n, d) de puntos n-dimensionales
        k: número de clusters
        convergence: distancia media máxima entre centroides
                     de dos iteraciones para terminar
        iterations: número máximo de iteraciones
        initCenters: (opcional) array (k, d) de centroides iniciales
        
    Returns:
        labels: array (n,) con índice de cluster para cada punto
        centers: array (k, d) con centroides finales
    """
```

## Ejemplo del Ejercicio

### Parámetros
```python
points = np.array([
    [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
    [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
    [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
])

k = 3
convergence = 0.1
iterations = 100
```

### Pregunta: ¿Hay una única solución?
**No.** El resultado depende de la inicialización:
- Con inicialización aleatoria → diferentes soluciones posibles
- Con `initCenters` fijos → solución determinista

## Test Case (con initCenters)

### Parámetros
```python
initCenters = np.array([[3, 20], [24, 13], [14, 2]])
```

### Resultado
```python
# Converge en 2 iteraciones
labels = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2]

# Centroides finales
final_centers = [
    [ 4.00,  21.33],  # Cluster 0: 6 puntos (región superior izquierda)
    [21.83,  11.17],  # Cluster 1: 6 puntos (región derecha)
    [12.67,   2.50]   # Cluster 2: 6 puntos (región inferior)
]
```

### Visualización de Clusters
```
Cluster 0 (6 points): [3,20], [4,22], [5,23], [3,18], [4,21], [5,24]
Cluster 1 (6 points): [21,10], [22,12], [23,13], [21,8], [20,11], [24,13]
Cluster 2 (6 points): [11,2], [12,1], [13,3], [15,4], [11,3], [14,2]
```

## Uso

### Ejecutar con ejemplos:
```bash
python lloyd.py
```

### Generar URL de submission:
```bash
python submit.py
```

## Implementación

### Algoritmo Detallado

```python
# Paso 1: Inicializar centroides
if initCenters is None:
    indices = np.random.choice(n, k, replace=False)
    centers = points[indices].copy()
else:
    centers = initCenters.copy()

# Paso 2: Iterar hasta convergencia
for iter in range(max_iterations):
    # 2a. Asignar puntos a centroide más cercano
    distances = calcular_distancias(points, centers)
    labels = np.argmin(distances, axis=1)
    
    # 2b. Recalcular centroides
    new_centers = []
    for j in range(k):
        cluster_points = points[labels == j]
        new_centers[j] = np.mean(cluster_points, axis=0)
    
    # 2c. Verificar convergencia
    avg_movement = np.mean(||new_centers - centers||)
    if avg_movement <= convergence:
        break
    
    centers = new_centers

# Paso 3: Retornar asignaciones finales
return labels, centers
```

### Complejidad
- **Tiempo por iteración**: O(n × k × d)
  - n = número de puntos
  - k = número de clusters
  - d = dimensionalidad
- **Total**: O(iter × n × k × d)
- **Espacio**: O(n + k × d)

### Garantías
- **Convergencia**: Siempre converge (MSE es monótona decreciente)
- **Óptimo**: NO garantiza óptimo global (puede quedar en mínimo local)
- **Solución**: Depende de inicialización

## Comparación con Farthest First

| Aspecto | Farthest First | Lloyd (K-means) |
|---------|----------------|-----------------|
| Tipo | Inicialización | Clustering completo |
| Iteraciones | 1 pasada | Múltiples |
| Objetivo | Maximizar separación | Minimizar MSE |
| Óptimo | Heurístico | Mínimo local |
| Uso | Inicializar K-means | Clustering final |

## Aplicación a Datos de Expresión

Podemos aplicar Lloyd a la matriz `dm` del Ejercicio 0:

```python
# Cargar dm matrix
dm = np.load('../expresion_tema5_eje0/dm_matrix.npy')

# Usar centroides de Farthest First como inicialización
init_centers = np.load('../farthest_first_tema5_eje1/centroids.npy')

# Ejecutar Lloyd
labels, final_centers = lloyd(dm, k=3, convergence=0.1, 
                               iterations=100, initCenters=init_centers)

# Analizar clusters
for i in range(3):
    print(f"Cluster {i}: {np.sum(labels == i)} genes")
```

Esto nos da clusters mejorados comparados con Farthest First.

## Propiedades del Algoritmo

### Convergencia
- **Garantía**: El MSE nunca aumenta
- **Razón**: Cada paso (asignación + actualización) reduce o mantiene MSE
- **Problema**: Puede converger a mínimo local

### Dependencia de Inicialización
```python
# Diferentes inicializaciones → diferentes resultados
np.random.seed(42)
labels1, _ = lloyd(points, k, conv, iter)

np.random.seed(123)
labels2, _ = lloyd(points, k, conv, iter)

# labels1 != labels2 (en general)
```

### Solución: K-means++
Para mejor inicialización, usar K-means++ (no requerido en este ejercicio):
1. Primer centroide aleatorio
2. Siguientes: probabilidad proporcional a distancia²
3. Farthest First es una aproximación determinista

## Métrica de Calidad

Podemos usar MSE del Ejercicio 2 para evaluar:

```python
from mse import mse

# Calcular calidad del clustering
quality = mse(points, final_centers)
print(f"MSE del clustering: {quality:.2f}")
```

Menor MSE = mejor clustering.

## Casos Especiales

### Cluster Vacío
Si ningún punto se asigna a un centroide:
```python
if len(cluster_points) == 0:
    # Mantener centroide anterior
    new_centers[j] = centers[j]
    # O: reasignar al punto más lejano
```

### Un Solo Punto por Cluster
El centroide es exactamente ese punto:
```python
center = np.mean([point]) = point
```

## Extensiones

1. **K-means++**: Mejor inicialización
2. **Mini-batch K-means**: Más rápido para datos grandes
3. **Kernel K-means**: Para clusters no lineales
4. **K-medoids**: Usar puntos reales como centroides (más robusto)

## Referencias

- Lloyd, S. P. (1982). Least squares quantization in PCM. *IEEE Transactions on Information Theory*, 28(2), 129-137.
- MacQueen, J. (1967). Some methods for classification and analysis of multivariate observations. *Proceedings of the 5th Berkeley Symposium*.
- Arthur, D., & Vassilvitskii, S. (2007). k-means++: The advantages of careful seeding. *SODA*.
