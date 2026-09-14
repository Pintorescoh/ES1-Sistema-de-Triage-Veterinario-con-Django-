# Planificación del Proyecto - Sistema de Triage (EVA 2)

## 1. Alcance del Proyecto
El sistema es una aplicación web backend desarrollada en el framework Django para la gestión y evaluación de pacientes en una sala de espera (Triage). Para esta fase del desarrollo, el alcance real del proyecto incluye:
* Almacenamiento de datos utilizando el motor de base de datos relacional SQLite.
* Implementación de las cuatro operaciones CRUD (Crear, Leer, Editar, Eliminar) mediante vistas web.
* Sistema de autenticación de usuarios y restricción de accesos mediante roles (admin, normal, viewer).
* Implementación de borrado lógico (soft delete) para preservar el historial de pacientes sin perder registros.

## 2. Priorización de Requerimientos (MoSCoW)

### Must Have (Debe tener)
* Conexión funcional y migrada a base de datos SQLite.
* Operaciones CRUD completamente operativas.
* Integración intacta de la regla de decisión de triage importada desde la lógica original.
* Sistema de Login y Logout para manejo de sesiones.
* Seguridad en servidor mediante decoradores para restringir vistas según el grupo del usuario.
* Borrado lógico de fichas médicas.

### Should Have (Debería tener)
* Administrador de Django fuertemente personalizado (columnas, filtros y barra de búsqueda).
* Formularios protegidos con tokens CSRF para evitar vulnerabilidades de seguridad.

### Could Have (Podría tener)
* Interfaz gráfica (HTML/CSS) estilizada para la vista de la lista de pacientes y formularios de ingreso.

### Won't Have (No tendrá en esta versión)
* Almacenamiento local basado en archivos de texto o `datos.json`.
* Motores de base de datos externos o alojados en la nube (ej. MongoDB o PostgreSQL).
* Creación de cuentas de usuario de forma pública (los perfiles son generados internamente por el administrador).