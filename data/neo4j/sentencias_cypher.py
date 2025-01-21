import csv

# Nombre del CSV de entrada
INPUT_CSV = "data/netflix_disney.csv"
# Nombre del archivo .cypher de salida
OUTPUT_CYPHER = "data/import_neo4j.cypher"

def limpiar_campo(valor):
    """
    Limpia o transforma un valor para que sea seguro/adecuado
    para usar en la sentencia Cypher entre comillas simples.
    Reemplaza comillas simples por comillas dobles, etc.
    """
    if valor is None:
        return ""
    # Aseguramos que sea string
    valor_str = str(valor)
    # Escapar comillas simples para no romper el Cypher
    valor_str = valor_str.replace("'", "\\'")
    return valor_str.strip()

def generar_sentencias_cypher(row):
    """
    A partir de una fila (row) del CSV, devuelve una lista de sentencias Cypher.
    Se usan sentencias MERGE para:
      - Nodos de la obra (Movie o TVShow).
      - Nodos de director(es).
      - Nodos de actores.
      - Nodos de países.
      - Nodos de categoría(s) (listed_in).
      - Relaciones correspondientes.
    """
    # Extraer campos relevantes (asegurarnos de limpiar los valores).
    show_id    = limpiar_campo(row["show_id"])
    tipo       = limpiar_campo(row["type"])  # Movie o TV Show
    title      = limpiar_campo(row["title"])
    directors  = limpiar_campo(row["director"])
    cast       = limpiar_campo(row["cast"])
    country    = limpiar_campo(row["country"])
    date_added = limpiar_campo(row["date_added"])
    r_year     = limpiar_campo(row["release_year"])
    rating     = limpiar_campo(row["rating"])
    duration   = limpiar_campo(row["duration"])
    categories = limpiar_campo(row["listed_in"])
    description= limpiar_campo(row["description"])
    
    # Definimos la etiqueta principal de la obra
    # Podrías usar una sola etiqueta :Title con una propiedad type,
    # pero aquí se ejemplifica con dos etiquetas distintas.
    if tipo == "Movie":
        label_obra = "Movie"
    else:
        label_obra = "TVShow"

    cypher_statements = []

    # 1) MERGE del nodo principal (Movie o TVShow).
    #    Se utiliza `show_id` como identificador único. 
    sentencia_obra = f"""
MERGE (obra:{label_obra} {{ show_id: '{show_id}' }})
ON CREATE SET obra.title = '{title}',
              obra.date_added = '{date_added}',
              obra.release_year = '{r_year}',
              obra.rating = '{rating}',
              obra.duration = '{duration}',
              obra.description = '{description}' 
    """
    cypher_statements.append(sentencia_obra)

    # 2) Directores (puede haber más de uno separados por coma).
    #    Crearemos nodos :Director y relación :DIRECTED_BY.
    if directors:
        # A veces en estos datasets, los directores se separan por comas
        # (cuando hay varios directores). Si este no fuera tu caso, ajusta la lógica.
        # Observa si Kaggle trae varios directores separados por una sola coma o algo distinto.
        lista_directores = [d.strip() for d in directors.split(",") if d.strip()]
        for d in lista_directores:
            d_escapado = limpiar_campo(d)
            # MERGE del director
            dir_stmt = f"""
MERGE (dir:Director {{ name: '{d_escapado}' }})
MERGE (obra)-[:DIRECTED_BY]->(dir)
            """
            cypher_statements.append(dir_stmt)

    # 3) Actores (columna cast). Mismo procedimiento con :Actor y relación :HAS_ACTOR.
    if cast:
        # separador por comas
        lista_actores = [a.strip() for a in cast.split(",") if a.strip()]
        for actor_name in lista_actores:
            actor_escapado = limpiar_campo(actor_name)
            actor_stmt = f"""
MERGE (act:Actor {{ name: '{actor_escapado}' }})
MERGE (obra)-[:HAS_ACTOR]->(act)
            """
            cypher_statements.append(actor_stmt)

    # 4) Países (columna country). 
    #    Por convención, un show puede tener varios países. Separamos por comas.
    if country:
        lista_paises = [c.strip() for c in country.split(",") if c.strip()]
        for pais in lista_paises:
            pais_escapado = limpiar_campo(pais)
            country_stmt = f"""
MERGE (co:Country {{ name: '{pais_escapado}' }})
MERGE (obra)-[:PRODUCED_IN]->(co)
            """
            cypher_statements.append(country_stmt)

    # 5) Categorías (columna listed_in). Suelen venir separadas por comas.
    #    Ejemplo: "Documentaries, Music & Musicals"
    if categories:
        lista_cat = [cat.strip() for cat in categories.split(",") if cat.strip()]
        for cat in lista_cat:
            cat_escapado = limpiar_campo(cat)
            cat_stmt = f"""
MERGE (categoria:Category {{ name: '{cat_escapado}' }})
MERGE (obra)-[:IN_CATEGORY]->(categoria)
            """
            cypher_statements.append(cat_stmt)

    return cypher_statements


def main():
    with open(INPUT_CSV, mode="r", encoding="utf-8") as f_in, \
         open(OUTPUT_CYPHER, mode="w", encoding="utf-8") as f_out:
        
        reader = csv.DictReader(f_in)
        
        # Cabecera del archivo Cypher
        # Puedes usar 'USING PERIODIC COMMIT' si planeas cargarlo en bloque.
        # Lo siguiente es opcional, pero recomendado para CSV muy grandes:
        f_out.write("// Carga de datos en Neo4j\n")
        f_out.write("BEGIN;\n\n")
        
        for idx, row in enumerate(reader, start=1):
            statements = generar_sentencias_cypher(row)
            for st in statements:
                # Escribimos cada sentencia. 
                f_out.write(st + ";\n")  # Cada sentencia con punto y coma
                
            # Para evitar archivos gigantescos, podrías hacer commits parciales
            # cada cierto número de filas, por ejemplo cada 1000, 5000, etc.
            # if idx % 1000 == 0:
            #     f_out.write("COMMIT;\nBEGIN;\n")
        
        # Finalizamos
        f_out.write("\nCOMMIT;\n")

if __name__ == "__main__":
    main()
