import app
import os

port = int(os.environ.get("PORT",5000))
app.aplicacion.run(host="0.0.0.0", port=port)
#import requests
#import flask
# import json


#aplicacion = flask.Flask(__name__)



#@aplicacion.route("/Telegram", methods=["POST"])
#def argumento_get():
#    try:
#        mandar_mensaje(370848782, "ENTRE aca")
#        print("Entre aca")
      #  update = json.loads(flask.request.data.decode("utf-8"))
       # print("pase update y es un {}".format(type(update)))
       # mandar_mensaje(370848782, "pase update, y es un {}".format(type(update)))
 #       return "hola"
        #comando = ""
        # largo = 0

  #  except Exception as err:
  #      mandar_mensaje(370848782, "paso este error {}".format(err))
  #      return "chao"
        # print("-"*500, "No es un diccionario, es {}".format(type(update)))

    # return argumento  # Aqui podemos recibir argumento

#@aplicacion.route("/Git", methods=["POST"])
#def arg_get(arg):

    #return arg

#def mandar_mensaje(chat_id, mensaje):
 #   url = "https://api.telegram.org/" \
 #         "bot430672963:AAGNYlLy5V-8teMWFaRaYBgpQQadYfkWFoQ/"
 #   r = requests.post(url, data={"method": "sendMessage",
  #                                 "text": mensaje,
  #                                 "chat_id": chat_id})
  #  return r

#aplicacion.run()
