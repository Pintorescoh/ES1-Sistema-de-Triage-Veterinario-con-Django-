from django.db import models
from django.utils import timezone

class Paciente(models.Model):
    # Definimos opciones cerradas para evitar errores de tipeo, tal como sugiere el PDF
    RESPIRACION_CHOICES = [
        ("Sí", "Sí"),
        ("No", "No")
    ]

    # Tus 4 campos originales traducidos a base de datos
    nombre = models.CharField(max_length=100)
    dificultad_respiracion = models.CharField(max_length=2, choices=RESPIRACION_CHOICES)
    dolor = models.IntegerField()
    gravedad = models.CharField(max_length=50)
    
    # Campos obligatorios agregados según la pauta de evaluación
    fecha = models.DateTimeField(default=timezone.now)
    
    # Borrado lógico: no se pierde nada, solo se oculta
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha"] # Ordena para que los más nuevos salgan primero

    def __str__(self):
        return f"{self.nombre} - {self.gravedad}"

    # Función obligatoria para ocultar el registro
    def soft_delete(self):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save() # Sin esto no guarda el cambio en la base de datos