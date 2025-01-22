import time
import csv
import pymongo
from neo4j import GraphDatabase
import statistics
from typing import List, Dict, Any
from bson import ObjectId

class DatabaseTester:
    def __init__(self):
        # MongoDB connection
        self.mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
        self.mongo_db = self.mongo_client["performance_test"]
        self.mongo_collection = self.mongo_db["test_collection"]
        
        # Neo4j connection
        self.neo4j_driver = GraphDatabase.driver("bolt://localhost:7687", 
                                               auth=("neo4j", "mango2016"))

    def load_csv_data(self, file_path: str) -> List[Dict[str, Any]]:
        """Load data from CSV file"""
        encodings = ['utf-8', 'latin-1', 'iso-8859-1', 'cp1252']
        
        for encoding in encodings:
            try:
                data = []
                with open(file_path, 'r', encoding=encoding) as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Add ObjectId for MongoDB
                        row['_id'] = ObjectId()
                        data.append(row)
                return data
            except UnicodeDecodeError:
                continue
        
        raise ValueError(f"No se pudo leer el archivo con ninguna de las codificaciones: {encodings}")

    def prepare_neo4j_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Convert MongoDB data format to Neo4j compatible format"""
        neo4j_data = []
        for item in data:
            # Create a new dict with converted data
            neo4j_item = {}
            for key, value in item.items():
                if isinstance(value, ObjectId):
                    # Convert ObjectId to string for Neo4j
                    neo4j_item[key] = str(value)
                else:
                    neo4j_item[key] = value
            neo4j_data.append(neo4j_item)
        return neo4j_data

    def test_mongodb_operations(self, data: List[Dict[str, Any]]):
        """Test MongoDB CRUD operations"""
        results = {
            "create": [],
            "read": [],
            "update": [],
            "delete": []
        }

        # CREATE - Bulk Insert
        start_time = time.time()
        self.mongo_collection.insert_many(data)
        results["create"].append(time.time() - start_time)

        # READ - Query con diferentes filtros
        test_id = data[0]["_id"]  # Guardamos el ID para las pruebas
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

        return {
            operation: {
                "avg": statistics.mean(times),
                "min": min(times),
                "max": max(times)
            }
            for operation, times in results.items()
        }

    def test_neo4j_operations(self, data: List[Dict[str, Any]]):
        """Test Neo4j CRUD operations"""
        results = {
            "create": [],
            "read": [],
            "update": [],
            "delete": []
        }

        # Convertir datos para Neo4j
        neo4j_data = self.prepare_neo4j_data(data)
        test_id = str(data[0]["_id"])  # Convertimos el ObjectId a string para las pruebas

        with self.neo4j_driver.session() as session:
            # CREATE - Bulk Insert
            start_time = time.time()
            for item in neo4j_data:
                session.run(
                    "CREATE (n:TestNode) SET n = $props",
                    props=item
                )
            results["create"].append(time.time() - start_time)

            # READ - Queries
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

    def run_performance_test(self, csv_file_path: str):
        """Ejecutar pruebas de rendimiento completas"""
        try:
            print("Cargando datos del CSV...")
            data = self.load_csv_data(csv_file_path)
            
            print("Iniciando pruebas de MongoDB...")
            mongo_results = self.test_mongodb_operations(data)
            
            print("Iniciando pruebas de Neo4j...")
            neo4j_results = self.test_neo4j_operations(data)
            
            return {
                "mongodb": mongo_results,
                "neo4j": neo4j_results
            }
        except Exception as e:
            print(f"Error durante la ejecución de las pruebas: {str(e)}")
            raise

    def close_connections(self):
        """Cerrar conexiones a las bases de datos"""
        self.mongo_client.close()
        self.neo4j_driver.close()

# Ejemplo de uso
if __name__ == "__main__":
    try:
        tester = DatabaseTester()
        results = tester.run_performance_test("data/netflix_disney.csv")
        
        print("\nResultados de las pruebas:".encode('utf-8').decode('utf-8'))
        print("\nMongoDB:")
        for operation, metrics in results["mongodb"].items():
            print(f"{operation.upper()}:")
            print(f"  Promedio: {metrics['avg']:.4f} segundos".encode('utf-8').decode('utf-8'))
            print(f"  Mínimo: {metrics['min']:.4f} segundos".encode('utf-8').decode('utf-8'))
            print(f"  Máximo: {metrics['max']:.4f} segundos".encode('utf-8').decode('utf-8'))
        
        print("\nNeo4j:")
        for operation, metrics in results["neo4j"].items():
            print(f"{operation.upper()}:")
            print(f"  Promedio: {metrics['avg']:.4f} segundos".encode('utf-8').decode('utf-8'))
            print(f"  Mínimo: {metrics['min']:.4f} segundos".encode('utf-8').decode('utf-8'))
            print(f"  Máximo: {metrics['max']:.4f} segundos".encode('utf-8').decode('utf-8'))
    
    except Exception as e:
        print(f"Error en la ejecución del programa: {str(e)}")
    finally:
        tester.close_connections()