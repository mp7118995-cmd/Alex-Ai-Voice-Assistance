import re


def clean_text(text):
    """
    Removes markdown symbols and extra spaces
    """
    text = re.sub(r'[*#`_>\-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


