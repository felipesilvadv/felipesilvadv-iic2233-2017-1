import requests
import json
class PrograPedia:

    def __init__(self):
        self.datos = dict()
        self.url = "https://es.wikipedia.org/w/api.php?"

    def buscar(self, palabra):
        if palabra in self.datos.keys():
            dato = self.datos[palabra]
            _id = list(dato["query"]["pages"].keys())[0]
            print(dato["query"]["pages"][_id]["extract"])
        else:
            r = requests.get(self.url,
                             params={"action": "query",
                                     "titles": palabra,
                                     "prop": "extracts",
                                     "format": "json",
                                     "explaintext":"",
                                     "exintro": ""
                                     })
            dato = json.loads(r.text)
            self.datos[palabra] = dato
            _id = list(dato["query"]["pages"].keys())[0]
            print(dato["query"]["pages"][_id]["extract"])

if __name__ == "__main__":
    wiki = PrograPedia()
    while True:
        accion = input("Que quieres hacer? 1.Buscar 2.Salir: ")
        if accion == "1":
            query = input("Que buscas?: ")
            wiki.buscar(query)
        elif accion == "2":
            print("Hasta luego!")
            break