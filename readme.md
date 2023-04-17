# Analizador Léxico, Sintáctico Y Semántico en Python.

### Gramatica.
- programa      ➯ declaraciones
- declaraciones ➯ declaraciones declaracion | declaracion
- declaracion   ➯ IDENTIFICADOR = expresion
- expresion     ➯ expresion + termino | expresion - termino | termino
- termino       ➯ termino * factor | termino / factor | factor
- factor        ➯ ENTERO | IDENTIFICADOR | ( expresion )