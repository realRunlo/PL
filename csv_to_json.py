import re
import statistics
import sys
import ply.lex as lex


# argumentos
args = sys.argv[1:] 

# verifica se recebeu 1 argumento
lenargs = len(args)
if lenargs != 1:
    print("number of arguments invalid! please give one argument.")
    sys.exit()

# verifica se o argumento que recebeu é um .csv
valid = re.match(r'\w+\.(CSV|csv)$',args[0])
if valid:
    print("Loading "+ args[0] +"...") 
else: 
    print("invalid arguments!")
    sys.exit()

# função que transforma uma string de números numa lista
def str_to_list (str):
    return [int(s) for s in re.findall("\d+",str)]

# função que transforma uma string de números numa soma
def str_to_sum (str):
    return sum([int(s) for s in re.findall("\d+",str)])

# função que transforma uma string de números na média
def str_to_media (str):
    return statistics.mean([int(s) for s in re.findall("\d+",str)])

# função que transforma uma string de números numa soma
def str_to_max (str):
    return max([int(s) for s in re.findall("\d+",str)])

# função que transforma uma string de números numa soma
def str_to_min (str):
    return min([int(s) for s in re.findall("\d+",str)])

# função que transforma uma string de números numa lista com os seus quadrados
def str_to_quadrado (str):
    return ([pow(int(s),2) for s in re.findall("\d+",str)])

# função que incrementa uma string
def increment_str(str):
    if(ord(str[0]) < 122):
        str = chr(ord(str[0])+1) + str[1:]
    else:
        str = "a" + str[0:]
    return str

# função que troca o nome de um ficheiro.csv para ficheiro.json
def change_name(csv):
    json = re.sub(r'(\w+\.)(CSV|csv)',r'\1json',csv)
    return json

"""PLY"""

tokens = ["LISTA","SEPARADOR","NOME"]

def t_LISTA(t):
    r'(([^",\n]+)|("[^"\n]+"))\{\d+(,\d+)?\}(::\w+)?'
    q_min = 0
    q_max = 0
    m = re.match(r'(?P<nome>([^",\n]+)|(\"[^"\n]+"))\{(?P<q_min>\d)(,(?P<q_max>\d))?\}(?P<funcao>::\w+)?',t.value)
    if(m.group("nome")):
        t.value = m.group("nome")
    if(m.group("funcao")):
        lexer.content.append((lexer.i,m.group("funcao"),t.value))
    else: lexer.content.append((lexer.i,"::",t.value))
    if(m.group("q_min")):
        q_min = int(m.group("q_min"))
    if(m.group("q_max")):
        q_max = int(m.group("q_max"))
    else:
        q_max = q_min
    lexer.exp = lexer.exp + r'(?P<' + lexer.i + r'>'
    for i in range(q_min-1):
        lexer.exp = lexer.exp + r'\d+,'
    lexer.exp = lexer.exp + r'\d+'
    for i in range(q_min,q_max):
        lexer.exp = lexer.exp + r',(\d+)?'
    lexer.separator = False
    lexer.exp = lexer.exp + r')'
    lexer.i = increment_str(lexer.i)
    lexer.nfields+=q_max+1

def t_NOME(t):
    r'([^",\n]+)|("[^"\n]+")'
    lexer.exp = lexer.exp + r'(?P<' + lexer.i + r'>([^",\n]+)|("[^"\n]+"))'
    lexer.content.append((lexer.i,"",t.value))
    lexer.i = increment_str(lexer.i)
    lexer.separator = False
    lexer.nfields+=1

def t_SEPARADOR(t):
    r','
    lexer.ncommas+=1
    if(not(lexer.separator)): 
        lexer.exp = lexer.exp + r','
        lexer.separator = True

t_ignore = "\n"

def t_ANY_error(t):
    print("Invalid Header in csv.")
    sys.exit()

lexer = lex.lex()
lexer.content = []
lexer.exp = r''
lexer.separator = False
lexer.i = "a"
lexer.ncommas = 0
lexer.nfields = 0

file = open(args[0],"r",encoding="utf-8")
header = file.readline()

lexer.input(header)
for tok in lexer:
    pass

#verifica se o header é valido (numero de virgulas = numero de campos-1)
if lexer.ncommas != lexer.nfields-1:
    print("invalid header")
    sys.exit()

# tira a virgula final na expressão regular que o lexer mete a mais caso acabe numa LISTA
if lexer.exp[-1] == ",":
    lexer.exp = lexer.exp[:-1]

# compilamos a expressão regular criada no lexer
exp = re.compile(lexer.exp)
# lemos o resto do csv
content = file.read()

#Cria e abre o ficheiro .json
json_filename = change_name(args[0])
fpjson = open(json_filename,"w+",encoding="utf-8")

mos = exp.finditer(content) #fazer a lista de match objects que deram match com o resto do ficheiro

#Escreve o dicionário no .json
fpjson.write("[\n")
for mo in mos: #para cada match object vamos construir o dicionario
    fpjson.write("  {\n")
    dict = mo.groupdict()
    for tuplo in lexer.content:
            nomeProv = tuplo[0]
            funcao = tuplo[1]
            strName = re.sub(r'^"|"$',"",str(tuplo[2]))
            if(funcao == "::"):
                strValue = str(str_to_list(dict[nomeProv]))
            elif(funcao == "::sum"):
                strValue = str(str_to_sum(dict[nomeProv]))
            elif(funcao == "::media"):
                strValue = str(str_to_media(dict[nomeProv]))
            elif(funcao == "::quadrado"):
                strValue = str(str_to_quadrado(dict[nomeProv]))
            elif(funcao == "::max"):
                strValue = str(str_to_max(dict[nomeProv]))
            elif(funcao == "::min"):
                strValue = str(str_to_min(dict[nomeProv]))
            else:
                strValue = '"' + re.sub(r'^"|"$',"",str(dict[nomeProv])) + '"'
            fpjson.write("      \"" + strName + "\"" + ": " + strValue)
            fpjson.write(",\n")
    fpjson.seek(fpjson.tell()-3)
    fpjson.write("\n  },\n")
fpjson.seek(fpjson.tell()-3)
fpjson.write("\n]")
fpjson.close()
file.close()

