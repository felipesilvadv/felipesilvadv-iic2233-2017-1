from EDD import ListaLigada
from Pais import Pais
from connections_generator import generate_connections
from random import randint, shuffle
import Infeccion as inf


class Planeta:
    def __init__(self, infeccion):
        self.paises = None
        self.poblacion_mundial = 0
        self.descubierto = False
        self.cura = 0
        self.implantado = False
        if self.paises:
            for pais in self:
                self.poblacion_mundial += pais.poblacion
                pais.infeccion = self.infeccion
        if infeccion.lower() == "virus":
            self.infeccion = inf.Virus()
        elif infeccion.lower() == "bacteria":
            self.infeccion = inf.Bacteria()
        elif infeccion.lower() == "parasito":
            self.infeccion = inf.Parasito()

    def descubrimiento_infeccion(self):
        p = self.infeccion.visibilidad * self.infectados * self.muertos**2 / self.poblacion_mundial**3
        if p == 1:
            self.descubierto = True
        elif p == 0:
            self.descubierto = False
        else:
            fract = int(p * 1000)
            if fract < 1:
                self.descubierto = False
            else:
                listat = ListaLigada(*(True for i in range(fract)))
                listaf = ListaLigada(*(False for i in range(1000 - fract)))
                lista = listaf + listat
                shuffle(lista)
                eleccion = randint(0, 1000)
                self.descubierto = lista[eleccion]

    def contagio_entre_paises(self):
        pais_que_contagia = ListaLigada()
        lista_contagiados = ListaLigada()
        pais_contagiado = False
        for pais in self:
            if pais.contagia:
                pais_que_contagia.append(pais.nombre)
                via = randint(0, 1)
                if via == 0:
                    num = pais.contagiar_aire()
                    pais_contagiado = pais.aeropuerto[num].title()
                else:
                    num = pais.contagiar_tierra()
                    pais_contagiado = pais.vecinos[num].title()
        if pais_contagiado:
            for pais in self:
                if pais.nombre == pais_contagiado and not pais.esta_infectado:
                    pais.infectados = 10
                    lista_contagiados.append(pais.nombre)
        return ListaLigada(lista_contagiados, pais_que_contagia)

    @property
    def vivos(self):
        contador = 0
        for pais in self:
            contador += pais.vivos
        return contador

    @property
    def muertos(self):
        contador = 0
        for pais in self:
            contador += pais.muertos
        return contador
    @property
    def infectados(self):
        contador = 0
        for pais in self:
            contador += pais.infectados
        return contador

    @property
    def sanos(self):
        contador = 0
        for pais in self:
            contador += pais.sanos
        return contador

    @property
    def esta_infectado(self):
        for pais in self:
            if pais.esta_infectado:
                return True
        else:
            return False
    @property
    def esta_muerto(self):
        for pais in self:
            if not pais.esta_muerto:
                return False
        else:
            return True

    def __iter__(self):
        return iter(self.paises)

    def __next__(self):
        return next(self.paises)

    def __len__(self):
        return len(self.paises)

    def poblar_mundo(self):
        with open("population.csv", "r") as f:
            archivo = ListaLigada(*f.readlines()[1:])
        for i in range(len(archivo)):
            archivo[i] = archivo[i].strip()
            archivo[i] = archivo[i].split(",")
            archivo[i] = Pais(nombre=archivo[i][0], poblacion=archivo[i][1])
        return archivo

    def agregar_aeropuertos(self):
        generate_connections()
        with open("random_airports.csv", "r") as f:
            archivo = ListaLigada(*f.readlines()[1:])
        for linea in archivo:
            linea = linea.strip()
            linea = ListaLigada(*linea.split(","))
            for pais in self:
                if linea[0].title() == pais.nombre:
                    pais.aeropuerto.append(linea[1].title())
                if linea[1].title() == pais.nombre:
                    pais.aeropuerto.append(linea[0].title())
        for pais in self:
            pais.ordenar_aeropueto()
            for elemento in pais.aeropuerto:
                if pais.aeropuerto.count(elemento) > 1:
                    pais.aeropuerto.remove(elemento)
            pais.respaldos[0] = pais.aeropuerto

    def agregar_vecinos(self):
        with open("borders.csv", "r") as f:
            archivo = ListaLigada(*f.readlines()[1:])
        for linea in archivo:
            linea = linea.strip()
            linea = ListaLigada(*linea.split(";"))
            for pais in self:
                if linea[0].title() == pais.nombre:
                    pais.vecinos.append(linea[1].title())
                if linea[1].title() == pais.nombre:
                    pais.vecinos.append(linea[0].title())
        for pais in self:
            pais.ordenar_vecinos()
            for elemento in pais.vecinos:
                if pais.vecinos.count(elemento) > 1:
                    pais.vecinos.remove(elemento)
            pais.respaldos[1] = pais.vecinos

    def progreso_cura(self):
        if self.descubierto:
            self.cura += int(self.sanos/(2 * self.poblacion_mundial))

    def implantar_cura(self):
        if self.cura >= 100:
            num = randint(0, len(self) - 1)
            self.paises[num].cura = True
            self.implantado = True

    def esparcir_cura(self):
        if self.cura >= 100:
            for pais in self:
                if pais.cura:
                    for otro in self:
                        if otro.nombre in pais.aeropuerto:
                            otro.cura = True

    def actualizar_promedio(self):
        for pais in self:
            for otro in self:
                if otro.nombre in pais.vecinos:
                    pais.promedio += otro.porcentaje_infectados
            if len(pais.vecinos) > 0:
                pais.promedio = pais.promedio / len(pais.vecinos)

if __name__ =="__main__":
    mundo = Planeta("Virus")
    mundo.agregar_aeropuertos()
    mundo.agregar_vecinos()
    for pais in mundo:
        print(pais.nombre, pais.respaldos)
