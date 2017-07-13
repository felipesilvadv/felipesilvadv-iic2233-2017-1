from Gobierno import Gobierno
from EDD import ListaLigada
from random import randint, shuffle


class Pais:

    def __init__(self, nombre, poblacion, infectados=0, muertos=0):
        self.nombre = str(nombre).title()
        self.vecinos = ListaLigada()
        self.aeropuerto = ListaLigada()
        self.gob = Gobierno()
        self.poblacion = int(poblacion)
        self.infectados = int(infectados)
        self.muertos = int(muertos)
        self.cura = False
        self.infeccion = None
        self.mascarillas = False
        self.dias = 0
        self.promedio = 0.0
        self.respaldos = ListaLigada(None, None)

    @property
    def porcentaje_infectados(self):
        return self.infectados/self.poblacion

    @property
    def porcentaje_muertos(self):
        return self.muertos / self.poblacion

    @property
    def sanos(self):
        return self.poblacion - self.infectados

    @property
    def vivos(self):
        return self.poblacion - self.muertos

    @property
    def esta_infectado(self):
        if self.infectados > 0:
            return True
        else:
            return False

    @property
    def esta_muerto(self):
        if self.muertos == self.poblacion:
            return True
        else:
            return False

    def ordenar_aeropueto(self):
        self.aeropuerto = self.aeropuerto.msort()

    def ordenar_vecinos(self):
        self.vecinos = self.vecinos.msort()

    @property
    def contagia(self):  # a otro pais
        valor = (7 * self.infectados)/self.vivos
        p = min(valor, 1)
        if p == 1:
            return True
        else:
            fract = int(p * 1000)
            if fract < 1:
                return False
            else:
                listat = ListaLigada(*(bool(i) for i in range(fract)))
                listaf = ListaLigada(*(not bool(i) for i in range(1000 - fract)))
                lista = listaf + listat
                shuffle(lista)
                eleccion = randint(0, 1000)
                return lista[eleccion]

    def contagiar_aire(self):
        if len(self.aeropuerto) != 0 and self.esta_infectado:
            pais_contagio = randint(0, len(self.aeropuerto))
            return int(pais_contagio)

    def contagiar_tierra(self):
        if len(self.vecinos) != 0 and self.esta_infectado:
            pais_contagio = randint(0, len(self.vecinos))
            return int(pais_contagio)

    def contagio_interno(self):
        if self.infectados:
            random = randint(0, 6)
            if self.mascarillas:
                random *= 0.3
            self.infectados *= int(self.infeccion.contagiosidad * random)

    def esparcir_cura(self):
        if self.cura:
            p = 0.25
            p *= self.infeccion.resistencia
            self.infectados = int(self.infectados - self.infectados * p)

    def muerte(self):
        if self.esta_infectado:
           p = min(max(0.2, (self.dias**2)/100000) * self.infeccion.mortalidad, 1)
           muertos = self.infectados * p
           self.infectados = int(self.infectados - muertos)
           self.muertos = int(self.muertos + muertos)
           if self.muertos > self.poblacion:
               self.muertos = self.poblacion

if __name__ == "__main__":
    Chile = Pais("Chile", 17000000, 100000, 1000)
    Chile.aeropuerto.append("Argentina")
    print(Chile.contagia)
