import itertools
import unittest
from pathlib import Path

from lector import cargar_maquina
from motor import ACEPTADA, simular

ALTERADORA = Path(__file__).resolve().parents[1] / 'maquinas' / 'alteradora.yaml'


class PruebasAlteradora(unittest.TestCase):
    def setUp(self):
        self.maquina = cargar_maquina(ALTERADORA)

    def test_cadenas_del_yaml_tienen_al_menos_cinco_simbolos(self):
        self.assertEqual(len(self.maquina.cadenas), 4)
        self.assertTrue(all(len(cadena) >= 5 for cadena in self.maquina.cadenas))

    def test_invierte_las_cadenas_del_yaml(self):
        for cadena in self.maquina.cadenas:
            with self.subTest(cadena=cadena):
                resultado = simular(self.maquina, cadena)
                self.assertEqual(resultado.veredicto, ACEPTADA)
                self.assertEqual(resultado.cinta_final, cadena[::-1])

    def test_no_deja_la_cinta_en_blancos(self):
        for cadena in self.maquina.cadenas:
            with self.subTest(cadena=cadena):
                cinta_final = simular(self.maquina, cadena).cinta_final
                self.assertTrue(cinta_final)
                self.assertTrue(set(cinta_final) <= {'a', 'b'})

    def test_invierte_todas_las_cadenas_cortas(self):
        for longitud in range(7):
            for simbolos in itertools.product('ab', repeat=longitud):
                palabra = ''.join(simbolos)
                with self.subTest(palabra=palabra):
                    resultado = simular(self.maquina, palabra, limite_pasos=10000)
                    self.assertEqual(resultado.veredicto, ACEPTADA)
                    self.assertEqual(resultado.cinta_final, palabra[::-1])


if __name__ == '__main__':
    unittest.main()
