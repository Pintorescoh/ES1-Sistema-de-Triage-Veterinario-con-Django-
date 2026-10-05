# Proyecto ES3: API RESTful de Triage Clínico 🏥

Sistema Django para la recepción y evaluación inicial de pacientes. La ES3 agrega una **API RESTful con Django REST Framework** sobre los mismos modelos y la misma base de datos de la ES2. Las pantallas HTML de la ES2 siguen funcionando igual: la API vive en paralelo, bajo `/api/`.

## 🚀 Características

* **Regla de triage:** `decidir()` se mantiene en `solucion.py` y el modelo calcula la gravedad al guardar un paciente, venga desde el HTML, el admin o la API.
* **API REST (ES3):** CRUD completo de pacientes en `/api/pacientes/` con `ModelViewSet` y `DefaultRouter`.
* **Autenticación JWT (ES3):** tokens con expiración y refresco (`djangorestframework-simplejwt`), con límite de intentos de login.
* **Roles y seguridad:** grupos `admin`, `normal` y `viewer`, con la misma regla en las pantallas HTML y en la API.
* **Configuración segura:** `SECRET_KEY`, `DEBUG` y `USERS_PASSWORD` se gestionan con `python-dotenv`.
* **Borrado lógico:** los pacientes eliminados se conservan como historial, también al borrar desde la API.

## ⚙️ Instrucciones de despliegue

Requisito: Python 3.12 o superior (Django 6.1). El proyecto se probó con Python 3.14.

1. Crear el entorno virtual dentro de la carpeta del proyecto:

```powershell
cd ES3_PintoJuan
python -m venv venv
.\venv\Scripts\activate
```

2. Instalar las dependencias:

```powershell
pip install -r requirements.txt
```

3. Crear el archivo `.env` a partir de `.env.example` y asignar valores para `SECRET_KEY`, `DEBUG` y `USERS_PASSWORD`.

4. Crear las tablas de SQLite:

```powershell
python manage.py migrate
```

5. Crear los grupos y usuarios base (`usuario_admin`, `usuario_normal`, `usuario_viewer`):

```powershell
python setup_roles.py
```

Si `USERS_PASSWORD` no está en `.env`, el script la solicitará de forma oculta en la terminal.

6. Levantar el servidor:

```powershell
python manage.py runserver
```

| Interfaz | URL |
|---|---|
| Pantallas HTML (ES2) | http://127.0.0.1:8000/login/ |
| Panel de administración | http://127.0.0.1:8000/admin/ |
| API REST (ES3) | http://127.0.0.1:8000/api/ |
| Documentación Swagger (solo con `DEBUG=True`) | http://127.0.0.1:8000/api/docs/ |

## 🔌 API REST

### Cómo autenticarse

La API usa **JWT**. Primero se pide un par de tokens con un usuario del sistema y luego se manda el token `access` en la cabecera `Authorization` de **cada** petición.

> ⚠️ La cabecera usa el prefijo **`Bearer`**, no `Token`. Con `Authorization: Token ...` la API responde 401.

Los comandos están en una sola línea y envían datos de formulario, así funcionan igual en PowerShell y en bash. En PowerShell hay que escribir **`curl.exe`**, porque `curl` a secas es un alias de `Invoke-WebRequest`.

```powershell
# 1. Pedir los tokens
curl.exe -X POST -d "username=usuario_normal&password=TU_CLAVE" http://127.0.0.1:8000/api/token/
# respuesta: {"refresh":"eyJhbGciOi...","access":"eyJhbGciOi..."}

# 2. Usar el access en cada petición
curl.exe -H "Authorization: Bearer eyJhbGciOi..." http://127.0.0.1:8000/api/pacientes/

# 3. Crear un paciente
curl.exe -X POST -H "Authorization: Bearer eyJhbGciOi..." -d "nombre=Ana&dificultad_respiracion=No&dolor=7" http://127.0.0.1:8000/api/pacientes/

# 4. Cuando el access caduque (30 min), pedir uno nuevo con el refresh
curl.exe -X POST -d "refresh=eyJhbGciOi..." http://127.0.0.1:8000/api/token/refresh/
```

> La API también acepta JSON (`-H "Content-Type: application/json"`). En Windows PowerShell 5.1 hay que mandarlo desde un archivo (`--data-binary "@cuerpo.json"`), porque PowerShell elimina las comillas dobles internas de `'{"nombre": "Ana"}'` y el JSON llega roto (400). Así lo hace el script de `pruebas/`. Otra opción es probar desde Swagger.

### Endpoints

| Verbo | Endpoint | Qué hace | Roles | Respuesta OK |
|---|---|---|---|---|
| POST | `/api/token/` | Entrega `access` y `refresh` a cambio de usuario y contraseña | Público (máx. 5 intentos/min) | 200 |
| POST | `/api/token/refresh/` | Entrega un `access` nuevo a cambio del `refresh` | Público | 200 |
| GET | `/api/pacientes/` | Lista los pacientes activos, paginados de a 10 | admin, normal, viewer | 200 |
| GET | `/api/pacientes/?gravedad=Rojo` | Filtra por gravedad (`Rojo`, `Amarillo`, `Verde`) | admin, normal, viewer | 200 |
| GET | `/api/pacientes/?page=2` | Siguiente página de resultados | admin, normal, viewer | 200 |
| POST | `/api/pacientes/` | Crea un paciente; la gravedad la calcula la regla | admin, normal | 201 |
| GET | `/api/pacientes/{id}/` | Muestra un paciente | admin, normal, viewer | 200 |
| PUT | `/api/pacientes/{id}/` | Reemplaza todos los datos del paciente | admin, normal | 200 |
| PATCH | `/api/pacientes/{id}/` | Cambia solo los campos enviados | admin, normal | 200 |
| DELETE | `/api/pacientes/{id}/` | Borrado lógico del paciente | admin | 204 |

Los roles son los grupos de la ES2. El superusuario de Django puede hacer todas las operaciones.

Para probar desde Swagger (`/api/docs/`): pedir el token en `POST /api/token/` con "Try it out", copiar el `access`, pegarlo en el botón **Authorize** y probar el resto de los endpoints.

### Campos del recurso `paciente`

| Campo | Tipo | Lectura / escritura | Regla |
|---|---|---|---|
| `id` | entero | solo lectura | Identificador para editar o borrar |
| `nombre` | texto (máx. 100) | lectura y escritura | Obligatorio, no puede ser solo números |
| `dificultad_respiracion` | `"Sí"` / `"No"` | lectura y escritura | Obligatorio |
| `dolor` | entero | lectura y escritura | Obligatorio, entre 0 y 10 |
| `gravedad` | texto | **solo lectura** | La calcula `decidir()`; si el cliente la envía, se ignora |
| `fecha` | fecha y hora | **solo lectura** | La asigna el servidor |

Los campos internos del borrado lógico (`eliminado`, `fecha_eliminacion`) no se exponen.

Ejemplo de creación:

```json
POST /api/pacientes/
{"nombre": "Ana", "dificultad_respiracion": "No", "dolor": 7}

201 Created
{"id": 9, "nombre": "Ana", "dificultad_respiracion": "No", "dolor": 7,
 "gravedad": "Amarillo", "fecha": "2026-10-04T21:24:15.033141-03:00"}
```

### Códigos de estado y errores

| Código | Cuándo ocurre | Ejemplo de cuerpo |
|---|---|---|
| 200 OK | Lectura o edición correcta | el paciente o la lista paginada |
| 201 Created | Paciente creado | el paciente creado |
| 204 No Content | Paciente borrado | sin cuerpo |
| 400 Bad Request | Datos inválidos, JSON mal formado o filtro inválido | `{"dolor": ["El nivel de dolor debe estar entre 0 y 10."]}` |
| 401 Unauthorized | Sin token, token inválido o expirado, o clave incorrecta | `{"detail": "Las credenciales de autenticación no se proveyeron."}` |
| 403 Forbidden | Token válido, pero el rol no alcanza | `{"detail": "Tu rol no tiene permiso para realizar esta acción."}` |
| 404 Not Found | El id no existe, está eliminado o la página no existe | `{"detail": "No existe un paciente activo con ese id."}` |
| 405 Method Not Allowed | Verbo no soportado en esa URL | `{"detail": "Método \"POST\" no permitido."}` |
| 429 Too Many Requests | Más de 5 intentos de login por minuto | `{"detail": "Solicitud fue regulada (throttled)..."}` |

Los errores de datos siempre tienen la forma `{"campo": ["mensaje"]}` (se informan todos los campos malos en una sola respuesta) y el resto de los errores la forma `{"detail": "mensaje"}`.

## 🛠️ Justificación de la configuración de DRF

La configuración está en el bloque `REST_FRAMEWORK` de `clinica/settings.py`:

* **JWT en vez de sesión o Token simple:** un cliente de API no tiene navegador ni cookies, así que se identifica con un token en la cabecera en cada petición. Se eligió JWT (`simplejwt`) y no `TokenAuthentication` porque el token simple de DRF no expira nunca: si alguien lo roba, sirve para siempre. Con JWT el `access` dura 30 minutos y se renueva con un `refresh` que dura 1 día.
* **`IsAuthenticated` como permiso por defecto:** todo endpoint nuevo nace cerrado. Encima, `PermisoPorRol` (`recepcion/permissions.py`) reutiliza la función `tiene_rol()` de la ES2, así la API y las pantallas aplican exactamente la misma regla por rol.
* **`PageNumberPagination` con `PAGE_SIZE` 10:** la sala de espera puede crecer y la API no debe devolver todos los pacientes de una vez. Diez pacientes caben en una pantalla de un cliente, y la respuesta trae `count`, `next` y `previous` para pedir el resto.
* **Solo `JSONRenderer`:** la API la consume otro programa. Las personas usan las pantallas HTML de la ES2. Para explorar la API se usa Swagger, que sí permite enviar el token JWT.
* **Límite de 5 intentos por minuto en `/api/token/`:** frena ataques de fuerza bruta contra las contraseñas. Los endpoints de token y de refresco son los únicos públicos de la API, porque para pedir un token todavía no se tiene uno; todo `/api/pacientes/` exige token.
* **Un solo estilo de vista (`ModelViewSet` + router):** las rutas se generan solas, siguen las convenciones REST (sustantivo en plural y verbo HTTP) y no hay rutas escritas a mano con verbos.
* **Swagger solo con `DEBUG=True`:** la documentación muestra la estructura de la API, no los datos. Igual no se publica fuera del entorno de desarrollo.

## 🧪 Pruebas con cliente HTTP

El script `pruebas/probar_api.ps1` ejecuta 31 peticiones con `curl.exe` y compara cada código de estado con el esperado. Cubre autenticación, CRUD, errores 400/404/405, permisos de cada rol (403), refresco de token y el bloqueo por intentos (429).

Con el servidor corriendo en otra terminal:

```powershell
powershell -ExecutionPolicy Bypass -File pruebas\probar_api.ps1
```

El script pide la contraseña de los `usuario_*` de forma oculta y guarda la salida en `pruebas/resultados_curl.txt`, con los tokens truncados y la contraseña como `***`. La evidencia entregada registra **31 de 31 pruebas con el código esperado**. Si se ejecuta dos veces en menos de un minuto, la segunda vez `/api/token/` responde 429 por el límite de intentos.

## 📁 Archivos de la API

| Archivo | Contenido |
|---|---|
| `recepcion/serializers.py` | `PacienteSerializer`: campos expuestos, campos de solo lectura y validaciones |
| `recepcion/api_views.py` | `PacienteViewSet` (CRUD, filtro, borrado lógico) y vista de token con límite de intentos |
| `recepcion/permissions.py` | `PermisoPorRol`: permisos diferenciados por grupo |
| `clinica/settings.py` | `INSTALLED_APPS`, `REST_FRAMEWORK`, `SIMPLE_JWT` y `SPECTACULAR_SETTINGS` |
| `clinica/urls.py` | Router, endpoints de token y documentación |
| `pruebas/probar_api.ps1` | Script de pruebas con `curl.exe` |
| `pruebas/resultados_curl.txt` | Evidencia: salida de las 31 pruebas |
| `ia.md` | Uso crítico de IA: qué se adoptó, qué se descartó y por qué |
