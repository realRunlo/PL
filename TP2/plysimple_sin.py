import re
import ply.yacc as yacc 
from plysimple_lex import tokens, literals 

def p_Ply(p):
    "Ply : Lex"
    p[0] = p[1]

def p_Lex(p):
    "Lex : LX Literals Ignore Tokens Lfuncs Lfuncerror"
    p[0] = p[2] + "\n" + p[3] +"\n" + p[4] + "\n" + p[5] + "\n" + p[6]

def p_Literals(p):
    "Literals : LT '=' aspval"
    p[3] = p[3][1:-1] #remove as aspas
    lits = [char for char in p[3]] #transforma a string numa lista de chars
    p[0] = "literals = " + str(lits)

def p_Literals_empty(p):
    "Literals : "
    p[0] = ""

def p_Ignore(p):
    "Ignore : IG '=' aspval"
    p[0] = "t_ignore = " + p[3]

def p_Ignore_empty(p):
    "Ignore : "
    p[0] = ""

def p_Tokens(p):
    "Tokens : TK '=' '[' Tokl ']'"
    p[0] = "tokens = " + str(p[4])

def p_Tokl(p):
    "Tokl : Tokl ',' pelval"
    p[0] = p[1] + [p[3][1:-1]]

def p_Tokl_single(p):
    "Tokl : pelval"
    p[0] = [p[1][1:-1]]

def p_Lfuncs(p):
    "Lfuncs : Lfuncs Lfunc"
    p[0] = p[1] + "\n" + p[2]


def p_Lfuncs_empty(p):
    "Lfuncs : "
    p[0] = ""

def p_Lfunc(p):
    "Lfunc : LFUNC RGX DOTS RT PA pelval ',' Tval PF "
    p[2] = re.sub(r'(\\:)',r':',p[2])
    p[0] = "def t_" + p[6][1:-1] + "(t):\n\tr'" + p[2] + "'\n" + p[8]

def p_Tval(p):
    "Tval : TVALUE"
    p[0] = "\treturn t"

def p_Tval_type(p):
    "Tval : TYPE PA TVALUE PF"
    p[0] = "\tt.value = " + p[1] + "(t.value)\n\treturn t"

def p_Lfuncerror(p):
    "Lfuncerror : LFUNC RGX DOTS ER Codigos PF" #o lexer n está a apanhar tudo para o ER,rever
    p[0] = "def t_error(t):\n\tprintf(" + p[5] + ")"

def p_Lfuncerror_empty(p):
    "Lfuncerror : "
    p[0] = 'def t_ANY_error(t):\n\tprint(f"Illegal character \'{t.value[0]}\', [{t.lexer.lineno}]")\n\tt.lexer.skip(1)'

def p_Codigos(p):
    "Codigos : Codigos Codigo"
    p[0] = p[1] + p[2]

def p_Codigos_empty(p):
    "Codigos : "
    p[0] = ""

def p_Codigo(p):
    "Codigo : cod"
    p[0] = p[1]

def p_Codigo_pc(p):
    "Codigo : PCA Codigo PCF"
    p[0] = "{" + p[1] + "}"

def p_Codigo_p(p):
    "Codigo : PA Codigo PF"
    p[0] = "(" + p[1] + ")"

def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

# Read line from input and parse it
import sys
parser.success = True

file = open("t.txt","r",encoding="utf-8",errors="surrogateescape")
program = file.read()
codigo = parser.parse(program)
if parser.success:
    print("Programa estruturalmente correto!")
    print(codigo)
else:
    print("Programa com erros... Corrija e tente novamente!")
