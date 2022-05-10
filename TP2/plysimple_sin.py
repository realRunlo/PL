import re
import ply.yacc as yacc 
from plysimple_limpo import tokens, literals 

def p_Ply(p):
    "Ply : Lexer Yc"
    p[0] = p[1] + "\n" + p[2]

def p_Lexer(p):
    "Lexer : LEX Literals Ignore Tokens Lfuncs Lerror"
    p[0] = p[2] + "\n" + p[3] +"\n" + p[4] + "\n" + p[5] + "\n" + p[6]

def p_Yc(p):
    "Yc : YACC Precedents Declarations Grammar Yfs"
    p[0] = p[2] + "\n" + p[3] + "\n" + p[4] + "\n" + p[5]

def p_Grammar(p):
    "Grammar : GRM Productions"
    p[0] = p[2]

def p_Yfs(p):
    "Yfs : YFUNCS Funcs"
    p[0] = p[2]

def p_Literals(p):
    "Literals : LTS '=' aspval"
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
    "Tokens : TKS '=' PRA Tokl PRF"
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
    "Lfunc : LFUNC rgx DS RT PA pelval ',' Tv PF "
    p[2] = re.sub(r'(\\:)',r':',p[2])
    p[0] = "def t_" + p[6][1:-1] + "(t):\n\tr'" + p[2] + "'\n" + p[8]

def p_Tv(p):
    "Tv : TVAL"
    p[0] = "\treturn t"

def p_Tv_type(p):
    "Tv : TYPE PA TVAL PF"
    p[0] = "\tt.value = " + p[1] + "(t.value)\n\treturn t"

def p_Lerror(p):
    "Lerror : ER Codes PF" #o lexer n está a apanhar tudo para o ER,rever
    p[0] = "def t_error(t):\n\tprintf(" + p[2] + ")"

def p_Lerror_empty(p):
    "Lerror : "
    p[0] = 'def t_ANY_error(t):\n\tprint(f"Illegal character \'{t.value[0]}\', [{t.lexer.lineno}]")\n\tt.lexer.skip(1)'

def p_Precedents(p):
    "Precedents : PRCD '=' PRA Prcdlist PRF"
    p[0] = "precedent = [" + p[4] + "]"

def p_Declarations(p):
    "Declarations : Declarations Declaration"
    p[0] = p[1] + p[2] + "\n"

def p_Declarations_empty(p):
    "Declarations : "
    p[0] = ""

def p_Declaration(p): #TODO: ver o que fazer com isto
    "Declaration : id '=' P"
    p[0] = p[1] + "=" + p[3]

def p_Productions(p):
    "Productions : Productions Production"
    p[0] = p[1] + p[2] + "\n"

def p_Productions_empty(p):
    "Productions : "
    p[0] = ""

def p_Production(p):
    "Production : nt DS Symbols PCA Codes PCF"
    p[0] = p[1] + ":" + p[3] + "{" + p[5] + "}"

def p_Symbols(p):
    "Symbols : Symbols S"
    p[0] = p[1] + p[2] + " "

def p_Symbols_empty(p):
    "Symbols : "
    p[0] = ""

def p_S(p):
    "S : symbol"
    p[0] = p[1]

def p_S_Prec(p):
    "S : PREC symbol"
    p[0] = "%prec " + p[2]

def p_P_pr(p): #TODO: ver o que fazer com isto
    "P : PRA PRF"
    p[0] = "[]"

def p_P_pc(p): #TODO: ver o que fazer com isto
    "P : PCA PCF"
    p[0] = "{}"

def p_Prcdlist(p):
    "Prcdlist : Prcdlist PA LTRG ',' Pelvals pelval PF ','"
    p[0] = p[1] + "(" + p[3] + "," + p[5] + p[6] + "),"

def p_Prcdlist_empty(p):
    "Prcdlist : "
    p[0] = ""

def p_Pelvals(p):
    "Pelvals : Pelvals pelval ','"
    p[0] = p[1] + p[2] + ','

def p_Pelvals_empty(p):
    "Pelvals : "
    p[0] = ""

def p_Funcs(p):
    "Funcs : Funcs Func"
    p[0] = p[1] + p[2] + "\n"

def p_Funcs_empty(p):
    "Funcs : "
    p[0] = ""

def p_Func(p):
    "Func : DEF name PA name PF PCA Codes PCF"
    p[0] = "def " + p[2] + "(" + p[4] + "):" + p[7]

def p_Codes(p):
    "Codes : Codes Code"
    p[0] = p[1] + p[2]

def p_Codes_empty(p):
    "Codes : "
    p[0] = ""

def p_Code(p):
    "Code : cod"
    p[0] = p[1]

def p_Code_p(p):
    "Code : PA Codes PF"
    p[0] = "(" + p[2] + ")"

def p_Code_pr(p):
    "Code : PRA Codes PRF"
    p[0] = "[" + p[2] + "]"

def p_Code_pc(p):
    "Code : PCA Codes PCF"
    p[0] = "{" + p[2] + "}"


def p_error(p):
    print('Erro sintático: ', p)
    parser.success = False

# Build the parser
parser = yacc.yacc()
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
