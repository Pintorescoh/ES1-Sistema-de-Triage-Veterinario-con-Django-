from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from solucion import decidir, normalizar_gravedad
from .models import Paciente

class TriageTests(TestCase):
    def test_decidir_logica_rojo(self):
        # Si tiene dificultad respiratoria (1) y dolor alto (10), debe ser Rojo
        resultado = decidir(1, 10)
        self.assertEqual(resultado, "Rojo")

    def test_decidir_logica_amarillo(self):
        # Si no tiene dificultad respiratoria pero el dolor es alto, corresponde a Amarillo
        resultado = decidir(0, 6)
        self.assertEqual(resultado, "Amarillo")

    def test_decidir_logica_verde(self):
        # Si no tiene dificultad (0) y dolor bajo (2), debe ser Verde
        resultado = decidir(0, 2)
        self.assertEqual(resultado, "Verde")

    def test_decidir_logica_verde_con_dolor_cero(self):
        # El rango válido incluye el valor 0
        resultado = decidir(0, 0)
        self.assertEqual(resultado, "Verde")

    def test_normalizar_gravedad_con_prefijo_legacy(self):
        self.assertEqual(normalizar_gravedad("Código Rojo"), "Rojo")
        self.assertEqual(normalizar_gravedad("Código Amarillo"), "Amarillo")
        self.assertEqual(normalizar_gravedad("Código Verde"), "Verde")


class PacienteAdminTests(TestCase):
    def setUp(self):
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin_test",
            email="admin@example.com",
            password="test-password-123",
        )
        self.paciente = Paciente.objects.create(
            nombre="Luna",
            dificultad_respiracion="No",
            dolor=2,
        )
        self.client.force_login(self.admin_user)

    def test_accion_masiva_marca_paciente_como_eliminado(self):
        response = self.client.post(
            reverse("admin:recepcion_paciente_changelist"),
            {
                "action": "eliminar_logicamente",
                "_selected_action": [str(self.paciente.pk)],
            },
        )

        self.assertEqual(response.status_code, 302)
        self.paciente.refresh_from_db()
        self.assertTrue(self.paciente.eliminado)
        self.assertIsNotNone(self.paciente.fecha_eliminacion)
        self.assertTrue(Paciente.objects.filter(pk=self.paciente.pk).exists())

    def test_admin_no_ofrece_eliminacion_fisica_masiva(self):
        request = self.client.get(
            reverse("admin:recepcion_paciente_changelist")
        ).wsgi_request
        actions = admin.site._registry[Paciente].get_actions(request)

        self.assertIn("eliminar_logicamente", actions)
        self.assertNotIn("delete_selected", actions)