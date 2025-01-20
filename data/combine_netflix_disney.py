import pandas as pd
import re

def combine_netflix_files(file1_path, file2_path, output_path):
    """
    Combina dos archivos CSV de Netflix y ajusta los show_ids para que sean secuenciales.
    
    Args:
        file1_path (str): Ruta del primer archivo CSV
        file2_path (str): Ruta del segundo archivo CSV
        output_path (str): Ruta donde se guardará el archivo combinado
    """
    # Leer los archivos CSV
    df1 = pd.read_csv(file1_path)
    df2 = pd.read_csv(file2_path)
    
    # Encontrar el último show_id del primer archivo
    last_id = 0
    for idx in df1['show_id']:
        # Extraer el número del show_id (asumiendo formato 's1', 's2', etc.)
        num = int(re.findall(r'\d+', idx)[0])
        last_id = max(last_id, num)
    
    # Actualizar los show_ids del segundo archivo
    new_ids = []
    for i in range(len(df2)):
        last_id += 1
        new_ids.append(f's{last_id}')
    
    # Asignar los nuevos IDs al segundo DataFrame
    df2['show_id'] = new_ids
    
    # Combinar los DataFrames
    df_combined = pd.concat([df1, df2], ignore_index=True)
    
    # Guardar el resultado
    df_combined.to_csv(output_path, index=False)
    
    print(f"Archivos combinados exitosamente. Resultado guardado en: {output_path}")

# Ejemplo de uso
if __name__ == "__main__":
    file1 = "data/netflix.csv"
    file2 = "data/disney_plus.csv"
    output = "netflix_combined.csv"
    
    combine_netflix_files(file1, file2, output)