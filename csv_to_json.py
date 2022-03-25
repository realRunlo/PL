
import re
import statistics
import sys
import ply.lex as lex
import platform
corr = 0
platform = platform.system()
print("Platform: " + platform)
if platform == "Linux" or  platform =="Darwin":
    corr = 2
elif platform == "Windows":
    corr = 3

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
    return re.findall(r'[^\n,]+',str)

# função que transforma uma string de números numa soma
def str_to_sum (str):
    return sum([float(s) for s in re.findall(r'(\d+(?:\.\d+)?)',str)])

# função que transforma uma string de números na média
def str_to_media (str):
    return statistics.mean([float(s) for s in re.findall(r'(\d+(?:\.\d+)?)',str)])

# função que transforma uma string de números numa soma
def str_to_max (str):
    return max([float(s) for s in re.findall(r'(\d+(?:\.\d+)?)',str)])

# função que transforma uma string de números numa soma
def str_to_min (str):
    return min([float(s) for s in re.findall(r'(\d+(?:\.\d+)?)',str)])

# função que transforma uma string de números numa lista com os seus quadrados
def str_to_quadrado (str):
    return ([pow(float(s),2) for s in re.findall(r'(\d+(?:\.\d+)?)',str)])

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
    m = re.match(r'(?P<nome>([^",\n]+)|(\"[^"\n]+"))\{(?P<min>\d+)(,(?P<max>\d+))?\}(?P<funcao>::\w+)?',t.value)
    num = r'(\d+(\.\d+)?)'
    elem = r'([^\n,]+)'
    
    t.value = m.group("nome")

    min = int(m.group("min"))
    max = min
    
    if(m.group("max")):
        max = int(m.group("max"))
    lexer.nfields+=max
    
    regex = r'(?P<' + lexer.i + r'>'

    if(m.group("funcao")):
        lexer.content.append((lexer.i,m.group("funcao"),t.value))
        cont = num
    else: 
        lexer.content.append((lexer.i,"::",t.value))
        cont = elem

    for i in range(min-1):
        regex += cont + r','
        lexer.commaslista+=1
    regex += cont
    for i in range(min,max):
        regex += r',' + cont + r'?'
        lexer.commaslista+=1  
    regex += r')'
    lexer.i = increment_str(lexer.i)
    lexer.regex+=regex
    lexer.ncommas+=lexer.commaslista

def t_NOME(t):
    r'([^",\n]+)|("[^"\n]+")'
    regex = r'(?P<' + lexer.i + r'>([^",\n]+)|("[^"\n]+"))?'
    lexer.content.append((lexer.i,"",t.value))
    lexer.i = increment_str(lexer.i)
    lexer.nfields+=1
    lexer.regex+=regex

def t_SEPARADOR(t):
    r','
    if lexer.commaslista > 0:
        lexer.commaslista-=1
    elif lexer.ncommas < lexer.nfields: 
        lexer.regex += r','
        lexer.ncommas+=1

t_ignore = "\n"

def t_ANY_error(t):
    print("Invalid Header in csv.")
    sys.exit()

lexer = lex.lex()
lexer.content = []
lexer.regex = r''
lexer.i = "a"
lexer.ncommas = 0
lexer.nfields = 0
lexer.commaslista = 0

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
if lexer.regex[-1] == ",":
    lexer.regex = lexer.regex[:-1]
    print(lexer.regex)

# compilamos a expressão regular criada no lexer
exp = re.compile(lexer.regex)
# lemos o resto do csv
content = file.read()

#Cria e abre o ficheiro .json
json_filename = change_name(args[0])
fpjson = open(json_filename,"w+",encoding="utf-8")

mos = exp.finditer(content) #fazer a lista de match objects que deram match com o resto do ficheiro

print("Creating " + json_filename + "...")
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
                strValue = re.sub(r"'([^\']+)'",r'"\1"',strValue)
                strValue = re.sub(r'"(\d+(.\d+)?)"',r'\1',strValue)
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
                strValue = re.sub(r'None',"",strValue)
            strValue = re.sub(r'"(\d+(.\d+)?)"',r'\1',strValue)
            fpjson.write("      \"" + strName + "\"" + ": " + strValue)
            fpjson.write(",\n")
    fpjson.seek(fpjson.tell()-corr)
    fpjson.write("\n  },\n")
fpjson.seek(fpjson.tell()-corr)
fpjson.write("\n]")
fpjson.close()
file.close()
