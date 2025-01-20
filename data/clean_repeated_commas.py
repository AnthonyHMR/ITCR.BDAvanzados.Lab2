import csv
import re

def clean_repeated_commas(input_file, output_file):
    """
    Limpia un archivo CSV eliminando comas repetidas.
    
    Args:
        input_file (str): Ruta del archivo CSV de entrada
        output_file (str): Ruta donde se guardará el archivo CSV limpio
    """
    try:
        # Leer el archivo original
        with open(input_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Eliminar comas repetidas usando expresiones regulares
        # Reemplaza dos o más comas consecutivas por una sola coma
        cleaned_content = re.sub(r',{2,}', ',', content)
        
        # Guardar el contenido limpio en un nuevo archivo
        with open(output_file, 'w', encoding='utf-8', newline='') as file:
            file.write(cleaned_content)
            
        print(f"Archivo limpiado exitosamente y guardado en: {output_file}")
        
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {input_file}")
    except Exception as e:
        print(f"Error inesperado: {str(e)}")

# Ejemplo de uso
if __name__ == "__main__":
    input_file = "data/disney_plus_titles.csv"
    output_file = "data/disney_plus.csv"
    clean_repeated_commas(input_file, output_file)