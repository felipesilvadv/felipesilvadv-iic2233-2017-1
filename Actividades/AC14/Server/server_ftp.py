import os
import socket
import pickle


def send(socket, mensaje):
    # Funcion para mandar comandos y archivos
    socket.send(pickle.dumps(mensaje))

def ls(socket):
    s = ""
    for elemento in os.listdir(os.getcwd()):
        if len(s) >= 80:
            s += elemento + "\n"
        else:
            s += elemento + " "
    send(socket, ('ls', s))

def get(archivo, nuevo_archivo, socket):
    if archivo not in os.listdir(os.getcwd()):
        send(socket, "Archivo no existe")
    elif os.path.isdir(archivo):
        send(socket, "Es un directorio")
    else:
        with open(archivo, "rb") as file:
            datos = file.read()
        tupla = pickle.dumps(('get', datos, nuevo_archivo))
        contador = 0
        while len(tupla):
            tupla = tupla[contador: contador + 1024]
            contador += 1024
            send(socket, tupla)
    #return datos, nuevo_archivo  # datos es el archivo en bytes y nuevo
                                 #  archivo es el nuevo nombre para guardarlo

def mandar(archivo_bytes):
    datos, nuevo_nombre = pickle.loads(archivo_bytes)
    if nuevo_nombre not in os.listdir(os.getcwd()):
        with open(nuevo_nombre, "wb") as file:
            file.write(datos)
        print("Archivo {} recibido".format(nuevo_nombre))
    else:
        print("No puedes sobre-escribir ese archivo")

def receive(cliente):
    # Funcion que recibe cualquier dato mandado por el servidor
    try:
        data = cliente.recv(2048)
        mensaje = pickle.loads(data)
        return mensaje
    except AttributeError:
        print('Cliente desconectado')
        return ""


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

    HOST = "localhost"
    PORT = 8080
    C_DIR = os.getcwd()

    s_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_servidor.bind((HOST, PORT))
    s_servidor.listen(2)

    client = None

    while True:
        # Conectarse al servidor
        client = s_servidor.accept()[0]
        print("cliente conectado")
        send(client, C_DIR)

        connected = True
        while connected:
            # Recibir comandos
            message = receive(client)
            action = message[0]
            if action == "ls":
                ls(client)

            elif action == "logout":
                client = None
                print('Cliente desconectado')
                break

            elif action == "get":
                get(*message[1:], client)

            elif action == "send":
                send(client, mandar(*message[1:]))
