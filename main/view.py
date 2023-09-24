import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QFrame, QPushButton, QVBoxLayout

class AppView:
    def __init__(self):
        
        self.app = QApplication(sys.argv)
        self.window = uic.loadUi("/home/abhinavkashyap/dev/journey/apps/checklist.ui")
        self.setup_ui()
        self.prepare_task_frame()
        print("initialized App View")
        

    def setup_ui(self) -> None:
        """
        Sets up all the references
        """
        
        # Reference Frames
        self.main_frame: QFrame  = self.window.findChild(QFrame, "central_widget")
        self.perf_frame: QFrame = self.window.findChild(QFrame, "perf_frame")
        self.task_frame: QFrame = self.window.findChild(QFrame, "task_frame")
        
        
        # Reference Performace Frame
        self.add_task_btn: QPushButton = self.perf_frame.findChild(QPushButton,"add_task")

    def show(self) -> None:
        self.window.show()
    
    def prepare_task_frame(self):
        self.task_frame_layout: QVBoxLayout = QVBoxLayout()
        self.task_frame.setLayout(self.task_frame_layout)



