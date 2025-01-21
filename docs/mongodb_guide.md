# Guía de Instalación de MongoDB en Windows 10

<p align="center">
  <a href="https://github.com/AnthonyHMR/ITCR.BDAvanzados.Lab2/blob/main/docs/mongodb_guide.md" target="blank"><img src="pics/logo/mongoDB_logo.png" width="400" alt="mongoDB_logo" /></a>
</p>

## Paso 1: Descargar MongoDB
1. **Accede a la página oficial** de MongoDB: [Descargar MongoDB](https://www.mongodb.com/try/download/community).
2. **Selecciona las opciones de descarga**:
   - **Versión**: Elige la última versión estable.
   - **Sistema operativo**: Selecciona `Windows`.
   - **Tipo de paquete**: Selecciona `MSI`.
3. Haz clic en **Download** y espera a que se descargue el archivo `.msi`.

---

## Paso 2: Instalar MongoDB
1. Ejecuta el archivo `.msi` descargado.
2. Sigue los pasos del instalador:
   - Acepta los términos de licencia.
   - Selecciona `Complete` como tipo de instalación.
3. Marca la opción **Install MongoDB as a Service** durante la instalación.
4. Finaliza la instalación.

---

## Paso 3: Configurar las Variables de Entorno
1. Localiza el directorio donde se instaló MongoDB, por defecto:
C:\Program Files\MongoDB\Server\<versión>\bin
> Reemplaza `<versión>` con la versión instalada, como `6.0`.
2. Copia la ruta completa del directorio `bin`.

### Agregar MongoDB al `PATH`:
1. Haz clic derecho en **Este equipo** o **Mi PC** y selecciona **Propiedades**.
2. Ve a **Configuración avanzada del sistema** > **Variables de entorno**.
3. En **Variables del sistema**, selecciona `Path` y haz clic en **Editar**.
4. Haz clic en **Nuevo** y pega la ruta del directorio `bin`.
5. Presiona **Aceptar** en todas las ventanas.

---

## Paso 4: Verificar la Instalación
1. Abre **Símbolo del sistema (CMD)** o **PowerShell**.
2. Ejecuta el siguiente comando para verificar MongoDB:
mongod --version

