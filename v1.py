from statistics import median
import re
import sys

class Header:
    def __init__(self, nome, quant_min, quant_max, tipo):
        self.nome = nome #nome do intervalo
        self.quant_min = quant_min #se nao for uma lista, quantidade = 1
        self.quant_max = quant_max #se nao for uma lista, quantidade = 1
        self.tipo = tipo #0 -> faz nada, 1 -> soma, 2 -> media

args = sys.argv[1:] # argumentos
fp = open(args[0])
hd = fp.readline() # le header do ficheiro

headerExp = re.compile(r"(?P<lm>[^,\s]+\{(\d,\d|\d)\}::media)|(?P<ls>[^,\s]+\{(\d,\d|\d)\}::sum)|(?P<l>[^,\s]+\{(\d,\d|\d)\})|(?P<n>(\w+)|\"\S+\")")
l = headerExp.finditer(hd)

listaExp = re.compile(r"(?P<nome>[^{]+)\{(?P<min>\d+)(,(?P<max>\d+))?\}")

headers = []
for i in l:
    nome = ""
    min = 0
    max = 0
    tipo = 0
    if i.group("n"):
        nome = re.sub(r'"',r'\"',i.group("n"))
        min = 1
        max = 1
        tipo = 0
    elif i.group("l") or i.group("ls") or i.group("lm"):
        if i.group("ls"):
            tipo = 1
            listaObj = listaExp.match(i.group("ls"))
        elif i.group("lm"):
            tipo = 2
            listaObj = listaExp.match(i.group("lm"))
        else:
            listaObj = listaExp.match(i.group("l"))
        nome = listaObj.group("nome")
        min = int(listaObj.group("min"))
        if listaObj.group("max"):
            max = int(listaObj.group("max"))
        else:
            max = min
        if i.group("ls"):
            tipo = 1
        elif i.group("lm"):
            tipo = 2
    headers.append(Header(nome,min,max,tipo))

json_filename = args[0][:-3]
json_filename += "json"

fpjson = open(json_filename,"w+")
fpjson.write("[")
for linha in fp:
    fpjson.write("{")
    linha = linha.split(",") # mas assim fica mal nos casos de virgulas nos nomes

    indice_linha = 0
    for h in headers:   
        if h.quant_min == 1 and h.quant_max == 1:
            fpjson.write("\"" + h.nome + "\"" + ":" + "\"" + linha[indice_linha] + "\"" + ",")
            indice_linha +=1
        elif h.quant_min != 1 and h.quant_max > 1:


            lista = []

            for i in range(h.quant_max):
                if linha[indice_linha] != "" and linha[indice_linha] != "\n":
                    lista.append(int(linha[indice_linha]))
                indice_linha += 1

            if h.tipo == 1:     #soma
                print(lista)
                fpjson.write("\"" + h.nome + "\"" + ":" + str(sum(lista)) + ",")
            elif h.tipo == 2:   #media
                fpjson.write("\"" + h.nome + "\"" + ":" + str(statistics.mean(lista)) + ",")
            else:
                fpjson.write("\"" + h.nome + "\"" + ":" + str(lista) + ",")
                print(lista)

            lista.clear()
    fpjson.seek(fpjson.tell()-1)
    fpjson.write("},\n")

fpjson.seek(fpjson.tell()-2) #remover a virgula que fica a mais
fpjson.write("]")
fpjson.close()

