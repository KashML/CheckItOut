from typing import Optional
from main.model.data_types import Era


def validate_text_input(text: str) -> str:
    if text.strip() == "":
        return "Dummy Task"

    return text


era_filter_dict = {
    "-m": Era.MONTHLY,
    "-monthly": Era.MONTHLY,
    "-daily": Era.DAILY,
    "-d": Era.DAILY
}

def find_era(line: str) -> Optional[Era]:
    """Finds the configuration of the task.

    Determines if in the line there is a configuration specified.
    """

    for key in era_filter_dict.keys():
        if key in line:
            return era_filter_dict[key]

    return None

def strip_era(line : str) -> str:
    """ Strips the era filter from the line"""

    for key in era_filter_dict.keys():
        if key in line:
            return line.replace(key, "")

    return line