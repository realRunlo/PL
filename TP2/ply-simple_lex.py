from lib2to3.pgen2 import literals
from re import T
import ply.lex as lex
import sys

states = [('REGEX','exclusive')]

literals = ['=',',','[',']','(',')']

tokens = ["LX","LT","IG","TK","RGX","YC","DOTS","RT","TVALUE","PCF","TYPE","aspval","pelval","str"]

t_ignore = "\t\n "

def t_LX(t):
    r"LEX:"
    return t

def t_LT(t):
    r"literals"
    return t

def t_IG(t):
    r"ignore"
    return t

def t_TK(t):
    r"tokens"
    return t

def t_RT(t):
    r"return"
    return t

def t_TVALUE(t):
    r"t.value"
    return t

def t_TYPE(t):
    r"float"
    return t

def t_LFUNC(t):
    r"lfunc:"
    t.lexer.begin('REGEX')

def t_REGEX_PCA(t):
    r"{"
    t.lexer.begin('INITIAL')


def t_PCF(t):
    r"}"
    return t

def t_YC(t):
    r"YACC"
    return t

def t_REGEX_DOTS(t):
    r":"
    t.lexer.begin('INITIAL')

def t_REGEX_RGX(t):
    r"((\\:)|[^:])+"
    return t

def t_aspval(t):
    r"\"[^0-9\n]+\"" #n percebo porque é que se puser \n funciona..
    return t

def t_pelval(t):
    r"'[A-Za-z]+'"
    return t



def t_error(t):
    print(f"Illegal character ’{t.value[0]}’, [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()
file = sys.stdin.read()

lexer.input(file)
for tok in lexer:
    print(tok)
