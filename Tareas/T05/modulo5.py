from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtCore
import sys
class Frontend(QMainWindow):
    key_trigger = QtCore.pyqtSignal(str)
    def __init__(self, *args):
        super().__init__(*args)
        self.tower = Tower()
        self.nexus = Nexus()

        self.key_trigger.connect(self.tower.un_metodo)
        self.key_trigger.connect(self.nexus.un_metodo)

    def keyPressEvent(self, event):
        self.key_trigger.emit(event.text())


class Tower:
    def un_metodo(self, key_event):
        print("Soy un Torre y apretaron la tecla {}".format(key_event))

class Nexus:
    def un_metodo(self, key_event):
        print("Soy un Nexo y apretaron la tecla {}".format(key_event))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Frontend()
    ex.show()
    sys.exit(app.exec_())