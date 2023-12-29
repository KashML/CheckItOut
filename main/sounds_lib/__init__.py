import os
from pathlib import Path

CURRENT_FILE_PATH = os.path.realpath(__file__)
SOUNDLIB_DIR = Path(CURRENT_FILE_PATH).parent

CLICK = os.path.join(SOUNDLIB_DIR, "click.wav")
GET_EMAIL = os.path.join(SOUNDLIB_DIR, "get_email.wav")
GET_EMAIL_VIOLIN = os.path.join(SOUNDLIB_DIR, "get_email_violin.wav")
MENU_CLICK = os.path.join(SOUNDLIB_DIR, "menu_buttons.wav")
TASK_DONE = os.path.join(SOUNDLIB_DIR, "task_done.wav")
WOW = os.path.join(SOUNDLIB_DIR, "wow.wav")
