# Evidencia de pruebas con cliente HTTP (curl)

* `probar_api.ps1`: script que ejecuta las 32 peticiones con `curl.exe` contra el servidor local.
* `resultados_curl.txt`: salida de cada petición: el comando `curl`, el código obtenido frente al esperado y el cuerpo de la respuesta. Los tokens aparecen truncados y la contraseña como `***`.

## Qué prueba cubre cada endpoint

Los números corresponden a `[n]` en `resultados_curl.txt`.

| Endpoint | Caso correcto | Casos de error |
|---|---|---|
| `POST /api/token/` | 1, 2, 3 (200) | 29, 30 clave incorrecta (401) · 31 demasiados intentos (429) |
| `POST /api/token/refresh/` | 27 (200) | 28 refresh inválido (401) |
| `GET /api/` | 32 (200) | — |
| `GET /api/pacientes/` | 7, 21 (200) · 12 filtro por gravedad (200) | 4 sin token, 5 prefijo `Token`, 6 token falso (401) · 17 filtro inválido (400) · 19 página inexistente (404) |
| `POST /api/pacientes/` | 8 (201) | 13, 14 datos inválidos, 15 JSON mal formado (400) · 22 rol viewer (403) |
| `GET /api/pacientes/{id}/` | 9 (200) | 18 id inexistente, 26 paciente borrado (404) |
| `PATCH /api/pacientes/{id}/` | 10 (200) | 23 rol viewer (403) |
| `PUT /api/pacientes/{id}/` | 11 (200) | 16 datos incompletos (400) |
| `DELETE /api/pacientes/{id}/` | 25 rol admin (204) | 24 rol normal (403) |
| `POST /api/pacientes/{id}/` | — | 20 verbo no permitido (405) |

## Cómo repetir las pruebas

Con el servidor corriendo (`python manage.py runserver`) en otra terminal:

```powershell
powershell -ExecutionPolicy Bypass -File pruebas\probar_api.ps1
```
