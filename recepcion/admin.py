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