from django.http import Http404
from drf_spectacular.utils import OpenApiParameter, extend_schema, extend_schema_view
from rest_framework import viewsets
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import ScopedRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import Paciente
from .permissions import PermisoPorRol
from .serializers import PacienteSerializer

GRAVEDADES = ["Rojo", "Amarillo", "Verde"]


@extend_schema_view(
    list=extend_schema(
        parameters=[
            OpenApiParameter(
                "gravedad",
                str,
                enum=GRAVEDADES,
                description="Filtra por gravedad (no distingue mayúsculas).",
            ),
        ],
    ),
)
class PacienteViewSet(viewsets.ModelViewSet):
    """
    CRUD de pacientes de la sala de espera.

    La gravedad no la manda el cliente: la calcula la regla decidir()
    dentro de Paciente.save(), igual que en las pantallas HTML de la ES2.
    """
    serializer_class = PacienteSerializer
    # IsAuthenticated primero: sin token responde 401; con token pero sin rol, 403.
    permission_classes = [IsAuthenticated, PermisoPorRol]

    def get_queryset(self):
        # Igual que la vista lista() de la ES2: los eliminados lógicamente no se ven.
        queryset = Paciente.objects.filter(eliminado=False)

        # Filtro opcional: /api/pacientes/?gravedad=Rojo
        gravedad = self.request.query_params.get("gravedad")
        if gravedad:
            if gravedad.capitalize() not in GRAVEDADES:
                # 400 en vez de una lista vacía: el cliente se equivocó y debe saberlo.
                raise ValidationError(
                    {"gravedad": [f"Valor no válido. Usa uno de: {', '.join(GRAVEDADES)}."]}
                )
            queryset = queryset.filter(gravedad__iexact=gravedad)
        return queryset

    def get_object(self):
        # El 404 por defecto viene en inglés; lo reemplazamos por un mensaje claro.
        try:
            return super().get_object()
        except Http404:
            raise NotFound("No existe un paciente activo con ese id.")

    def perform_destroy(self, instance):
        # DELETE no borra la fila: usa el mismo borrado lógico de la ES2,
        # así el historial de pacientes se conserva.
        instance.soft_delete()


class TokenConLimiteView(TokenObtainPairView):
    """
    Entrega el par de tokens JWT (access + refresh) a cambio de usuario y contraseña.
    Limita los intentos por IP para frenar ataques de fuerza bruta a las contraseñas.
    """
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "token"
