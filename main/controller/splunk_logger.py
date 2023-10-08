"""
Logging Module

To do : Expand into a proper logger
"""
from main.view import AppView

class SplunkLogger:

    def __init__(self, status_bar_view: AppView = None, do_print: bool = True) -> None:

        if status_bar_view is None:
            self.status_bar = None

        else:
            self.status_bar = status_bar_view.status_bar
        
        self.do_print =do_print

    def log(self, message : str, status = True):

        if self.do_print is True:
            print(message)
        
        if status is True:
            self.status_bar.showMessage(message)


