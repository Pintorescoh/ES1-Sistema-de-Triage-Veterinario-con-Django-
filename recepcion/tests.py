from django.test import TestCase
from solucion import decidir, normalizar_gravedad

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