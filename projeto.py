import re
import statistics
import ply.lex as lex

def str_to_list (str):
    return [int(s) for s in str.split(',')]

def str_to_sum (str):
    return sum([int(s) for s in str.split(',')])

def str_to_media (str):
    return statistics.mean([int(s) for s in str.split(',')])

tokens = ["LISTA","SEPARADOR","NOME"]

def t_LISTA(t):
    r'(([^,\n]+)|("[^"]+"))\{\d+(,\d+)?\}(::\w+)?'
    q_min = 0
    q_max = 0
    m = re.match(r'(?P<nome>([^,\n]+)|(\"[^"]+"))\{(?P<q_min>\d)(,(?P<q_max>\d))?\}(?P<funcao>::\w+)?',t.value)
    if(m.group("nome")):
        t.value = m.group("nome")
    if(m.group("funcao")):
        lexer.funcoes.append((t.value,m.group("funcao")))
    else: lexer.funcoes.append((t.value,"normal"))
    if(m.group("q_min")):
        q_min = int(m.group("q_min"))
    if(m.group("q_max")):
        q_max = int(m.group("q_max"))
    lexer.exp = lexer.exp + r'(?P<' + t.value+ r'>'
    for i in range(q_min-1):
        lexer.exp = lexer.exp + r'\d+,'
    lexer.exp = lexer.exp + r'\d+'
    for i in range(q_min,q_max):
        lexer.exp = lexer.exp + r',(\d+)?'
    lexer.separator = False
    lexer.exp = lexer.exp + r')'
    return t

def t_NOME(t):
    r'([^,\n]+)|("[^"]+")'
    lexer.exp = lexer.exp + r'(?P<' + t.value + r'>([^,\n]+)|("[^"]+"))'
    lexer.separator = False
    return t

def t_SEPARADOR(t):
    r','
    if(not(lexer.separator)): 
        lexer.exp = lexer.exp + r','
        lexer.separator = True
    return t

t_ignore = "\n"

def t_ANY_error(t):
    print("Illegal Character")

lexer = lex.lex()
lexer.funcoes = []
lexer.exp = r''
lexer.separator = False
lexer.i = 0

file = open("texto.csv","r",encoding="utf-8")

header = file.readline()

lexer.input(header)
for tok in lexer:
    pass

if lexer.exp[-1] == ",":
    lexer.exp = lexer.exp[:-1]

#print(lexer.funcoes)

#lexer.exp = lexer.exp + r'$'

exp = re.compile(lexer.exp)
i = 0

content = file.read()

"""
for l in file:
    print(l[:-1])
    print(lexer.exp)
    m = exp.match(l)
    if(m):
        dict = m.groupdict()
        for lista in lexer.funcoes:
            if(lista[1] == "normal"):
                dict[lista[0]] = str_to_list(dict[lista[0]])
            elif(lista[1]=="::sum"):
                dict[lista[0]] = str_to_sum(dict[lista[0]])
            elif(lista[1]=="::media"):
                dict[lista[0]] = str_to_media(dict[lista[0]])
            i+=1
        print(dict)
"""
print(lexer.exp)
mos = exp.finditer(content)
for mo in mos:
    dict = mo.groupdict()
    for tuplo in lexer.funcoes:
            funcao = tuplo[1]
            nome = tuplo[0]
            if(funcao == "normal"):
                dict[nome] = str_to_list(dict[nome])
            elif(funcao == "::sum"):
                dict[nome] = str_to_sum(dict[nome])
            elif(funcao == "::media"):
                dict[nome] = str_to_media(dict[nome])
            i+=1
    print(dict)
file.close()