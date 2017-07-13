__author__ = 'Ignacio Castaneda, Diego Iruretagoyena, Ivania Donoso, CPB'

import random
from datetime import datetime


"""
Escriba sus decoradores y funciones auxiliares en este espacio.
"""


def verificar_transferencia(funcion):
    def _verificar_transferencia(self, origen, destino, monto, clave):
        if origen in self.cuentas.keys():
            corigen = self.cuentas[origen]
        else:
            raise AssertionError("No existe la cuenta de origen")
        if destino in self.cuentas.keys():
            cdestino = self.cuentas[destino]
        else:
            raise AssertionError("No existe la cuenta de destino")
        if clave != corigen.clave:
            raise AssertionError("La clave es incorrecta, no puedes transferir")
        else:
            funcion(self, origen, destino, monto, clave)
    return _verificar_transferencia


def verificar_inversion(funcion):
    def _verificar_inversion(self, cuenta, monto, clave):
        if cuenta in self.cuentas.keys():
            cuenta1 = self.cuentas[cuenta]
        else:
            raise AssertionError("La cuenta no existe")

        if cuenta1.saldo < monto:
            raise AssertionError("No tienes saldo suficiente para realizar esta inversión")
        elif cuenta1.clave != clave:
            raise AssertionError("Clave incorrecta, no puedes invertir")
        elif cuenta1.inversiones > 10000000:
            raise AssertionError("Tienes más de 10.000.000, en inversiones, no puedes invertir más")
        else:
            funcion(self, cuenta, monto, clave)
    return _verificar_inversion


def verificar_cuenta(funcion):
    def _verificar_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        while numero in self.cuentas.keys():
            numero = int(random.random() * 100)
        if rut[-2] != "-":
            raise AssertionError("Rut inválido, no tiene guión en la penúltima posición")
        elif not rut[-1].isdecimal():
            raise AssertionError("Rut inválido, último dígito no es un número")
        rut1 = ("b" + rut).strip(rut[-1])
        rut1 = rut1.strip(rut1[-1]).strip("b")
        for letra in rut1:
            if not letra.isdecimal():
                raise AssertionError("Rut inválido, no todos sus elementos son números")
        for numero in clave:
            if not numero.isdecimal():
                raise AssertionError("Clave inválida, solo debe tener números")
        if len(clave) != 4:
            raise AssertionError("Clave inválida, debe tener 4 números")
        funcion(self, nombre, rut, clave, numero, saldo_inicial=0)
    return _verificar_cuenta


def verificar_saldo(funcion):
    def _verificar_saldo(self, numero_cuenta):
        try:
            cuenta1 = self.cuentas[numero_cuenta]
        except KeyError:
            raise AssertionError("La cuenta no existe, no puedes verificar el saldo")
        return cuenta1.saldo
    return _verificar_saldo


def log(path):
    f = open(path, "w")
    f.close()

    def _log(cls):
        saldo = getattr(cls, "saldo")
        transferir = getattr(cls, "transferir")
        crear_cuenta = getattr(cls, "crear_cuenta")
        invertir = getattr(cls, "invertir")

        def saldo_nuevo(cls, numero_cuenta):
            ahora = datetime.now()
            a = saldo(cls, numero_cuenta)
            with open(path, "a") as archivo:
                archivo.write("{0}-Consulta Saldo: {1} |{2}\n".format(ahora, numero_cuenta, a))
            return a

        def transferir_nuevo(cls, origen, destino, monto, clave):
            ahora = datetime.now()
            with open(path, "a") as archivo:
                archivo.write("{0}-Transferencia: {1}, {2}, {3}, {4} | \n".format(ahora,
                                                                                   origen, destino, monto, clave))
            transferir(cls, origen, destino, monto, clave)

        def nuevo_crear_cuenta(cls, nombre, rut, clave, numero, saldo_inicial=0):
            ahora = datetime.now()
            with open(path, "a") as archivo:
                archivo.write(
                    "{0}-Crear Cuenta: {1}, {2}, {3}, {4}, {5} | \n".format(ahora,
                                                                              nombre,
                                                                              rut, clave, numero, saldo_inicial))
            crear_cuenta(cls, nombre, rut, clave, numero, saldo_inicial=0)

        def nuevo_invertir(cls, cuenta, monto, clave):
            ahora = datetime.now()
            with open(path, "a") as archivo:
                archivo.write("{0}-Inversion: {1}, {2}, {3} | \n".format(ahora, cuenta, monto, clave))
            invertir(cls, cuenta, monto, clave)
        setattr(cls, "invertir", nuevo_invertir)
        setattr(cls, "saldo", saldo_nuevo)
        setattr(cls, "crear_cuenta", nuevo_crear_cuenta)
        setattr(cls, "transferir", transferir_nuevo)
        return cls
    return _log



"""
No pueden modificar nada más abajo, excepto para agregar los decoradores a las 
funciones/clases.
"""
@log("Operaciones.txt")
class Banco:
    def __init__(self, nombre, cuentas=None):
        self.nombre = nombre
        self.cuentas = cuentas if cuentas is not None else dict()

    @verificar_saldo
    def saldo(self, numero_cuenta):
        # Da un saldo incorrecto
        return self.cuentas[numero_cuenta].saldo * 5

    @verificar_transferencia
    def transferir(self, origen, destino, monto, clave):
        # No verifica que la clave sea correcta, no verifica que las cuentas 
        # existan
        self.cuentas[origen].saldo -= monto
        self.cuentas[destino].saldo += monto

    @verificar_cuenta
    def crear_cuenta(self, nombre, rut, clave, numero, saldo_inicial=0):
        # No verifica que el número de cuenta no exista
        cuenta = Cuenta(nombre, rut, clave, numero, saldo_inicial)
        self.cuentas[numero] = cuenta

    @verificar_inversion
    def invertir(self, cuenta, monto, clave):
        # No verifica que la clave sea correcta ni que el monto de las 
        # inversiones sea el máximo
        self.cuentas[cuenta].saldo -= monto
        self.cuentas[cuenta].inversiones += monto

    def __str__(self):
        return self.nombre

    def __repr__(self):
        datos = ''

        for cta in self.cuentas.values():
            datos += '{}\n'.format(str(cta))

        return datos

    @staticmethod
    def crear_numero():
        return int(random.random() * 100)


class Cuenta:
    def __init__(self, nombre, rut, clave, numero, saldo_inicial=0):
        self.numero = numero
        self.nombre = nombre
        self.rut = rut
        self.clave = clave
        self.saldo = saldo_inicial
        self.inversiones = 0

    def __repr__(self):
        return "{} / {} / {} / {}".format(self.numero, self.nombre, self.saldo,
                                          self.inversiones)


if __name__ == '__main__':
    bco = Banco("Santander")
    bco.crear_cuenta("Mavrakis", "4057496-7", "1234", bco.crear_numero())
    bco.crear_cuenta("Ignacio", "19401259-4", "1234", 1, 24500)
    bco.crear_cuenta("Diego", "19234023-3", "1234", 2, 13000)
    bco.crear_cuenta("Juan", "19231233--3", "1234", bco.crear_numero())

    print(repr(bco))
    print()

    """
    Estos son solo algunos casos de pruebas sugeridos. Sientase libre de agregar 
    las pruebas que estime necesaria para comprobar el funcionamiento de su 
    solucion.
    """
    try:
        print(bco.saldo(10))
    except AssertionError as error:
        print('Error: ', error)

    try:
        print(bco.saldo(1))
    except AssertionError as error:
        print('Error: ', error)

    try:
        bco.transferir(1, 2, 5000, "1234")
    except AssertionError as msg:
        print('Error: ', msg)

    try:
        bco.transferir(1, 2, 5000, "4321")
    except AssertionError as msg:
        print('Error: ', msg)

    print(repr(bco))
    print()

    try:
        bco.invertir(2, 200000, "1234")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))

    try:
        bco.invertir(2, 200000, "4321")
    except AssertionError as error:
        print('Error: ', error)
    print(repr(bco))
