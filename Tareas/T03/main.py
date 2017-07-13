from gui.Gui import MyWindow
from PyQt5 import QtWidgets
import sys
from comandos_datos import *
from Consultas_numericas import *
from Comandos_booleanos import *
import Exception as myerror
import Data as d


class T03Window(MyWindow):
    def __init__(self):
        super().__init__()
        self.contador = 1

    def process_consult(self, querry_array):
        # Agrega en pantalla la solución. Muestra los graficos!!
        #print(querry_array)
        for querry in  querry_array:
            self.add_answer(str(traducir(querry))+"\n")
            text = "Probando funcion\nConsulta {}\n\n".format(self.contador)
            self.add_answer(text)
            self.contador += 1

    def save_file(self, querry_array):
        # Crea un archivo con la solucion. NO muestra los graficos!!
        self.add_answer("Guardando consultas y generando archivo\n")
        archivo = open("resultados.txt", "w")
        archivo.close()
        with open("resultados.txt", "a") as f:
            contador = 1
            for querry in querry_array:
                text = "Consulta {}\n".format(contador)
                f.write(str(traducir(querry, guardar=True))+"\n")
                f.write(text)
                contador += 1
        #print(querry_array)


def traducir(s, guardar=False):
    if guardar:
        funciones = {"asignar": asignar,
                     "comparar": comparar,
                     "PROM": prom,
                     "DESV": desv,
                     "VAR": var,
                     "extraer_columna": extraer_columna,
                     "MEDIAN": median,
                     "comparar_columna": comparar_columna,
                     "crear_funcion": crear_funcion,
                     "filtrar": filtrar,
                     "operar": operar,
                     "evaluar": evaluar,
                     "LEN": len
                     }
    else:
        funciones = {"asignar": asignar,
                 "comparar": comparar,
                 "PROM": prom,
                 "DESV": desv,
                 "VAR": var,
                 "extraer_columna": extraer_columna,
                 "graficar": graficar,
                 "MEDIAN": median,
                 "comparar_columna": comparar_columna,
                 "crear_funcion": crear_funcion,
                 "filtrar": filtrar,
                 "operar": operar,
                 "evaluar": evaluar,
                 "LEN": len
                 }
    if isinstance(s, list):
        if s[0] == "do_if":
            if traducir(s[2]):
                return traducir(s[1])
            else:
                return traducir(s[3])
        if s[0] in funciones.keys():
            try:
                #print(s)
                return funciones[s[0]](*[traducir(elemento)
                                     if isinstance(elemento, list) and
                                        isinstance(elemento[0], str)
                                     else elemento
                                     for elemento in s[1:]])
            except myerror.ErrorDeTipo as err:
                if guardar:
                    return str(err)
                print(err)
               # s = [d.data[s[i]] if s[i] in d.data.keys() else s[i]
                #     for i in range(len(s))]
                #try:
                 #   return funciones[s[0]](*[traducir(elemento)
                  #                       if isinstance(elemento, list) and
                   #                         isinstance(elemento[0], str)
                    #                     else elemento
                     #                    for elemento in s[1:]])
               # except myerror.ErrorDeTipo as err:
                #    print(err)
              #  except myerror.ImposibleProcesar as err:
               #     print(err)
              #  except myerror.ErrorMatematico as err:
               #     print(err)

            except myerror.ErrorMatematico as err:
                print(err)
                return str(err)
            except myerror.ImposibleProcesar as err:
                print(err)
                return str(err)
            except myerror.ReferenciaInvalida as err:
                print(err)
                return str(err)
            except myerror.ArgumentoInvalido as err:
                print(err)
                return str(err)

    return s


if __name__ == '__main__':
#    a = [
#	["asignar", "x", ["extraer_columna", "registros", "tiempo_sano"]],
#	["asignar", "y", ["extraer_columna", "registros", "muertos_avistados"]],
#	["comparar", ["PROM", "x"], ">", ["DESV", "y"]],
#	["asignar", "filtrado", ["filtrar", "x", ">", 100]],
#	["asignar", "funcion_normal", ["evaluar", ["crear_funcion", "normal", 0, 0.5], -3, 5, 0.1]],
#	["PROM", "filtrado"],
#	["VAR", "funcion_normal"],
#	["do_if", ["VAR", "funcion_normal"], ["comparar_columna", "funcion_normal", ">", "DESV", "x"], ["PROM", "x"]],
#	["graficar", "filtrado", "numerico"],
#	["graficar", "funcion_normal", "rango: -3,5,0.1"],
#	["asignar", "funcion_gamma", ["evaluar", ["crear_funcion", "gamma", 2, 1], 0, 40, 4e-05]],
#	["comparar_columna", "x", ">", "DESV", "funcion_gamma"],
#	["graficar", "x", "rango: 0.00004, 40, 0.00004"],
#	["graficar", "x", "normalizado"]
#]
    #inicio = datetime.now()
    #for i in range(len(a)):
        #print(a[i])
     #   traducir(a[i])
    #print(datetime.now()-inicio)
    #print(d.data["filtrado"])
    consulta = ["operar", [1,2,3], "+", 3]
    consulta2 =  ['VAR', ['crear_funcion', 'normal', 0, 1]]
    consulta3 = ['crear_funcion', 'gamma', 2, -10]
    #print(traducir(consulta))
    #print(traducir(consulta3))
    #print(traducir(consulta2))

    app = QtWidgets.QApplication(sys.argv)
    window = T03Window()
    sys.exit(app.exec_())
