# Proyecto 3: simulador de máquinas de Turing

Proyecto en parejas para Teoría de la Computación. El simulador lee una máquina de Turing de una cinta desde un archivo YAML, ejecuta cada cadena de la configuración y muestra las descripciones instantáneas (IDs), la cinta final y si la cadena fue aceptada o rechazada.

## Preparación

Requiere Python 3.10 o superior y PyYAML.

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```

## Uso

Desde la raíz del proyecto, indique la ruta del YAML:

```sh
python simulador.py maquinas/reconocedora.yaml
python simulador.py maquinas/alteradora.yaml
```

Opcionalmente, puede limitar el número de pasos por cadena con `--limite-pasos` (predeterminado: 10000):

```sh
python simulador.py maquinas/reconocedora.yaml --limite-pasos 500
```

Por cada cadena de `simulation_strings` se imprime:

- una línea `Paso n | estado | memoria | cabezal` con el estado, la memoria y la posición del cabezal (la primera celda de la entrada es la posición 0);
- una línea `ID` con la descripción instantánea, donde el estado aparece entre `<>` justo antes del símbolo que está bajo el cabezal y el blanco se muestra como `_`;
- la cinta final y el resultado.

El resultado puede ser:

- **aceptada**: la máquina llegó al `final` del YAML;
- **rechazada**: no hay una transición aplicable y todavía no se llegó al estado final;
- **indeterminado**: se alcanzó el límite de pasos sin llegar al estado final. No es un rechazo, porque la máquina podría seguir y aceptar después.

Si el YAML tiene errores, el programa muestra el problema en la salida de error y termina con código 1.

## Archivos

- `simulador.py`: punto de entrada por línea de comandos; carga la máquina, ejecuta cada cadena y muestra el resultado
- `motor.py`: simulación general (`simular`), con las descripciones instantáneas y el veredicto
- `cinta.py`: clase `Cinta`, que guarda solo las celdas ocupadas y puede crecer hacia ambos lados
- `modelo.py`: estructuras `Maquina` y `Transicion`
- `lector.py`: `cargar_maquina(ruta)` lee el YAML, lo valida y devuelve una `Maquina`; ante un error lanza `ErrorConfiguracion`
- `maquinas/reconocedora.yaml`: reconoce el lenguaje a^n b^n con n ≥ 1
- `maquinas/alteradora.yaml`: invierte la cadena de entrada dentro de la cinta
- `tests/`: pruebas del lector, la cinta, el motor, la alteradora y el programa principal

## Formato del YAML

El lector respeta los nombres de campos del YAML del enunciado. Como el ejemplo del documento lista en `tape_alphabet` únicamente símbolos adicionales, el alfabeto efectivo de la cinta es la unión de ese campo, `alphabet` y `null` (blanco). Los estados deben escribirse entre comillas para que YAML los interprete como cadenas.

La memoria inicial es `None`: cada transición se busca con `(estado, memoria, símbolo leído)` y actualiza la memoria con el valor de salida. Los movimientos son `L`, `R` y `S`. La cinta empieza con la cadena en las celdas 0 a n-1 y el resto son blancos.

## Máquina alteradora

`maquinas/alteradora.yaml` invierte la cadena dentro de la misma cinta, sin convertirla en blancos. Usa seis estados y 23 transiciones, y aprovecha la memoria para llevar un símbolo de un lado a otro:

1. Busca el primer símbolo `a` o `b` sin procesar, lo borra de la cinta y lo guarda en la memoria como `A` o `B`.
2. Regresa al inicio de la parte procesada, que está formada por las marcas `A` y `B`.
3. Corre cada marca una celda a la derecha: en cada celda entra el símbolo guardado y sale el que estaba ahí. Así el símbolo nuevo queda al inicio de la parte procesada.
4. Repite hasta que no quedan símbolos sin procesar y luego convierte las marcas de nuevo en `a` y `b`.

Por ejemplo, `ab` pasa por `A` y luego `BA`, y termina en `ba`.

## Video

Enlace al video del proyecto: https://uvggt-my.sharepoint.com/:f:/r/personal/vil24033_uvg_edu_gt/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fvil24033%5Fuvg%5Fedu%5Fgt%2FDocuments%2F6o%2E%20Semestre%2FTDLC%2FVideo%20Proyecto%203&share=cgpUf9DYRQXmSZJNOjdVdoWGEgUCrOpGU6l70BdjV6SaC0fqrQ

## Casos para el video

Reconocedora: acepta `aaabbb` y `aaaabbbb`; rechaza `aabbb` y `ababab`. Todos tienen al menos cinco caracteres.

Alteradora: invierte `aabba`, `bbbaab`, `abaabb` y `ababbb`. Todos tienen al menos cinco caracteres. La cinta final de cada una es la cadena al revés (`abbaa`, `baabbb`, `bbaaba` y `bbbaba`).

Ejecute `python simulador.py maquinas/reconocedora.yaml` o `python simulador.py maquinas/alteradora.yaml` para mostrar cada caso.
