import os
from pathlib import Path

CURRENT_FILE_PATH = os.path.realpath(__file__)
ICON_DIR = Path(CURRENT_FILE_PATH).parent

SAVE_ICON = os.path.join(ICON_DIR, "icon_1.svg")