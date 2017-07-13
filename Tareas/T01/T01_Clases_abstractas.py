# Modulo clases abstractas
import T01_Datos as D
import T01_Funciones as F
from abc import ABCMeta, abstractmethod


class Entidad(metaclass=ABCMeta):
    
    @abstractmethod
    def crear_usuario(self):
        pass

    @abstractmethod
    def ver_datos(self):
        pass

    @abstractmethod
    def acceder_incendio(self):
        pass

    @abstractmethod
    def agregar_incendio(self):
        pass

    @abstractmethod
    def agregar_recurso(self):
        pass

    @abstractmethod
    def agregar_pronostico(self):
        pass

    @abstractmethod
    def asignar_recurso_a_incendio(self):
        pass

    @abstractmethod
    def consulta_avanzada(self):
        pass


class Anaf(Entidad):
    def crear_usuario(self):    
        nombre = input("Seleccione un nombre de usuario: ")
        contraseña = input("Seleccione una contraseña: ")
        recurso = ""
        id_ultimo_recurso = int(D.base.datos["recursos"][-1].id)
        while not recurso.isdecimal():
            recurso = input("Señale el id del recurso al que esta relacionado: ")
            if recurso.isdecimal() and int(recurso) <= id_ultimo_recurso:
                print("Id de recurso válido")
            else:
                print("Id inválido, intentalo de nuevo")
        entidad = ""
        while entidad not in ["anaf", "piloto", "jefe"]:
            entidad = input("A que entidad pertenece el usuario[anaf,piloto,jefe]: ")
            entidad = entidad.lower()
            if entidad not in ["anaf", "piloto", "jefe"]:
                print("Debe elegir una entidad válida")
            else:
                print("Entidad válida")
        ultimo_id = int(D.base.datos["usuarios"][-1].id)
        algo = D.Usuario(ultimo_id + 1, nombre, contraseña, recurso)
        algo.entidad = entidad
        D.base.datos["usuarios"].append(algo)
    
    def ver_datos(self):
        tipo_datos = ""
        posibles = D.base.datos.keys()
        while tipo_datos not in posibles:
            tipo_datos = input("Que tipo de Datos quieres ver: ").lower()
            if tipo_datos not in posibles:
                print("No existe ese tipo de datos")
        for elemento in D.base.datos[tipo_datos]:
            print(elemento)

    def acceder_incendio(self):
        numero_incendio = F.verificar_int("id de incendio")
        incendio = D.base.datos["incendios"][numero_incendio]
        print("¿Quieres ver el incendio?")
        print("1.-Sí        2.-No")
        ver = F.verificar_int("Opcion", menu=True)
        if ver == 1:
            print(incendio)
        return incendio  # ver bien que pasa acá si se retorna o no
    
    def agregar_incendio(self):
        lat, lon = F.pedir_ubicacion("incendio")
        potencia = F.verificar_int("potencia de incendio")
        radio = F.verificar_int("radio de incendio")
        fecha = F.pedir_fecha("incendio")
        ultimo_id = int(D.base.datos["incendios"][-1].id)
        incendio = D.Incendio(ultimo_id+1, lat, lon, potencia, fecha)
        incendio.radio = radio
        D.base.datos["incendios"].append(incendio)

    def agregar_recurso(self):
        nuevo_id = int(D.base.datos["recursos"][-1].id)+1
        tipo = ""
        while tipo not in ["BOMBERO", "AVION", "HELICOPTERO", "BRIGADA"]:
            tipo = input("Que tipo de recurso es?: ").upper()
            if tipo not in ["BOMBERO", "AVION", "HELICOPTERO", "BRIGADA"]:
                print("Tipo inválido, vuelve a intentarlo")
            else:
                print("Tipo ingresado")
        lat, lon = F.pedir_ubicacion("recurso")
        velocidad = F.verificar_int("Velocidad")
        autonomia = F.verificar_int("Autonomía")
        delay = F.verificar_int("Delay")
        tasa = F.verificar_int("Tasa de extinción")
        costo = F.verificar_int("Costo")
        recurso = D.Recurso(nuevo_id, tipo, lat, lon, velocidad, autonomia, delay, tasa, costo)
        D.base.datos["recursos"].append(recurso)

    def agregar_pronostico(self):
        nuevo_id = int(D.base.datos["meteorologia"][-1].id) + 1
        fecha_inicio = F.pedir_fecha("pronostico meteorologico", inicio=True)
        fecha_termino = F.pedir_fecha("pronostico meteorologico", termino=True)
        tipo = ""
        while tipo not in ["NUBES", "VIENTO", "LLUVIA", "TEMPERATURA"]:
            tipo = input("Que tipo de pronostico meteorologico es?: ").upper()
            if tipo not in ["NUBES", "VIENTO", "LLUVIA", "TEMPERATURA"]:
                print("Tipo inválido, vuelve a intentarlo")
            else:
                print("Tipo ingresado")
        error = True
        while error:
            valor = input("Que valor tiene el pronostico meteorologico?: ")
            try:
                valor = float(valor)
                error = False
            except ValueError:
                print("Valor inválido")
        lat, lon = F.pedir_ubicacion("pronostico meteorologico")
        radio = F.verificar_int("Radio")
        pronostico = D.Clima(nuevo_id, fecha_inicio, fecha_termino, tipo, valor, lat, lon,radio)
        D.base.datos["meteorologia"].append(pronostico)

    def asignar_recurso_a_incendio(self):
        id_recurso = F.verificar_int("id de recurso")
        id_incendio = F.verificar_int("id de incendio")
        recurso = D.base.datos["recursos"][id_recurso]
        incendio = D.base.datos["incendios"][id_incendio]
        recurso.incendio = incendio
        incendio.recursos.append(recurso)
        print("Se ha asignado el incendio {0} al recurso {1}".format(id_incendio, id_recurso))

    def consulta_avanzada(self):
        print("""Que consulta quieres hacer
        1.-Incendios Activos
        2.-Incendios Apagados
        3.-Recursos más utilizados
        4.-Recursos más eficientes""")
        opcion = F.verificar_int("opcion", menu=True, posibles="1-4", lista_posibles=[1, 2, 3, 4])
        if opcion == 1:
            activos = []
            for incendio in D.base.datos["incendios"]:
                if not incendio.incendio_apagado():
                    activos.append(incendio)
            for incendio in activos:
                print("fecha de inicio {0},\n recursos usados {1}".format(incendio.inicio, incendio.recursos))
        elif opcion == 2:
            apagados = []
            for incendio in D.base.datos["incendios"]:
                if incendio.incendio_apagado():
                    apagados.append(incendio)
            for incendio in apagados:
                print("fecha de inicio {0},fecha de termino {1}\n "
                      "recursos usados {2}".format(incendio.inicio, incendio.variable, incendio.recursos))
        elif opcion == 3:
            pass
        else:
            pass



class Jefe(Entidad):

    def crear_usuario(self):
        print("No rienes acceso a esta función")

    def ver_datos(self, *args):
        if len(args) == 1:
            print("Tu recurso asignado es:")
        else:
            print("Tus recursos asignados son:")
        for arg in args:
            print(arg)

    def acceder_incendio(self):
        pass

    def agregar_incendio(self):
        print("No tienes acceso a esta función")

    def agregar_recurso(self):
        print("No tienes acceso a esta función")

    def agregar_pronostico(self):
        print("No tienes acceso a esta función")

    def consulta_avanzada(self):
        print("No tienes acceso a esta función")

    def asignar_recurso_a_incendio(self):
        print("No tienes acceso a esta función")


class Piloto(Entidad):

    def crear_usuario(self):
        print("No tienes acceso a esta función")

    def ver_datos(self):
        pass

    def acceder_incendio(self):
        pass
    
    def agregar_incendio(self):
        print("No tienes acceso a esta función")

    def agregar_recurso(self):
        print("No tienes acceso a esta función")

    def agregar_pronostico(self):
        print("No tienes acceso a esta función")

    def asignar_recurso_a_incendio(self):
        print("No tienes acceso a esta función")

    def consulta_avanzada(self):
        print("No tienes acceso a esta función")

if __name__ == "__main__":
    usuario = Jefe()
    usuario.ver_datos(12)
