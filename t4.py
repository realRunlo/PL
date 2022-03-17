import re 
import sys
from tokenize import group
import ply.lex as lex
import json

class Header:
    def __init__(self, nome, quant_min, quant_max, tipo):
        self.nome = nome #nome do intervalo
        self.quant_min = quant_min #se nao for uma lista, quantidade = 1
        self.quant_max = quant_max #se nao for uma lista, quantidade = 1
        self.tipo = tipo #0 -> faz nada, 1 -> soma, 2 -> media


headerExp = re.compile(r"(?P<lm>[^,\s]+\{(\d,\d|\d)\}::media)|(?P<ls>[^,\s]+\{(\d,\d|\d)\}::sum)|(?P<l>[^,\s]+\{(\d,\d|\d)\})|(?P<n>(\w+)|\"\S+\")")
l = headerExp.finditer("Número,Nome,Curso,Notas{3,5}::sum,,,,,Cenas{3,5}::media,,,,,Cenas{3,5},,,,")

listaExp = re.compile(r"(?P<nome>[^{]+){(?P<min>\d+)(,(?P<max>\d+))?}")

headers = []
for i in l:
    nome = ""
    min = 0
    max = 0
    tipo = 0
    if i.group("n"):
        nome = i.group("n")
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
    
for i in headers:
    print(i.nome +","+str(i.quant_min)+","+str(i.quant_max)+","+str(i.tipo))