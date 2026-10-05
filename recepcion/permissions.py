from rest_framework import permissions
from .views import tiene_rol


class PermisoPorRol(permissions.BasePermission):
    """
    Misma regla de roles que las pantallas HTML de la ES2:
    - leer (GET): cualquier usuario autenticado (admin, normal, viewer)
    - crear y editar (POST, PUT, PATCH): admin y normal
    - borrar (DELETE): solo admin
    El superusuario puede todo (tiene_rol ya lo considera).
    """
    message = "Tu rol no tiene permiso para realizar esta acción."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == "DELETE":
            return tiene_rol(request.user, "admin")
        return tiene_rol(request.user, "admin", "normal")
