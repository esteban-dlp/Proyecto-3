DESPLAZAMIENTOS = {'L': -1, 'R': 1, 'S': 0}
TEXTO_BLANCO = '_'


class Cinta:
    def __init__(self, contenido=''):
        # solo se guardan las celdas ocupadas para que la cinta pueda crecer hacia ambos lados
        self._celdas = {posicion: simbolo for posicion, simbolo in enumerate(contenido)}
        self.cabezal = 0

    def leer(self):
        return self._celdas.get(self.cabezal)

    def escribir(self, simbolo):
        if simbolo is None:
            self._celdas.pop(self.cabezal, None)
        else:
            self._celdas[self.cabezal] = simbolo

    def mover(self, desplazamiento):
        self.cabezal += DESPLAZAMIENTOS[desplazamiento]

    def simbolo_en(self, posicion):
        return self._celdas.get(posicion)

    def texto(self, estado=None):
        # muestra el tramo entre la celda ocupada mas a la izquierda y la mas a la derecha
        # si se pasa un estado se inserta antes de la celda del cabezal como en una descripcion instantanea
        posiciones = list(self._celdas)
        if estado is not None:
            posiciones.append(self.cabezal)
        if not posiciones:
            return ''
        partes = []
        for posicion in range(min(posiciones), max(posiciones) + 1):
            if estado is not None and posicion == self.cabezal:
                partes.append(f'<{estado}>')
            simbolo = self.simbolo_en(posicion)
            partes.append(TEXTO_BLANCO if simbolo is None else simbolo)
        return ''.join(partes)
