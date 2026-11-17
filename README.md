# Proyecto 3: simulador de máquinas de Turing

Proyecto en parejas para Teoría de la Computación. El repositorio contiene la primera parte: lector y validación de archivos YAML, modelo de datos y una máquina reconocedora. El motor de simulación y la máquina alteradora quedan pendientes de integración.

## Preparación

Requiere Python 3.10 o superior y PyYAML.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Archivos

- `modelo.py`: estructuras `Maquina` y `Transicion`
- `lector.py`: `cargar_maquina(ruta)` lee el YAML, lo valida y devuelve una `Maquina`; ante un error lanza `ErrorConfiguracion`
- `maquinas/reconocedora.yaml`: reconoce el lenguaje a^n b^n con n ≥ 1
- `tests/test_lector.py`: pruebas del lector y de las transiciones de la reconocedora
- `PROMPT_COMPANERO.md`: contrato de integración y tareas pendientes

El lector respeta los nombres de campos del YAML del enunciado. Como el ejemplo del documento lista en `tape_alphabet` únicamente símbolos adicionales, el alfabeto efectivo de la cinta es la unión de ese campo, `alphabet` y `null` (blanco). Los estados deben escribirse entre comillas para que YAML los interprete como cadenas.

La memoria inicial se considera `None`: cada transición se busca con `(estado, memoria, símbolo leído)` y actualiza la memoria con el valor de salida. Los movimientos son `L`, `R` y `S`. La reconocedora no usa la memoria, por lo que sus valores son `null`.

## Casos para el video

Reconocedora: acepta `aaabbb` y `aaaabbbb`; rechaza `aabbb` y `ababab`. Todos tienen al menos cinco caracteres. Falta ejecutar estos casos con el motor completo y crear una máquina alteradora con cuatro cadenas de la longitud indicada.
