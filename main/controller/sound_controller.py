from PyQt5.QtMultimedia import QSound
from main.sounds_lib import (
    CLICK,
    WOW,
    GET_EMAIL,
    GET_EMAIL_VIOLIN,
    MENU_CLICK,
    TASK_DONE
)


class SoundController:
    """ A Class to control the sounds from various button pressed.

    The idea is the interface remains the same, but it will have multiple setter
    which will change the theme of the sounds by modifying its attributes.
    """

    def __init__(self):
        self.click_sound_path: str = CLICK
        self.menu_click_sound_path: str = MENU_CLICK
        self.wow_sound_path = WOW
        self.violin_sound_path = GET_EMAIL_VIOLIN
        self.email_notify_path = GET_EMAIL
        self.task_done = TASK_DONE

    def click_sound(self):
        QSound.play(self.click_sound_path)

    def menu_click_sound(self):
        QSound.play(self.menu_click_sound_path)

    def complete_celebrate(self):
        QSound.play(self.wow_sound_path)

    def get_email_sound(self):
        QSound.play(self.email_notify_path)

    def task_toggle_sound(self):
        QSound.play(self.task_done)