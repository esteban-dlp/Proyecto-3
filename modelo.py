from dataclasses import dataclass


@dataclass(frozen=True)
class Transicion:
    estado_inicial: str
    memoria_inicial: str | None
    simbolo_leido: str | None
    estado_final: str
    memoria_final: str | None
    simbolo_escrito: str | None
    desplazamiento: str


@dataclass(frozen=True)
class Maquina:
    estados: tuple[str, ...]
    estado_inicial: str
    estado_final: str
    alfabeto: tuple[str, ...]
    alfabeto_cinta: tuple[str | None, ...]
    transiciones: dict[tuple[str, str | None, str | None], Transicion]
    cadenas: tuple[str, ...]
