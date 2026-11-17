from dataclasses import dataclass

from cinta import Cinta

ACEPTADA = 'aceptada'
RECHAZADA = 'rechazada'
INDETERMINADA = 'indeterminada'


@dataclass(frozen=True)
class Instantanea:
    estado: str
    memoria: str | None
    cabezal: int
    descripcion: str


@dataclass(frozen=True)
class Resultado:
    cadena: str
    veredicto: str
    instantaneas: tuple[Instantanea, ...]
    cinta_final: str

    @property
    def pasos(self):
        return len(self.instantaneas) - 1


def _instantanea(cinta, estado, memoria):
    return Instantanea(estado, memoria, cinta.cabezal, cinta.texto(estado))


def simular(maquina, cadena, limite_pasos=None):
    cinta = Cinta(cadena)
    estado, memoria = maquina.estado_inicial, None
    instantaneas = [_instantanea(cinta, estado, memoria)]
    pasos = 0
    while True:
        # la aceptacion se revisa antes de buscar otra transicion
        if estado == maquina.estado_final:
            veredicto = ACEPTADA
            break
        if limite_pasos is not None and pasos >= limite_pasos:
            veredicto = INDETERMINADA
            break
        transicion = maquina.transiciones.get((estado, memoria, cinta.leer()))
        if transicion is None:
            veredicto = RECHAZADA
            break
        cinta.escribir(transicion.simbolo_escrito)
        cinta.mover(transicion.desplazamiento)
        estado, memoria = transicion.estado_final, transicion.memoria_final
        instantaneas.append(_instantanea(cinta, estado, memoria))
        pasos += 1
    return Resultado(cadena, veredicto, tuple(instantaneas), cinta.texto())
