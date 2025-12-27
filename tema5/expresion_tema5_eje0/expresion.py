"""
Ejercicio 0 - Análisis de Expresión Génica
Experimento de DeRisi sobre diauxic shift en Saccharomyces cerevisiae

Este script:
1. Descarga el experimento de DeRisi (si no existe)
2. Carga la matriz de expresión con numpy
3. Selecciona genes con expresión (log2) en valor absoluto >2.3 para alguno de los tiempos
"""

import numpy as np
import urllib.request
import os


def download_data(url, filename):
    """
    Descarga el archivo de datos si no existe.
    
    Args:
        url (str): URL del archivo a descargar
        filename (str): Nombre del archivo de destino
    """
    if not os.path.exists(filename):
        print(f"Descargando datos desde {url}...")
        urllib.request.urlretrieve(url, filename)
        print(f"Datos guardados en {filename}")
    else:
        print(f"El archivo {filename} ya existe.")


def load_expression_data(filename):
    """
    Carga la matriz de expresión desde el archivo.
    
    Args:
        filename (str): Nombre del archivo con los datos
        
    Returns:
        tuple: (data, gene_names) donde data es la matriz numérica y gene_names son los nombres de genes
    """
    print(f"\nCargando datos desde {filename}...")
    
    # Cargar los datos usando numpy.genfromtxt
    # - delimiter='\t': los datos están separados por tabuladores
    # - names=True: la primera fila contiene los nombres de las columnas
    # - dtype=None: detectar automáticamente el tipo de datos
    # - skip_header=0: no saltar filas (names=True ya maneja la cabecera)
    # - usecols: usaremos todas las columnas
    # - filling_values=0: usar 0 para valores perdidos
    data = np.genfromtxt(
        filename,
        delimiter='\t',
        skip_header=1,  # Saltar la cabecera
        usecols=range(1, 8),  # Solo las columnas numéricas (1-7)
        filling_values=0
    )
    
    # Cargar los nombres de genes por separado
    gene_names = np.genfromtxt(
        filename,
        delimiter='\t',
        skip_header=1,
        usecols=0,
        dtype=str
    )
    
    return data, gene_names


def analyze_dimensions(data):
    """
    Analiza y muestra las dimensiones de la matriz.
    
    Args:
        data (numpy.ndarray): Matriz de expresión
    """
    print(f"\n--- Dimensiones de la matriz ---")
    print(f"Forma de la matriz: {data.shape}")
    print(f"Número de genes: {data.shape[0]}")
    print(f"Número de tiempos/condiciones: {data.shape[1]}")


def select_differentially_expressed_genes(data, gene_names, threshold=2.3):
    """
    Selecciona genes con expresión diferencial significativa.
    
    Selecciona genes con valor absoluto de log2 fold-change > threshold
    para al menos uno de los tiempos.
    
    Args:
        data (numpy.ndarray): Matriz de expresión
        gene_names (numpy.ndarray): Nombres de los genes
        threshold (float): Umbral de log2 fold-change
        
    Returns:
        tuple: (dm, dgenes, indices) donde:
               - dm es la matriz de expresión de genes diferenciales
               - dgenes son los nombres de genes diferenciales
               - indices son los índices de los genes seleccionados
    """
    print(f"\n--- Selección de genes diferencialmente expresados ---")
    print(f"Umbral: |log2 FC| > {threshold}")
    
    # Calcular el valor absoluto de la matriz
    abs_data = np.abs(data)
    
    # Encontrar genes donde al menos un tiempo tiene |log2 FC| > threshold
    # numpy.any devuelve True si algún valor en cada fila cumple la condición
    mask = np.any(abs_data > threshold, axis=1)
    
    # numpy.where devuelve los índices donde la condición es True
    indices = np.where(mask)[0]
    
    # Seleccionar los genes diferencialmente expresados
    dm = data[indices]
    dgenes = gene_names[indices]
    
    print(f"Número de genes diferencialmente expresados: {len(dgenes)}")
    
    return dm, dgenes, indices


def show_sample_genes(dgenes, dm, n=10):
    """
    Muestra una muestra de los genes seleccionados.
    
    Args:
        dgenes (numpy.ndarray): Nombres de genes diferenciales
        dm (numpy.ndarray): Matriz de expresión de genes diferenciales
        n (int): Número de genes a mostrar
    """
    print(f"\n--- Muestra de los primeros {n} genes diferencialmente expresados ---")
    print(f"{'Gen':<12} {'Valores de expresión (log2 FC)'}")
    print("-" * 70)
    for i in range(min(n, len(dgenes))):
        values_str = "  ".join([f"{v:6.2f}" for v in dm[i]])
        print(f"{dgenes[i]:<12} {values_str}")


def main():
    """
    Función principal del ejercicio.
    """
    # URL del archivo de datos
    url = "http://vis.usal.es/rodrigo/documentos/bioinfo/expresion/2010diauxic-edited.txt"
    filename = "2010diauxic-edited.txt"
    
    print("=" * 70)
    print("Ejercicio 0 - Análisis de Expresión Génica")
    print("Experimento de DeRisi (Diauxic Shift)")
    print("=" * 70)
    
    # 1) Descargar el experimento (si no existe)
    download_data(url, filename)
    
    # Información sobre el origen de la matriz
    print("\n--- Información sobre la matriz ---")
    print("Origen: Experimento de DeRisi et al. sobre diauxic shift")
    print("Referencia: DeRisi, J. L., Iyer, V. R., & Brown, P. O. (1997).")
    print("            Science, 278(5338), 680-686.")
    print("Datos disponibles en: Stanford Microarray Database (SMD)")
    print("                      Gene Expression Omnibus (GEO)")
    
    # 2) Cargar la matriz con Python
    data, gene_names = load_expression_data(filename)
    
    # Mostrar dimensiones
    analyze_dimensions(data)
    
    # 3) Seleccionar genes con expresión |log2 FC| > 2.3
    dm, dgenes, indices = select_differentially_expressed_genes(data, gene_names, threshold=2.3)
    
    # Mostrar una muestra de los genes seleccionados
    show_sample_genes(dgenes, dm, n=10)
    
    print("\n" + "=" * 70)
    print("RESUMEN")
    print("=" * 70)
    print(f"✓ Matriz original: {data.shape[0]} genes × {data.shape[1]} tiempos")
    print(f"✓ Genes diferencialmente expresados (|log2 FC| > 2.3): {len(dgenes)}")
    print(f"✓ Porcentaje de genes diferenciales: {len(dgenes)/data.shape[0]*100:.1f}%")
    print("=" * 70)


if __name__ == "__main__":
    main()
