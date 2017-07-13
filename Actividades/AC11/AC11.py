import sys
from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication, QLabel, QWidget, QVBoxLayout,QGridLayout
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtTest import QTest
from random import shuffle

# Creamos nuestra clase en donde tendremos los componentes graficos de nuestro programa
# Hereda de QMainWindow

class Progarice(QWidget):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.botones = []
        self.init_progarice()

        #definimos un metodo en donde inicializaremos cada componente
    # y definiremos las conexiones de nuestro programa
    def init_progarice(self):
        # Titulo
        # Para crear un texto sobre nuestra ventana principal, usamos un QLabel,
        #  fijamos su contenido
        # y luego lo movemos a la posicion deseada. Por ultimo,
        # usamos show para que aparezca al correr el programa

        self.titulo = QLabel(self)
        self.titulo.setText("Progarice")
        self.titulo.move(450,10)
        self.titulo.show()
        self.grilla = QGridLayout()
        self.posiciones = ["Imgs/{}.png".format(i) for i in range(1,13)
                           for j in range(2)] + ["Imgs/b.png"]
        shuffle(self.posiciones)
        posicion = [(i,j) for i in range(5) for j in range(5)]
        valores = ["Imgs/back.png" for i in range(25)]
        self.intentos = 0
        i = 0
        for posicion, valor in zip(posicion,valores):

            if valor == "":
                continue

            #foto/boton
            carta = QPixmap(valor)#.scaled(1000,1000)
            carta = QIcon(carta)
            boton = QPushButton(self)
            boton.setFixedHeight(100)
            boton.setFixedWidth(100)
            boton.setIconSize(QSize(100,100))
            boton.setIcon(carta)
            boton.vuelta = False
            boton.cara = self.posiciones[i]
            self.botones.append(boton)
            i += 1
            # Con esta linea, conectaremos el click a nuestro boton
            # con cierta funcionalidad que hayamos creado
            self.grilla.addWidget(boton, *posicion)
            boton.clicked.connect(self.cambiar_imagen)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("",self))
        vbox.addLayout(self.grilla)
        self.setLayout(vbox)

        # Cantidad de matches
        self.nro_matches = QLabel(self)
        self.nro_matches.setText("Intentos:  ")
        self.nro_matches.move(10,10)
        self.nro_matches.show()

        self.path_imagenes = "Imgs/"


        # se da forma a la ventana principal y se muestra
        self.setGeometry(100, 100, 900, 600)
        self.show()


    def cambiar_imagen(self):
        boton = self.sender()
        if boton.vuelta:
           pass
        #idx = self.grilla.indexOf(boton)
        #posicion = self.grilla.getItemPosition(idx)
        else:
            if boton.cara == "Imgs/b.png":
                self.intentos += 10
                self.nro_matches.setText("Intentos: {}".format(self.intentos))
            try:
                carta = QPixmap(boton.cara)  # .scaled(1000,1000)
                carta = QIcon(carta)
                boton.vuelta = True
                boton.setIcon(carta)
                dados_vuelta = []
                for elemento in self.botones:
                    if elemento.vuelta:
                        dados_vuelta.append(elemento)
                if len(dados_vuelta) % 2 == 0:
                    self.revisar(dados_vuelta)
            except Exception as err:
                print(err)

    def revisar(self,dados_vuelta):
        self.intentos += 1
        self.nro_matches.setText("Intentos: {}".format(self.intentos))
        QTest.qWait(3000)
        for i in range(len(dados_vuelta)):
            if dados_vuelta.count(dados_vuelta[i]) == 1:
                carta = QPixmap("Imgs/back.png")  # .scaled(1000,1000)
                carta = QIcon(carta)
                dados_vuelta[i].vuelta = False
                dados_vuelta[i].setIcon(carta)
        else:
            pass

    def hacer_match(self):
        self.numero_matches += 1
        self.cambiar_imagen()
        self.nro_matches.setText("Matches: {0}".format(self.numero_matches))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Progarice()
    sys.exit(app.exec_())