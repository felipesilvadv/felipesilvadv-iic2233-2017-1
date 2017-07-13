import requests
import json

url = "https://api.telegram.org/bot430672963:AAGNYlLy5V-8teMWFaRaYBgpQQadYfkWFoQ/"

def mandar_mensaje(chat_id, mensaje):
    url = "https://api.telegram.org/" \
          "bot430672963:AAGNYlLy5V-8teMWFaRaYBgpQQadYfkWFoQ/"
    r = requests.get(url, params={"method": "sendMessage",
                                   "text": mensaje,
                                   "chat_id": chat_id})
    return r.status_code

with open("credentials") as file:
    credentials = tuple(file.read().splitlines())

r = requests.get("https://api.github.com/repos/felipesilvadv/tarea7/issues/1",
                 auth=credentials)
print(isinstance(r.headers["Status"],str))
print(r.json()["body"])
print(mandar_mensaje(434519265, "hola nacho"))

#r = requests.get(url, params={"method": "getMe"})
#print(r.json())
#r = requests.get(url, params=({"method": "forwardMessage",
 #                              "chat_id": "370848782",
 #                              "message_id": "20
 #                              "disable_notification": False}))
#r = requests.get(url, params=({"method": "sendMessage",
 #                              "text": "hola",
  #                             "chat_id": "370848782"
  #                             }))

#print(r.status_code)
#print(r.json())
#lista_comandos = {"/mandame_un_mensaje": mandar_mensaje}
#if int(r.status_code) == 200:
    #ultimo_mensaje = len(r.json()["result"]) - 1
#    mensaje = r.json()["result"][-1]["message"]["text"]
#    chat_id = r.json()["result"][-1]["message"]["chat"]["id"]
#    if "/" == mensaje[0]:
#        idx = mensaje.find(" ")
#        comando = mensaje[0:idx]
#        if comando in lista_comandos.keys():
#            parametros = mensaje[idx + 1:]
#            lista_comandos[comando](chat_id, parametros)


#print(r.status_code)
#print(r.json())
def algo():
    update = {}
    if isinstance(update, dict):
        if "message" in update.keys():
            if "text" in update["message"].keys():
                if "entities" in update["message"].keys():
                    # largo = len(update["message"]["entities"])
                    if update["message"]["entities"][0]["type"] == \
                            "bot_command":
                        slash = int(update["message"]["entities"][0]["offset"])
                        espacio = int(update["message"]
                                      ["entities"][0]["length"]) + slash
                        comando = update["message"]["text"][slash:espacio]
                    else:
                        mandar_mensaje(370848782,
                                       "Fallo update['message']"
                                       "['entities'][0]['type'] == \
                                       'bot_command'")
                        return ""
                else:
                    mandar_mensaje(370848782, "Falla entities")
                    return ""
            else:
                mandar_mensaje(370848782, "Falla text")
                return ""
        else:
            mandar_mensaje(370848782, "falla message")
            return ""

        with open("credentials") as file:
            credentials = tuple(file.read().splitlines())
        for j in range(0):
            if comando == "get":
                hashtag = update["message"]["text"].find("#")
                texto_siguiente = update["message"]["text"][hashtag:]
                largo_hashtag = texto_siguiente.find(" ")
                try:
                    num = int(update["message"]["text"][hashtag:hashtag +
                                                                largo_hashtag])
                except ValueError:
                    chat_id = update["message"]["chat"]["id"]
                    mandar_mensaje(chat_id,"Numero invalido de issue")
                    return ""
                url = "https://api.github.com/repos/felipesilvadv/tarea7/" \
                      "issues/{}".format(num)
                r = requests.get(url, auth=credentials)
                if r.headers["Status"] == "200 OK":
                    dic = r.json()

                    msg = """[{author}]
                [#{num_issue}-{titulo_issue}]
                {texto}
                [Link: {link_issue}]""".format(author=dic["user"]["login"],
                                               texto=dic["body"],
                                               titulo_issue=dic["title"],
                                               link_issue=dic["html-url"],
                                               num_issue=dic["number"])
                else:
                    msg = "No se logro conectar a esa issue"
                chat_id = update["message"]["chat"]["id"]
                mandar_mensaje(chat_id, msg)
                return msg

            elif comando == "post":
                hashtag = update["message"]["text"].find("#")
                texto_siguiente = update["message"]["text"][hashtag:]
                largo_hashtag = texto_siguiente.find(" ")
                try:
                    num = int(update["message"]["text"][hashtag:hashtag +
                                                                largo_hashtag])
                except ValueError:
                    chat_id = update["message"]["chat"]["id"]
                    mandar_mensaje(chat_id, "Numero invalido de issue")
                    return ""

                url = "https://api.github.com/repos/felipesilvadv/" \
                      "tarea7/issues/{}/comments".format(num)
                inicio = (update["message"]["text"].find("#{}".format(num)) +
                          1 + largo_hashtag)
                msg = update["message"]["text"][inicio:]
                r = requests.post(url, data=json.dumps({"body": msg}), auth=credentials)
                if r.headers["Status"] == "201 Created":
                    mensaje = "Se comento {msg} en la issue " \
                              "#{num}".format(msg=msg, num=num)
                else:
                    mensaje = "Hubo un problema al conectar con esa issue"
                chat_id = update["message"]["chat"]["id"]
                mandar_mensaje(chat_id, mensaje)
                return mensaje
            elif comando == "label":
                hashtag = update["message"]["text"].find("#")
                texto_siguiente = update["message"]["text"][hashtag:]
                largo_hashtag = texto_siguiente.find(" ")
                try:
                    num = int(update["message"]["text"][hashtag:hashtag +
                                                                largo_hashtag])
                except ValueError:
                    chat_id = update["message"]["chat"]["id"]
                    mandar_mensaje(chat_id, "Numero invalido de issue")
                    return ""

                url = "https://api.github.com/repos/felipesilvadv/" \
                      "tarea7/issues/{}/labels".format(num)
                inicio = (update["message"]["text"].find("#{}".format(num)) +
                          1 + largo_hashtag)
                msg = update["message"]["text"][inicio:]
                msg = msg.split(",")
                r = requests.post(url, data=json.dumps(msg), auth=credentials)
                if r.headers["Status"] == "200 OK":
                    mensaje = "Se agregaron los label {msg} en la issue" \
                              " #{num}".format(msg=msg, num=num)
                else:
                    mensaje = "No se pudo conectar a esa issue"
                chat_id = update["message"]["chat"]["id"]
                mandar_mensaje(chat_id, mensaje)
                return mensaje
            elif comando == "close":
                hashtag = update["message"]["text"].find("#")
                texto_siguiente = update["message"]["text"][hashtag:]
                largo_hashtag = texto_siguiente.find(" ")
                try:
                    num = int(update["message"]["text"][hashtag:hashtag +
                                                                largo_hashtag])
                except ValueError:
                    chat_id = update["message"]["chat"]["id"]
                    mandar_mensaje(chat_id, "Numero invalido de issue")
                    break
                url = "https://api.github.com/repos/felipesilvadv/tarea7/" \
                      "issues/{}".format(num)
                issue = requests.get(url, auth=credentials)
                if issue.headers["Status"] == "200 OK":
                    dic = issue.json()
                    dic.update({"state":"close"})
                    url = "https://api.github.com/repos/felipesiladv/tarea7/" \
                          "issues/{}".format(num)
                    r = requests.patch(url, data=json.dumps(dic) , auth=credentials)
                    if r.headers["Status"] == "200 OK":
                        mensaje = "Se cerró la issue #{num}".format(num=num)
                    else:
                        mensaje = "No se pudo conectar a esa issue"

                else:
                    mensaje = "No se pudo conectar a esa issue"
                chat_id = update["message"]["chat"]["id"]
                mandar_mensaje(chat_id, mensaje)

            else:
                mensaje = "No ingresaste ningun comando"
                chat_id = update["message"]["chat"]["id"]
                mandar_mensaje(chat_id, mensaje)
                return mensaje
        return ""
    else:
        mandar_mensaje(370848782, "No es un diccionario es {}".format(type(update)))
        return "No es un diccionario es {}".format(type(update))
        # print("-"*500, "No es un diccionario, es {}".format(type(update)))

    # return argumento  # Aqui podemos recibir argumento

#@aplicacion.route("/Git", methods=["POST"])
#def arg_get(arg):

    #return arg

#flask.Flask(__name__)
