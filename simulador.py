import argparse
import sys

from lector import ErrorConfiguracion, cargar_maquina
from motor import ACEPTADA, INDETERMINADA, simular

LIMITE_PREDETERMINADO = 10000


def construir_parser():
    parser = argparse.ArgumentParser(description='Simula una máquina de Turing de una cinta a partir de un YAML.')
    parser.add_argument('ruta', help='ruta del archivo YAML con la máquina')
    parser.add_argument('--limite-pasos', type=int, default=LIMITE_PREDETERMINADO,
                        help=f'número máximo de pasos por cadena (predeterminado: {LIMITE_PREDETERMINADO})')
    return parser


def mostrar_resultado(resultado):
    print(f'Cadena: {resultado.cadena!r}')
    for numero, instantanea in enumerate(resultado.instantaneas):
        print(f'Paso {numero} | estado: {instantanea.estado} | memoria: {instantanea.memoria} | cabezal: {instantanea.cabezal}')
        print(f'  ID: {instantanea.descripcion}')
    print(f'Cinta final: {resultado.cinta_final or "(vacía)"}')
    if resultado.veredicto == ACEPTADA:
        print(f'Resultado: aceptada en {resultado.pasos} pasos')
    elif resultado.veredicto == INDETERMINADA:
        print(f'Resultado: indeterminado, se alcanzó el límite de {resultado.pasos} pasos sin llegar al estado final')
    else:
        estado = resultado.instantaneas[-1].estado
        print(f'Resultado: rechazada, no hay transición aplicable en el estado {estado}')
    print()


def main(argumentos=None):
    argumentos = construir_parser().parse_args(argumentos)
    if argumentos.limite_pasos < 0:
        print('Error: el límite de pasos no puede ser negativo', file=sys.stderr)
        return 1
    try:
        maquina = cargar_maquina(argumentos.ruta)
    except ErrorConfiguracion as error:
        print(f'Error: {error}', file=sys.stderr)
        return 1
    for cadena in maquina.cadenas:
        mostrar_resultado(simular(maquina, cadena, argumentos.limite_pasos))
    return 0


if __name__ == '__main__':
    sys.exit(main())
