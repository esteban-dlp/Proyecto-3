import unittest
from pathlib import Path

from cinta import Cinta
from lector import cargar_maquina, interpretar_maquina
from motor import ACEPTADA, INDETERMINADA, RECHAZADA, simular

RECONOCEDORA = Path(__file__).resolve().parents[1] / 'maquinas' / 'reconocedora.yaml'


def transicion(estado, memoria, leido, nuevo_estado, nueva_memoria, escrito, desplazamiento):
    return {
        'params': {'initial_state': estado, 'mem_cache_value': memoria, 'tape_input': leido},
        'output': {'final_state': nuevo_estado, 'mem_cache_value': nueva_memoria,
                   'tape_output': escrito, 'tape_displacement': desplazamiento},
    }


def maquina_de_prueba(delta, cadenas=('ab',), inicial='q0', final='qf'):
    datos = {
        'q_states': {'q_list': ['q0', 'q1', 'qf'], 'initial': inicial, 'final': final},
        'alphabet': ['a', 'b'],
        'tape_alphabet': ['X', None],
        'delta': delta,
        'simulation_strings': list(cadenas),
    }
    return interpretar_maquina(datos)


class PruebasCinta(unittest.TestCase):
    def test_crece_hacia_ambos_lados(self):
        cinta = Cinta('ab')
        cinta.cabezal = -2
        cinta.escribir('X')
        cinta.cabezal = 3
        cinta.escribir('Y')
        self.assertEqual(cinta.texto(), 'X_ab_Y')

    def test_celda_fuera_de_la_entrada_es_blanco(self):
        cinta = Cinta('ab')
        cinta.cabezal = 7
        self.assertIsNone(cinta.leer())

    def test_escribir_blanco_libera_la_celda(self):
        cinta = Cinta('ab')
        cinta.escribir(None)
        self.assertIsNone(cinta.leer())
        self.assertEqual(cinta.texto(), 'b')

    def test_texto_con_estado_ubica_el_cabezal(self):
        cinta = Cinta('ab')
        cinta.cabezal = 1
        self.assertEqual(cinta.texto('q1'), 'a<q1>b')


class PruebasMotor(unittest.TestCase):
    def test_instantanea_inicial(self):
        resultado = simular(cargar_maquina(RECONOCEDORA), 'aaabbb')
        inicial = resultado.instantaneas[0]
        self.assertEqual(inicial.estado, 'inicio')
        self.assertIsNone(inicial.memoria)
        self.assertEqual(inicial.cabezal, 0)
        self.assertEqual(inicial.descripcion, '<inicio>aaabbb')

    def test_hay_una_instantanea_por_paso_mas_la_inicial(self):
        resultado = simular(cargar_maquina(RECONOCEDORA), 'aaabbb')
        self.assertEqual(len(resultado.instantaneas), resultado.pasos + 1)

    def test_reconocedora_acepta_y_rechaza_los_casos_del_video(self):
        maquina = cargar_maquina(RECONOCEDORA)
        esperados = {'aaabbb': ACEPTADA, 'aaaabbbb': ACEPTADA, 'aabbb': RECHAZADA, 'ababab': RECHAZADA}
        for cadena, veredicto in esperados.items():
            with self.subTest(cadena=cadena):
                self.assertEqual(simular(maquina, cadena).veredicto, veredicto)

    def test_cinta_final_de_una_aceptada(self):
        resultado = simular(cargar_maquina(RECONOCEDORA), 'aaabbb')
        self.assertEqual(resultado.cinta_final, 'XXXYYY')

    def test_acepta_si_el_estado_inicial_es_final(self):
        maquina = maquina_de_prueba([], inicial='qf')
        resultado = simular(maquina, 'ab')
        self.assertEqual(resultado.veredicto, ACEPTADA)
        self.assertEqual(resultado.pasos, 0)

    def test_rechaza_sin_transicion_aplicable(self):
        maquina = maquina_de_prueba([transicion('q0', None, 'a', 'q1', None, 'X', 'R')])
        resultado = simular(maquina, 'ab')
        self.assertEqual(resultado.veredicto, RECHAZADA)
        self.assertEqual(resultado.instantaneas[-1].estado, 'q1')

    def test_limite_de_pasos_da_resultado_indeterminado(self):
        delta = [
            transicion('q0', None, 'a', 'q0', None, 'a', 'R'),
            transicion('q0', None, None, 'q0', None, None, 'R'),
        ]
        maquina = maquina_de_prueba(delta)
        resultado = simular(maquina, 'a', limite_pasos=5)
        self.assertEqual(resultado.veredicto, INDETERMINADA)
        self.assertEqual(resultado.pasos, 5)

    def test_usa_la_memoria_para_elegir_la_transicion(self):
        delta = [
            transicion('q0', None, 'a', 'q1', 'a', 'a', 'R'),
            transicion('q1', 'a', 'b', 'qf', None, 'b', 'S'),
        ]
        maquina = maquina_de_prueba(delta)
        self.assertEqual(simular(maquina, 'ab').veredicto, ACEPTADA)
        self.assertEqual(simular(maquina, 'aa').veredicto, RECHAZADA)


if __name__ == '__main__':
    unittest.main()
