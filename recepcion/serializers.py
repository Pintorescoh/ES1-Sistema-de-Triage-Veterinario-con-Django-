from rest_framework import serializers
from .models import Paciente


class PacienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paciente
        # Campos enumerados a mano (nunca "__all__"): eliminado y fecha_eliminacion
        # son de uso interno del borrado lógico y no se exponen.
        fields = ["id", "nombre", "dificultad_respiracion", "dolor", "gravedad", "fecha"]
        # gravedad la calcula la regla decidir() en Paciente.save(); si fuera editable,
        # cualquier cliente podría declararse "Rojo" mandándolo en el JSON.
        # fecha la pone el servidor al crear el registro.
        read_only_fields = ["gravedad", "fecha"]
        extra_kwargs = {
            "dolor": {
                "error_messages": {
                    "invalid": "El dolor debe ser un número entero.",
                    "min_value": "El nivel de dolor debe estar entre 0 y 10.",
                    "max_value": "El nivel de dolor debe estar entre 0 y 10.",
                },
            },
            "dificultad_respiracion": {
                "error_messages": {
                    "invalid_choice": 'La dificultad respiratoria debe ser "Sí" o "No".',
                },
            },
        }

    def validate_nombre(self, valor):
        # Validación nueva de la ES3: un programa puede mandar cualquier texto, y un
        # nombre hecho solo de números es casi seguro un error del cliente.
        if valor.isdigit():
            raise serializers.ValidationError("El nombre no puede ser solo números.")
        return valor
