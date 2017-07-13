import os
import socket
import pickle
import threading


def send(socket, mensaje):
    # Funcion para mandar comandos y archivos
    socket.send(pickle.dumps(mensaje))


def receive(server):
    # Funcion que recibe cualquier dato mandado por el servidor
    try:
        mensaje = server.recv(4096)
        return pickle.loads(mensaje)

    except AttributeError:
        print("Estas desconectado del servidor")
        return ""

def get(datos):
    string, escribir, nuevo_archivo = pickle.loads(datos)
    with open(nuevo_archivo, "wb") as file:
        file.write(escribir)

def mandar(archivo, nuevo_archivo, socket):
    if archivo not in os.listdir(os.getcwd()):
        print("Archivo no existe")
    elif os.path.isdir(archivo):
        print("Es un directorio")
    else:
        with open(archivo, "rb") as file:
            datos = file.read()
        tupla = pickle.dumps((datos, nuevo_archivo))
        send(socket, tupla)

def recibidor_mensajes(servidor):
    while True:
        variable = bytearray()
        aux = True
        while aux:
            data = servidor.recv(1024)
            variable += data
            try:
                mensaje = pickle.loads(data)
            except EOFError:
                pass
            except Exception:
                pass
            else:
                aux = False
        accion = mensaje[0]
        if accion == 'ls':
            print(mensaje[1])
        elif accion == 'get':
            get(data)
        else:
            print(mensaje)

def get_path(path):
    abs_path = get_abs_path(path)
    if not os.path.exists(abs_path):
        return -1
    elif not os.path.isdir(abs_path):
        return 0
    else:
        return abs_path


def get_abs_path(path):
    if os.path.isabs(path):
        return path
    else:
        return os.path.abspath(os.sep.join(C_DIR.split(os.sep) +
                                           path.split(os.sep)))

if __name__ == '__main__':

    C_DIR = os.getcwd()
    HOST = "localhost"
    PORT = 8080

    s_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s_cliente.connect((HOST, PORT))

    except socket.error:
        print("No es posible realizar la conexion")

    S_DIR = receive(s_cliente)
    connected = True
    funcion = threading.Thread(target=recibidor_mensajes, args=(s_cliente,))
    funcion.start()
    while connected:
        command = input(S_DIR + " $ ")
        commands = command.split(" ")

        if commands[0] == "logout":
            # Aviso al servidor que me desconecto
            connected = False
            send(s_cliente, commands)

        elif commands[0] == "ls":
            # Muetra carpetas y archivos en el directorio del servidor
            send(s_cliente, commands)

        elif commands[0] == "get":
            # Le pides un archivo al servidor
            send(s_cliente, commands)

        elif commands[0] == "send":
            # le mandas un archivo al servidor
            file_path = get_abs_path(commands[1])
            if os.path.exists(file_path):
                mandar(*commands[1:], s_cliente)

            else:
                print(commands[1] + " doesn't exist.")
