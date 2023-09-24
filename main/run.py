import sys
from PyQt5.QtWidgets import QApplication


from model import AppModel
from view import AppView
from controller import AppController



if __name__ == '__main__':
    
    model = AppModel()
    view = AppView()
    controller = AppController(model, view)
    view.show()
    
    sys.exit(view.app.exec_())
