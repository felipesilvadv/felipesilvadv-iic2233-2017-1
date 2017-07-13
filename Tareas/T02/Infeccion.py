class Infeccion:

    def __init__(self, resistencia=0.0, visibilidad=0.0, mortalidad=0.0, contagiosidad=0.0):
        self.resistencia = resistencia
        self.visibilidad = visibilidad
        self.mortalidad = mortalidad
        self.contagiosidad = contagiosidad


class Virus(Infeccion):

    def __init__(self):
        super().__init__(contagiosidad=1.5, mortalidad=1.2, resistencia=1.5, visibilidad=0.5)


class Bacteria(Infeccion):

    def __init__(self):
        super().__init__(contagiosidad=1.0, mortalidad=1.0, resistencia=0.5, visibilidad=0.7)


class Parasito(Infeccion):

    def __init__(self):
        super().__init__(contagiosidad=0.5, mortalidad=1.5, resistencia=1.0, visibilidad=0.45)


if __name__ == "__main__":
    pass
