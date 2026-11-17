import copy
import itertools
import unittest
from pathlib import Path

import yaml

from lector import ErrorConfiguracion, cargar_maquina, interpretar_maquina

RUTA = Path(__file__).resolve().parents[1] / 'maquinas' / 'reconocedora.yaml'


class PruebasLector(unittest.TestCase):
    def setUp(self):
        self.datos = yaml.safe_load(RUTA.read_text(encoding='utf-8'))

    def test_carga_archivo(self):
        maquina = cargar_maquina(RUTA)
        self.assertEqual(len(maquina.transiciones), 12)
        self.assertEqual(maquina.cadenas, ('aaabbb', 'aaaabbbb', 'aabbb', 'ababab'))
        self.assertTrue({'a', 'b', 'X', 'Y', None} <= set(maquina.alfabeto_cinta))

    def test_rechaza_transicion_duplicada(self):
        datos = copy.deepcopy(self.datos)
        datos['delta'].append(copy.deepcopy(datos['delta'][0]))
        with self.assertRaises(ErrorConfiguracion):
            interpretar_maquina(datos)

    def test_rechaza_cadena_ajena_al_alfabeto(self):
        self.datos['simulation_strings'] = ['abc']
        with self.assertRaises(ErrorConfiguracion):
            interpretar_maquina(self.datos)

    def test_rechaza_desplazamiento_invalido(self):
        self.datos['delta'][0]['output']['tape_displacement'] = 'N'
        with self.assertRaises(ErrorConfiguracion):
            interpretar_maquina(self.datos)

    def test_reconocedora_exhaustiva_cadenas_cortas(self):
        # interprete minimo de prueba que no sustituye el simulador del companero
        maquina = cargar_maquina(RUTA)
        for longitud in range(9):
            for simbolos in itertools.product('ab', repeat=longitud):
                palabra = ''.join(simbolos)
                cinta = dict(enumerate(palabra))
                estado, memoria, posicion = maquina.estado_inicial, None, 0
                for _ in range(1000):
                    if estado == maquina.estado_final:
                        break
                    transicion = maquina.transiciones.get((estado, memoria, cinta.get(posicion)))
                    if transicion is None:
                        break
                    cinta[posicion] = transicion.simbolo_escrito
                    estado, memoria = transicion.estado_final, transicion.memoria_final
                    posicion += {'L': -1, 'R': 1, 'S': 0}[transicion.desplazamiento]
                else:
                    self.fail(f'La simulación no terminó: {palabra!r}')
                esperado = any(palabra == 'a' * n + 'b' * n for n in range(1, 5))
                self.assertEqual(estado == maquina.estado_final, esperado, palabra)


if __name__ == '__main__':
    unittest.main()
