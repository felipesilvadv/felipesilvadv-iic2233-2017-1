from PyQt5.QtWidgets import (QMainWindow, QPushButton, QApplication, QLabel,
                             QWidget, QVBoxLayout,QGridLayout, QGraphicsItem,
                             QGraphicsWidget, QProgressBar)
from PyQt5.QtGui import (QPixmap, QIcon, QPalette, QKeyEvent, QImage, QBrush,
                         QKeySequence, QMouseEvent, QCursor, QFont, QColor,
                         QTextItem)
from PyQt5.QtCore import Qt, QSize, QThread, QRect, QPoint, pyqtSignal
from PyQt5.QtTest import QTest
from modulo2 import (movimiento_w, movimiento_a, movimiento_s,
                     movimiento_d, sobre, animate_link, animate_naruto)
import modulo3 as m3
import sys
from modulo4 import Tienda
from time import sleep

class MiVentana(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("League of Progra")
        self.nombre_champ = ""
        self.setMouseTracking(True)
        self.setMaximumSize(1100, 650)
        self.setMinimumSize(1100, 650)
        self.move(0, 0)
        self.in_game = False
        self.estructuras = []
        self.contador = 0
        #self.animate = m3.Animation(self)

        ## Titulo de pantalla de inicio
        self.inicio = QLabel(self.window())
        self.inicio.setGeometry(120, 40, 800, 100)
        font = QFont("Helvenica", 30, italic=True)
        font.setBold(True)
        self.inicio.setStyleSheet("color: red")
        self.inicio.setFont(font)
        self.inicio.setText("Bienvenido a League of Progra !!")

        ## Se forma el fondo de pantalla
        imagen = QImage("./IMGS/pantalla_inicio.png")
        imagen = imagen.scaled(QSize(1100, 650))
        self.fondo = QPalette()
        self.fondo.setBrush(10, QBrush(imagen))
        self.setPalette(self.fondo)

        # Icono del juego
        icono = QIcon("./IMGS/icon.jpeg")
        self.setWindowIcon(icono)


        # Cursor personalizado
        self.mouse = QCursor(QPixmap("./IMGS/cursor.png"))
        self.setCursor(self.mouse)


        # Tienda
        self.tienda = Tienda(self.mouse)
        self.tienda.setWindowTitle("Tienda")

        # Boton de inicio del juego
        self.boton_partida = QPushButton(self.window())
        self.boton_partida.setGeometry(350, 400, 300, 100)
        icon = QPixmap("./IMGS/boton_inicio.jpg")
        icon = icon.scaled(QSize(300,100))
        self.boton_partida.setIconSize(QSize(300,100))
        self.boton_partida.setIcon(QIcon(icon))
        self.boton_partida.clicked.connect(self.menu)

        ## Se muestra el menu inicial
        self.show()

        ### Todo lo que se define de aqui en adelante es para usarlo despues

        """----------Pantalla de eleccion modo de juego---------------"""

        # Titulo de esta pantalla
        self.eleccion = QLabel(self.window())
        self.eleccion.setGeometry(300, 30, 800, 75)
        self.eleccion.setText("Escoge el modo de juego")
        fuente = QFont("Helvenica", 30, italic=True)
        fuente.setBold(True)
        self.eleccion.setFont(fuente)
        self.eleccion.setStyleSheet("color: red")


        # Boton para elegir partida nueva
        self.partida_nueva = QPushButton(self.window())
        self.partida_nueva.setGeometry(0, 0, 400,100)
        self.partida_nueva.move(self.boton_partida.x() - 300,
                                self.boton_partida.y())
        self.partida_nueva.setText("Partida Nueva")
        self.partida_nueva.setStyleSheet("color: red")
        fuente = QFont("Helvenica", 20, italic=True)
        fuente.setBold(True)
        self.partida_nueva.setFont(fuente)
        pallet = QPalette()
        pallet.setBrush(1, QBrush(QImage()))
        self.partida_nueva.setPalette(pallet)
        self.partida_nueva.clicked.connect(self.ir_a_seleccion)


        # Boton para elegir cargar partida
        self.cargar_partida = QPushButton(self.window())
        self.cargar_partida.setGeometry(0,0, 400, 100)
        self.cargar_partida.move(self.boton_partida.x() + 300,
                                self.boton_partida.y())
        self.cargar_partida.setText("Cargar Partida")
        self.cargar_partida.setStyleSheet("color: red")
        self.cargar_partida.setFont(fuente)
        self.cargar_partida.setPalette(pallet)
        self.cargar_partida.clicked.connect(self.menu_partidas)


        """ ----------Pantalla de seleccion de campeon -------------"""
        # Titulo
        self.seleccion_campeon = QLabel(self.window())
        self.seleccion_campeon.setStyleSheet("color: red")
        fuente = QFont("Helvenica", 30)
        fuente.setBold(True)
        self.seleccion_campeon.setGeometry(300, 5, 500, 50)
        self.seleccion_campeon.setFont(fuente)
        self.seleccion_campeon.setText("Elige a tu campeon")

        # Boton para seleccionar a Hernan
        self.seleccionar_hernan = QPushButton(self.window())
        self.seleccionar_hernan.setGeometry(100, 60, 250, 250)
        hernan = QIcon("./IMGS/hernan.png")
        self.seleccionar_hernan.setIconSize(QSize(250,250))
        self.seleccionar_hernan.setIcon(hernan)
        self.seleccionar_hernan.clicked.connect(self.iniciar_partida)
        self.hernan = QLabel(self.window())
        self.hernan.setGeometry(100, 315, 250, 40)
        fuente = QFont("Helvenica", 14)
        fuente.setBold(True)
        self.hernan.setFont(fuente)
        self.hernan.setStyleSheet("color: yellow")
        self.hernan.setText("Hernan el destructor")

        # Boton para seleccionar a Chau
        self.seleccionar_chau = QPushButton(self.window())
        self.seleccionar_chau.setGeometry(700, 60, 250, 250)
        self.seleccionar_chau.clicked.connect(self.iniciar_partida)
        chau = QIcon("./IMGS/chau.png")
        self.seleccionar_chau.setIconSize(QSize(250,250))
        self.seleccionar_chau.setIcon(chau)
        self.chau = QLabel(self.window())
        self.chau.setGeometry(700, 315, 250, 40)
        self.chau.setFont(fuente)
        self.chau.setStyleSheet("color: yellow")
        self.chau.setText("Chau la hechicera")


        # Boton para seleccionar a tercer Campeon
        self.seleccionar_campeon_sorpresa = QPushButton(self.window())
        self.seleccionar_campeon_sorpresa.setGeometry(400, 360, 250, 250)
        self.seleccionar_campeon_sorpresa.clicked.connect(self.iniciar_partida)
        self.seleccionar_campeon_sorpresa.setIconSize(QSize(250,250))
        naruto = QIcon("./IMGS/cara_naruto.png")
        self.seleccionar_campeon_sorpresa.setIcon(naruto)
        self.naruto = QLabel(self.window())
        self.naruto.setFont(fuente)
        self.naruto.setStyleSheet("color: yellow")
        self.naruto.setGeometry(400, 360 + 250 +5, 250, 40)
        self.naruto.setText("Naruto Uzumaki")

        # Nexo aliado

        self.nexo_a = Estructura("./IMGS/nexo.png",
                                 "./IMGS/nexo_resaltado.png",
                                 (100, 100), 1200, self)
        self.nexo_a.setGeometry(70, 520, 100,100)
       # self.barra_nexo_a = QProgressBar(self)
       # self.barra_nexo_a.setGeometry(70, 510, 100, 10)
       # self.barra_nexo_a.setValue(100)
        self.estructuras.append(self.nexo_a)

        # Nexo enemigo
        self.nexo_b = Estructura("./IMGS/nexo_enemigo.png",
                                 "./IMGS/destacado_enemigo.png",
                                 (100, 100), 1200, self)
        self.nexo_b.setGeometry(880, 20, 100, 100)
       # self.barra_nexo_b = QProgressBar(self)
       # self.barra_nexo_b.setGeometry(1000, 0, 100, 10)
       # self.barra_nexo_b.setValue(100)
        self.estructuras.append(self.nexo_b)

        # Torre aliada
        self.torre_a = Estructura("./IMGS/torre.png",
                                  "./IMGS/torre_resaltado.png",
                                  (50,120), 800, self)
        self.torre_a.setGeometry(220, 400, 50,120)
       # self.barra_torre_b = QProgressBar(self)
       # self.barra_torre_b.setGeometry(70, 510, 100, 10)
       # self.barra_torre_b.setValue(100)
        self.estructuras.append(self.torre_a)

        # Torre enemiga
        self.torre_b = Estructura("./IMGS/torre_derecha.png",
                                  "./IMGS/destacado_derecho.png",
                                  (50, 120), 800, self)
        self.torre_b.setGeometry(730, 140, 50, 120)
        self.estructuras.append(self.torre_b)

        # Inhibidor aliado
        self.inhibidor = Estructura("./IMGS/inhibidor_azul.png",
                                    "./IMGS/inhibidor_azul.png",
                                    (50,50), 600, self)
        self.inhibidor.setGeometry(170, 500, 50,50)
        self.estructuras.append(self.inhibidor)

        # Inhibidor enemigo
        self.inhibidor_p = Estructura("./IMGS/inhibitor_p.png",
                                    "./IMGS/inhibitor_p.png",
                                    (50, 50), 600, self)
        self.inhibidor_p.setGeometry(800, 100, 50, 50)
        self.estructuras.append(self.inhibidor_p)

        #self.animacion = Animation(self)

        #self.link.barra.setValue(self.link.vida)
        #self.barra_champion = QProgressBar(self)
        #self.barra_champion.setGeometry(0, 480, 120, 20)
        #self.barra_champion.setValue(100)
      #  self.webeo = QPushButton(self)
      #  self.webeo.move(210, 100)
      #  self.webeo.setText("Zumbar")
      #  self.webeo.clicked.connect(self.empezo_webeo)
      #  self.boton = QPushButton(self)
      #  self.boton.setGeometry(20, 800, 100, 50)
      #  self.boton.move(300, 100)
      #  self.boton.setText("Adelante")
      #  self.boton.clicked.connect(self.apretaste_boton)
      #  self.boton2 = QPushButton(self)
      #  self.boton2.setText("atras")
      #  self.boton2.setGeometry(20, 800, 100, 50)
      #  self.boton2.clicked.connect(self.apretaste_boton2)
      # self.boton2.move(100, 100)
      #  self.mapa = QPushButton(self)
      #  self.mapa.setGeometry(200, 200, 55, 30) #557 309
       # self.pixmap = QPixmap("./IMGS/Aram.png")
        #self.pixmap = self.pixmap.scaled(557*2.5, 309*2.5)
      #  self.mapa.setIcon(QIcon(self.pixmap))
       # self.mapa.setIconSize(QSize(577, 309))
       # self.mapa.clicked.connect(self.moverse)



    def keyPressEvent(self, QKeyEvent):
        tecla = QKeyEvent.key()
        if self.in_game:
            direccion = self.definir_lado()
            if tecla == ord("W"):
                x, y = movimiento_w(self.mouse.pos()-self.pos(),
                                    self.link.pos(), 5)
                self.link.move(x, y)
                self.link.barra.move(x, y)
                if self.nombre_champ == "hernan":
                    pixmap = animate_link(self.pixmap, direccion, self.contador)
                    maximo = 10
                elif self.nombre_champ == "naruto":
                    pixmap = animate_naruto(self.pixmap, direccion, self.contador)
                    maximo = 4

                else:
                    maximo = 0
                    pixmap = self.pixmap
                self.contador += 1
                if self.contador >= maximo:
                    self.contador = 0
                self.link.setPixmap(pixmap)
                #self.barra.setValue(self.barra.value() - 1)
            elif tecla == ord("S"):
                x, y = movimiento_s(self.mouse.pos()-self.pos(),
                                    self.link.pos(), 5)
                self.link.move(x, y)
                self.link.barra.move(x, y)
                dic_direcciones = {"derecha": "izquierda", "arriba": "abajo",
                                   "izquierda": "derecha", "abajo": "arriba",
                                   "": ""}
                if self.nombre_champ == "hernan":
                    pixmap = animate_link(self.pixmap,
                                          dic_direcciones[direccion],
                                          self.contador)
                    maximo = 10
                elif self.nombre_champ == "naruto":
                    pixmap = animate_naruto(self.pixmap,
                                            dic_direcciones[direccion],
                                            self.contador)
                    maximo = 4

                else:
                    maximo = 0
                    pixmap = self.pixmap
                self.contador += 1
                if self.contador >= maximo:
                    self.contador = 0
                self.link.setPixmap(pixmap)
            elif tecla == ord("D"):
                x, y = movimiento_d(self.mouse.pos()-self.pos(),
                                    self.link.pos(), 5)
                self.link.move(x, y)
                self.link.barra.move(x, y)
                dic_direcciones = {"derecha": "abajo", "arriba": "derecha",
                                   "izquierda": "arriba", "abajo": "izquierda",
                                   "": ""}
                if self.nombre_champ == "hernan":
                    pixmap = animate_link(self.pixmap,
                                          dic_direcciones[direccion],
                                          self.contador)
                    maximo = 10
                elif self.nombre_champ == "naruto":
                    pixmap = animate_naruto(self.pixmap,
                                            dic_direcciones[direccion],
                                            self.contador)
                    maximo = 4

                else:
                    maximo = 0
                    pixmap = self.pixmap
                self.contador += 1
                if self.contador >= maximo:
                    self.contador = 0
                self.link.setPixmap(pixmap)
            elif tecla == ord("A"):
                x, y = movimiento_a(self.mouse.pos()-self.pos(),
                                    self.link.pos(), 5)
                self.link.move(x, y)
                self.link.barra.move(x, y)
                dic_direcciones = {"derecha": "arriba", "arriba": "izquierda",
                                   "izquierda": "abajo", "abajo": "derecha",
                                   "":""}
                if self.nombre_champ == "hernan":
                    pixmap = animate_link(self.pixmap,
                                          dic_direcciones[direccion],
                                          self.contador)
                    maximo = 10
                elif self.nombre_champ == "naruto":
                    pixmap = animate_naruto(self.pixmap,
                                            dic_direcciones[direccion],
                                            self.contador)
                    maximo = 4

                else:
                    maximo = 0
                    pixmap = self.pixmap
                self.contador += 1
                if self.contador >= maximo:
                    self.contador = 0
                self.link.setPixmap(pixmap)

            elif tecla == ord("R"):
                print("Mouse : ({},{})".format(self.mouse.pos().x(),
                                               self.mouse.pos().y()))
                print("link: ({},{})".format(self.link.pos().x(),
                                             self.link.pos().y()))
            elif tecla == ord("O"):
                self.tienda.show()
            elif tecla == ord("P"):
                self.pausa()
            elif tecla == ord("I"):
                self.menu_partidas()
            else:
                print(tecla)
        #print(self.mapa.pos())

    def empezo_webeo(self):
        for i in range(300):
            self.mapa.move(self.mapa.x() + i, self.mapa.y())
            QTest.qWait(10)
            self.mapa.move(self.mapa.x() - 2*i, self.mapa.y())
            QTest.qWait(10)
            self.mapa.move(self.mapa.x() + i, self.mapa.y())

    def mousePressEvent(self, QMouseEvent):
        pos = self.mouse.pos() - self.pos()
        x, y = pos.x(), pos.y()
        boton = QMouseEvent.button()
        if sobre(self, self.mouse, self.nexo_a):
            print("Funciono")
        if boton == Qt.RightButton:
            pass
        elif boton == Qt.LeftButton:
            #print("IZQ")
            pass


        #print(QMouseEvent)
        #print(dir(QMouseEvent))
        #print(dir(self.boton))
 #       if self.boton.clicked():
  #          print("Apretaste el boton con el mouse")
   #         self.apretaste_boton()
    #    else:
     #       print("Apretaste el mouse")

    def apretaste_boton(self):
        self.mapa.move(self.mapa.x() + 5, self.mapa.y())


    def apretaste_boton2(self):
        self.mapa.move(self.mapa.x() - 5, self.mapa.y())

    def mouseGrabber(self):
        self.moverse()

    def moverse(self):
        self.mapa.move(self.mouse.pos().x()-self.geometry().x(),
                       self.mouse.pos().y()-self.geometry().y())

    def abrir_tienda(self):
        self.tienda.show()


    def mouseMoveEvent(self, QMouseEvent):
        #self.mapa.move(self.mouse.pos())
        #esta = sobre(self, self.mouse, self.nexo_a)
        #print(esta)

        #if esta:
        #    print("EL MOUSE ESTA SOBRE LA TORRE")
        #print(self.mouse.pos()-self.pos())
        if self.in_game:
            for estructura in self.estructuras:
                if self.area_mouse.intersects(estructura.area):
                    estructura.resaltar()
                else:
                    estructura.volver_normal()

    @property
    def area_mouse(self):
        inicio = self.mouse.pos() - self.pos()
        algo_mas = inicio + QPoint(10, 10)
        mouse = QRect(inicio, algo_mas)
        return mouse

    def menu(self):
        self.boton_partida.hide()
        self.inicio.hide()
        #delattr(self, "boton_partida")
        #delattr(self, "inicio")
        #self.setPalette(QPalette())
        #self.boton_tienda.show()
        self.partida_nueva.show()
        self.cargar_partida.show()
        self.eleccion.show()

    def closeEvent(self, QCloseEvent):
        self.tienda.close()
        super().closeEvent(QCloseEvent)

    def ir_a_seleccion(self):
        self.cargar_partida.hide()
        self.partida_nueva.hide()
        self.eleccion.hide()
        imagen = QImage("./IMGS/mapa.png").scaled(1100, 650)
        palette = QPalette()
        palette.setBrush(10, QBrush(imagen))
        self.setPalette(palette)
        self.seleccionar_hernan.show()
        self.seleccionar_chau.show()
        self.seleccionar_campeon_sorpresa.show()
        self.seleccion_campeon.show()
        self.hernan.show()
        self.chau.show()
        self.naruto.show()

    def iniciar_partida(self):
        self.in_game = True
        self.seleccionar_campeon_sorpresa.hide()
        self.seleccionar_chau.hide()
        self.seleccionar_hernan.hide()
        self.hernan.hide()
        self.seleccion_campeon.hide()
        self.chau.hide()
        self.naruto.hide()
        sender = self.sender()
        if sender is self.seleccionar_hernan:
            self.nombre_champ = "hernan"
            self.link = MovilLabel(666, self.window())
            self.pixmap = QPixmap("./IMGS/link.png").scaled(1200//2, 1040//2)
            # print(self.pixmap.width(), self.pixmap.height())
            pixmap = self.pixmap.copy(QRect(0, 910//2, 120//2, 1040//2))
            self.link.setPixmap(pixmap)
            self.link.setGeometry(0, 500, 120//2, 130//2)
            self.link.show()
        elif sender is self.seleccionar_chau:
            self.nombre_champ = "chau"
            self.link = MovilLabel(500, self.window())
            self.pixmap = QPixmap("./IMGS/link.png").scaled(1200//2, 1040//2)
            # print(self.pixmap.width(), self.pixmap.height())
            pixmap = self.pixmap.copy(QRect(0, 910//2, 120//2, 1040//2))
            self.link.setPixmap(pixmap)
            self.link.setGeometry(0, 500, 120, 130)
            self.link.show()
        elif sender is self.seleccionar_campeon_sorpresa:
            self.nombre_champ = "naruto"
            self.link = MovilLabel(700, self.window())
            self.pixmap = QPixmap("./IMGS/naruto.png")
            #print(self.pixmap.width(), self.pixmap.height())
            pixmap = self.pixmap.copy(QRect(0, 0, 46, 64))
            self.link.setPixmap(pixmap)
            self.link.setGeometry(0, 500, 46, 64)
            self.link.show()
        for estructura in self.estructuras:
            estructura.show()



    def menu_partidas(self):
        for elemento in self.__dict__.values():
            if hasattr(elemento, "hide"):
                elemento.hide()
        self.inicio.show()
        self.boton_partida.show()
        self.setPalette(self.fondo)
#    def mouseGrabber(self):
 #       pass
    def pausa(self):
        while True:
            pass

    def definir_lado(self):
        x = self.link.pos().x()
        xw = x + self.link.width()
        y = self.link.pos().y()
        area = self.link.area
        arriba = QRect(x, 0, xw, y)
        abajo = QRect(x, y + self.link.height(), xw, 650)
        izquierda = QRect(0, 0, x, 650)
        derecha = QRect(xw, 0, 1100, 650)
        if self.area_mouse.intersects(arriba):
            return "arriba"
        elif self.area_mouse.intersects(abajo):
            return "abajo"
        elif self.area_mouse.intersects(derecha):
            return "derecha"
        elif self.area_mouse.intersects(izquierda):
            return "izquierda"
        elif self.area_mouse.intersects(area):
            return ""


class MovilLabel(QLabel):
    def __init__(self, vida, parent, *args):
        super().__init__(parent,*args)
        self.vida = vida
        self.barra = QProgressBar(parent)
        self.barra.setValue(100)


    def setGeometry(self, *__args):
        super().setGeometry(*__args)
        self.barra.setGeometry(self.pos().x(), self.pos().y() - 10,
                               self.width(), 10)


    def show(self):
        self.barra.setVisible(True)
        super().show()

    def hide(self):
        self.barra.hide()
        super().hide()

    @property
    def area(self):
        pos = self.pos()
        nuevox = pos.x() + self.width()
        nuevoy = pos.y() + self.height()
        return QRect(pos, QPoint(nuevox, nuevoy))

class Estructura(MovilLabel):
    def __init__(self, normal, resaltado, escala, vida, parent, *args):
        super().__init__(vida, parent, *args)
        self.resaltado = QPixmap(resaltado).scaled(*escala)
        self.normal = QPixmap(normal).scaled(*escala)
        self.setPixmap(self.normal)

    def resaltar(self):
        self.setPixmap(self.resaltado)

    def volver_normal(self):
        self.setPixmap(self.normal)


class Animation(QThread):
    trigger = pyqtSignal(QPixmap)
    def __init__(self, parent):
        super().__init__()
        self.contador = 0
        self.link = MovilLabel(parent)
        self.pixmap = QPixmap("./IMGS/link.png")
        # print(self.pixmap.width(), self.pixmap.height())
        pixmap = self.pixmap.copy(QRect(0, 910, 120, 1040))
        self.link.setPixmap(pixmap)
        self.link.setGeometry(0, 500, 120, 130)
        self.trigger.connect(parent.animar)

    def run(self):
        while True:
            sleep(0.01)
            pixmap = self.pixmap.copy(
                QRect(120 * self.contador, 910, 120 * (self.contador + 1),
                      1040))
            self.contador += 1
            if self.contador >= 10:
                self.contador = 0
            self.link.setPixmap(pixmap)




if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MiVentana()
    sys.exit(app.exec_())
