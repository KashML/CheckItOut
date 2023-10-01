import os
import sys

from PyQt5 import uic
from PyQt5.QtWidgets import (
    QApplication, QFrame, QPushButton, QVBoxLayout, QLineEdit, QMainWindow,
    QMenuBar, QMenu, QAction

)
from main.Widgets.progress_bar import RoundProgressbar

import main.ui

MAIN_DIR_PATH = os.path.dirname(main.ui.__file__)
UI_PATH = os.path.join(MAIN_DIR_PATH, "checklist.ui")

class AppView:
    def __init__(self):
        
        self.app = QApplication(sys.argv)
        self.window = uic.loadUi(UI_PATH)
        self._setup_ui()
        self._prepare_task_frame()
        self._prepare_progress_frame()
        print("initialized App View")
        

    def _setup_ui(self) -> None:
        """
        Sets up all the references
        """
        
        self.main_window: QMainWindow = self.window.findChild(QMainWindow, "MainWindow")

        # Reference top level Frames
        self.main_frame: QFrame  = self.window.findChild(QFrame, "central_widget")
        self.perf_frame: QFrame = self.window.findChild(QFrame, "perf_frame")
        self.task_frame: QFrame = self.window.findChild(QFrame, "task_frame")
        self.action_frame: QFrame = self.perf_frame.findChild(QFrame,"action_frame")
        self.progress_frame: QFrame = self.perf_frame.findChild(QFrame,"progress_frame")

        # Reference Action Frame
        self.add_task_btn: QPushButton = self.action_frame.findChild(QPushButton,"add_task")
        self.add_task_line: QLineEdit = self.action_frame.findChild(QLineEdit,"task_title")

        # Refence menu_bar
        self.menu_bar: QMenuBar = self.window.findChild(QMenuBar, "menubar")
        
        # Referance main menu
        self.main_menu: QMenu = self.menu_bar.findChild(QMenu, "menu_menu")
        self.save_action: QAction = self.window.findChild(QAction, "save_action")
        self.clear_all_action: QAction = self.window.findChild(QAction, "clear_all_action")
        self.load_last_action: QAction = self.window.findChild(QAction, "load_last_session_action")


    def show(self) -> None:
        self.window.show()
    
    def _prepare_task_frame(self):
        self.task_frame_layout: QVBoxLayout = QVBoxLayout()
        self.task_frame.setLayout(self.task_frame_layout)
    
    def _prepare_progress_frame(self):
        self.progress_frame_layout: QVBoxLayout = QVBoxLayout()
        self.progress_bar = RoundProgressbar(thickness=30)
        self.progress_frame_layout.addWidget(self.progress_bar)
        self.progress_frame.setLayout(self.progress_frame_layout)
        self.progress_bar.set_value(100)
        self.progress_bar.show()



