# Guía de Configuración para Importar un Archivo .csv en MongoDB

## Requisitos Previos

* MongoDB y MongoDB Compass instalados
* Archivo [netflix_disney.csv](https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/data/netflix_disney.csv) descargado
* Acceso al sistema con permisos de administrador

## Pasos de Configuración

### 1. Iniciar el Servidor de MongoDB

1. Abre una terminal o el símbolo del sistema (CMD).
2. Inicia el servidor ejecutando el comando:

   ```bash
   mongod
   ```

4. Para verificar que el servidor esté corriendo correctamente, abre otro terminal y ejecuta el comando:

   ```bash
   mongosh
   ```

Deberías ver un mensaje indicando que el servidor está escuchando en el puerto 27017 (por defecto).

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/mongodb_config.md" target="blank"><img src="pics/mongodb/mongodb_config/mongosh.jpg" width="500" alt="Mongosh" /></a>
</p>

---

### 1. Iniciar MongoDB Compass

1. Abre MongoDB Compass desde tu sistema.
2. Crea una nueva conexión para conectarte al servidor local utilizando la URI de conexión correspondiente y dale un nombre (por ejemplo, `Laboratorio_2`).

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/mongodb_config.md" target="blank"><img src="pics/mongodb/mongodb_config/mongodb_compass_connection.jpg" width="500" alt="MongoDB Compass" /></a>
</p>

3. Haz clic en `Save & Connect`.
---

### 2. Crear una Nueva Base de Datos (si es necesario)

1. En la conexión creada anteriormente, haz clic en el botón `Create Database`.
2. Ingresa un nombre para la base de datos (por ejemplo, `MovieDB`) y una colección inicial (por ejemplo, `Entertainment`).
3. Haz clic en `Create Database`.

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/mongodb_config.md" target="blank"><img src="pics/mongodb/mongodb_config/create_database.jpg" width="500" alt="Crear Base de Datos" /></a>
</p>

---

### 3. Navegar a la Herramienta de Importación

1. Ve a la colección creada anteriormente.
2. Haz clic en el botón `Add Data` y selecciona la opción `Import JSON or CSV file`.

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/mongodb_config.md" target="blank"><img src="pics/mongodb/mongodb_config/import_data.jpg" width="500" alt="Importar Datos" /></a>
</p>

---

### 4. Seleccionar el Archivo .csv

1. En el explorador de archivos, navega hasta la ubicación del archivo [netflix_disney.csv](https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/data/netflix_disney.csv)
2. Selecciona el archivo y haz clic en `Import`.

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/mongodb_config.md" target="blank"><img src="pics/mongodb/mongodb_config/select_csv_file.jpg" width="500" alt="Seleccionar Archivo CSV" /></a>
</p>

---

### 5. Verificar la Importación

1. Una vez completada la importación, MongoDB Compass mostrará un mensaje de confirmación.
2. Ve a la colección y utiliza el panel de exploración para revisar los datos importados.

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/mongodb_config.md" target="blank"><img src="pics/mongodb/mongodb_config/import_success.jpg" width="500" alt="Importación Exitosa" /></a>
</p>

---

### 7. Consultar los Datos Importados

Puedes usar el siguiente comando en la consola de MongoDB para verificar los datos:

```javascript
use MovieDB;
db.Entertainment.find().pretty();
```

Esto mostrará los documentos importados de forma estructurada.

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/mongodb_config.md" target="blank"><img src="pics/mongodb/mongodb_config/data_verified.jpg" width="500" alt="Datos Verificados" /></a>
</p>

---

## Solución de Problemas Comunes

* **Error al importar:** Verifica que el archivo .csv esté en la ubicación correcta.
* **Problemas de conexión:** Asegúrate de que MongoDB esté en ejecución y que las credenciales sean correctas.
* **Campos mal mapeados:** Revisa que al momento de importar el documento .CSV, la opción de delimitador esté en `Comma`.
