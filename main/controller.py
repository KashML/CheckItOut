from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from main.model import AppModel
from main.view import AppView
from main.Widgets.task_button import TaskbuttonWidget

class AppController:
    def __init__(self, model, view):
        self.model: AppModel = model
        self.view: AppView = view


        # Connect UI interactions to model manipulations
        self.view.add_task_btn.clicked.connect(self.add_layout)
        print("Initialized Controller")
        
        
    def add_tasks(self):
        print("Add Task Action ..")
        new_button = QPushButton(f"Button {self.view.task_frame_layout.count() + 1}")
        #new_button.clicked.connect(self.change_color)
        new_button.setCheckable(True)
        new_button.toggled.connect(self.change_color)
        self.view.task_frame_layout.addWidget(new_button)

    def add_layout(self):
        new_task = TaskbuttonWidget()
        new_task.clicked.connect(self.click_task)
        self.view.task_frame_layout.addWidget(new_task)

    def click_task(self, checked):
        button: TaskbuttonWidget = self.view.app.sender()
        button.toggle(checked)
    
    def change_color(self, checked):

        button: QPushButton = self.view.app.sender()
        if checked:
            button.setStyleSheet("background-color: red")
        else:
            button.setStyleSheet("")




