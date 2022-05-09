from lib2to3.pgen2 import literals
from re import T
import re
import ply.lex as lex
import sys

states = [('REGEX','exclusive'),('GRAMMAR','exclusive'),('CODIGO','exclusive'),('YFUNC','exclusive'),('ARGS','exclusive')]

literals = ['=',',','[',']']

tokens = ["LX","LT","IG","TK","RGX","YC","DOTS","RT","TVALUE","PA","PF","PCA","PCF","TYPE","aspval","pelval","str","DEC"
,"PRECEDENT","PREC","LEFT","RIGHT","ID","NT","T","grammar","yfuncs","L","ER","cod","LFUNC","DEF","FUNC","arg"]

t_INITIAL_REGEX_GRAMMAR_CODIGO_YFUNC_ARGS_ignore = "\t\n "

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

def t_DEC(t):
    r"declatarion:"
    return t

def t_PRECEDENT(t):
    r"precedend"
    return t

def t_GRAMMAR_PREC(t):
    r"%prec"
    return t

def t_LEFT(t):
    r"'left'"
    return t

def t_RIGHT(t):
    r"'right'"
    return t

def t_grammar(t):
    r"grammar:"
    t.lexer.push_state('GRAMMAR')
    return t

def t_INITIAL_DEF(t):
    r"def"
    t.lexer.push_state('YFUNC')
    return t

def t_YFUNC_DEF(t):
    r"def"
    return t

def t_YFUNC_FUNC(t):
    r"[a-z][\w_]*"
    return t

def t_ARGS_arg(t):
    r"[a-z]+"
    return t

def t_TYPE(t):
    r"(float)|(int)|(double)"
    return t

def t_LFUNC(t):
    r"lfunc:"
    t.lexer.push_state('REGEX')
    return t

def t_REGEX_PCA(t):
    r"{"
    t.lexer.pop_state()
    return t

def t_GRAMMAR_YFUNC_CODIGO_PCA(t):
    r"{"
    t.lexer.push_state('CODIGO')
    return t

def t_CODIGO_PCF(t):
    r"}"
    t.lexer.pop_state()
    return t

def t_PCA(t):
    r"{"
    return t

def t_PCF(t):
    r"}"
    return t

def t_INITIAL_PA(t):
    r"\("
    return t

def t_YFUNC_PA(t):
    r"\("
    t.lexer.push_state('ARGS')
    return t

def t_ARGS_PF(t):
    r"\)"
    t.lexer.pop_state()
    return t

def t_INITIAL_YFUNC_PF(t):
    r"\)"
    return t

def t_YC(t):
    r"YACC:"
    return t

def t_GRAMMAR_yfuncs(t):
    r"yfuncs:"
    t.lexer.pop_state()
    return t

def t_REGEX_DOTS(t):
    r":"
    t.lexer.pop_state()
    return t

def t_INITIAL_GRAMMAR_DOTS(t):
    r":"
    return t

def t_YFUNCS_DOTS(t):
    r":\n"
    return t

def t_REGEX_RGX(t):
    r"((\\:)|[^:])+"
    return t

def t_aspval(t):
    r"\"[^0-9\n]+\"" #n percebo porque é que se puser \n funciona..
    return t

def t_pelval(t):
    r"'[^']+'"
    return t

def t_ER(t):
    r"error([^)]*)"
    return t

def t_GRAMMAR_NT(t):
    r"[a-z]+"
    return t

def t_GRAMMAR_T(t):
    r"[A-Z]+"
    return t

def t_GRAMMAR_L(t):
    r"'.'"
    return t

def t_ID(t):
    r"[A-Za-z]+"
    return t

def t_CODIGO_cod(t):
    r"([^{}])+"
    return t

def t_YFUNC_cod(t):
    r"\t[^\n]+\n"
    return t

def t_INITIAL_REGEX_CODIGO_GRAMMAR_YFUNC_error(t):
    print(f"Illegal character ’{t.value[0]}’, [{t.lexer.lineno}]")
    t.lexer.skip(1)

lexer = lex.lex()

