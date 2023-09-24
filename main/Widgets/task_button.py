from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from main.ui.stylesheets_constants import BTN_ORIG, BTN_PRESSED


class TaskbuttonWidget(QPushButton):
    def __init__(self):
        super().__init__()
        self.init_view()
        
    def init_view(self):
        self.setText("I am Task")
        self.setCheckable(True)
        self.set_form()
        
    def set_form(self):
        self.setStyleSheet(BTN_ORIG)

    def toggle(self, checked):
        if checked:
            self.setStyleSheet(BTN_PRESSED)
        else:
            self.setStyleSheet(BTN_ORIG)