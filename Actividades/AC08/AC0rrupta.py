__author__ = "cotehidalgov"
__coauthor__ = "Diego Andai"
# -*- coding: utf-8 -*-
import random

###############################################################################
#Solo puedes escribir código aquí, cualquier modificación fuera de las lineas
#será penalizada con nota 1.0


class MetaPerson(type):
    def __new__(meta, name, bases, dic):
        if bases != (Person,):
            bases = (Person,)

        def cook(self):
            plato = Plate()
            self.choose_food(plato)
            self.choose_drink(plato)
            return plato

        def eat(self, plato):
            # Se asume que las clases de plato.food y de plato.drink solo pueden ser Food y/o Drink
            # si el plato es correcto
            if issubclass(plato.food.__class__, Food):
                if issubclass(plato.drink.__class__, Drink):
                    calidad = plato.drink.quality + plato.food.quality
                    if calidad > 50:
                        print("Que delicia!")
                    elif calidad <= 50:
                        print("Esto no es digno de mi paladar")

                # si el plato es incorrecto porque drink es food
                else:
                    print("El plato tiene dos comidas")
                    # si el plato es incorrecto porque food es drink
            else:
                print("El plato tiene dos bebidas")

        restaurant_asignado = None

        if name == "Chef":
            dic["restaurant_asignado"] = restaurant_asignado
            dic["cook"] = cook
        elif name == "Client":
            dic["eat"] = eat

        return super().__new__(meta, name, bases, dic)

    def __init__(cls, name, bases, dic):
        super().__init__(name, bases, dic)

    def __call__(cls, *args, **kwargs):
        return super().__call__(*args, **kwargs)


class MetaRestaurant(type):
    def __new__(meta, name, bases, dic):
        def valido(self, chef):
            todos_los_chefs = set()
            for restorant in self.lista_instancias:
                if restorant.name != self.name:
                    for cocinero in restorant.chefs:
                        todos_los_chefs.add(cocinero)
            if chef in todos_los_chefs:
                return False
            else:
                return True
        dic["valido"] = valido
        dic["lista_instancias"] = []
        return super().__new__(meta, name, bases, dic)

    def __init__(cls, name, bases, dic):
        def llega_cliente(self, cliente):
            if isinstance(cliente, Client):
                self.clients.append(cliente)

        def cliente_se_va(self, cliente):
            if cliente in self.clients:
                self.clients.remove(cliente)

        def start(self):
            if not self.clients:
                print("{} no tiene clientes, que pena".format(self.name))
            cls.__dict__["start"]()

        dic["llega_cliente"] = llega_cliente
        dic["cliente_se_va"] = cliente_se_va
        dic["start"] = start
        super().__init__(name, bases, dic)

    def __call__(cls, *args, **kwargs):
        try:
            a = super().__call__(*args, **kwargs)
            if len(a.chefs) == 0:
                raise ValueError("Debe haber algun chef para tener un restorant")
            for chef in a.chefs:
                chef.restaurant_asignado = a.name
                if not a.valido(chef):
                    raise ValueError("No todos los chefs son validos")
            else:
                print("Instanciación existosa")
            cls.lista_instancias.append(a)
            return a
        except TypeError:
            print("Debes introducir, nombre, chefs y clientes")
            a = super().__call__("nombre", [], [])
            return a






###############################################################################
#De aquí para abajo no puedes cambiar ABSOLUTAMENTE NADA


class Person:
    def __init__(self, name):
        self.name = name


class Food:
    def __init__(self, ingredients):
        self._quality = random.randint(50, 200)
        self.preparation_time = 0
        self.ingredients = ingredients


    @property
    def quality(self):
        return self._quality * random.random()


class Drink:
    def __init__(self):
        self._quality = random.randint(5, 15)

    @property
    def quality(self):
        return self._quality * random.random()


class Restaurant(metaclass = MetaRestaurant):
    def __init__(self, name, chefs, clients):
        self.name = name
        self.chefs = chefs
        self.clients = clients


    def start(self):
        for i in range(1):  # Se hace el estudio por 5 dias
            print("----- Día {} -----".format(i + 1))
            plates = []
            for chef in self.chefs:
                for j in range(3):  # Cada chef cocina 3 platos
                    plates.append(chef.cook())  # Retorna platos de comida y bebida

            for client in self.clients:
                for plate in plates:
                    client.eat(plate)


class Pizza(Food):
    def __init__(self, ingredients):
        super(Pizza, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 100)


class Salad(Food):
    def __init__(self, ingredients):
        super(Salad, self).__init__(ingredients)
        self.preparation_time = random.randint(5, 60)


class Coke(Drink):
    def __init__(self):
        super(Coke, self).__init__()
        self._quality -= 5


class Juice(Drink):
    def __init__(self):
        super(Juice, self).__init__()
        self._quality += 5


class Plate:
    def __init__(self):
        self.food = None
        self.drink = None


class Chef(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Chef, self).__init__(name)

    def choose_food(self, plate):
        food_choice = random.randint(0, 1)
        ingredients = []
        if food_choice == 0:
            for i in range(3):
                ingredients.append(random.choice(["pepperoni", "piña", "cebolla", "tomate", "jamón", "pollo"]))
            plate.food = Pizza(ingredients)
        else:
            for i in range(2):
                ingredients.append(random.choice(["crutones", "espinaca", "manzana", "zanahoria", "palta"]))
            plate.food = Salad(ingredients)

    def choose_drink(self, plate):
        drink_choice = random.randint(0, 1)
        if drink_choice == 0:
            plate.drink = Coke()
        else:
            plate.drink = Juice()


class Client(Pizza, metaclass=MetaPerson):
    def __init__(self, name):
        super(Client, self).__init__(name)


if __name__ == '__main__':

    chefs = [Chef("Enzo"), Chef("Nacho"), Chef("Diego")]
    clients = [Client("Bastian"), Client("Flori"),
                Client("Rodolfo"), Client("Felipe")]
    McDollars = Restaurant("Mc", chefs, clients)

    BurgerPimp = Restaurant("BK")

    KFK = Restaurant("KFK", [Chef("Enzo")])

    McDollars.start()
    KFK.start()
