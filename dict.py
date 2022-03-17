# Operações suportadas:
# {N} -> lista 
# {N,M} -> lista (N-min M-max)
# As funções são aplicaveis ás listas:
# ::sum -> soma os valores à estrutura que é aplicada
# ::media -> faz a média com os valores da estrutura a que é aplicada


# O que fazer:
#fazer um tokenizer que identifica tokens e faz a tradução

#TOKENS:
# {N}
# {N,M}
# ::sum
# ::media
import sys
import re
import json

args = sys.argv[1:] # get filename

f = open(args[0])
fjson = open("teste.json","w")
header = f.readline()
columns = header.split(",")
headerexp = re.compile(r'[^,\d{}:\n]+')

exp = r""
for c in headerexp.findall(header):
    exp = exp + r"(?P<" + c + r">[\w\s]+),?"
xp = re.compile(exp)

fjson.write("[")
for line in f:
    fjson.write(json.dumps(xp.match(line).groupdict()))
    fjson.write(",")

fjson.write("]")