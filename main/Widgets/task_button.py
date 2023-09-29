from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal
from main.ui.stylesheets_constants import BTN_ORIG, BTN_PRESSED


class TaskbuttonWidget(QPushButton):

    doubleClicked = pyqtSignal()  # Define a new signal

    def __init__(self, task_name: str = "No title given", id: int = 0):
        super().__init__()
        self.title_text = task_name
        self.complete: bool = False
        self.id: int = id
        self.init_view()
        
        
    def init_view(self):
        self.setText(self.title_text)
        self.setCheckable(True)
        self.set_form()
        
    def set_form(self):
        self.setStyleSheet(BTN_ORIG)

    def toggle(self, checked):
        self.complete = checked
        if checked:
            self.setStyleSheet(BTN_PRESSED)
        else:
            self.setStyleSheet(BTN_ORIG)

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
        
