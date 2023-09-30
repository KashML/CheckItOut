from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal
import random

from main.ui.stylesheets_constants import BUTTON_COLOR_LIST, get_button_style


class TaskbuttonWidget(QPushButton):

    doubleClicked = pyqtSignal()  # Define a new signal

    def __init__(self, task_name: str = "No title given", id: int = 0):
        super().__init__()
        self.title_text = task_name
        self.id: int = id
        self.init_view()
        
        
    def init_view(self):
        self.setText(self.title_text)
        self.setCheckable(True)
        self.set_style()
        

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
    
    def set_style(self) -> None:
        selected_color = random.choice(BUTTON_COLOR_LIST)
        self.setStyleSheet(get_button_style(selected_color))
        
