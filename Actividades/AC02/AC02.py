__author__ = "cotehidalgov"

#Herencia
# -*- coding: utf-8 -*-

import random
from abc import ABCMeta, abstractmethod

class Plate:
    def __init__(self, food, drink):
        self.food = food
        self.drink = drink
    @property
    def calidad(self):
        return (self.food.calidad+self.drink.calidad)/2
    def check_ingredientes(self):
        if type(self.food) == Pizza:
            for ingrediente in self.food.ingredientes:
                if ingrediente == "pepperoni":
                    self.food.calidad += 50
                elif ingrediente == "piña":
                    self.food.calidad -= 50
        else:
            for ingrediente in self.food.ingredientes:
                if ingrediente == "crutones":
                    self.food.calidad += 20
                elif ingrediente == "manzana":
                    self.food.calidad -= 20


class Food(metaclass=ABCMeta):
    def __init__(self,ingredients):
        self.ingredientes = ingredients
        self.calidad = random.randint(50,200)

    @abstractmethod
    def check_time(self):
        pass


class Pizza(Food):
    def __init__(self,ingredients):
        super().__init__(ingredients)
        self.tiempo = random.randint(20,100)

    def check_time(self):
        if self.tiempo < 30:
            pass
        else:
            self.calidad = self.calidad - 30

class Salad(Food):
    def __init__(self,ingredients):
        super().__init__(ingredients)
        self.tiempo = random.randint(5,60)

    def check_time(self):
        if self.tiempo < 30:
            pass
        else:
            self.calidad = self.calidad - 30

class Drink(metaclass=ABCMeta):
    def __init__(self):
        self.calidad = random.randint(50,150)

class Soda(Drink):
    def __init__(self):
       super().__init__()
       self.calidad -= 30

class Juice(Drink):
    def __init__(self):
       super().__init__()
       self.calidad += 30
class Personality(metaclass = ABCMeta):
    def react(self,quality):
        if quality>=100:
            return True
        else:
            return False
    @abstractmethod
    def im_happy(self):
        pass
    @abstractmethod
    def im_mad(self):
        pass
class Hater(Personality):
    def im_happy(self):
        print("No está malo, pero prefiero Pizza x2")
    def im_mad(self):
        print("Nunca más vendré a Daddy Juan´s!")
class Cool(Personality):
    def im_happy(self):
        print("Yumi! Que rico")
    def im_mad(self):
        print("Preguntaré si puedo cambiar el plato")

class Person(metaclass = ABCMeta): # Solo los clientes tienen personalidad en esta actividad
    def __init__(self, name):
        self.name = name

class Chef(Person):
    ingredientes_pizza = ["pepperoni","piña","cebolla","tomate","jamon","pollo"]
    ingredientes_ensalada = ["crutones","espinaca","manzana","zanahoria"]
    def __init__(self,name):
        super().__init__(name)
        self.algo =  None
    def cook(self):
        valor = random.randint(0,1)
        otro = random.randint(0,1)
        ingredientes =[]
        if valor == 0:
            ingredientes.append("queso")
            ingredientes.append("salsa de tomate")
            for i in range(3):
                aleatoria = random.randint(0,5)
                ingredientes.append(Chef.ingredientes_pizza[aleatoria])
                Comida = Pizza(ingredientes)
        else:
            ingredientes.append("lechuga")
            for i in range(2):
                aleatoria = random.randint(0,3)
                ingredientes.append(Chef.ingredientes_ensalada[aleatoria])
                Comida = Salad(ingredientes)
        if otro == 0:
            Vaso = Soda()
        else:
            Vaso = Juice()
        Plato = Plate(Comida,Vaso)
        Plato.check_ingredientes()
        return Plato

class Client(Person):
    def __init__(self,name,perso):
        super().__init__(name)
        self.personalidad = perso
    def eat(self,plate):
        if self.personalidad.react(plate.calidad):
            self.personalidad.im_happy()
        else:
            self.personalidad.im_mad()

class Restaurant:
    def __init__(self, chefs, clients):
        self.chefs = chefs
        self.clients = clients

    def start(self):
        for i in range(3): # Se hace el estudio por 3 dias
            print("----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    plates.append(chef.cook()) # Retorna platos de comida y bebida

            for client in self.clients:
                for plate in plates:
                    print(plate.calidad)
                    client.eat(plate)



if __name__ == '__main__':
    chefs = [Chef("Cote"), Chef("Joaquin"), Chef("Andres")]
    clients = [Client("Bastian", Hater()), Client("Flori", Cool()),
                Client("Antonio", Hater()), Client("Felipe", Cool())]

    restaurant = Restaurant(chefs, clients)
    restaurant.start()
