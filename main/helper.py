

def validate_text_input(text: str) -> str:

    if text.strip() == "":
        return "Dummy Task"

    return text