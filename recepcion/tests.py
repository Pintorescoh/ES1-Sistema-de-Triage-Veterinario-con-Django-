from django.test import TestCase
from solucion import decidir

class TriageTests(TestCase):
    def test_decidir_logica_rojo(self):
        # Si tiene dificultad respiratoria (1) y dolor alto (10), debe ser Rojo
        resultado = decidir(1, 10)
        self.assertEqual(resultado, "Rojo")
        
    def test_decidir_logica_verde(self):
        # Si no tiene dificultad (0) y dolor bajo (2), debe ser Verde
        resultado = decidir(0, 2)
        self.assertEqual(resultado, "Verde")