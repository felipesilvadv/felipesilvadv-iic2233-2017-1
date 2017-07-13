from PyQt5.QtCore import QThread, QTimer, pyqtSignal, QRect
from PyQt5.QtWidgets import QProgressBar
from PyQt5.QtGui import QPixmap
from time import sleep

class Campeon(QThread):

    #trigger = pyqtSignal(QRect)  # no se si ponerle QRect u otra cosa

    def __init__(self, vida, ataque, habilidad, parent, tipo=None,
                 *args, **kwargs):
        self.vida = vida
        self.ataque = ataque
        self.habilidad = habilidad
        self.tipo = tipo
        self.barra = QProgressBar(parent)
        super().__init__(*args, **kwargs)

    def atacar(self):
        pass

    def mover(self):
        pass

    def run(self):
        while self.vida:
            if self.vida <= 0:
                self.vida = 0



class Minion(QThread):

    def __init__(self, vida, ataque, *args, **kwargs):
        self.vida = vida
        self.ataque = ataque
        super().__init__(*args, **kwargs)

    def atacar(self):
        pass

    def mover(self):
        pass


