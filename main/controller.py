from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from main.model import AppModel
from main.view import AppView
from main.ui.stylesheets_constants import BTN_ORIG, BTN_PRESSED

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
        new_task = TaskbuttonVC(self.view.app)
        self.view.task_frame_layout.addWidget(new_task)

    
    def change_color(self, checked):

        button: QPushButton = self.view.app.sender()
        if checked:
            button.setStyleSheet("background-color: red")
        else:
            button.setStyleSheet("")

#An element acts like View-Controller format
class TaskbuttonVC(QPushButton):
    
    def __init__(self, app: QApplication):
        super().__init__()
        self.init_view()
        self.init_controller()
        self.app = app
        

    def init_view(self):
        self.setText("I am Task")
        self.setCheckable(True)
        self.set_form()
        
    def set_form(self):
        self.setStyleSheet(BTN_ORIG)


    def init_controller(self):
        self.clicked.connect(self.toggle)

    def toggle(self, checked):
        task: QPushButton = self.app.sender()
        if checked:
            task.setStyleSheet(BTN_PRESSED)
        else:
            task.setStyleSheet(BTN_ORIG)


#Test Commit



