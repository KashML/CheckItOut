from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QWidget,
    QHBoxLayout, QSizePolicy
)
from model import AppModel
from view import AppView

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


BTN_STYLE = """QPushButton {
            background-color: white; 
            border: 6px solid pink; 
            color: black; 
            padding: 10px 40px; 
            font-size: 16px; 
            font-weight: bold;
            border-radius: 20px; 
        }
        """

CHANGE_COLOR = """QPushButton {
            background-color: green; 
            }
            """

BTN_PLAIN ="""QPushButton:hover {
                background-color: #f0f0f0;
            }
            """
BIN_RED  ="QPushButton:hover {background-color: #FF4500;}"



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
        self.setStyleSheet(BTN_STYLE + BTN_PLAIN)


    def init_controller(self):
        self.clicked.connect(self.toggle)

    def toggle(self, checked):
        task: QPushButton = self.app.sender()
        if checked:
            task.setStyleSheet(CHANGE_COLOR)
        else:
            task.setStyleSheet(BTN_STYLE + BTN_PLAIN)






