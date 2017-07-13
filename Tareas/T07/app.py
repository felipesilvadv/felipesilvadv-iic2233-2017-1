import requests
import flask
import json
from get_issue import get_issue
from add_label import add_label
from close_issue import close_issue
from post_comment_issue import comment_issue

aplicacion = flask.Flask(__name__)

lista_chats = []


@aplicacion.route("/Telegram", methods=["POST"])
def argumento_get():
    update = json.loads(flask.request.data.decode("utf-8"))
   # mandar_mensaje(370848782, "ENTRE aca y el update es de tipo {}".format(type(update)))
   # mandar_mensaje(370848782, str(update))
    chat_id = ""
    comandos = {
        "/get": get_issue,
        "/post": comment_issue,
        "/label": add_label,
        "/close": close_issue
    }
    global lista_chats
    try:
        mensaje = update["message"]["text"]
        chat_id = update["message"]["chat"]["id"]
        if chat_id not in lista_chats:
            lista_chats.append(chat_id)
        slash = mensaje.find("/")
        gato = mensaje.find("#")
        asterisco = mensaje.find("*")
        comando = mensaje[slash:gato].strip()
        if asterisco == -1:
            num = int(mensaje[gato:].strip("#"))
            contenido = ""
        else:
            num = int(mensaje[gato:asterisco].strip("#"))
            contenido = mensaje[asterisco:].strip("*")

        if comando == "/label":
            contenido = contenido.split(",")
        mandar_mensaje(370848782, str(comando)+str(num) + str(contenido))
        mensaje_final = comandos[comando](number=num, content=contenido)
        mandar_mensaje(chat_id, mensaje_final)

    except Exception as err:
        mandar_mensaje(370848782, "hubo un error en algun chat de tipo\n {}"
                       .format(err))
        if chat_id != "":
            mandar_mensaje(chat_id, "Comando invalido")
        else:
            mandar_mensaje(370848782, "Comando invalido en algun chat")
    finally:
        try:
            return flask.Response(response="Funciono", status=201)
        finally:
            return ""
    # largo = 0
@aplicacion.route("/Git", methods=["POST"])
def git_post():
    try:
        global lista_chats
        data = json.loads(flask.request.data.decode("utf-8"))
        if data["action"] == "opened" or data["action"] == "reopened":
            msg = """[{author}]
               [#{num_issue}-{titulo_issue}]
               {texto}
               [Link: {link_issue}]""".format(
                author=data["issue"]["user"]["login"],
                texto=data["issue"]["body"],
                titulo_issue=data["issue"]["title"],
                link_issue=data["issue"]["html_url"],
                num_issue=data["issue"]["number"])
            for chat in lista_chats:
                mandar_mensaje(chat, msg)
    except Exception as err:
        mandar_mensaje(370848782, "Fallo la notificacion de Git, con este error"
                                  "\n{}".format(err))
    finally:
        return ""
def mandar_mensaje(chat_id, mensaje):
    url = "https://api.telegram.org/" \
          "bot430672963:AAGNYlLy5V-8teMWFaRaYBgpQQadYfkWFoQ/"
    r = requests.post(url, data={"method": "sendMessage",
                                   "text": mensaje,
                                   "chat_id": chat_id})
    return r

