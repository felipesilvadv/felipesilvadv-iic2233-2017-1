#  Funciones
from os import getcwd,makedirs,chdir
import T01_Datos as D


def pedir_ubicacion(string_pedido):
    error = True
    error1 = True
    while error:
        lat = input("Que latitud tiene el {}?: ".format(string_pedido))
        try:
            lat = float(lat)
            error = False
        except ValueError:
            print("Latitud inválida")
    while error1:
        lon = input("Que longitud tiene el {}?: ".format(string_pedido))
        try:
            lon = float(lon)
            error1 = False
        except ValueError:
            print("Longitud inválida")
    return lat, lon


def verificar_int(variable, menu=False, posibles="1 o 2", lista_posibles=(1, 2)):
    algo = ""
    while not algo.isdecimal():
        algo = input("Ingrese {}: ".format(variable))
        algo = sacar_espacio(algo)
        if not algo.isdecimal():
            print("ERROR, debes ingresar un número entero")
        else:
            if not menu:
                print("{} se ingreso correctamente".format(variable))
            elif int(algo) not in lista_posibles:
                print("Debes ingresar {}".format(posibles))
                algo = ""
    return int(algo)


def sacar_espacio(s):
    i = 0
    resultado = ""
    while i < len(s):
        if s[i] != " ":
            resultado = resultado + s[i]
        i += 1
    return resultado


def pedir_fecha(variable, inicio=False, termino=False):
    lista = []
    if inicio:
        agregar = "inicio "
    elif termino:
        agregar = "termino "
    else:
        agregar = ""
    for elemento in ["año", "mes", "dia", "hora", "minuto"]:
        tiempo = verificar_int("{0} de "+agregar+"{1}".format(elemento, variable))
        lista.append(tiempo)
    fecha = "{2}-{1}-{0} {3}:{4}:00".format(*lista)
    return fecha


def escribir_base_en_csv(base):
    pass


def menu():
    opcion = 0
    while opcion != 2:
        user = None
        print("""               MENU DE ACCIONES
        ¿Que deseas hacer?:
        1.- Iniciar sesión
        2.- Salir del programa
        Tu elección [ingresa número]""")
        opcion = verificar_int("opcion", menu=True)
        if opcion == 1:
            nombre = input("Ingresa tu nombre de usuario: ")
            contraseña = input("Ingresa tu contraseña: ")
            for usuario in D.base.datos["usuarios"]:
                if usuario.nombre == nombre and usuario._contraseña == contraseña:
                    user = usuario
                    user.asignar_entidad(D.base)
                    user.asignar_recurso(D.base)
                    print("Ingreso existoso")
                    menu_para_usuario(user)






def menu_para_usuario(usuario):
    opcion = 0
    while opcion < 10:
        print("""¿Que deseas hacer?
         1.-Crear un nuevo usuario
         2.-Ver datos
         3.-Acceder a incendio
         4.-Agregar incendio
         5.-Agregar pronostico
         6.-Agregar recurso
         7.-Asignar recurso
         8.-Consulta avanzada
         9.-Cambiar fecha
         10.-Cerrar sesión""")
        opcion = verificar_int("opcion", menu=True, posibles="numero entero entre 1-9",
                               lista_posibles=[i for i in range(1, 11)])
        if opcion == 1:
            usuario.entidad.crear_usuario()
        elif opcion == 2:
            usuario.entidad.ver_datos(usuario.recurso)
        elif opcion == 3:
            usuario.entidad.acceder_incendio()
        elif opcion == 4:
            usuario.entidad.agregar_incendio()
        elif opcion == 5:
            usuario.entidad.agregar_pronostico()
        elif opcion == 6:
            usuario.entidad.agregar_recurso()
        elif opcion == 7:
            usuario.entidad.consulta_avanzada()
        elif opcion == 8:
            print("No esta implementado")
        elif opcion == 9:
            print("No esta implemnetado")
        else:
            opcion = 10
if __name__ == "__main__":
    print("""---------------BIENVENIDO A SUPERLUCHIN------------""")
    menu()