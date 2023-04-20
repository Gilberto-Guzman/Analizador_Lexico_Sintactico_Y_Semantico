import re

Test_Analizador_Sintactico = True
Test_Analizador_Semantico = True
# --- ANALIZADOR LEXICO ---

class Token:
    def __init__(self, tipo, valor=None):
        self.tipo = tipo
        self.valor = valor

class Lexer:
    def __init__(self, codigo):
        self.codigo = codigo
        self.posicion = 0
        self.tokens = []

    def obtener_tokens(self):
        while self.posicion < len(self.codigo):
            if self.codigo[self.posicion].isdigit():
                self.obtener_numero()
            elif self.codigo[self.posicion].isalpha():
                self.obtener_variable()
            elif self.codigo[self.posicion] in "+-*/()=":
                self.obtener_operador()
            elif self.codigo[self.posicion] == "#":
                self.obtener_comentario()
            else:
                self.posicion += 1

        return self.tokens

    def obtener_numero(self):
        numero = ""
        while self.posicion < len(self.codigo) and self.codigo[self.posicion].isdigit():
            numero += self.codigo[self.posicion]
            self.posicion += 1
        self.tokens.append(Token("ENTERO", int(numero)))

    def obtener_variable(self):
        variable = ""
        while self.posicion < len(self.codigo) and (self.codigo[self.posicion].isalnum() or self.codigo[self.posicion] == "_"):
            variable += self.codigo[self.posicion]
            self.posicion += 1
        self.tokens.append(Token("IDENTIFICADOR", variable))

    def obtener_operador(self):
        operador = self.codigo[self.posicion]
        self.tokens.append(Token(operador))
        self.posicion += 1

    def obtener_comentario(self):
        while self.posicion < len(self.codigo) and self.codigo[self.posicion] != "\n":
            self.posicion += 1

# --- ANALIZADOR SINTACTICO ---

class Analizador:
    def __init__(self, tokens):
        self.tokens = tokens
        self.posicion = 0

    def analizar(self):
        declaraciones = []
        while self.posicion < len(self.tokens):
            declaraciones.append(self.declaracion())
        return declaraciones

    def declaracion(self):
        identificador = self.esperar("IDENTIFICADOR").valor
        self.esperar("=")
        expresion = self.expresion()
        return (identificador, expresion)

    def expresion(self):
        termino = self.termino()
        while self.posicion < len(self.tokens) and self.tokens[self.posicion].tipo in ("+", "-"):
            operador = self.tokens[self.posicion].tipo
            self.posicion += 1
            siguiente_termino = self.termino()
            termino = (operador, termino, siguiente_termino)
        return termino

    def termino(self):
        factor = self.factor()
        while self.posicion < len(self.tokens) and self.tokens[self.posicion].tipo in ("*", "/"):
            operador = self.tokens[self.posicion].tipo
            self.posicion += 1
            siguiente_factor = self.factor()
            factor = (operador, factor, siguiente_factor)
        return factor

    def factor(self):
        if self.tokens[self.posicion].tipo == "ENTERO":
            valor = self.tokens[self.posicion].valor
            self.posicion += 1
            return valor
        elif self.tokens[self.posicion].tipo == "IDENTIFICADOR":
            identificador = self.tokens[self.posicion].valor
            self.posicion += 1
            return identificador
        elif self.tokens[self.posicion].tipo == "(":
            self.posicion += 1
            expresion = self.expresion()
            self.esperar(")")
            return expresion
        else:
            # raise Exception("Error de sintaxis")
            global Test_Analizador_Sintactico
            Test_Analizador_Sintactico = False
            print("Error de sintaxis")

    def esperar(self, tipo):
        if self.posicion < len(self.tokens) and self.tokens[self.posicion].tipo == tipo:
            token = self.tokens[self.posicion]
            self.posicion += 1
            return token
        else:
            # raise Exception(f"Se esperaba un token de tipo {tipo}")
            global Test_Analizador_Sintactico
            Test_Analizador_Sintactico = False
            print(f"Se esperaba un token de tipo {tipo}")

# --- ANALIZADOR SEMANTICO ---

class AnalizadorSemantico:
    def __init__(self, declaraciones):
        self.declaraciones = declaraciones

    def analizar(self):
        variables = set()
        for declaracion in self.declaraciones:
            identificador, expresion = declaracion
            self.verificar_variables(expresion, variables)
            variables.add(identificador)

    def verificar_variables(self, expresion, variables):
        if isinstance(expresion, tuple):
            operador, izquierda, derecha = expresion
            self.verificar_variables(izquierda, variables)
            self.verificar_variables(derecha, variables)
        elif isinstance(expresion, str) and expresion not in variables:
            # raise Exception(f"Variable no declarada: {expresion}")
            global Test_Analizador_Semantico 
            Test_Analizador_Semantico = False
            print(f"Variable no declarada: {expresion}")

codigo = """
x = 2
y { x + 3
z = (x + y) * 4
"""
lexer = Lexer(codigo)
tokens = lexer.obtener_tokens()
analizador = Analizador(tokens)
declaraciones = analizador.analizar()
analizador_semantico = AnalizadorSemantico(declaraciones)
analizador_semantico.analizar()

if Test_Analizador_Sintactico == True:
    print('Analisis Sintactico Exitoso')
if Test_Analizador_Semantico == True:
    print('Analisis Semantico Exitoso')
