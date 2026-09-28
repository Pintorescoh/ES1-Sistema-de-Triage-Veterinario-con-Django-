from django.contrib import admin
from .models import Paciente

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    actions = ("eliminar_logicamente",)

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

    def get_actions(self, request):
        actions = super().get_actions(request)
        actions.pop("delete_selected", None)
        return actions

    @admin.action(description="Eliminar seleccionados (borrado lógico)")
    def eliminar_logicamente(self, request, queryset):
        pacientes_activos = queryset.filter(eliminado=False)
        cantidad = pacientes_activos.count()
        for paciente in pacientes_activos:
            paciente.soft_delete()
        self.message_user(
            request,
            f"Se marcaron {cantidad} paciente(s) como eliminados.",
        )