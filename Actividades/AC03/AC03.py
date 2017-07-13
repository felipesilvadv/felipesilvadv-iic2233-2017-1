from collections import deque
class Camion:
    def __init__(self,capacidad,urgencia):
        self.productos =  deque()
        self.capacidad_maxima = capacidad
        self.urgencia = urgencia
    @property
    def capacidad_actual(self):
        contador = 0
        for producto in self.productos:
            contador+= producto.peso
        return contador
    def agregar_producto(self,producto):
        if self.capacidad_actual<= self.capacidad_maxima:
            self.productos.append(producto)
        
    def __str__(self):
        lista_tipos = set()
        lista_nombres = []
        cantidades = dict()
        string = ""
        for producto in self.productos:
            lista_tipos.add(producto.tipo)
            lista_nombres.append(producto.nombre)
        for producto in self.productos:
            cantidades[producto.nombre] = lista_nombres.count(producto.nombre)
        return str(cantidades) + "\n"+ str(lista_tipos)
    
class CentroDistribucion:
    def __init__(self):
        self.fila = list()
        self.bodega = dict()
    def recibir_donacion(self,*args):
        for arg in args:
            if arg.tipo in self.bodega.keys():
                if arg.nombre in self.bodega[arg.tipo].keys():
                    self.bodega[arg.tipo][arg.nombre].append(arg)
                else:
                    self.bodega[arg.tipo][arg.nombre] = []
                    self.bodega[arg.tipo][arg.nombre].append(arg)
            else:
                self.bodega[arg.tipo] = dict()
                self.bodega[arg.tipo][arg.nombre]=[]
                self.bodega[arg.tipo][arg.nombre].append(arg)

    def recibir_camion(self,camion):
        if len(self.fila)==0:
            self.fila.append(camion)
        else:
            for i in range(len(self.fila)-1):
                if self.fila[i].urgencia > camion.urgencia:
                    self.fila.insert(i,camion)
                    return
            self.fila.append(camion)
            
    def enviar_camion(self):
        self.fila.pop()
    def rellenar_camion(self):
        camion = self.fila[-1]
        while camion.capacidad_actual < camion.capacidad_maxima:
            maximo = 0
            producto_maximo = None
            for tipo in self.bodega.values():
                for nombre in tipo.values():
                    for producto in nombre:
                       if producto.peso > maximo:
                           producto_maximo = producto
                           maximo = producto.peso
            camion.agregar_producto(producto_maximo)
            for producto in self.bodega[producto_maximo.tipo][producto_maximo.nombre]:
                if producto.peso == maximo:
                    self.bodega[producto_maximo.tipo][proucto_maximo.nombre].remove(producto)
            
    def productos_por_tipo(self,tipo):
        for nombres in self.bodega[tipo]:
            print(str(nombres)+" :"+str(len(self.bodega[tipo][nombres])))
class Producto:
    def __init__(self,nombre,tipo,peso):
        self.nombre = nombre
        self.tipo = tipo
        self.peso = peso


def crear_Camion():
    lista = []
    with open("caminones.txt", encoding="utf-8") as f:
        for line in f.read().splitlines():
            line = line.strip()
            line = line.split(",")
            lista.append(Camion(line[0],line[1]))
        return lista
        
def crear_producto():
    lista = []
    with open("productos.txt", encoding="utf-8") as f:
        for line in f.read().splitlines():
            line = line.strip()
            line = line.split(",")
            lista.append(Producto(line[0], line[1],line[2]))
        return lista
if __name__=="__main__":
    camiones = crear_Camion()
    productos = crear_producto()
    distribuidora = CentroDistribucion()
    
