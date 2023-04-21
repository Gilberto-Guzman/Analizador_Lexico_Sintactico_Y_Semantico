
# Interfaz Grafica
import tkinter
import customtkinter

# Multimedia
import os
from PIL import Image

# Activamos el modo claro
customtkinter.set_appearance_mode("light")

Test_Analizador_Sintactico = True
Test_Analizador_Semantico = True
Texto_Concatenado = ""

class Analizador_Lexico_Sintactico_Y_Semantico(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Definimos el titulo y el tamaño de la ventana
        self.title("Analizador Léxico, Sintáctico y Semántico")
        
        # Definimos el tamaño de la ventana
        self.geometry(f"{800}x{600}")

        # Desactivamos el redimensionamiento de la ventana
        self.resizable(False, False)

        # Centramos la pantalla
        ancho_pantalla = self.winfo_screenwidth()
        largo_pantalla = self.winfo_screenheight()
        x = int((ancho_pantalla - 800) / 2)
        y = int((largo_pantalla - 600) / 2)
        self.geometry(f"+{x}+{y}")


        # Creamos una ruta relativa para las imagenes
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "imgs")

        # Cargamos las imagenes
        self.img_analizar = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "analizar.png")), size=(120, 120)
        )
        self.img_limpiar = customtkinter.CTkImage(
            Image.open(os.path.join(image_path, "limpiar.png")), size=(120, 120)
        )

        # Creamos el cuadro de texto
        self.textbox = customtkinter.CTkTextbox(
            master=self,
            font=("Helvetica", 32),
            width=500, 
        )
        # Lo posicionamos
        self.textbox.place(relx=0.5, rely=0.25, anchor=tkinter.CENTER)
        
        # Le agregamos por defecto un texto de prueba
        self.textbox.insert(
            "0.0", 
            "x = 2\ny = x + 3\nz = (x + y) * 4"
        )


        # Botones
        self.btn_analizar = customtkinter.CTkButton(
            master=self,
            text="Analizar",
            font=("Helvetica", 32),
            image=self.img_analizar,
            text_color="white",
            fg_color="#3BE772",
            hover_color="#41AB63",
            compound="top",
            command=self.analizador_consola,
        )
        self.btn_analizar.place(relx=0.275, rely=0.63, anchor=tkinter.CENTER)

        self.btn_limpiar = customtkinter.CTkButton(
            master=self,
            text="Limpiar",
            font=("Helvetica", 32),
            image=self.img_limpiar,
            text_color="white",
            fg_color="#FD4040",
            hover_color="#C63333",
            compound="top",
            command=self.limpiar_textbox,
        )
        self.btn_limpiar.place(relx=0.725, rely=0.63, anchor=tkinter.CENTER)      

        self.label_resultados = customtkinter.CTkLabel(
            master=self,
            text="Resultados",
            text_color="white",
            font=("Helvetica", 32),
            fg_color="#10C2DE",
            corner_radius=10
        )
        self.label_resultados.place(relx=0.5, rely=0.9, anchor=tkinter.CENTER)
       
    def analizador_consola(self):

        
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
                    print("Error de sintaxis")
                    global Texto_Concatenado
                    Texto_Concatenado += "Error de sintaxis\n" 
                    return Texto_Concatenado                  
            
            def esperar(self, tipo):
                if self.posicion < len(self.tokens) and self.tokens[self.posicion].tipo == tipo:
                    token = self.tokens[self.posicion]
                    self.posicion += 1
                    return token
                else:
                    # raise Exception(f"Se esperaba un token de tipo {tipo}")
                    global Test_Analizador_Sintactico 
                    Test_Analizador_Sintactico = False
                    global Texto_Concatenado
                    Texto_Concatenado += f"Se esperaba un token de tipo {tipo}\n"
                    print(f"Se esperaba un token de tipo {tipo}")
                    return Test_Analizador_Sintactico, Texto_Concatenado
    

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
                    global Texto_Concatenado
                    print(f"Variable no declarada: {expresion}")
                    Texto_Concatenado += f"Variable no declarada: {expresion}"
                    return Test_Analizador_Semantico, Texto_Concatenado

        # codigo = """
        # x = 2
        # y = x + 3
        # z = (x + y) * 4
        # """
        codigo = self.textbox.get("1.0", tkinter.END).strip()
        lexer = Lexer(codigo)
        tokens = lexer.obtener_tokens()
        analizador = Analizador(tokens)
        declaraciones = analizador.analizar()
        analizador_semantico = AnalizadorSemantico(declaraciones)
        analizador_semantico.analizar()
        global Texto_Concatenado 
        if Test_Analizador_Sintactico == True:
            print('Analisis Sintactico Exitoso')
            Texto_Concatenado += 'Analisis Sintactico Exitoso\n'
        if Test_Analizador_Semantico == True:
            print('Analisis Semantico Exitoso')
            Texto_Concatenado += 'Analisis Semantico Exitoso\n'
        self.label_resultados.configure(text=Texto_Concatenado)
        
        
    def limpiar_textbox(self):
        self.textbox.delete("1.0", "end")
        self.label_resultados.configure(text="Resultados")

if __name__ == "__main__":
    app = Analizador_Lexico_Sintactico_Y_Semantico()
    app.mainloop()
