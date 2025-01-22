# -*- coding: utf-8 -*-
# Importación de librerías necesarias
import time  # Para medir tiempos de ejecución
import csv   # Para manejo de archivos CSV
import sys   # Para configuración del sistema
import io    # Para manejo de entrada/salida
import matplotlib.pyplot as plt  # Para crear gráficos
import pandas as pd             # Para análisis de datos
import seaborn as sns          # Para visualizaciones mejoradas
from pathlib import Path       # Para manejo de rutas de archivos

# Configuración de la codificación de salida para manejar caracteres especiales
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Importación de las librerías para bases de datos
import pymongo  # Cliente de MongoDB
from neo4j import GraphDatabase  # Cliente de Neo4j
import statistics  # Para cálculos estadísticos
from typing import List, Dict, Any  # Para type hints
from bson import ObjectId  # Para manejar IDs de MongoDB

class DatabaseTester:
    """
    Clase principal para realizar pruebas de rendimiento entre MongoDB y Neo4j.
    Permite comparar operaciones CRUD básicas entre ambas bases de datos.
    """
    def __init__(self):
        """
        Constructor que inicializa las conexiones a ambas bases de datos.
        MongoDB se conecta al puerto 27017 y Neo4j al puerto 7687.
        """
        # Conexión a MongoDB
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mongo_db = self.mongo_client["performance_test"]
        self.mongo_collection = self.mongo_db["test_collection"]
        
        # Conexión a Neo4j
        self.neo4j_driver = GraphDatabase.driver(
            "bolt://localhost:7687", 
            auth=("neo4j", "mango2016")
        )

    def load_csv_data(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Carga datos desde un archivo CSV y los prepara para su uso en las bases de datos.
        
        Args:
            file_path (str): Ruta al archivo CSV
        
        Returns:
            List[Dict[str, Any]]: Lista de diccionarios con los datos del CSV
        
        Raises:
            ValueError: Si no se puede leer el archivo con ninguna codificación
        """
        # Lista de codificaciones a probar
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        # Intenta leer el archivo con diferentes codificaciones
        for encoding in encodings:
            try:
                data = []
                with open(file_path, 'r', encoding=encoding) as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Añade un ID único de MongoDB a cada fila
                        row['_id'] = ObjectId()
                        data.append(row)
                return data
            except UnicodeDecodeError:
                continue
        
        raise ValueError(f"No se pudo leer el archivo con ninguna de las codificaciones: {encodings}")

    def prepare_neo4j_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Convierte los datos del formato MongoDB al formato compatible con Neo4j.
        Principalmente convierte los ObjectId a strings.
        
        Args:
            data: Lista de diccionarios con datos de MongoDB
        
        Returns:
            Lista de diccionarios con datos compatibles con Neo4j
        """
        neo4j_data = []
        for item in data:
            neo4j_item = {}
            for key, value in item.items():
                # Convierte ObjectId a string para Neo4j
                if isinstance(value, ObjectId):
                    neo4j_item[key] = str(value)
                else:
                    neo4j_item[key] = value
            neo4j_data.append(neo4j_item)
        return neo4j_data

    def test_mongodb_operations(self, data: List[Dict[str, Any]]):
        """
        Realiza pruebas de operaciones CRUD en MongoDB y mide los tiempos.
        
        Args:
            data: Lista de documentos para insertar
            
        Returns:
            Dict con estadísticas de tiempo para cada operación
        """
        # Inicializa diccionario para almacenar resultados
        results = {
            "create": [],
            "read": [],
            "update": [],
            "delete": []
        }

        # CREATE - Inserción masiva
        start_time = time.time()
        self.mongo_collection.insert_many(data)
        results["create"].append(time.time() - start_time)

        # READ - 100 consultas de lectura
        test_id = data[0]["_id"]
        for _ in range(100):
            start_time = time.time()
            self.mongo_collection.find_one({"_id": test_id})
            results["read"].append(time.time() - start_time)

        # UPDATE - Actualización masiva
        start_time = time.time()
        self.mongo_collection.update_many(
            {}, 
            {"$set": {"test_field": "updated"}}
        )
        results["update"].append(time.time() - start_time)

        # DELETE - Eliminación masiva
        start_time = time.time()
        self.mongo_collection.delete_many({})
        results["delete"].append(time.time() - start_time)

        # Calcula estadísticas para cada operación
        return {
            operation: {
                "avg": statistics.mean(times),
                "min": min(times),
                "max": max(times)
            }
            for operation, times in results.items()
        }

    def test_neo4j_operations(self, data: List[Dict[str, Any]]):
        """
        Realiza pruebas de operaciones CRUD en Neo4j y mide los tiempos.
        Similar a test_mongodb_operations pero adaptado para Neo4j.
        
        Args:
            data: Lista de documentos para insertar
            
        Returns:
            Dict con estadísticas de tiempo para cada operación
        """
        results = {
            "create": [],
            "read": [],
            "update": [],
            "delete": []
        }

        # Prepara datos para Neo4j
        neo4j_data = self.prepare_neo4j_data(data)
        test_id = str(data[0]["_id"])

        with self.neo4j_driver.session() as session:
            # CREATE - Inserción uno por uno
            start_time = time.time()
            for item in neo4j_data:
                session.run(
                    "CREATE (n:TestNode) SET n = $props",
                    props=item
                )
            results["create"].append(time.time() - start_time)

            # READ - 100 consultas de lectura
            for _ in range(100):
                start_time = time.time()
                session.run(
                    "MATCH (n:TestNode) WHERE n._id = $id RETURN n",
                    id=test_id
                )
                results["read"].append(time.time() - start_time)

            # UPDATE - Actualización masiva
            start_time = time.time()
            session.run(
                "MATCH (n:TestNode) SET n.test_field = 'updated'"
            )
            results["update"].append(time.time() - start_time)

            # DELETE - Eliminación masiva
            start_time = time.time()
            session.run("MATCH (n:TestNode) DELETE n")
            results["delete"].append(time.time() - start_time)

        return {
            operation: {
                "avg": statistics.mean(times),
                "min": min(times),
                "max": max(times)
            }
            for operation, times in results.items()
        }

    def run_performance_test(self, csv_file_path: str, generate_graphs: bool = True):
        """
        Ejecuta el conjunto completo de pruebas de rendimiento.
        
        Args:
            csv_file_path: Ruta al archivo CSV con datos de prueba
            generate_graphs: Si se deben generar visualizaciones
            
        Returns:
            Dict con resultados de ambas bases de datos
        """
        try:
            print("Cargando datos del CSV...")
            data = self.load_csv_data(csv_file_path)
            
            print("Iniciando pruebas de MongoDB...")
            mongo_results = self.test_mongodb_operations(data)
            
            print("Iniciando pruebas de Neo4j...")
            neo4j_results = self.test_neo4j_operations(data)
            
            results = {
                "mongodb": mongo_results,
                "neo4j": neo4j_results
            }
            
            if generate_graphs:
                print("\nGenerando visualizaciones y reportes...")
                self.generate_visualizations(results)
                print("✓ Visualizaciones guardadas en el directorio 'resultados'")
            
            return results
            
        except Exception as e:
            print(f"Error durante la ejecución de las pruebas: {str(e)}")
            raise

    def generate_visualizations(self, results, output_dir="testing/resultados"):
        """
        Genera visualizaciones comparativas de los resultados de las pruebas.
        
        Args:
            results: Diccionario con resultados de las pruebas
            output_dir: Directorio donde guardar las visualizaciones
        """
        # Crea directorio si no existe
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Prepara datos para visualización
        data = []
        for db in ['mongodb', 'neo4j']:
            for operation, metrics in results[db].items():
                data.append({
                    'Database': db.upper(),
                    'Operation': operation.upper(),
                    'Average Time': metrics['avg'],
                    'Min Time': metrics['min'],
                    'Max Time': metrics['max']
                })
        
        df = pd.DataFrame(data)
        
        # 1. Gráfico de barras comparativo
        plt.figure(figsize=(12, 6))
        sns.barplot(x='Operation', y='Average Time', hue='Database', data=df)
        plt.title('Comparación de Tiempos de Operación entre MongoDB y Neo4j')
        plt.ylabel('Tiempo (segundos)')
        plt.yscale('log')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/comparacion_tiempos.png')
        plt.close()
        
        # 2. Tabla de resultados detallados
        tabla_comparativa = pd.pivot_table(
            df,
            values=['Average Time', 'Min Time', 'Max Time'],
            index=['Operation'],
            columns=['Database'],
            aggfunc='first'
        )
        
        # Formatea y guarda la tabla
        tabla_formateada = tabla_comparativa.round(4)
        tabla_formateada.to_csv(f'{output_dir}/resultados_detallados.csv')
        
        # 3. Gráfico de calor (heatmap)
        plt.figure(figsize=(10, 6))
        pivot_avg = df.pivot(index='Operation', columns='Database', values='Average Time')
        sns.heatmap(pivot_avg, annot=True, fmt='.4f', cmap='YlOrRd')
        plt.title('Heatmap de Tiempos Promedio por Operación')
        plt.tight_layout()
        plt.savefig(f'{output_dir}/heatmap_tiempos.png')
        plt.close()
        
        # 4. Gráfico de violín para distribución de tiempos
        plt.figure(figsize=(12, 6))
        df_melt = df.melt(
            id_vars=['Database', 'Operation'],
            value_vars=['Average Time', 'Min Time', 'Max Time'],
            var_name='Metric',
            value_name='Time'
        )
        sns.violinplot(x='Operation', y='Time', hue='Database', data=df_melt)
        plt.title('Distribución de Tiempos por Operación')
        plt.ylabel('Tiempo (segundos)')
        plt.yscale('log')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(f'{output_dir}/distribucion_tiempos.png')
        plt.close()

        return {
            'dataframe': df,
            'tabla_comparativa': tabla_comparativa
        }

    def close_connections(self):
        """
        Cierra las conexiones a ambas bases de datos.
        Importante llamar a este método al finalizar las pruebas.
        """
        self.mongo_client.close()
        self.neo4j_driver.close()

# Bloque principal de ejecución
if __name__ == "__main__":
    try:
        # Crea instancia del tester
        tester = DatabaseTester()
        # Ejecuta las pruebas con el archivo CSV especificado
        results = tester.run_performance_test("data/netflix_disney.csv")
        
        # Imprime resultados
        print("\nResultados de las pruebas:")
        print("\nMongoDB:")
        for operation, metrics in results["mongodb"].items():
            print(f"{operation.upper()}:")
            print(f"  Promedio: {metrics['avg']:.4f} segundos")
            print(f"  Mínimo: {metrics['min']:.4f} segundos")
            print(f"  Máximo: {metrics['max']:.4f} segundos")
        
        print("\nNeo4j:")
        for operation, metrics in results["neo4j"].items():
            print(f"{operation.upper()}:")
            print(f"  Promedio: {metrics['avg']:.4f} segundos")
            print(f"  Mínimo: {metrics['min']:.4f} segundos")
            print(f"  Máximo: {metrics['max']:.4f} segundos")
    
    except Exception as e:
        print(f"Error en la ejecución del programa: {str(e)}")
    finally:
        # Asegura que las conexiones se cierren incluso si hay errores
        tester.close_connections()