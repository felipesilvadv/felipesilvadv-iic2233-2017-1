import re
import os
import requests

with open("AC15.txt", "r") as file:
    enunciado = file.readlines()
    for i in range(len(enunciado)):
        if enunciado[i] != "\n":
            enunciado[i] = enunciado[i].strip()
    parrafo1 = enunciado[0:enunciado.index("\n")]
    enunciado = enunciado[enunciado.index("\n")+1:]
    parrafo2 = enunciado[0:enunciado.index("\n")]
    enunciado = enunciado[enunciado.index("\n")+1:]
    parrafo3 = enunciado
s = ""
for i  in range(len(parrafo1)):
    parrafo1[i] = re.split("@", parrafo1[i])
    for j in range(len(parrafo1[i])):
        if not re.search("\d+", parrafo1[i][j]):
            s += parrafo1[i][j] + " "
    s += "\n"
parrafo1 = s
s = ""
for i  in range(len(parrafo2)):
    parrafo2[i] = re.split("@", parrafo2[i])
    for j in range(len(parrafo2[i])):
        if re.search("\.correcta", parrafo2[i][j]):
            parrafo2[i][j] = re.sub("\.correcta", "", parrafo2[i][j])
            s += parrafo2[i][j] + " "
    s += "\n"
parrafo2 = s
s = ""
for i  in range(len(parrafo3)):
    parrafo3[i] = re.split("@", parrafo3[i])
    for j in range(len(parrafo3[i])):
        if re.search("\.[a-z]", parrafo3[i][j]):
            parrafo3[i][j] = re.sub("\.", "", parrafo3[i][j])
            s += parrafo3[i][j] + " "
    s += "\n"
parrafo3 = s
""" Tratamos de hacer el pdf compilandolo con pdflatex, pero no funcionaba bien"""
#os.system("rm AC15_arreglado.tex AC15_arreglado.log AC15_arreglado.aux AC15_arreglado.pdf")
#with open("AC15_arreglado.tex", "w") as file:
#    file.write("\\documentclass{article}\n")
#    file.write("\\usepackage[utf8]{inputenc}\n")
#    file.write("\\begin{document}\n")
#    file.write(parrafo1+"\n" +  parrafo2 +"\n" + parrafo3 + "\n")
#    file.write("\\end{document}\n")
#os.system("pdflatex AC15_arreglado.tex")
#os.system("xdg-open AC15_arreglado.pdf")
print(parrafo1)
print(parrafo2)
print(parrafo3)

