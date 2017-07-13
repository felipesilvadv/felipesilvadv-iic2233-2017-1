from Planeta import Planeta
from EDD import ListaLigada


class Partida:

    def __init__(self, infeccion=""):
        if infeccion:
            self.planeta = Planeta(infeccion)
            self.planeta.agregar_vecinos()
            self.planeta.agregar_aeropuertos()
        else:
            self.planeta = None
        self.sucesos_dia = ""
        self.dia_actual = 0

    def menu(self):
        # diseño del menu del usuario
        print("""Bienvendido a Pandemic""")
        print("Que tipo de partida quieres jugar?: \n"
              "1. Nueva\n"
              "2. Anterior\n")
        opcion = verificar_int("Tipo de Partida", menu=True)
        if opcion == 1:
            self.partida_nueva()
        else:
            self.cargar_partida()
        while self.planeta.esta_infectado and not self.planeta.esta_muerto:
            if self.dia_actual > 0:
                print("Dia actual : {}".format(self.dia_actual))
            print("Opciones de Juego\n"
                  "1. Pasar de dia\n"
                  "2. Consultar Estadisticas\n"
                  "3. Guardar Partida\n"
                  "4. Salir\n")
            opcion_juego = verificar_int("Opcion", menu=True, posibles="[1-4]", lista_posibles=(1, 2, 3, 4))
            if opcion_juego == 1:
                self.pasar_dia()
            elif opcion_juego == 2:
                self.estadisticas()
            elif opcion_juego == 3:
                self.guardar_partida()
            else:
                print("Hasta luego!")
                break

        if self.planeta.esta_muerto:
            print("Ganaste, destruiste al mundo completo")
        elif opcion != 4:
            print("Perdiste, ha desaparecido tu infección")

    def cargar_partida(self):
        # Tiene que leer una partida guardada por este mismo programa y instanciar todos los objetos
        # para poder continuar una partida
        print("No esta implementado")

    def guardar_partida(self):
        # tiene que guardar de una forma sencilla los paises, poblacion:
        # viva,infectada,muerta y el tipo de infeccion que habia
        # guardar las conecciones terrestres y aereas
        print("No esta implementado")

    def partida_nueva(self):
        # Tiene que crear una partida a partir de los csv dados inicialmente
        infeccion = "algo"
        tipo = ListaLigada("Virus", "Bacteria", "Parasito")
        while infeccion not in tipo:
            infeccion = input("Escoja su tipo de infeccion [Virus-Bacteria-Parasito]: ").title()
            if infeccion not in tipo:
                print("Intentalo de nuevo, recuerda que debes escoger entre Virus-Bacteria-Parasito")
        self.planeta = Planeta(infeccion)
        self.planeta.paises = self.planeta.poblar_mundo()
        for pais in self.planeta:
            self.planeta.poblacion_mundial += pais.poblacion
            pais.infeccion = self.planeta.infeccion
        self.planeta.agregar_aeropuertos()
        self.planeta.agregar_vecinos()
        lista_nombres = ListaLigada(*(pais.nombre for pais in self.planeta))
        while True:
            nombre = input("Desde que país quieres partir la infeccion?: ").title()
            if nombre in lista_nombres:
                break
            else:
                print("El pais dado no es válido")
        for pais in self.planeta:
            if pais.nombre == nombre:
                pais.infectados = 10

    def estadisticas(self):
        # Resumen del dia: Gente que murio/infecto, a que paises llego la infeccion,
        # aeropuertos que cerraron, que paises cerraron fronteras y cuales empezaron
        # a entregar mascarillas
        # Por pais: estatus general(vivos/inf/muertos) y ver la cola de prioridades del gobierno del dia
        # Global: Mostrar paises limpios, infectados y muertos y totales de poblacion (v/i/m)
        # Lista de infecciones y muertes por día
        # Debe mostrar la tasa de vida y muerte de las personas del día actual o el acumulado hasta la fecha
        while True:
            opcion = input("Que estadisticas deseas ver?\n"
                           "1. Resumen del dia\n"
                           "2. Por pais\n"
                           "3. Global\n")
            try:
                opcion = int(opcion)
                if opcion > 3 or opcion < 1:
                    raise ValueError
                break
            except ValueError:
                print("Debes ingresar alguno de los números: 1, 2 o 3")
        if opcion == 1:
            print(self.sucesos_dia)
        elif opcion == 2:
            lista_nombres = ListaLigada(*(pais.nombre for pais in self.planeta))
            while True:
                nombre = input("Sobre que país quieres saber?: ").title()
                if nombre in lista_nombres:
                    break
                else:
                    print("El pais dado no es válido")
            for pais in self.planeta:
                if nombre == pais.nombre:
                    estatus = "Vivos: {0}, Infectados: {1}, Muertos: {2}".format(pais.vivos,
                                                                                 pais.infectados, pais.muertos) + "\n"
                    estatus += str(pais.gob)
                    print(estatus)
        else:
            paises_limpios = ListaLigada(*(pais.nombre for pais in self.planeta if not pais.esta_infectado))
            paises_infectados = ListaLigada(*(pais.nombre for pais in self.planeta if pais.esta_infectado))
            paises_muertos = ListaLigada(*(pais.nombre for pais in self.planeta if pais.esta_muerto))
            vmis = "Vivos/Muertos: {0}/{2}\nSanos/Infectados: {3}/{1}".format(self.planeta.vivos,
                                                                              self.planeta.infectados,
                                                                              self.planeta.muertos,
                                                                              self.planeta.sanos)
            status = vmis + "\nPaises Limpios:\n" + "\n".join(paises_limpios) + "\nPaises Infectados:\n" + "\n".join(
                paises_infectados) + "\nPaises Muertos: \n" + "\n".join(paises_muertos)
            print(status)
        input("<Presione Enter para continuar>")

    def pasar_dia(self):
        # tiene que considerar muertes de humanos, infecciones de humanos,
        # traslado de la infeccion a otro pais, mejora de la cura,
        # traslado de la cura, cerrar aeropuertos o fronteras
        # y entrega de mascarillas
        infectados_iniciales = self.planeta.infectados
        muertos_iniciales = self.planeta.muertos
        cerraron_aeropuertos = ListaLigada()
        cerraron_fronteras = ListaLigada()
        entrego_mascarillas = ListaLigada()
        for pais in self.planeta:
            pais.gob.formar_cola(pais)
            try:
                medidas = pais.gob.cola[0:3]
                for i in range(3):
                    pais.gob.cola.pop(0)
            except IndexError:
                medidas = pais.gob.cola[0:]
                pais.gob.cola.clear()
            for medida in medidas:
                if medida.nombre == "Cerrar aeropuertos":
                    for otro in self.planeta:
                        if otro.nombre in pais.aeropuerto:
                            otro.aeropuerto.remove(pais.nombre)
                    pais.aeropuerto.clear()
                    cerraron_aeropuertos.append(pais.nombre)
                elif medida.nombre == "Cerrar fronteras":
                    for otro in self.planeta:
                        if otro.nombre in pais.vecinos:
                            otro.vecinos.remove(pais.nombre)
                    pais.vecinos.clear()
                    cerraron_fronteras.append(pais.nombre)
                elif medida.nombre == "Abrir fronteras":
                    pais.aeropuerto, pais.vecinos = pais.respaldos
                    for otro in self.planeta:
                        if otro.nombre in pais.vecinos:
                            otro.vecinos.append(pais.nombre)
                        elif otro.nombre in pais.aeropuerto:
                            otro.aeropuerto.append(pais.nombre)
                elif medida.nombre == "Mandar mascarillas":
                    pais.infeccion.contagiosidad *= 0.3
                    entrego_mascarillas.append(pais.nombre)
            pais.muerte()
            pais.contagio_interno()
        self.planeta.descubrimiento_infeccion()
        muertos_dia = self.planeta.muertos - muertos_iniciales
        infectados_dia = self.planeta.infectados - infectados_iniciales
        datos_dia = ListaLigada("Infectados del dia: {}".format(infectados_dia),
                                "Muertos del dia : {}".format(muertos_dia))
        contagio_paises = self.planeta.contagio_entre_paises()
        if len(contagio_paises[0]) > 0 and len(contagio_paises)[1] > 0:
            for nombre_pais, otro_pais in contagio_paises:
                print("{0} contagio a {1}".format(nombre_pais, otro_pais))
        contagio_paises = contagio_paises[0].msort()
        cerraron_aeropuertos = cerraron_aeropuertos.msort()
        cerraron_fronteras = cerraron_fronteras.msort()
        entrego_mascarillas = entrego_mascarillas.msort()
        if self.planeta.cura >= 100 and not self.planeta.implantado:
            self.planeta.implantar_cura()
        if self.planeta.descubierto:
            self.planeta.progreso_cura()
        self.planeta.actualizar_promedio()
        self.sucesos_dia = "\n".join(datos_dia) + "\nPaises infectados hoy:\n " + "\n".join(contagio_paises) + \
                           "\nPaises que cerraron fronteras:\n" + "\n".join(cerraron_fronteras) + \
                           "\nPaises que cerraron aeropuerto: \n" + "\n".join(cerraron_aeropuertos) + "\nPaises que" \
                           " repartieron mascarillas: \n" + "\n".join(entrego_mascarillas)


def verificar_int(variable, menu=False, posibles="1 o 2", lista_posibles=(1, 2)):
    def sacar_espacio(s):
        i = 0
        resultado = ""
        while i < len(s):
            if s[i] != " ":
                resultado = resultado + s[i]
            i += 1
        return resultado
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

if __name__ == "__main__":
    juego = Partida()
    juego.menu()
