from pathlib import Path

import yaml

from modelo import Maquina, Transicion


class ErrorConfiguracion(ValueError):
    pass


def _lista(valor, nombre):
    if not isinstance(valor, list):
        raise ErrorConfiguracion(f'{nombre} debe ser una lista')
    return valor


def _simbolo(valor, nombre):
    if valor is not None and (not isinstance(valor, str) or len(valor) != 1):
        raise ErrorConfiguracion(f'{nombre} debe ser un carácter o null')
    return valor


def cargar_maquina(ruta):
    try:
        with Path(ruta).open(encoding='utf-8') as archivo:
            datos = yaml.safe_load(archivo)
    except (OSError, yaml.YAMLError) as error:
        raise ErrorConfiguracion(f'No se pudo leer el YAML: {error}') from error
    return interpretar_maquina(datos)


def interpretar_maquina(datos):
    try:
        if not isinstance(datos, dict):
            raise ErrorConfiguracion('La configuración debe ser un objeto YAML')
        estados_yaml = datos['q_states']
        estados = _lista(estados_yaml['q_list'], 'q_states.q_list')
        if not estados or any(not isinstance(e, str) or not e for e in estados):
            raise ErrorConfiguracion('Los estados deben ser cadenas no vacías')
        if len(set(estados)) != len(estados):
            raise ErrorConfiguracion('Hay estados repetidos')
        inicial, final = estados_yaml['initial'], estados_yaml['final']
        if inicial not in estados or final not in estados:
            raise ErrorConfiguracion('Los estados inicial y final deben pertenecer a q_list')
        alfabeto = _lista(datos['alphabet'], 'alphabet')
        cinta = _lista(datos['tape_alphabet'], 'tape_alphabet')
        for simbolo in alfabeto:
            if _simbolo(simbolo, 'alphabet') is None:
                raise ErrorConfiguracion('El alfabeto de entrada no puede contener null')
        for simbolo in cinta:
            _simbolo(simbolo, 'tape_alphabet')
        # el ejemplo del enunciado lista solo los simbolos adicionales de la cinta
        cinta_completa = tuple(dict.fromkeys([*alfabeto, *cinta, None]))
        cadenas = _lista(datos['simulation_strings'], 'simulation_strings')
        if any(not isinstance(c, str) or any(s not in alfabeto for s in c) for c in cadenas):
            raise ErrorConfiguracion('Cada cadena debe contener solo símbolos del alfabeto de entrada')
        transiciones = {}
        for entrada in _lista(datos['delta'], 'delta'):
            parametros, salida = entrada['params'], entrada['output']
            transicion = Transicion(
                parametros['initial_state'], _simbolo(parametros['mem_cache_value'], 'mem_cache_value'),
                _simbolo(parametros['tape_input'], 'tape_input'), salida['final_state'],
                _simbolo(salida['mem_cache_value'], 'mem_cache_value'),
                _simbolo(salida['tape_output'], 'tape_output'), salida['tape_displacement'])
            if transicion.estado_inicial not in estados or transicion.estado_final not in estados:
                raise ErrorConfiguracion('Una transición usa un estado desconocido')
            if transicion.simbolo_leido not in cinta_completa or transicion.simbolo_escrito not in cinta_completa:
                raise ErrorConfiguracion('Una transición usa un símbolo ajeno al alfabeto de cinta')
            if transicion.desplazamiento not in ('L', 'R', 'S'):
                raise ErrorConfiguracion('El desplazamiento debe ser L, R o S')
            clave = (transicion.estado_inicial, transicion.memoria_inicial, transicion.simbolo_leido)
            if clave in transiciones:
                raise ErrorConfiguracion(f'Transición duplicada: {clave}')
            transiciones[clave] = transicion
        return Maquina(tuple(estados), inicial, final, tuple(alfabeto), cinta_completa, transiciones, tuple(cadenas))
    except (KeyError, TypeError) as error:
        raise ErrorConfiguracion(f'Falta un campo o tiene una estructura incorrecta: {error}') from error
