import re

LETTERS = 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ_'
NUMBERS = '0123456789'
DIGITS = '0123456789eE'

RESERVEDWORDS = [
    'and',
    'constantes',
    'hasta',
    'matriz',
    'paso',
    'registro',
    'sino',
    'vector',
    'archivo',
    'desde',
    'inicio',
    'mientras',
    'subrutina',
    'repetir',
    'tipos',
    'caso',
    'eval',
    'lib',
    'not',
    'programa',
    'retorna',
    'var',
    'const',
    'fin',
    'libext',
    'or',
    'ref',
    'si',
    'variables',
    "libext",
    "numerico",
    "cadena",
    "logico",
    "alen",
    "dim",
    "imprimir",
    "cls",
    "leer",
    "set_ifs",
    "abs",
    "arctan",
    "ascii",
    "cos",
    "dec",
    "eof",
    "exp",
    "get_ifs",
    "inc",
    "int",
    "log",
    "lower",
    "mem",
    "ord",
    "paramval",
    "pcount",
    "pos",
    "random",
    "sec",
    "set_stdin",
    "set_stdout",
    "sin",
    "sqrt",
    "str",
    "strdup",
    "strlen",
    "substr",
    "tan",
    "upper",
    "val",
    "SI",
    "NO",
    "TRUE",
    "FALSE",
]

class Error:
    def __init__(self, line, column):
        self.line = line
        self.column = column 

    def as_string(self):
        result = f'>>> Error lexico(linea:{self.line},posicion:{self.column})'
        return result
    
class IllegalCharError(Error):
    def __init__(self, line, details):
        super().__init__(line, details)

tk_ID = 'id'
tk_cadena = 'tk_cadena'
tk_numero = 'tk_numero'
tk_asignacion = 'tk_asignacion'
tk_coma = 'tk_coma'
tk_corchete_derecho = 'tk_corchete_derecho'
tk_corchete_izquierdo = 'tk_corchete_izquierdo'
tk_distinto_de = 'tk_distinto_de'
tk_division = 'tk_division'
tk_dos_puntos = 'tk_dos_puntos'
tk_igual_que = 'tk_igual_que'
tk_llave_derecha = 'tk_llave_derecha'
tk_llave_izquierda = 'tk_llave_izquierda'
tk_mayor = 'tk_mayor'
tk_mayor_igual = 'tk_mayor_igual'
tk_menor = 'tk_menor'
tk_menor_igual = 'tk_menor_igual'
tk_modulo = 'tk_modulo'
tk_multiplicacion = 'tk_multiplicacion'
tk_parentesis_derecho = 'tk_parentesis_derecho'
tk_parentesis_izquierdo = 'tk_parentesis_izquierdo'
tk_potenciacion = 'tk_potenciacion'
tk_punto = 'tk_punto'
tk_punto_y_coma = 'tk_punto_y_coma'
tk_resta = 'tk_resta'
tk_suma = 'tk_suma'

class Token:
    
    def __init__(self, type, line, column, value=None):
        self.type = type
        self.value = value
        self.line = line
        self.column = column

    def __repr__(self):
        if self.value: return f'<{self.type},{self.value},{self.line},{self.column}>'
        return f'<{self.type},{self.line},{self.column}>'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.line = 1
        self.column = -1
        self.realcolumn = 0
        self.current_char = None
        self.next_char = None
        self.advance()

    def advance(self):
        self.column += 1
        self.realcolumn += 1
        self.current_char = self.text[self.column] if self.column < len(self.text) else None
        if self.column < len(self.text)-1:
            self.next_char = self.text[self.column + 1] if self.column < len(self.text) else None

    def line_end(self):
        while self.current_char != '\n' and self.column < len(self.text):
            self.advance()

    def validDecimal(self, num_str):
        for i in range(len(num_str)):
            if num_str[i] in DIGITS + '.' + '-' + '+':
                continue
            else:
                return False
        return True

    def make_tokens(self):
        tokens = []
        #print(self.current_char)
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char in '\n':
                self.line += 1
                self.realcolumn = 0
                self.advance()
            elif self.current_char == '/' and self.next_char == '/':
                self.line_end()
            elif self.current_char == '/' and self.next_char == '*':
                error = self.make_block_comment()
                if error: return tokens, error
            elif self.current_char == '"':
                token , error = self.make_string()
                if error: return tokens, error
                tokens.append(token)
            elif self.current_char == "'":
                token , error = self.make_string2()
                if error: return tokens, error
                tokens.append(token)
            elif self.current_char in LETTERS:
                #print("Entro por LETTERS")
                tokens.append(self.make_word())
            elif self.current_char in DIGITS:
                token , error = self.make_number()
                if error: return tokens, error
                tokens.append(token)
            elif self.current_char == '=' and self.next_char == '=':
                tokens.append(Token(tk_igual_que, self.line, self.realcolumn))
                self.advance()
                self.advance()
            elif self.current_char == '=':
                tokens.append(Token(tk_asignacion, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == ',':
                tokens.append(Token(tk_coma, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == ']':
                tokens.append(Token(tk_corchete_derecho, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '[':
                tokens.append(Token(tk_corchete_izquierdo, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '<' and self.next_char == '>':
                tokens.append(Token(tk_distinto_de, self.line, self.realcolumn))
                self.advance()
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(tk_division, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == ':':
                tokens.append(Token(tk_dos_puntos, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '}':
                tokens.append(Token(tk_llave_derecha, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '{':
                tokens.append(Token(tk_llave_izquierda, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '>' and self.next_char == '=':
                tokens.append(Token(tk_mayor_igual, self.line, self.realcolumn))
                self.advance()
                self.advance()
            elif self.current_char == '>':
                tokens.append(Token(tk_mayor, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '<' and self.next_char == '=':
                tokens.append(Token(tk_menor_igual, self.line, self.realcolumn))
                self.advance()
                self.advance()
            elif self.current_char == '<':
                tokens.append(Token(tk_menor, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '%':
                tokens.append(Token(tk_modulo, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(tk_multiplicacion, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(tk_parentesis_derecho, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(tk_parentesis_izquierdo, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(tk_potenciacion, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '.':
                tokens.append(Token(tk_punto, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == ';':
                tokens.append(Token(tk_punto_y_coma, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(tk_resta, self.line, self.realcolumn))
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(tk_suma, self.line, self.realcolumn))
                self.advance()
            else:
                #print("Ñ")
                self.advance()
                return tokens, IllegalCharError(self.line,self.realcolumn -1)
            
        return tokens, None

    def make_word(self):
        wrd_str = ''
        pattern = '[a-zA-ZÑñ_][a-zA-ZÑñ0-9]*'

        while self.current_char != None and (self.current_char in LETTERS or self.current_char in NUMBERS):
            wrd_str += self.current_char 
            self.advance()
        
        if wrd_str in RESERVEDWORDS:
            return "<" + wrd_str + f",{self.line},{self.realcolumn - len(wrd_str)}>"
        elif re.search(pattern, wrd_str) and len(wrd_str) <= 32:
            return Token(tk_ID, self.line, self.realcolumn - len(wrd_str), wrd_str)

    def make_number(self):
        num_str = ''
        dot_count = 0

        while self.current_char != None and self.current_char in DIGITS + '.' + '-' + '+':
            if self.current_char == '.' and self.next_char in NUMBERS:
                if dot_count == 1: break
                dot_count += 1
                num_str += '.'
            elif self.current_char == '.' and self.next_char not in DIGITS:
                break
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(tk_numero, self.line, self.realcolumn - len(num_str), num_str), None
        elif self.validDecimal(num_str):
            return Token(tk_numero, self.line, self.realcolumn - len(num_str), num_str), None
        else:
            return None, IllegalCharError(self.line, self.realcolumn - len(num_str))

    def make_string(self):
        posible_string = '"'
        self.advance()

        while (self.current_char != None) and (self.current_char != '"'):
            if self.current_char == '\n':
                return None, IllegalCharError(self.line, self.realcolumn - len(posible_string))
            posible_string += self.current_char
            self.advance()

        if self.current_char == '"':
            posible_string += self.current_char
            self.advance()
            return Token(tk_cadena, self.line, self.realcolumn - len(posible_string), posible_string), None
        else:
            return None, IllegalCharError(self.line, self.realcolumn - len(posible_string))

    def make_string2(self):
        posible_string = "'"
        self.advance()

        while (self.current_char != None) and (self.current_char != "'"):
            if self.current_char == '\n':
                return None, IllegalCharError(self.line, self.realcolumn - len(posible_string))
            posible_string += self.current_char
            self.advance()

        if self.current_char == "'":
            posible_string += self.current_char
            self.advance()
            return Token(tk_cadena, self.line, self.realcolumn - len(posible_string), posible_string), None
        else:
            return None, IllegalCharError(self.line, self.realcolumn - len(posible_string))

    def make_block_comment(self):
        posible_comment = '/*'
        self.line_count = 0
        self.advance()
        self.advance()
        
        while (self.current_char != None) and not(self.current_char == '*' and self.next_char == '/'):
            if self.current_char == '\n':
                self.realcolumn = 0
                self.line +=1
                self.line_count += 1
            posible_comment += self.current_char
            self.advance()

        if self.current_char == '*' and self.next_char == '/':
            posible_comment += (self.current_char + self.next_char)
            self.advance()
            self.advance()
        else:
            return IllegalCharError(self.line - self.line_count, self.realcolumn)


def run(text):
    lexero = Lexer(text)
    tokens, error = lexero.make_tokens()

    return tokens, error