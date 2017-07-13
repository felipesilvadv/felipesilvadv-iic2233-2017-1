from PyQt5.QtWidgets import (QApplication, QMainWindow, QLCDNumber,
                             QWidget, QDialogButtonBox, QListWidgetItem)
from PyQt5.QtGui import QPalette, QBrush, QImage, QIcon, QPixmap
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import pyqtSignal, QObject, Qt
from PyQt5.QtTest import QTest, QSignalSpy
import pickle
from main import Client
from PyQt5 import uic
import sys
from random import choice, shuffle
import threading
import time

chat_juego = uic.loadUiType("juego_chat.ui")
window = uic.loadUiType("MainWindow.ui")
ingreso = uic.loadUiType("ingreso.ui")
seleccion_sala = uic.loadUiType("seleccion_sala.ui")
clase_mensaje = uic.loadUiType("mensaje.ui")

class MainWindow(window[0], window[1]):


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.client = None
        self.ingreso = Ingreso(self)
        self.ingreso.pasar.connect(self.pasar)
        self.setCentralWidget(self.ingreso)
        self.sonido = None



#        self.respuesta1.clicked.connect(self.printear)
#        self.farruko = QSound(r"../../server/songs/Reggaeton/Farruko_-_Cositas_Que_Haciamos.wav")
#        self.respuesta2.clicked.connect(self.reproducir)
#        self.daddy = QSound(r"../../server/songs/Reggaeton/Daddy_Yankee_Feat_Varios_-_Llegamos_A_La_Disco_Off.wav")
#        self.respuesta3.clicked.connect(self.reproducir)
#        self.respuesta4.clicked.connect(self.reproducir)
#        self.contador_tiempo.display(20)
#        print(self.contador_tiempo.value())

   #     music = QImage("./imgs/music.png").scaled(1100, 650)
   #     pal = QPalette()
   #     pal.setBrush(10, QBrush(music))
   #     self.setPalette(pal)
    def pasar(self, sala=""):
        sender = self.sender()
        #print("sender parent:{}".format(sender.parent()))
        print(isinstance(sender, Ingreso))
        print(sender)
        if isinstance(sender, Ingreso):
            sala = SeleccionSala(self)
            self.setCentralWidget(sala)

        elif sender.text() == "Elegir Sala":
            chat = Chat(self, sala)
            self.setCentralWidget(chat)
            #if sender.text() == "Respuesta1":
            #    ingreso = Ingreso(self)
            #    self.setCentralWidget(ingreso)
        elif sender.text() == "Volver a Seleccion de Salas":
            sala = SeleccionSala(self)
            self.setCentralWidget(sala)

        elif sender is self:
            print("Problemas")
#        else:
            #chat = Chat(self)
            #print(sender.parent())
            #self.setCentralWidget(chat)

    def printear(self):
        print("Aprestaste boton 1")

    def reproducir(self):
        boton = self.sender()
        if boton is self.respuesta2:
            self.farruko.play()
        elif boton is self.respuesta3:
            self.daddy.play()
        else:
            if self.contador_tiempo.value() > 0:
                self.contador_tiempo.display(self.contador_tiempo.value() - 1)
            else:
                pass

    def closeEvent(self, QCloseEvent):
        if self.client is not None:
            self.client.desconectar()
        super().closeEvent(QCloseEvent)


class Chat(chat_juego[0], chat_juego[1]):

    def __init__(self, parent, nombre, *args):
        super().__init__(*args)
        self.parent = parent
        self.setupUi(self)
        # self.sala = Sala(nombre)
        self.ventana = Mensaje("Cargando la Sala")
        self.preguntas = ["¿Cuál es el ARTISTA de esta canción?",
                          "¿Cuál es el NOMBRE de esta canción?"]
        self.nombre_sala.setText(nombre)
        self.respuestas = [getattr(self, "respuesta{}".format(i))
                           for i in range(1,5)]
        self.respuesta1.clicked.connect(self.enviar_respuesta)
        self.respuesta2.clicked.connect(self.enviar_respuesta)
        self.respuesta3.clicked.connect(self.enviar_respuesta)
        self.respuesta4.clicked.connect(self.enviar_respuesta)
        self.enviar.clicked.connect(self.enviar_chat)
        self.nombre_usuario.setText(self.parent.client.nombre)
        self.mensaje_chat.setPlaceholderText("Escribe un mensaje aquí")
        self.parent.client.sala_actual.connect(self.empezar_juego)
        self.volver_salas.clicked.connect(self.parent.pasar)
        self.pasar_cancion = True
        self.ventana.show()
        self.parent.client.mandar_sala_actual()
        #QTest.qWait(10000)
        #self.parent.client.mandar_sala_actual()
      #  cambiar = threading.Thread(target=self.cambiar_cancion, daemon=True)
      #  cambiar.start()


    def cambiar_cancion(self):
        while True:
            timer = threading.Timer(20, self.aux)
            timer.setDaemon(True)
            timer.start()

    def aux(self):
        self.pasar_cancion = not self.pasar_cancion

    def reproducir(self):
        with open("../../server/songs/Reggaeton/Farruko_-_Cositas_Que_Haciamos.wav", "rb") as file:
            datos = file.read()
        audio = QSound(datos)
        audio.play()

    def enviar_chat(self):
        mensaje = self.mensaje_chat.text()
        self.chat_sala.insertPlainText(mensaje + "\n")
        self.mensaje_chat.clear()

    def enviar_respuesta(self):
        sender = self.sender()
        self.parent.client.send(sender.text())

    def empezar_juego(self, salas):
        if self.pasar_cancion:
            self.sonido = QSound(r"./cancion_en_reproduccion.wav")
            pregunta = choice(self.preguntas)
            self.pregunta.setText(pregunta)
            if "ARTISTA" in pregunta:
                correcta = salas[0].artista
                salas = salas[1:]
                shuffle(self.respuestas)
                for i in range(3):
                    cancion = choice(salas)
                    salas.remove(cancion)
                    self.respuestas[i].setText(cancion[1])
                self.respuestas[3].setText(correcta)
            elif "NOMBRE" in pregunta:
                correcta = salas[0].nombre
                salas = salas[1:]
                shuffle(self.respuestas)
                for i in range(3):
                    cancion = choice(salas)
                    salas.remove(cancion)
                    self.respuestas[i].setText(cancion[0])
                self.respuestas[3].setText(correcta)
            self.sonido.play()
            self.pasar_cancion = False



#class MiSenal(QObject):
#    senal = pyqtSignal(object)

class Ingreso(ingreso[0], ingreso[1]):
    pasar = pyqtSignal()
    def __init__(self, parent, *args):
        super().__init__(*args)
        self.parent = parent
        self.setupUi(self)
       # self.s = MiSenal()
        self.ventana = Mensaje("")
        self.usuario.setPlaceholderText("Nombre usuario")
        self.password.setPlaceholderText("Contraseña")
        self.eleccion.accepted.connect(self.inicializar)
        self.eleccion.rejected.connect(self.cancelar)


    def inicializar(self):
        nombre = self.usuario.text()
        contraseña = self.password.text()
        self.usuario.clear()
        self.password.clear()
        self.parent.client = Client(nombre, contraseña)
        self.parent.client.cerrar.connect(self.cerrar)
        self.pasar.emit()

    def cerrar(self):
        print("ESTE ES EL EVENTO")
        self.ventana.mensaje.setText("No puedes ingresar con ese nombre")
        self.ventana.show()
        self.parent.client = None
        self.parent.close()

    def cancelar(self):
        sender = self.sender()
        if isinstance(sender, QDialogButtonBox):
            self.parent.close()




class SeleccionSala(seleccion_sala[0], seleccion_sala[1]):
    pasar = pyqtSignal()
    def __init__(self, parent, *args):
        super().__init__(*args)
        self.parent = parent
        self.ventana = Mensaje("Cargando la Sala")
        self.setupUi(self)
        self.salas_recibidas = False
        self.parent.client.salas.connect(self.agregar_salas)
        self.nombre_usuario.setText(self.parent.client.nombre)
        self.aceptar_sala.clicked.connect(self.elegir_sala)
        self.parent.client.mandar_sala()

    def agregar_salas(self, salas):
        if not self.salas_recibidas:
            print(salas)
            self.parent.client.sala_recibida = True
            for sala in salas: # Falta cambiar lo que se emite
                item = QListWidgetItem()
                item.setText(sala)
                item.setIcon(QIcon(QPixmap("./imgs/icono.png")))
                #item.setCheckState(Qt.Unchecked)
                item.setFlags(Qt.ItemIsEditable)
                self.lista_salas.addItem(sala)
            self.salas_recibidas = True
       # else:
        #    for sala in salas:
        #        for i in range(len(self.lista_salas)):
        #            if (self.lista_salas.item(i).text() ==
        #                    sala[0:sala.find(" ")]):
        #                self.lista_salas.item(i).setText(sala)

    def elegir_sala(self):
        for i in range(len(self.lista_salas)):
            if self.lista_salas.item(i).isSelected():
                msg = MensajeEspecial(self.lista_salas.item(i).text(), "sala")
                self.parent.client.send(msg)
                break
        else:
            msg = ""

        if isinstance(msg, MensajeEspecial):
            self.parent.pasar(msg.text)
        else:
            self.parent.pasar(msg)

class Mensaje(clase_mensaje[0], clase_mensaje[1]):

    def __init__(self, mensaje, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.mensaje.setText(mensaje)

class MensajeEspecial:
    def __init__(self, text, tipo=None):
        self.text = text
        self.tipo = tipo

class Sala:

    def __init__(self, nombre):
        self.nombre = nombre
        self.canciones = []
        self.clientes = []
        self.canciones_reproducidas = []

    @property
    def cancion_actual(self):
        if len(self.canciones):
            cancion = choice(self.canciones)
            self.canciones_reproducidas.append(cancion)
            self.canciones.remove(cancion)
        else:
            self.canciones = [song for song in self.canciones_reproducidas]
            cancion = choice(self.canciones)
            self.canciones_reproducidas = []
        return cancion

class Cancion:

    def __init__(self, nombre, artista, b=b""):
        self.nombre = nombre
        self.artista = artista
        self.bytes = b
    def __str__(self):
        return """nombre: {}
        artista: {}""".format(self.nombre, self.artista)

    def __eq__(self, other):
        return self.nombre == other.nombre and self.artista == other.artista

    def __ne__(self, other):
        return self.nombre != other.nombre or self.artista != other.artista

if __name__ == "__main__":
    teststring = u'\U0001f604'
    # convert to unicode
    #teststring = teststring.encode("utf-8")

    # encode it with string escape
    #teststring = teststring.encode('unicode_escape')
    #teststring = teststring.decode("unicode_escape")
    #print(teststring)
    app = QApplication([])
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())