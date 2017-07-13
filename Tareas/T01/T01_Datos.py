#Modulo de carga de datos y instanciar los objetos
from copy import deepcopy
from os import getcwd,makedirs,chdir
import T01_Clases_abstractas as ca
import numpy as np

class BaseDeDatos:
    fecha_inicial = "2017-01-01 00:00:00"

    def __init__(self, *args):
        self.datos = dict()
        self.fecha_actual = Fecha(BaseDeDatos.fecha_inicial)
        for base in args:  # recordar q usuario siempre puede cambiar la hora
            nombre_base = base[0:base.find(".")]
            archivo = open(base, "r", encoding="utf-8")
            lines = archivo.readlines()
            for i in range(1, len(lines)):
                lines[i] = lines[i].strip()
                lines[i] = lines[i].split(",")
                if nombre_base == "usuarios":
                    lines[i] = Usuario(*lines[i])
                elif nombre_base == "recursos":
                    lines[i] = Recurso(*lines[i])
                elif nombre_base == "meteorologia":
                    lines[i] = Clima(*lines[i])
                elif nombre_base == "incendios":
                    lines[i] = Incendio(*lines[i])
            self.datos[nombre_base] = lines[1:]
            archivo.close()

    def paso_un_minuto(self):
        self.fecha_actual.avanzar()
        for usuario in self.datos["usuarios"]:
            if usuario.entidad.moviendo:
                usuario.entidad.mover()

    def paso_una_hora(self, tasa):
        for i in range(60):
            self.paso_un_minuto()
        for incendio in self.datos["incendios"]:
            if incendio.radio == 1:
                incendio.radio = 500
            else:
                incendio.radio += 500 + tasa  # metros

    def actualizar_incendios(self):
        for evento in self.datos["meteorologia"]:
            afectados = list()
            for incendio in self.datos["incendios"]:
                if evento.afecta_incendio(incendio) and (self.fecha_actual < evento.termino) and \
                        (evento.inicio < self.fecha_actual):
                    afectados.append(evento)
            minimo = 100000
            elegido = ""
            for event in afectados:
                distancia = event.inicio.distancia(self.fecha_actual)
                if distancia < minimo:
                    minimo = distancia
                    elegido = evento
            if isinstance(elegido, Clima):
                if elegido.tipo == "VIENTO":
                    tasa = elegido.valor*0.01
                elif elegido.tipo == "TEMPERATURA":
                    if elegido.valor > 30:
                        tasa = (elegido.valor - 30) * 25
                elif elegido.tipo == "LLUVIA":
                    tasa = -50*elegido.valor
                self.paso_una_hora(tasa)


class Incendio:
    encabezado = "id:string,lat:float,lon:float,potencia:int,fecha_inicio:string"

    def __init__(self, *args):
        if len(args) == 5:
            self.id = str(args[0])
            self.lat = float(args[1])
            self.lon = float(args[2])
            self.potencia = abs(int(args[3]))
            self.inicio = Fecha(args[4])
            self.radio = 1  # radio inicial en metros
            self.recursos = []
            self.variable = deepcopy(self.inicio)  # esta es para variar la fecha actual y
            # darle una fecha de termino en caso de extinguirlo
        else:
            raise SyntaxError
        
    def __repr__(self):
        return "Incendio:\nid: {0}\n posicion: ({1},{2})\n potencia: {3}\n fecha de inicio: {4}".format(*self.lista)

    @property
    def lista(self):
        return [self.id, self.lat, self.lon, self.potencia, self.inicio]
    
    @property
    def puntos_poder(self):
        return self.area_afectada * self.potencia
    
    @property
    def area_afectada(self):
        return (self.radio**2)*np.pi

    @property
    def ubicacion(self):
        return self.lat, self.lon
    
    def incendio_apagado(self):
        if self.potencia <= 0:
            return True
        else:
            return False

    def para_escribir(self):
        pass


class Usuario:
    encabezado = "id:string,nombre:string,contraseña:string,recurso_id:string"

    def __init__(self, *args):
        if len(args) == 4:
            self.id = str(args[0])
            self.nombre = str(args[1])
            self._contraseña = str(args[2])
            self.id_recurso = str(args[3])
            self.recurso = None
            self.entidad = None
        else:
            raise SyntaxError
        
    def __repr__(self):
        if not self.entidad:
            retorna = self.lista
            retorna.pop()
            return str(retorna)
        else:
            return str(self.lista)

    def asignar_entidad(self, base):
        if self.id_recurso == "":
            self.entidad = ca.Anaf()
        else:
            tipo = base.datos["recursos"][int(self.id_recurso)].tipo
            if tipo in ["HELICOPTERO", "AVION"]:
                self.entidad = ca.Piloto()
            else:
                self.entidad = ca.Jefe()

    def asignar_recurso(self,base):
        if not isinstance(self.entidad, ca.Anaf):
            self.recurso = base.datos["recursos"][int(self.id_recurso)]
        else:
            self.recurso = None

    @property
    def lista(self):
        return [self.id, self.nombre, self._contraseña, self.id_recurso, self.entidad]

    def para_escribir(self):
        pass


class Clima:

    encabezado = "id:string,fecha_inicio:string,fecha_termino:string," \
                "tipo:string,valor:float,lat:float,lon:float,radio:int"

    def __init__(self, *args):
        if len(args) == 8:
            self.id = str(args[0])
            self.inicio = Fecha(args[1])
            self.termino = Fecha(args[2])
            self.tipo = str(args[3])
            self.valor = abs(float(args[4]))
            self.lat = float(args[5])
            self.lon = float(args[6])
            self.radio = abs(int(args[7]))
        else:
            raise SyntaxError
    
    def afecta_incendio(self, incendio):
        if not incendio.incendio_apagado():
            x, y = self.lat*(1000000/90), self.lon*(40000000/360)  # Estos factores
            #  permiten calcular las distancias en metros
            h, k = incendio.lat*(1000000/90), incendio.lon*(40000000/360)
            esta_en_radio = (x-h)**2 + (y-k)**2 <= incendio.radio**2
            if not esta_en_radio:
                return False
            else:
                return incendio.inicio < self.termino
        else:
            return False

    def para_escribir(self):
        pass
    

class Recurso:
    encabezado = "id:string,tipo:string,lat:float,lon:float," \
                 "velocidad:int,autonomia:int,delay:int,tasa_extincion:int,costo:int"
    moviendo = False

    def __init__(self, *args):
        if len(args) == 9:
            self.id = str(args[0])
            self.tipo = str(args[1])
            self.lat = float(args[2])
            self.lon = float(args[3])
            self.velocidad = int(args[4])
            self.autonomia = int(args[5])
            self.delay = int(args[6])
            self.tasa = int(args[7])
            self.costo = int(args[8])
            self.lat_inicial = self.lat
            self.lon_inicial = self.lon
            self.incendio = None
        else:
            raise SyntaxError
        
    @property
    def lista(self):
        return [self.id, self.tipo, self.lat, self.lon, self.velocidad, self.autonomia, self.delay, self.tasa,
                self.costo]

    @property
    def ubicacion(self):
        return self.lat, self.lon

    @property
    def estado(self):
        if self.ubicacion == (self.lat_inicial, self.lon_inicial):
            return "Standby"
        elif self.distancia_incendio() == 0:
            return "Trabajando en incendio"
        elif self.ubicacion != (self.lat_inicial, self.lon_inicial) and isinstance(self.incendio, type(None)):
            return "En ruta a base"
        elif self.ubicacion != (self.lat_inicial, self.lon_inicial) and isinstance(self.incendio, Incendio):
            return "En ruta a incendio"

    def distancia_incendio(self):
        distancia = self.mover(distancia=True)
        if distancia <= 0:
            self.lat, self.lon = self.incendio.ubicacion
            distancia = 0
        return distancia

    def para_escribir(self):
        return ",".join(self.lista)

    def mover(self, distancia=False, inverso=False):
        def convertir_grados(grados):
            radianes = (2 * np.pi * grados) / 360
            return radianes

        def generar_posicion(elemento, inicial=False):
            r = 6371000  # Radio medio de la Tierra
            posicion = np.zeros([3, 1])
            if inicial:
                seno_phi = np.sin(convertir_grados(elemento.lat_inicial))
                posicion[0] = r * np.cos(convertir_grados(elemento.lon_inicial)) * seno_phi
                posicion[1] = r * np.sin(convertir_grados(elemento.lon_inicial)) * seno_phi
                posicion[2] = r * np.cos(convertir_grados(elemento.lat_inicial))
            else:
                seno_phi = np.sin(convertir_grados(elemento.lat))
                posicion[0] = r * np.cos(convertir_grados(elemento.lon)) * seno_phi
                posicion[1] = r * np.sin(convertir_grados(elemento.lon)) * seno_phi
                posicion[2] = r * np.cos(convertir_grados(elemento.lat))
            return posicion

        def convertir_radianes(radianes):
            grados = (360 * radianes) / (2 * np.pi)
            return grados

        def obtener_lat_lon(posicion):
            # x = float(posicion[0])
            y = float(posicion[1])
            z = float(posicion[2])
            r = 6371000
            lat = -np.arccos(z/r)
            lon = np.arcsin(y/(r*np.sin(lat)))
            lat = convertir_radianes(lat)
            lon = convertir_radianes(lon)
            return float(lat), float(lon)
        posicion_recurso = generar_posicion(self, inicial=inverso)
        posicion_incendio = generar_posicion(self.incendio)
        direccion = posicion_incendio - posicion_recurso
        if inverso:
            direccion = -direccion
        movimiento = (direccion/np.linalg.norm(direccion)) * self.velocidad * 60  # Velocidad queda en m/min
        direccion_final = posicion_recurso + movimiento
        if distancia:
            return np.linalg.norm(direccion) - self.incendio.radio  # Distancia entre el borde del incendio y el recurso
        Recurso.moviendo = True
        self.lat, self.lon = obtener_lat_lon(direccion_final)


class Fecha:
    
    def __init__(self, s):
        s = s.replace(" ", "-")
        s = s.replace(":", "-")
        s = s.split("-")
        self.año = int(s[0])
        self.mes = int(s[1])
        self.dia = int(s[2])
        self.hora = int(s[3])
        self.minutos = int(s[4])
        self.segundos = int(s[5])
        
    @property
    def lista(self):
        return [self.dia, self.mes, self.año, self.hora, self.minutos, self.segundos]
        
    def __str__(self):
        return "{0}-{1}-{2}  {3}:{4}:{5}".format(*self.lista)
    
    def __repr__(self):
        return "{0}-{1}-{2}  {3}:{4}:{5}".format(*self.lista)
    
    def __neq__(self, other):
        return not ((self.dia == other.dia) and (self.mes == other.mes) and (self.año == other.año) and
                    (self.hora == other.hora) and (self.minutos == other.minutos) and (self.segundos == other.segundos))
    
    def __eq__(self, other):
        return((self.dia == other.dia) and (self.mes == other.mes) and (self.año == other.año) and
               (self.hora == other.hora) and (self.minutos == other.minutos) and (self.segundos == other.segundos))
    
    def __lt__(self, other):
        if self == other:
            return False
        año = self.año == other.año
        mes = self.mes == other.mes
        dia = self.dia == other.dia
        hora = self.hora == other.hora
        minuto = self.minutos == other.minutos
        if self.año < other.año:
            return True
        elif año and self.mes < other.mes:
            return True
        elif año and mes and self.dia < other.dia:
            return True
        elif año and mes and dia and self.hora < other.hora:
            return True
        elif año and mes and dia and hora and self.minutos < other.minutos:
            return True
        elif año and mes and dia and hora and minuto and self.segundos < other.segundos:
            return True
        else:
            return False
        
    def __le__(self, other):
        return (self == other) or (self < other)
    
    def __ge__(self, other):
        return not (self < other)
    
    def __gt__(self, other):
        return (self >= other) and (self == other)
    
    def año_bisiesto(self):
        return ((self.año % 100 != 0)or(self.año % 400 == 0))and(self.año % 4 == 0)
    
    def avanzar(self):  # modifica la fecha minuto a minuto
        if self.mes == 2:
            if self.año_bisiesto():
                maximodedias = 29
            else:
                maximodedias = 28
        elif self.mes in [1, 3, 5, 7, 8, 10, 12]:
            maximodedias = 31
        else:
            maximodedias = 30

        if self.minutos < 59:
            self.minutos += 1
        elif self.minutos == 59 and self.hora < 23:
            self.minutos = 0
            self.hora += 1
        elif self.hora == 23 and self.dia < maximodedias:
            self.minutos = 0
            self.hora = 0
            self.dia += 1
        elif self.dia == maximodedias and self.mes < 12:
            self.minutos = 0
            self.hora = 0
            self.dia = 1
            self.mes += 1
        else:
            self.minutos = 0
            self.hora = 0
            self.dia = 1
            self.mes = 1
            self.año += 1
            
    def distancia(self, other):
        contador = 0
        while self < other:
            self.avanzar()
            contador += 1
        return contador

    
base = BaseDeDatos("incendios.csv", "meteorologia.csv", "usuarios.csv", "recursos.csv")
if __name__ == "__main__":
    print(getcwd())
    recurso = base.datos["recursos"][4]
    incendio = base.datos["incendios"][5]
    recurso.incendio = incendio
    print(incendio.ubicacion)
    print(recurso.ubicacion)
    recurso.mover()
    print(recurso.ubicacion)
    
