import ply.lex as lex
literals = ['(', ')', '+', '*', '-']
t_ignore = "\t\n "
tokens = ['num']

def t_num(t):
	r'\d+ '
	t.value = int(t.value)
	return t
def t_ANY_error(t):
	print(f"Illegal character '{t.value[0]}', [{t.lexer.lineno}]")
	t.lexer.skip(1)

lexer = lex.lex()

import ply.yacc as yacc




def p_Z(p):
	"Z : Sexp "
	print(p[1])

def p_Sexp(p):
	"Sexp : '(' '+' Lista ')' "
	p[0]= somatorio(p[3])

def p_Sexp_1(p):
	"Sexp : '(' '*' Lista ')' "
	p[0]= produtorio(p[3])

def p_Sexp_2(p):
	"Sexp : num "
	p[0]= p[1]

def p_Lista(p):
	"Lista : Lista Sexp "
	p[0]= p[1]+ [p[2]]

def p_Lista_1(p):
	"Lista : Sexp Sexp "
	p[0]= [p[1],p[2]]


def somatorio(lista):
    res = 0
    for n in lista:
        res += n
    return res

def produtorio(lista):
    res = 1
    for n in lista:
        res *= n
    return res



parser = yacc.yacc()
parser.parse("(+ 1 2)")