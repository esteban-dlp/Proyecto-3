# Tareas para integrar el simulador

Estamos desarrollando un simulador general de máquinas de Turing de una cinta para el Proyecto 3 de Teoría de la Computación. Ya están implementados el lector YAML (`lector.py`), las estructuras (`modelo.py`), y la máquina reconocedora (`maquinas/reconocedora.yaml`). Lee primero estos archivos y el enunciado del proyecto.

Tu parte consiste en:

1. Implementar la cinta y el motor de simulación general, sin codificar una máquina específica en el motor.
2. Tomar una `Maquina` obtenida con `cargar_maquina(ruta)` y ejecutar cada cadena de `maquina.cadenas` desde una cinta y configuración iniciales independientes.
3. Al iniciar usa `maquina.estado_inicial`, memoria `None`, cabezal en la primera celda y blanco `None` fuera de la entrada. Busca en `maquina.transiciones` por `(estado_actual, memoria_actual, simbolo_leido)`; la transición indica estado, memoria y símbolo nuevos y desplazamiento `L`, `R` o `S`. La cinta debe crecer en ambas direcciones.
4. Mostrar la descripción instantánea inicial y la de cada paso, incluyendo estado y posición del cabezal; mostrar la cinta final y el resultado aceptado o rechazado. Acepta al llegar a `maquina.estado_final`. Si no hay transición y aún no se ha aceptado, rechaza. Si agregas un límite de pasos, reporta un resultado indeterminado, no rechazo.
5. Diseñar en otro YAML una máquina alteradora de una cinta y preparar cuatro cadenas de al menos cinco caracteres. No vale una máquina que solo convierta toda la cinta en blancos. Escribir pruebas del motor y de la alteradora.
6. Crear una interfaz de ejecución que reciba la ruta del YAML y documentar su uso en README. Revisar con Esteban la integración y los casos del video.

La reconocedora existente espera aceptar `aaabbb` y `aaaabbbb`, y rechazar `aabbb` y `ababab`. Ejecuta también `python -m unittest discover -s tests -v`. Conserva los campos y contratos existentes o acuerda cambios antes de hacerlos. No hagas commits: Esteban los hará al final.
