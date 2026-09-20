# Proyecto EVA 2: Sistema de Triage Clínico 🏥

Sistema web desarrollado en Django para la recepción y evaluación inicial de pacientes en un entorno clínico. El sistema utiliza una base de datos SQLite y se enfoca en la automatización del cálculo de gravedad y la seguridad de los datos.

## 🚀 Novedades y Características de la EVA 2

En esta iteración se implementaron mejoras significativas en la arquitectura, seguridad y usabilidad del sistema:

*   **Automatización de Reglas de Negocio (Triage):** Se trasladó la lógica de evaluación (función `decidir()`) directamente al método `save()` del modelo `Paciente`. Esto garantiza que el sistema asigne automáticamente el código de gravedad (Rojo, Amarillo o Verde) basado en el dolor y la respiración, asegurando la integridad de los datos tanto en la interfaz de usuario como en el panel de administración.
*   **Control de Acceso Basado en Roles (RBAC):** Se implementó seguridad a nivel de vistas. Las operaciones CRUD están restringidas según tres niveles de grupos: `admin`, `normal` y `viewer`. 
*   **Gestión de Entornos y Seguridad:** Aislamiento de variables sensibles (`SECRET_KEY`, `DEBUG`) utilizando `python-dotenv`. El repositorio está saneado (sin rastros de `.env` en el caché de Git) siguiendo las mejores prácticas de versionamiento.
*   **Feedback de Interfaz:** Integración del framework de mensajes de Django para proveer retroalimentación visual al usuario cuando intenta realizar acciones sin los permisos correspondientes.
*   **Optimización de Dependencias:** Limpieza del entorno virtual y configuración de un archivo `requirements.txt` estandarizado en formato UTF-8 para máxima compatibilidad multiplataforma.

---

## ⚙️ Instrucciones de Despliegue (Prueba de Clon Limpio)

Para ejecutar este proyecto desde cero en un entorno local, sigue estos pasos:

**1. Clonar el repositorio y crear el entorno virtual:**
```bash
git clone -b eva2 <URL_DE_TU_REPOSITORIO>
cd <NOMBRE_DE_TU_CARPETA>
python -m venv venv

**2. Activar el entorno virtual:

Windows: .\venv\Scripts\activate

Mac/Linux: source venv/bin/activate

**3. Instalar las dependencias:
pip install -r requirements.txt

**4. Configurar variables de entorno:
Copia el archivo de ejemplo y renómbralo para crear tu entorno local:

Copia .env.example y renómbralo a .env

Abre el archivo .env y asigna valores válidos (ej. SECRET_KEY=clave_segura y DEBUG=True).

**5. Generar la base de datos (SQLite):
python manage.py migrate

**6. Configurar Roles y Usuarios base:
Ejecuta el script de poblamiento para crear automáticamente los grupos de seguridad y un usuario de prueba para cada uno (la contraseña por defecto para todos es Inacap2026!):

**7. Levantar el servidor:
python manage.py runserver

El sistema estará disponible en http://127.0.0.1:8000/.