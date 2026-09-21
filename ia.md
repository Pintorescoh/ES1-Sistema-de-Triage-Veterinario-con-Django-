# Uso de Inteligencia Artificial (EVA 2)

Durante este proyecto, utilicé IA (Gemini) como un asistente de aprendizaje para entender la sintaxis de Python y la estructura base de Django.

* Pregunta textual: "¿Cómo migro mi proyecto desde datos.json a un modelo Django con SQLite, manteniendo la función decidir() y agregando migraciones?"

	La IA me propuso utilizar MongoDB Atlas en la nube, pero rechacé esa sugerencia basándome en el documento de migración y mantuve SQLite localmente.

* Pregunta textual: "¿Cómo implemento login, grupos admin/normal/viewer y permisos seguros en las vistas y en el administrador Django?"

	La IA entregó inicialmente código que intentaba importar una función inventada llamada `evaluar_triage`. Al levantar el servidor, el sistema arrojó un error. Corregí la propuesta para importar la función original `decidir()` desde `solucion.py`, mantuve la regla de decisión intacta y protegí las vistas con decoradores de servidor.

	También corregí la gestión de contraseñas: no quedan escritas en el código, sino que se leen desde `USERS_PASSWORD` o se solicitan de forma oculta al ejecutar `setup_roles.py`. En el administrador Django, solo el grupo `admin` y los superusuarios pueden gestionar pacientes.