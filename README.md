# MovieDB-NoSQL

Este proyecto compara el rendimiento de dos bases de datos NoSQL, MongoDB y Neo4j, en un escenario inspirado en sistemas de gestión de películas y series como IMDb o Netflix. El objetivo principal es evaluar las capacidades de cada base de datos para manejar operaciones CRUD (Create, Read, Update, Delete) en un ambiente controlado, utilizando un conjunto de datos significativo y consultas representativas.

## Índice
- [Escenario de Pruebas](#escenario-de-pruebas)
- [Instrucciones de Uso](#instrucciones-de-uso)
- [Resultados Esperados](#resultados-esperados)
- [Ejecución de Pruebas](#ejecucion-de-pruebas)
- [Desarrolladores](#desarrolladores)

# Escenario de Pruebas
El proyecto utiliza un modelo de datos basado en la industria del entretenimiento. Cada base de datos implementa un esquema adaptado a sus características únicas:

- MongoDB: Modelo documental con documentos anidados para películas, directores, actores, reviews y premios.
- Neo4j: Modelo de grafos con nodos y relaciones para representar películas, directores, actores, géneros y premios.

# Instrucciones de Uso

## Requisitos Previos

- Docker y Docker Compose instalados (opcional).
- Python, Node.js o Java (según los scripts utilizados para las pruebas).
- Acceso a MongoDB y Neo4j.

## Instalación

1. Clona este repositorio:
```bash
git clone https://github.com/tu_usuario/MovieDB-NoSQL-Benchmark.git
cd MovieDB-NoSQL-Benchmark
```

2. Sigue las instrucciones específicas:

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/pics/mongoDB_logo.png" target="blank"><img src="docs/pics/mongoDB_logo.png" width="525" alt="mongoDB_logo" /></a>
</p>

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/pics/neo4j_logo.png" target="blank"><img src="docs/pics/neo4j_logo.png" width="525" alt="neo4j_logo.png" /></a>
</p>

- MongoDB: `docs/mongodb.md`
- Neo4j: `docs/neo4j.md`

3. Genera los datos de prueba:
```bash
python generate_data.py
```

# Ejecución de Pruebas

1. Asegúrate de que las bases de datos estén corriendo.

2. Ejecuta los scripts de prueba:
```bash
python run_tests.py
```

3. Los resultados se guardarán en la carpeta `results`

# Resultados Esperados

Este proyecto espera identificar:

- La base de datos más eficiente en operaciones CRUD específicas
- Las fortalezas de cada sistema en términos de modelado de datos y consultas
- Áreas de mejora y casos de uso ideales para cada tecnología

# Desarrolladores

* **Anthony Montero** - [AnthonyHMR](https://github.com/issolis)
* **Kun Zheng** - [kunZhen](https://github.com/kunZhen)