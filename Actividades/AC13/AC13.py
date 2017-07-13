import json
import pickle
from os import listdir, mkdir, path, system
from datetime import datetime

class Usuario:
    def __init__(self, name="", contacts=(), phone_number=0, *args, **kwargs):
        self.name = name
        self.contacts = contacts
        self.phone_number = phone_number
def set_id():
    i = 0
    while True:
        yield i
        i += 1
gen = set_id()

class Mensaje:

    def __init__(self,**kwargs):
        if not len(kwargs):
            pass
           # self.send_to = send_to
           # self.send_by = send_by
        #    self.content = content
         #   self.last_view = last_view
         #   self.date = date
        else:
            self._id = next(gen)
            self.send_to = kwargs["send_to"]
            self.send_by = kwargs["send_by"]
            self.content = kwargs["content"]
            self.last_view = kwargs["last_view_date"]
            self.date = kwargs["date"]

    def __getstate__(self):
        nueva = self.__dict__.copy()
        nueva.update({"content":
                          encriptar_msg(self.content, int(self.send_by))})
        return nueva

    def __setstate__(self, state):
        state.update({"last_view_date": str(datetime.now())})
        self.__dict__ = state

def sacar_usr(obj):
    return Usuario(**obj)


def sacar_msg(obj):
    return Mensaje(**obj)

def msg():
    mensajes = []
    for archivo in listdir("./db/msg/"):
        with open("./db/msg/"+archivo) as file:
            lista = file.readlines()[0]
        mensajes.append(json.loads(lista, object_hook=sacar_msg))
    return mensajes
def usr():
    usuarios = []
    for archivo in listdir("./db/usr/"):
        with open("./db/usr/"+archivo) as file:
            lista = file.readlines()[0]
        usuarios.append(json.loads(lista, object_hook=sacar_usr))
    return usuarios

def encriptar_msg(msg,n):
    s = ""
    for letra in msg:
        s += chr((ord(letra)+n)%26)
    return s

def crear_contactos(mensajes, usuarios):
    for msg in mensajes:
        for usr in usuarios:
            if msg.send_by == usr.phone_number:
                for user in usuarios:
                    user.contacts = set(user.contacts)
                    if user is usr:
                        pass
                    elif msg.send_to == user.phone_number:
                        user.contacts.add(usr.phone_number)
                    user.contacts = list(user.contacts)


def serializar_todo(usuarios, mensajes):
    try:
        mkdir(path.join(".", "secure_db"))
    except FileExistsError:
        pass
    try:
        mkdir(path.join(".", "secure_db", "usr"))
    except FileExistsError:
        pass
    try:
        mkdir("./secure_db/msg")
    except FileExistsError:
        pass

    for usr in usuarios:
        with open(path.join(".", "secure_db", "usr", "") + usr.name + ".json",
                  "w") as f:
            f.write(json.dumps(usr.__dict__))

    for msg in mensajes:
        with open(path.join(".", "secure_db","msg","")+"mensaje_nro_"+str(msg._id),"wb") as file:
            pickle.dump(msg, file)


if __name__ == "__main__":
    usuarios = usr()
    mensajes = msg()
    crear_contactos(mensajes, usuarios)
    serializar_todo(usuarios, mensajes)





