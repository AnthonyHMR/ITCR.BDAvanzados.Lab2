# MovieDB-NoSQL

Proyecto que compara el rendimiento de MongoDB y Neo4j en un sistema de gestión de películas y series. Evalúa operaciones CRUD usando datos de IMDb y Netflix.

## Índice
- [Escenario](#escenario)
- [Instalación](#instalación)
- [Pruebas](#pruebas) 
- [Desarrolladores](#desarrolladores)

## Escenario
El proyecto utiliza datos de entretenimiento de Kaggle:
- [Netflix Shows Dataset](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- [Disney+ Movies Dataset](https://www.kaggle.com/datasets/shivamb/disney-movies-and-tv-shows)

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2.git
cd ITCR.BDAvanzados.Lab2
```

2. Instalar las dependencias mediante pip:

```bash
pip install -r requirements.txt
```

3. Configurar bases de datos:

<div align="center">
  <a href="docs/mongodb_guide.md">
    <img src="docs/pics/logo/mongoDB_logo.png" width="450" alt="MongoDB Logo">
    <br>
    <em>Guía de instalación MongoDB</em>
  </a>
<br><br>
  <a href="docs/neo4j_guide.md">
    <img src="docs/pics/logo/neo4j_logo.png" width="400" alt="Neo4j Logo">
    <br>
    <em>Guía de instalación Neo4j</em>
  </a>
</div>


## Ejecución de Pruebas

1. Asegúrate de que las bases de datos estén corriendo.

2. Ejecuta el script de python en `testing/databaseTester.py`

3. Los resultados se guardan en `testing/results`

## Desarrolladores

* **Anthony Montero** - [AnthonyHMR](https://github.com/issolis)
* **Kun Zheng** - [kunZhen](https://github.com/kunZhen)