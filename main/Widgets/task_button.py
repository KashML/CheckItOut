from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from PyQt5.QtCore import pyqtSignal
import random

from main.ui.stylesheets_constants import BUTTON_COLOR_LIST, get_button_style, get_button_style_checked


class TaskbuttonWidget(QPushButton):

    doubleClicked = pyqtSignal()  # Define a new signal

    def __init__(self, task_name: str = "No title given", id: int = 0, color=None):
        super().__init__()
        self.title_text = task_name
        self.id: int = id
        self.color = color
        self.init_view()
        
        
    def init_view(self):
        self.setText(self.title_text)
        self.setCheckable(True)

        if self.color is None:
            self.color = random.choice(BUTTON_COLOR_LIST)

        self.set_style_og()
    
    def toggle(self, checked):
        
        if checked is True:
            self.set_style_checked()
        else:
            self.set_style_og()
        

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()
    
    def set_style_og(self) -> None:
        self.setStyleSheet(get_button_style(self.color))
    
    def set_style_checked(self) -> None:
        self.setStyleSheet(get_button_style_checked(self.color))
