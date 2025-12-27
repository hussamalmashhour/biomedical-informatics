# Ejercicio 2 - Mean Squared Error (MSE)

## Objetivo
Implementar una función que calcula el **Error Cuadrático Medio (MSE)** para evaluar la calidad de un clustering.

## Descripción

### Mean Squared Error (MSE)
El MSE es una métrica que mide qué tan bien los puntos están agrupados alrededor de sus centroides:

1. **Para cada punto**: Encontrar el centroide más cercano
2. **Calcular**: Distancia euclidiana al cuadrado hasta ese centroide
3. **Promediar**: Todas las distancias cuadradas

### Fórmula

```
MSE = (1/n) × Σ min_c ||point_i - center_c||²
```

Donde:
- `n` = número de puntos
- `min_c` = mínimo sobre todos los centroides
- `||·||²` = distancia euclidiana al cuadrado

### Interpretación
- **MSE bajo**: Los puntos están cerca de sus centroides → buen clustering
- **MSE alto**: Los puntos están lejos de sus centroides → mal clustering

## Especificación de la Función

```python
def mse(points, centers):
    """
    Calcula el error cuadrático medio del clustering.
    
    Args:
        points: array (n, d) de puntos n-dimensionales
        centers: array (k, d) de centroides n-dimensionales
        
    Returns:
        float: error cuadrático medio
    """
```

## Ejemplos

### Ejemplo 1 (Validación)
```python
points = np.array([
    [ 1, 24], [ 4,  2], [23, 20], [24, 22], [25, 23], [23, 18],
    [24, 21], [25, 24], [31, 10], [32, 12], [33, 13], [31,  8],
    [30, 11], [34, 13], [21,  2], [22,  1], [23,  3], [25,  4],
    [21,  3], [24,  2]
])

centers = np.array([[1, 24], [31, 8], [4, 2]])

result = mse(points, centers)
# Expected: 104.95
```

### Ejemplo 2 (Test Case)
```python
points = np.array([
    [3, 20], [4, 22], [5, 23], [3, 18], [4, 21], [5, 24],
    [21, 10], [22, 12], [23, 13], [21, 8], [20, 11], [24, 13],
    [11, 2], [12, 1], [13, 3], [15, 4], [11, 3], [14, 2]
])

centers = np.array([[3, 20], [24, 13], [14, 2]])

result = mse(points, centers)
# Result: 8.50
```

## Uso

### Ejecutar la función con ejemplos:
```bash
python mse.py
```

### Generar URL de submission:
```bash
python submit.py
```

## Implementación

### Algoritmo
1. Inicializar array de distancias mínimas con infinito
2. Para cada centroide:
   - Calcular distancia cuadrada de todos los puntos al centroide
   - Actualizar distancias mínimas si esta es menor
3. Retornar el promedio de las distancias mínimas

### Complejidad
- **Tiempo**: O(n × k × d) donde:
  - n = número de puntos
  - k = número de centroides
  - d = dimensionalidad
- **Espacio**: O(n) para almacenar distancias mínimas

### Vectorización con NumPy
```python
# Calcular distancias cuadradas vectorizadas
sq_distances = np.sum((points - center) ** 2, axis=1)

# Mantener mínimo para cada punto
min_sq_distances = np.minimum(min_sq_distances, sq_distances)

# Promedio
return np.mean(min_sq_distances)
```

## Resultados

### Ejemplo 1
- **Puntos**: 20 puntos en 2D
- **Centroides**: 3 centroides
- **MSE**: 104.95 ✓

### Ejemplo 2 (Test)
- **Puntos**: 18 puntos en 2D
- **Centroides**: 3 centroides
- **MSE**: 8.50

## Relación con K-means

El MSE es la función objetivo que **K-means minimiza**:

1. **K-means objetivo**: Minimizar Σ ||x - μ_c(x)||²
2. **MSE**: Promedio de esas distancias cuadradas
3. **Lloyd's algorithm**: Iterativamente reduce el MSE

### Comparación de Clusterings
```python
# Clustering A
mse_A = mse(points, centers_A)  # 8.50

# Clustering B  
mse_B = mse(points, centers_B)  # 15.30

# Clustering A es mejor (menor MSE)
```

## Aplicación a Expresión Génica

Si aplicamos MSE a los centroides del Ejercicio 1:

```python
from farthest_first import load_dm_matrix

# Cargar dm matrix
dm = load_dm_matrix()

# Cargar centroides del ejercicio 1
centroids = np.load('../farthest_first_tema5_eje1/centroids.npy')

# Calcular MSE
clustering_quality = mse(dm, centroids)

print(f"MSE del Farthest First clustering: {clustering_quality:.2f}")
```

Este MSE indica qué tan bien los 3 centroides representan los 229 genes diferencialmente expresados.

## Conceptos Clave

### Distancia Euclidiana al Cuadrado
```
d²(p, c) = Σ(p_i - c_i)²
```
- No necesita raíz cuadrada (más eficiente)
- Preserva el orden de distancias
- Penaliza fuertemente puntos lejanos

### Asignación al Centroide Más Cercano
- Cada punto se asigna al centroide con menor distancia
- Esto define las particiones/clusters implícitos
- Base del algoritmo K-means

### Métricas Alternativas
| Métrica | Fórmula | Uso |
|---------|---------|-----|
| MSE | Promedio de distancias² | K-means, Lloyd |
| SSE | Suma de distancias² | Optimización |
| RMSE | √MSE | Interpretación |
| Silhouette | Cohesión vs separación | Validación |

## Referencias

- K-means clustering algorithm
- Lloyd's algorithm (1957/1982)
- Within-cluster sum of squares (WCSS)

## Extensiones

1. **Weighted MSE**: Pesos diferentes por cluster
2. **Normalized MSE**: Dividir por varianza de datos
3. **Elbow method**: Plot MSE vs k para seleccionar k óptimo
4. **Comparison**: Comparar MSE de Farthest First vs K-means
