import numpy as np
from math import ceil, floor
from PyQt5.QtCore import QPoint, QRect
from PyQt5.QtGui import QPixmap
class Punto2D:

    def __init__(self, x, y):
        self.posx = x
        self.posy = y

    def x(self):
        return self.posx

    def y(self):
        return self.posy

def movimiento_w(pos1, pos2, velocidad=1):
    #m = np.array(pos1)
    #i = np.array(pos2)
    #return pos2
    if pos1.x() != pos2.x() or pos1.y() != pos2.y():
        dx = pos1.x() - pos2.x()
        dy = pos1.y() - pos2.y()
        norma = (dx**2 + dy**2)**0.5
        x = pos2.x() + velocidad*dx/norma
        y = pos2.y() + velocidad*dy/norma
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        #if x > pos1.x():
       #     x = pos1.x()
       # if y > pos1.y():
       #     y = pos1.y()
        if x < pos2.x() and y < pos2.y():
            return floor(x), floor(y)
        elif x > pos2.x() and y < pos2.y():
            return ceil(x), floor(y)
        elif x < pos2.x() and y > pos2.y():
            return floor(x), ceil(y)
        else:
            return ceil(x), ceil(y)
    else:
        return pos2.x(), pos2.y()


def movimiento_s(pos1, pos2, velocidad=1):
    if pos1.x() != pos2.x() or pos1.y() != pos2.y():
        dx = pos1.x() - pos2.x()
        dy = pos1.y() - pos2.y()
        norma = (dx**2 + dy**2)**0.5
        x = pos2.x() - velocidad*dx/norma
        y = pos2.y() - velocidad*dy/norma
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x < pos2.x() and y < pos2.y():
            return floor(x), floor(y)
        elif x > pos2.x() and y < pos2.y():
            return ceil(x), floor(y)
        elif x < pos2.x() and y > pos2.y():
            return floor(x), ceil(y)
        else:
            return ceil(x), ceil(y)
    else:
        return pos2.x(), pos2.y()

def movimiento_a(pos1, pos2, velocidad=1):
    if pos1.x() != pos2.x() or pos1.y() != pos2.y():
        dx = pos1.x() - pos2.x()
        dy = pos1.y() - pos2.y()
        norma = (dx**2 + dy**2)**0.5
        x = pos2.x() + velocidad*dy/norma
        y = pos2.y() - velocidad*dx/norma
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x < pos2.x() and y < pos2.y():
            return floor(x), floor(y)
        elif x > pos2.x() and y < pos2.y():
            return ceil(x), floor(y)
        elif x < pos2.x() and y > pos2.y():
            return floor(x), ceil(y)
        else:
            return ceil(x), ceil(y)
    else:
        return pos2.x(), pos2.y()

def movimiento_d(pos1, pos2, velocidad=1):
    if pos1.x() != pos2.x() or pos1.y() != pos2.y():
        dx = pos1.x() - pos2.x()
        dy = pos1.y() - pos2.y()
        norma = (dx**2 + dy**2)**0.5
        x = pos2.x() - velocidad*dy/norma
        y = pos2.y() + velocidad*dx/norma
        if x < 0:
            x = 0
        if y < 0:
            y = 0

        if x < pos2.x() and y < pos2.y():
            return floor(x), floor(y)
        elif x > pos2.x() and y < pos2.y():
            return ceil(x), floor(y)
        elif x < pos2.x() and y > pos2.y():
            return floor(x), ceil(y)
        else:
            return ceil(x), ceil(y)
    else:
        return pos2.x(), pos2.y()

def sobre(ventana,mouse, obj):
    objx1 = obj.pos().x()
    objx2 = objx1 + obj.width()
    objy1 = obj.pos().y()
    objy2 = objx2 + obj.height()
    mousex = mouse.pos().x() - ventana.pos().x()
    mousey = mouse.pos().y() - ventana.pos().y()
    return objx1 <= mousex and mousex <= objx2 and \
           objy1 <= mousey and mousey <= objy2

def animate_link(pixmap, direccion, contador):
    if direccion == "derecha":
        new_pixmap = pixmap.copy(
            QRect(120//2 * contador, 910//2, 120//2 * (contador + 1),
                  1040//2))
        return new_pixmap
    elif direccion == "arriba":
        new_pixmap = pixmap.copy(
            QRect(120//2 * contador, 650//2, 120//2 * (contador + 1),
                  780//2))
        return new_pixmap
    elif direccion == "abajo":
        new_pixmap = pixmap.copy(
            QRect(120//2 * contador, 350//2, 120//2 * (contador + 1),
                  480//2))
        return new_pixmap
    elif direccion == "izquierda":
        new_pixmap = pixmap.copy(
            QRect(120//2 * contador, 435//2, 120//2 * (contador + 1),
                  560//2))
        return new_pixmap
    else:
        new_pixmap = pixmap.copy(
            QRect(120 // 2 * 1, 350 // 2, 120 // 2 * (1 + 1),
                  480 // 2))
        return new_pixmap

def animate_naruto(pixmap, direccion, contador):
    if direccion == "derecha":
        new_pixmap = pixmap.copy(
            QRect(46 * contador, 255-64-7-14-64-14-7, 46 * (contador + 1),
                  255-64-7-14-14-7))
        return new_pixmap
    elif direccion == "arriba":
        new_pixmap = pixmap.copy(
            QRect(46 * contador, 255-64-7, 46 * (contador + 1),
                  255-7))
        return new_pixmap
    elif direccion == "abajo":
        new_pixmap = pixmap.copy(
            QRect(46 * contador, 0, 46 * (contador + 1),
                  64))
        return new_pixmap
    elif direccion == "izquierda":
        new_pixmap = pixmap.copy(
            QRect(46 * contador, 255-64-7-14-64-64, 46 * (contador + 1),
                  255-64-7-14-64))
        return new_pixmap
    else:
        return pixmap.copy(QRect(46, 0, 46 * (1 + 1), 64))


if __name__ == "__main__":
    imagen = Punto2D(10,10)
    puntero = Punto2D(100, 100)
    print(movimiento_w(puntero, imagen, 200))
    print(id(imagen), id(None))