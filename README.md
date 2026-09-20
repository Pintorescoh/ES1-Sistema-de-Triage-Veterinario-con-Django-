## ⚙️ Instrucciones de Despliegue (Prueba de Clon Limpio)

Para ejecutar este proyecto desde cero en un entorno local, sigue estos pasos:

**1. Clonar el repositorio y crear el entorno virtual:**
```bash
git clone -b eva2 <URL_DE_TU_REPOSITORIO>
cd <NOMBRE_DE_TU_CARPETA>
python -m venv venv
**2. Activar el entorno virtual:**
```bash
Windows: .\venv\Scripts\activate

Mac/Linux: source venv/bin/activate

**3. Instalar las dependencias:**
```bash
pip install -r requirements.txt

**4. Configurar variables de entorno:**
```bash
Copia el archivo de ejemplo y renómbralo para crear tu entorno local:
Copia .env.example y renómbralo a .env
Abre el archivo .env y asigna valores válidos (ej. SECRET_KEY=clave_segura y DEBUG=True).

**5. Generar la base de datos (SQLite):**
```bash
python manage.py migrate

**6. Configurar Roles y Usuarios base:**
Ejecuta el script de poblamiento para crear automáticamente los grupos de seguridad y un usuario de prueba para cada uno (la contraseña por defecto para todos es Inacap2026!):
```bash
python setup_roles.py

**7. Levantar el servidor:**
```bash
python manage.py runserver

El sistema estará disponible en [http://127.0.0.1:8000/](http://127.0.0.1:8000/).