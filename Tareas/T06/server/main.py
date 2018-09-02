import socket
import pickle
import threading
import os
from random import choice, shuffle


PORT = 1206
#HOST = "192.168.1.135"
#HOST = "10.221.28.142"
#HOST = "felipe-X451CAP"
HOST = "felipe-X405UQ"
def set_id():
    contador = 0
    while True:
        yield str(contador)
        contador += 1
_id = set_id()
next(_id)


class Server:

    def __init__(self):
        self.s_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = HOST
        self.port = PORT
        self.s_servidor.bind((self.host, self.port))
        self.s_servidor.listen(10)
        self.clientes = {}
        self.salas = {}
        if "users" not in os.listdir("./"):
            os.mkdir("users")
        else:
            if len(os.listdir("./users/")):
                for dir in os.listdir("./users/"):
                    with open("./users/" + dir, "rb") as file:
                        archivo = file.read()
                        self.clientes[dir] = pickle.loads(archivo)
        self.lista_nombres = []
        for dir in os.listdir("./songs/"):
            nombre = dir.replace("/", "")
            self.lista_nombres.append(nombre)
            sala = Sala(nombre)
            for directorio in os.listdir("./songs/" + nombre + "/"):
                with open("./songs/" + nombre + "/" + directorio, "rb") as file:
                    archivo= file.read()
                    archivo = bytearray(archivo)
                    if determinar_wav(archivo):
                        archivo = acortar_cancion(archivo, 20)
                #with open("/home/felipe/Música/editado_" + directorio, "wb") as file:
                #    file.write(archivo)  # Por si queremos escribirlo en alguna parte
                valor = directorio[0:directorio.find(".wav")].split("-")
                valor.reverse()
                valor = valor + [archivo]
                song = Cancion(*valor)
                sala.canciones.append(song)
            self.salas[nombre] = sala
        thread = threading.Thread(target=self.aceptar, daemon=True)
        thread.start()

    def aceptar(self):
        while True:
            cliente_nuevo, address = self.s_servidor.accept()
            print('Cliente conectado')  # Borrar despues
            #del self.clientes[1]
            #self.clientes[next(_id)] = cliente_nuevo
            #print(self.clientes)
            salas = pickle.dumps(self.lista_nombres)
            largo = len(salas).to_bytes(8, byteorder="big")
            servidor = pickle.dumps("server-salas")
            largo_nombre = len(servidor).to_bytes(8, byteorder="big")
            cliente_nuevo.send(largo_nombre + servidor + largo + salas)
            thread_cliente = threading.Thread(target=self.recibir_mensajes, args=(cliente_nuevo,))
            thread_cliente.daemon = True
            thread_cliente.start()

    def send(self, mensaje, id_client, servidor=False):
        msj = pickle.dumps(mensaje)
        largo_msj = len(msj).to_bytes(8, byteorder="big")
        if not servidor:
            nombre_client = pickle.dumps(id_client)
        else:
            nombre_client = pickle.dumps("server")
        largo_nombre = len(nombre_client).to_bytes(8, byteorder="big")
        try:
            self.clientes[id_client].s_user.send(largo_nombre + nombre_client
                                          + largo_msj + msj)
        except KeyError:
            print("Ese usuario no existe o no esta conectado")


    def recibir_mensajes(self, cliente):
        primer_mensaje = True
        while True:
            try:
                largo_user = cliente.recv(8)
                user = cliente.recv(int.from_bytes(largo_user, byteorder="big"))
                user = pickle.loads(user)
                largo_bytes = cliente.recv(8)
                largo_mensaje = int.from_bytes(largo_bytes, byteorder="big")
                mensaje = b""

                while len(mensaje) < largo_mensaje:
                    mensaje += cliente.recv(512)

                mensaje_final = pickle.loads(mensaje)
                if primer_mensaje:
                    if user not in self.clientes.keys():
                        self.clientes[user] = Usuario(user, mensaje_final[1],
                                                      cliente)
                    elif isinstance(self.clientes[user], Usuario):
                        if mensaje_final[1] == self.clientes[user].password:
                            self.clientes[user].s_user = cliente
                        else:
                            self.clientes["repetido"] = Usuario("repetido",
                                                                "repetido",
                                                                cliente)
                            print(self.clientes)
                            self.send("<usuario_invalido>", "repetido", True)
                            self.desconectar("repetido")
                            print("Contraseña invalida")
                            print("Ya existe ese usuario")
                            print(self.clientes)
                    else:
                        self.clientes["repetido"] = Usuario("repetido",
                                                            "repetido", cliente)
                        print(self.clientes)
                        self.send("<usuario_invalido>", "repetido", True)
                        self.desconectar("repetido")
                        print("Ya existe ese usuario")
                        print(self.clientes)
                        # AUN no se como se filtrara esto
                        break
                    primer_mensaje = False
                with open("./users/"+ user, "wb") as file:
                    file.write(pickle.dumps(self.clientes[user]))

                if mensaje_final == "<desconectar>":
                    self.desconectar(user)
                    break
                elif isinstance(mensaje_final, MensajeEspecial):
                    if mensaje_final.tipo == "sala":
                        self.mandar_canciones(mensaje_final, user)

                print("{}: '{}'".format(user, mensaje_final))
                # Falta agregar que hacer con los distintos tipos de mensajes
                # que llegan

                if determinar_wav(mensaje):
                    print("Es un archivo .wav")
                #elif isinstance(mensaje, Cancion):
                #    print("Es cancion y funciono")

            except EOFError as err:
                print(err)
                pass

    def desconectar(self, cliente):
        try:
            #print(self.clientes[cliente])
            print(cliente)
            self.clientes[cliente].s_user.close()
            self.clientes.pop(cliente)
            print("Se desconecto el cliente: {}".format(cliente))

        except KeyError:
            print("Algo salio mal")

    def mandar_canciones(self, mensaje_final, user):
        self.salas[mensaje_final.text].clientes.append(user)
        mandado = \
            self.salas[mensaje_final.text].mandar_canciones()
        msg = MensajeEspecial(mandado,
                              "sala")
        self.send(msg, user)


def determinar_wav(codigo):
    _id = codigo[0:4]
    try:
        if _id.decode("ascii") == "RIFF":
            return True
    except UnicodeDecodeError:
        pass
    else:
        return False

def little_bin(binario):
    valor = binario[binario.find("b"):]
    lista = [letra for letra in valor]
    lista.reverse()
    return "0b"+"".join(lista)

def acortar_cancion(cancion, n):
    numero = int.from_bytes(cancion[28:32],
                            byteorder="little") * n
    cancion[40:44] = numero.to_bytes(4, byteorder="little")
    cancion[4:8] = (int.from_bytes(cancion[4:8],
                                   byteorder="little") +
                    36).to_bytes(4, byteorder="little")
    return cancion[0:44] + cancion[44:numero]

def largo_wav(codigo):
    if determinar_wav(codigo):
        largo = codigo[4:8]
        largo = int(little_bin(largo), 2)
        return largo
    else:
        return 0


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

    def mandar_canciones(self):
        cancion = self.cancion_actual
        lista_canciones = [elemento for elemento in self.canciones]
        shuffle(lista_canciones)
        lista = []
        if len(lista_canciones) >= 3:
            for i in range(3):
                eleccion = lista_canciones[0]
                lista_canciones = lista_canciones[1:]
                lista.append((eleccion.nombre, eleccion.artista))
        else:
            for i in range(len(lista_canciones)):
                eleccion = lista_canciones[0]
                lista_canciones = lista_canciones[1:]
                lista.append((eleccion.nombre, eleccion.artista))
            lista_canciones = [elemento for elemento
                               in self.canciones_reproducidas]
            for i in range(3 - len(lista_canciones)):
                eleccion = lista_canciones[0]
                lista_canciones = lista_canciones[1:]
                lista.append((eleccion.nombre, eleccion.artista))
        return [cancion] + lista



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
        a.pop("s_user")
        return a

    def __setstate__(self, state):
        state.update({"s_user": None})
        self.__dict__ = state


if __name__ == "__main__":
    server = Server()

    while len(server.clientes) or True:
        print(server.clientes)
        texto = input("Manda algo: ")
        cliente = input("A que usuario?: ")
        if texto == "desconectar":
            server.desconectar(cliente)
            server.send(texto, cliente)
            break
        elif texto == "mostrar":
            print(server.clientes)
        else:
            server.send(texto, cliente)
