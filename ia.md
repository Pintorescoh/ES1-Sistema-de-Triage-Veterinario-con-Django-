# Uso de Inteligencia Artificial (ES3)

Herramienta: Claude (Claude Code en VS Code). La usé para construir la API paso a paso a partir del PDF de instrucciones. Cada propuesta la revisé contra mi proyecto de la ES2 y la verifiqué con pruebas antes de aceptarla.

## 1. Autenticación (seguridad)

* **Qué le pedí:** configurar la autenticación de la API según el bloque 7 del PDF.
* **Qué me respondió:** usar JWT (`simplejwt`) en vez del `TokenAuthentication` de los ejemplos del PDF, con un `access` de 30 minutos, un `refresh` de 1 día y un límite de 5 intentos por minuto en `/api/token/`.
* **Qué estaba mal o era riesgoso:** el cambio rompe los `curl` del PDF, porque JWT usa `Authorization: Bearer` y no `Token`. Además, `/api/token/` tiene que ser público, y había que confirmar que eso no era el error de `AllowAny`.
* **Qué hice yo:** adopté JWT porque el Token simple no expira y la rúbrica pide expiración o refresco. Comprobé que la cabecera `Token ...` responde 401 y lo advertí en el README. Dejé públicos solo los dos endpoints de token (para pedir un token no se puede tener uno) y todo lo demás con `IsAuthenticated` por defecto. Para probar antes de tener los tokens no apagué los permisos: usé `force_authenticate` en pruebas.

## 2. Permisos diferenciados (seguridad)

* **Qué le pedí:** permisos por rol como el `SoloStaffBorra` del PDF.
* **Qué me respondió:** revisó mi base y advirtió que `usuario_admin` tiene `is_staff=False`. Propuso usar mis grupos de la ES2 en vez de `is_staff`.
* **Qué estaba mal:** con el ejemplo del PDF, mi administrador no habría podido borrar, y la API habría tenido una regla distinta a la de mis pantallas.
* **Qué hice yo:** creé `PermisoPorRol`, que reutiliza mi función `tiene_rol()`: viewer solo lee, normal además crea y edita, y solo admin borra. Verifiqué los 401, 403, 200, 201 y 204 de cada rol con curl (`pruebas/`).

## 3. Script de evidencia (seguridad)

* **Qué le pedí:** un script que probara todos los endpoints con curl y guardara la salida.
* **Qué me respondió:** `pruebas/probar_api.ps1`, que pide la contraseña oculta y trunca los tokens.
* **Qué estaba mal:** la primera versión dejaba un *refresh token* completo en el archivo de resultados, porque el cuerpo de la petición no se truncaba. Además, PowerShell 5.1 leía mal la "í" de `"Sí"` y la API respondía 400.
* **Qué hice yo:** lo corregimos (truncar también los cuerpos y guardar el script en UTF-8 con BOM) y revisé el archivo de resultados para confirmar que no quedara ningún token completo ni la contraseña. Un token en un archivo entregado es tan grave como una contraseña escrita en el código.

## 4. Afirmaciones sin verificar y documentación

* **Qué le pedí:** comentarios en el código y la justificación de la configuración para el README.
* **Qué me respondió:** escribió en `serializers.py` que validar "nombre solo números" era "el mismo criterio de la ES2", y en el README que `PAGE_SIZE` 10 "coincide con la documentación oficial". Para Swagger propuso publicarlo solo con `DEBUG=True`.
* **Qué estaba mal:** la ES2 nunca validó eso, y lo de la documentación oficial no estaba comprobado. Si lo hubiera entregado así, no habría podido defenderlo.
* **Qué hice yo:** corregí el comentario (es una validación nueva) y dejé en el README solo argumentos propios. Acepté la decisión de Swagger porque la documentación no necesita token para leerse, pero no debe quedar publicada fuera del desarrollo; para probar endpoints desde ahí igual se necesita el token.
