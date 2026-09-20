from django.db import models
from django.utils import timezone
from solucion import decidir

class Paciente(models.Model):
    # 1. Primero definimos las opciones
    RESPIRACION_CHOICES = [
        ("Sí", "Sí"),
        ("No", "No")
    ]

    # 2. Luego definimos todos los campos de la base de datos
    nombre = models.CharField(max_length=100)
    dificultad_respiracion = models.CharField(max_length=2, choices=RESPIRACION_CHOICES)
    dolor = models.IntegerField()
    gravedad = models.CharField(max_length=50, blank=True) # Se llenará automáticamente
    
    fecha = models.DateTimeField(default=timezone.now)
    
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    # 3. Después definimos las funciones (acciones)
    def save(self, *args, **kwargs):
        # Convertimos "Si"/"No" a 1 o 0
        resp_num = 1 if str(self.dificultad_respiracion).lower() in ["si", "sí"] else 0
        
        # Calculamos la gravedad automáticamente usando tu regla de negocio
        self.gravedad = decidir(resp_num, self.dolor)
        
        # Guardamos el registro en la base de datos
        super().save(*args, **kwargs)

    def soft_delete(self):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()

    def __str__(self):
        return f"{self.nombre} - {self.gravedad}"

    class Meta:
        ordering = ["-fecha"]