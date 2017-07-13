
class Descifrador:
    def __init__(self, nombre):
        self.nombre = nombre
        self.suma=0
        with open(self.nombre, "r") as self.archivo:
            lineas = self.archivo.readlines()
            self.codigo = ''
            self.texto = "".join(lineas).replace('\n', '')
            i = 0

    def lectura_archivo(self):
        with open(self.nombre, "r") as archivo:
            lineas = archivo.readlines()
            self.codigo = ''
            texto = "".join(lineas).replace('\n', '')
            for caracter in texto:
                self.codigo += caracter
            if "a" in self.codigo:
                raise CustomException(self.codigo)
            return self.codigo

    def elimina_incorrectos(self):
        lista=self.codigo.split(" ")
        self.codigo=''
        for i in lista:
            if len(i) < 6 or len(i) > 7:
                pass
            else:
                self.codigo+=' '+i
        return self.codigo

    def cambiar_binario(self, binario):
        lista = binario.split(' ')
        texto = []
        for x in lista[1:]:
            texto.append(chr(int(x, 2)))
        return texto

    def limpiador(self, lista):
        i = -1
        string = ''
        while i < len(lista):
            i += 1
            try:
                if '$' != lista[i]:
                    string += lista[i]
            except IndexError:
                break
        return string


class CustomException(Exception):
    def __init__(self, codigo):
        self.codigo = codigo

    def arreglar(self):
        lista = self.codigo.split(" ")

        num = self.codigo.find("a")
        chunks = self.codigo[num:]
        chunks = chunks.strip("a")
        chunks = chunks.split(" ")
        for palabra in chunks:
            if palabra in lista:
                lista.remove(palabra)
            palabra = [letra for letra in palabra]
            palabra.reverse()
            palabra = "".join(palabra)
            lista.append(palabra)
        for elemento in lista:
            if "a" in elemento:
                lista.remove(elemento)
        self.codigo = " ".join(lista)
        return self.codigo


if __name__ == "__main__":
    try:
        des = Descifrador('mensaje_marciano.txt')
        try:
            codigo = des.lectura_archivo()
        except CustomException as err:
            des.codigo = err.arreglar()
            codigo = des.codigo
        codigo = des.elimina_incorrectos()
        try:
            lista = des.cambiar_binarios(des.codigo)
        except AttributeError as err:
            print("Error: {}".format(err))
            lista = des.cambiar_binario(des.codigo)
        texto = des.limpiador(lista)
        print(texto)

    except Exception as err:
        print('Esto no debiese imprimirse')
