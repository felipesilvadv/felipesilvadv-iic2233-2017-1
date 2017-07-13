from EDD import ListaLigada
from random import randint


class Gobierno:

    def __init__(self):
        self.cola = ListaLigada()

    def __repr__(self):
        return "\n".join(self.cola)

    def formar_cola(self, pais):
        cf = Medida(*self.cerrar_fronteras(pais))
        ca = Medida(*self.cerrar_aeropuertos(pais))
        mm = Medida(*self.mandar_mascarillas(pais))
        af = Medida(*self.abrir_fronteras(pais))
        if cf.bool:
            self.cola.append(cf)
        elif af.bool:
            self.cola.append(af)
        if ca.bool:
            self.cola.append(ca)
        if mm.bool:
            self.cola.append(mm)
        self.cola = self.cola.msort()

    def cerrar_aeropuertos(self, pais):
        # basandose en la situacion del pais debe determinar si cierra su aeropuerto
        # si la mitad esta infectada o un cuarto esta muerto se cierran
        infectados = pais.porcentaje_infectados
        muertos = pais.porcentaje_muertos
        prioridad = 0.8 * infectados
        return "Cerrar aeropuertos", infectados >= 0.8 or muertos >= 0.2, prioridad

    def cerrar_fronteras(self, pais):
        # basandose en la situacion del self.pais debe determinar si se cierran la fronteras terrestres
        # Se cierran si es que mas del 80% esta infectado o mas del 20% esta muerto
        infectados = pais.porcentaje_infectados
        muertos = pais.porcentaje_muertos
        accion = pais.promedio
        prioridad = accion * infectados
        return "Cerrar fronteras", infectados >= 0.5 or muertos >= 0.25, prioridad

    def mandar_mascarillas(self, pais):
        # si mas de un tercio de la poblacion esta infectada se mandan mascarillas lo que baja
        # la tasa de contagiosidad (multiplica por 0.3 la cantidad aleatoria de infectados)
        infectados = pais.porcentaje_infectados
        prioridad = 0.5 * infectados
        return "Mandar mascarillas", infectados >= 0.33, prioridad

    def abrir_fronteras(self, pais):
        if pais.cura:
            prioridad = 1
        else:
            prioridad = pais.porcentaje_infectados * 0.7
        return "Abrir fronteras", not (self.cerrar_aeropuertos(pais) or self.cerrar_fronteras(pais)), prioridad


class Medida:

    def __init__(self, nombre, bool, prioridad):
        self.nombre = nombre
        self.bool = bool
        self.prioridad = prioridad

    def __repr__(self):
        return str(self.nombre) + "\n Nivel prioridad: {}".format(self.prioridad)

    def __eq__(self, other):
        return self.bool and other.bool and self.prioridad == other.prioridad

    def __gt__(self, other):
        return self.bool and other.bool and self.prioridad > other.prioridad

    def __lt__(self, other):
        return self.bool and other.bool and self.prioridad < other.prioridad

    def __le__(self, other):
        return self.bool and other.bool and self.prioridad <= other.prioridad

    def __ge__(self, other):
        return self.bool and other.bool and self.prioridad >= other.prioridad

    def __ne__(self, other):
        return self.bool and other.bool and self.prioridad != other.prioridad

if __name__ == "__main__":
    lista = ListaLigada()
    for i in range(10):
        lista.append(Medida("", True, i + randint(0, 10)))
    lista = lista.msort()
    print(lista)