from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    # Columnas que se verán en la lista principal
    list_display = ("nombre", "gravedad", "dificultad_respiracion", "dolor", "fecha", "eliminado")
    
    # Filtros laterales para buscar rápido (ej: ver solo Códigos Rojos)
    list_filter = ("gravedad", "eliminado")
    
    # Barra de búsqueda por nombre de mascota
    search_fields = ("nombre",)
    
    # Protegemos el campo de fecha de eliminación para que no se edite a mano
    readonly_fields = ("fecha_eliminacion",)

    def _puede_administrar(self, user):
        return user.is_superuser or user.groups.filter(name="admin").exists()

    def has_module_permission(self, request):
        return self._puede_administrar(request.user)

    def has_view_permission(self, request, obj=None):
        return self._puede_administrar(request.user)

    def has_add_permission(self, request):
        return self._puede_administrar(request.user)

    def has_change_permission(self, request, obj=None):
        return self._puede_administrar(request.user)

    def has_delete_permission(self, request, obj=None):
        return self._puede_administrar(request.user)

    def delete_model(self, request, obj):
        obj.soft_delete()