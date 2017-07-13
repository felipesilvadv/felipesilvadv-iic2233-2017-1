from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication, QLabel,
                             QWidget, QVBoxLayout,QGridLayout, QGraphicsItem,
                             QGraphicsWidget)
from PyQt5.QtGui import (QPixmap, QIcon, QPalette, QKeyEvent, QImage, QBrush,
                         QKeySequence, QMouseEvent, QCursor, QFont, QColor,
                         QTextItem)

import sys

class Tienda(QWidget):
    def __init__(self, mouse, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init(mouse)

    def init(self, QCursor):
        self.setGeometry(20, 20, 600, 300)
        self.setMaximumSize(600, 300)
        self.setMinimumSize(600, 300)
        self.mouse = QCursor
        self.setCursor(self.mouse)
        #self.boton = QPushButton(self)
        self.titulo = QLabel(self)
        self.titulo.setGeometry(150, 0, 300, 20)
        self.titulo.setText("Apreta el objeto que quieras comprar")
        self.titulo.setFont(QFont("Sans Serif", 12))
        self.titulo.setStyleSheet("color: {red}")
        #self.boton.setText("Comprar")
        #self.boton.setGeometry(40, 40, 100, 50)
        #self.link = QLabel(self)
        #self.pixmap = QPixmap("./IMGS/link.png")  # .scaled(1200//4, 1040//4)
        # pixmap = QRect(0,0, 20,20)
#        pixmap = self.pixmap.copy(QRect(0, 900, 100, 1040))
 #       self.link.setPixmap(pixmap)
 #       self.link.setGeometry(0, 0, 120, 170)
        # self.link.setGeometry(200, 200, 100, 100)
        self.contador = 0
        #self.show()
        self.grilla = QGridLayout()
        posiciones = [(i, j ) for i in range(2) for j in range(3)]
        valores = ["Arma de mano", "Botas", "Arma de distancia", "Baculo",
                   "Armadura", "Carta Earthstone"]
        for posicion, valor in zip(posiciones, valores):
            boton = QPushButton(valor)
            self.grilla.addWidget(boton, *posicion)

        self.setLayout(self.grilla)

    def keyPressEvent(self, QKeyEvent):
        tecla = QKeyEvent.key()

        if tecla == ord("O"):
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mouse = QCursor(QPixmap("./IMGS/cursor.png"))
    ex = Tienda(mouse)
    sys.exit(app.exec_())