import re
import statistics
import sys
import ply.lex as lex

def str_to_list (str):
    return [int(s) for s in str.split(',')]

def str_to_sum (str):
    return sum([int(s) for s in str.split(',')])

def str_to_media (str):
    return statistics.mean([int(s) for s in str.split(',')])

def increment_str(str):
    if(ord(str[0]) < 122):
        str = chr(ord(str[0])+1) + str[1:]
    else:
        str = "a" + str[0:]
    return str

def change_name(csv):
    json = re.sub(r'(\w+\.)(CSV|csv)',r'\1json',csv)
    print(json)
    return json

tokens = ["LISTA","SEPARADOR","NOME"]

def t_LISTA(t):
    r'(([^",\n]+)|("[^"]+"))\{\d+(,\d+)?\}(::\w+)?'
    q_min = 0
    q_max = 0
    m = re.match(r'(?P<nome>([^",\n]+)|(\"[^"]+"))\{(?P<q_min>\d)(,(?P<q_max>\d))?\}(?P<funcao>::\w+)?',t.value)
    if(m.group("nome")):
        t.value = m.group("nome")
    if(m.group("funcao")):
        lexer.content.append((lexer.i,m.group("funcao"),t.value))
    else: lexer.content.append((lexer.i,"::",t.value))
    if(m.group("q_min")):
        q_min = int(m.group("q_min"))
    if(m.group("q_max")):
        q_max = int(m.group("q_max"))
    lexer.exp = lexer.exp + r'(?P<' + lexer.i + r'>'
    for i in range(q_min-1):
        lexer.exp = lexer.exp + r'\d+,'
    lexer.exp = lexer.exp + r'\d+'
    for i in range(q_min,q_max):
        lexer.exp = lexer.exp + r',(\d+)?'
    lexer.separator = False
    lexer.exp = lexer.exp + r')'
    lexer.i = increment_str(lexer.i)
    return t

def t_NOME(t):
    r'([^",\n]+)|("[^"]+")'
    lexer.exp = lexer.exp + r'(?P<' + lexer.i + r'>([^",\n]+)|("[^"]+"))'
    lexer.content.append((lexer.i,"",t.value))
    lexer.i = increment_str(lexer.i)
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
lexer.content = []
lexer.exp = r''
lexer.separator = False
lexer.i = "a"

#file = open(sys.argv[1],"r",encoding="utf-8")
args = sys.argv[1:] # argumentos
file = open(args[0],"r",encoding="utf-8")
json_filename = args[0][:-3]
json_filename += "json"
fpjson = open(json_filename,"w+")

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
dicts = []
mos = exp.finditer(content)
for mo in mos:
    dict = mo.groupdict()
    for tuplo in lexer.content:
            nomeProv = tuplo[0]
            funcao = tuplo[1]
            nomeCorr = tuplo[2]
            if(funcao == "::"):
                dict[nomeProv] = str_to_list(dict[nomeProv])
            elif(funcao == "::sum"):
                dict[nomeProv] = str_to_sum(dict[nomeProv])
            elif(funcao == "::media"):
                dict[nomeProv] = str_to_media(dict[nomeProv])
            dict[nomeCorr] = dict.pop(nomeProv)
            i+=1
    dicts.append(dict)
file.close()


#file = open(change_name(sys.argv[1]),"w+",encoding="utf-8")
fpjson.write("[\n")
for d in dicts:
    fpjson.write("{")
    for elem in d.items():

        strName = re.sub(r'^"|"$',"",str(elem[0])) # tirar aspas
        strValue = re.sub(r'^"|"$',"",str(elem[1])) # tirar aspas

        fpjson.write("\"" + strName + "\"" + ":" + "\"" + strValue + "\"" )
        fpjson.write(",")

    fpjson.seek(fpjson.tell()-1)
    fpjson.write("},\n")

fpjson.seek(fpjson.tell()-2)
fpjson.write("\n]")
fpjson.close()