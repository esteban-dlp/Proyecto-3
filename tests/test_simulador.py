import contextlib
import io
import unittest
from pathlib import Path

from simulador import main

RAIZ = Path(__file__).resolve().parents[1]
RECONOCEDORA = RAIZ / 'maquinas' / 'reconocedora.yaml'
ALTERADORA = RAIZ / 'maquinas' / 'alteradora.yaml'


class PruebasSimulador(unittest.TestCase):
    def ejecutar(self, argumentos):
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            codigo = main(argumentos)
        return codigo, salida.getvalue()

    def test_muestra_veredicto_de_cada_cadena(self):
        codigo, salida = self.ejecutar([str(RECONOCEDORA)])
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.count('Resultado: aceptada'), 2)
        self.assertEqual(salida.count('Resultado: rechazada'), 2)

    def test_alteradora_muestra_las_cuatro_cadenas(self):
        codigo, salida = self.ejecutar([str(ALTERADORA)])
        self.assertEqual(codigo, 0)
        self.assertEqual(salida.count('Cadena:'), 4)
        self.assertEqual(salida.count('Resultado: aceptada'), 4)

    def test_limite_pequeno_reporta_indeterminado(self):
        codigo, salida = self.ejecutar([str(RECONOCEDORA), '--limite-pasos', '3'])
        self.assertEqual(codigo, 0)
        self.assertIn('Resultado: indeterminado', salida)
        self.assertNotIn('Resultado: rechazada', salida)

    def test_archivo_inexistente_termina_con_error(self):
        with contextlib.redirect_stderr(io.StringIO()):
            codigo, _ = self.ejecutar([str(RAIZ / 'no_existe.yaml')])
        self.assertEqual(codigo, 1)


if __name__ == '__main__':
    unittest.main()
