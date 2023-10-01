import sys
from PyQt5.QtWidgets import QApplication

from main.model.model import AppModel
from main.view import AppView
from main.controller.main_controller import AppController



if __name__ == '__main__':
    
    model = AppModel()
    view = AppView()
    controller = AppController(model, view)
    view.show()
    
    sys.exit(view.app.exec_())
