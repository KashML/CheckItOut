from PyQt5.QtMultimedia import QSound
from main.sounds_lib import (
    CLICK,
    WOW,
    THEME,
    GET_EMAIL_VIOLIN,
    MENU_CLICK,
    TASK_DONE,
    DESTROY
)


class SoundController:
    """ A Class to control the sounds from various button pressed.

    The idea is the interface remains the same, but it will have multiple setter
    which will change the theme of the sounds by modifying its attributes.
    """

    def __init__(self):
        self.sound_off: bool = True
        self.click_sound_path: str = CLICK
        self.menu_click_sound_path: str = MENU_CLICK
        self.wow_sound_path = WOW
        self.violin_sound_path = GET_EMAIL_VIOLIN
        self.theme_path = THEME
        self.task_done_path = TASK_DONE
        self.task_delete_path = DESTROY

    def click_sound(self):
        if not self.sound_off:
            QSound.play(self.click_sound_path)

    def menu_click_sound(self):
        if not self.sound_off:
            QSound.play(self.menu_click_sound_path)

    def complete_celebrate(self):
        if not self.sound_off:
            QSound.play(self.wow_sound_path)

    def get_email_sound(self):
        if not self.sound_off:
            QSound.play(self.violin_sound_path)

    def task_toggle_sound(self):
        if not self.sound_off:
            QSound.play(self.task_done_path)

    def task_delete_sound(self):
        if not self.sound_off:
            QSound.play(self.task_delete_path)

    def save_sound(self):
        if not self.sound_off:
            QSound.play(self.theme_path)

    def set_sound_on(self):
        self.sound_off = False

    def set_sound_off(self):
        self.sound_off = True

