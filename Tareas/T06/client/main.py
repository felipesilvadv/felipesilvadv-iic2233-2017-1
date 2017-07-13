import socket
import pickle
import threading
import sys
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtGui import QCloseEvent

PORT = 1206
HOST = "felipe-X451CAP"
#HOST = "192.168.1.135"
#HOST = "10.221.28.142"

#class MiSenal(QObject):

 #   cerrar = pyqtSignal(object)
#    salas = pyqtSignal(list)

#class Event:
   # def __init__(self, mensaje):
        #self.mensaje = mensaje


class Client(QObject):
    cerrar = pyqtSignal()
    salas = pyqtSignal(list)
    user = pyqtSignal(object)
    sala_actual = pyqtSignal(list)

    def __init__(self, nombre, contraseña, *args):
        super().__init__(*args)
        self.nombre = nombre
        self.contraseña = contraseña
        self.host = HOST
        self.port = PORT
        #self.signal = MiSenal()
        self.lista_salas = []
        self.sala_para_mandar = []
        self.sala_recibida = False
        self.canciones_recibidas = False
        self.s_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Un cliente se puede conectar solo a un servidor.
            self.s_cliente.connect((self.host,
                                    self.port))  # El cliente revisa que el servidor esté disponible
            # Una vez que se establece la conexión, se pueden recibir mensajes
            self.send(("<mandando user name>", self.contraseña))
            recibidor = threading.Thread(target=self.recibir_mensajes, args=(self.s_cliente,))
            recibidor.daemon = True
            self._isalive = True
            recibidor.start()

        except socket.error:
            print("No fue posible realizar la conexión")
            # self.cerrar.emit()
            self._isalive = False
            sys.exit()

    def send(self, mensaje):
        msj = pickle.dumps(mensaje)
        largo_msj = len(msj).to_bytes(8, byteorder="big")
        usuario = pickle.dumps(self.nombre)
        largo_user = len(usuario).to_bytes(8, byteorder="big")
        self.s_cliente.send(largo_user + usuario + largo_msj + msj)


    def recibir_mensajes(self, servidor):
        while True:
            try:
                largo_user = servidor.recv(8)
                user = servidor.recv(int.from_bytes(largo_user, byteorder="big"))
                user = pickle.loads(user)
                largo_bytes = servidor.recv(8)
                largo_mensaje = int.from_bytes(largo_bytes, byteorder="big")
                mensaje = b""

                while len(mensaje) < largo_mensaje:
                    mensaje += servidor.recv(512)

                mensaje_final = pickle.loads(mensaje)
                if user == "server":
                    print("pase aqui")
                    if mensaje_final == "<usuario_invalido>":
                        print("Aqui tambien")
                        #evento = Event("cerrar")
                        self.cerrar.emit()
                        self._isalive = False
                        self.s_cliente.close()
                        print("No puedes usar ese nombre de usuario")
                        print("Presiona enter")
                        break

                   # self.desconectar()
                   # exit()
                if self.nombre == user:
                    user = "self"
                elif user == "server-salas":
                    self.lista_salas = mensaje_final
                   # thread_salas = threading.Thread(target=self.mandar_sala,
                    #                                daemon=True)
                   # thread_salas.start()
                #print("tipo de mensaje ", type(mensaje_final))
                #print(isinstance(mensaje_final, globals()[__name__].MensajeEspecial))
                #print(isinstance(mensaje_final, MensajeEspecial))
                #print(type(MensajeEspecial("hola")))
                if hasattr(mensaje_final, "tipo") and hasattr(mensaje_final, "text"):
                    print(mensaje_final.tipo)
                    if mensaje_final.tipo == "sala":
                        with open("cancion_en_reproduccion.wav", "wb") as file:
                            file.write(mensaje_final.text[0].bytes)
                        self.sala_para_mandar = mensaje_final.text
                        self.sala_actual.emit(self.sala_para_mandar)

                print("{}: '{}'".format(user, mensaje_final))
                # Falta agregar que hacer con los distintos tipos de mensajes
                # que llegan

                if determinar_wav(mensaje):
                    print("Es un archivo .wav")
                    # elif isinstance(mensaje, Cancion):
                    #    print("Es cancion y funciono")

            except EOFError as err:
                print(err)


    def desconectar(self):
        self.send("<desconectar>")
        self._isalive = False
        self.s_cliente.close()

    def mandar_sala(self):
        self.salas.emit(self.lista_salas)

    def mandar_sala_actual(self):
        while not len(self.sala_para_mandar):
            if len(self.sala_para_mandar):
                self.sala_actual.emit(self.sala_para_mandar)


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

class MensajeEspecial:
    def __init__(self, text, tipo=None):
        self.text = text
        self.tipo = tipo

class Usuario:

    def __init__(self, nombre, password, sock=None, puntaje=0):
        self.nombre = nombre
        self.password = password
        self.puntaje = puntaje
        self.s_user = sock

    def __getstate__(self):
        a = self.__dict__.copy()
        a.pop(self.s_user)
        return  a

    def __setstate__(self, state):
        state.update({"s_user": None})
        self.__dict__ = state

def determinar_wav(codigo):
    _id = codigo[0:4]
    try:
        if _id.decode("ascii") == "RIFF":
            return True
    except UnicodeDecodeError:
        pass
    else:
        return False

if __name__ == "__main__":
    while True:
        nombre = input("Ingrese nombre de usuario: ")
        client = Client(nombre, "soafnbaoif")
        print(client._isalive)
        if client._isalive:
            break

    while client._isalive:
        inputing = input('[1] Mandar mensaje\n[2] Desconectarse\n>  ')
        if inputing == '1':
            texto = input('>    ')
            client.send(texto)
        elif inputing == '2':
            client.desconectar()
            break
        elif inputing == '3':
           song = Cancion("Somewhere I belong", "Linkin Park")
           client.send(song)