import re
import ply.yacc as yacc 
from plysimple_lex import tokens, literals 

def p_Ply(p):
    "Ply : Lex"
    p[0] = p[1]

def p_Lex(p):
    "Lex : LX Literals Ignore Tokens Lfuncs"
    p[0] = p[2] + "\n" + p[3] +"\n" + p[4] + "\n" + p[5]

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
    p[0] = p[1] + [p[3]]

def p_Tokl_single(p):
    "Tokl : pelval"
    p[0] = [p[1]]

def p_Lfuncs(p):
    "Lfuncs : Lfuncs Lfunc"
    p[0] = ""


def p_Lfuncs_empty(p):
    "Lfuncs : "
    p[0] = ""


def p_Lfunc(p):
    "Lfunc : LFUNC RGX DOTS RT PA pelval ',' TVALUE PF "
    p[0] = ""


def p_Lfunc_type(p):
    "Lfunc : LFUNC RGX DOTS RT PA pelval ',' TYPE PA TVALUE PF PF"
    p[0] = ""


def p_Lfunc_error(p):
    "Lfunc : LFUNC RGX DOTS ER PF " #o lexer n está a apanhar tudo para o ER,rever
    p[0] = ""




def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()

# Read line from input and parse it
import sys
parser.success = True
program = sys.stdin.read()
codigo = parser.parse(program)
if parser.success:
    print("Programa estruturalmente correto!")
    print(codigo)
else:
    print("Programa com erros... Corrija e tente novamente!")
