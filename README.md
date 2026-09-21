# Proyecto EVA 2: Sistema de Triage Clínico 🏥

Sistema web desarrollado en Django para la recepción y evaluación inicial de pacientes en un entorno clínico. Utiliza SQLite y automatiza el cálculo de gravedad mediante la regla de triage original.

## 🚀 Características

* **Regla de triage:** `decidir()` se mantiene en `solucion.py` y el modelo calcula automáticamente la gravedad al guardar un paciente.
* **Roles y seguridad:** las operaciones CRUD están restringidas mediante los grupos `admin`, `normal` y `viewer`. El administrador Django también está protegido por rol.
* **Configuración segura:** las variables `SECRET_KEY`, `DEBUG` y `USERS_PASSWORD` se gestionan mediante `python-dotenv`.
* **Borrado lógico:** los pacientes eliminados se conservan como historial.
* **Interfaz:** formularios y lista de pacientes con validaciones, mensajes y protección CSRF.

## ⚙️ Instrucciones de despliegue

Para ejecutar el proyecto desde cero:

1. Clonar el repositorio y crear el entorno virtual:

```powershell
git clone <URL_DEL_REPOSITORIO>
cd miproyecto
python -m venv venv
```

2. Activar el entorno virtual:

```powershell
.\venv\Scripts\activate
```

3. Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

4. Crear el archivo `.env` a partir de `.env.example` y asignar valores para `SECRET_KEY`, `DEBUG` y `USERS_PASSWORD`.

5. Crear las tablas de SQLite:

```powershell
python manage.py migrate
```

6. Crear los grupos y usuarios base:

```powershell
python setup_roles.py
```

Si `USERS_PASSWORD` no está en `.env`, el script la solicitará de forma oculta en la terminal.

7. Levantar el servidor:

```powershell
python manage.py runserver
```

La aplicación estará disponible en http://127.0.0.1:8000/login/.

El panel de administración estará disponible en http://127.0.0.1:8000/admin/ para el usuario del grupo `admin`.
