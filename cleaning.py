import re
from bs4 import BeautifulSoup
def clean_price(text):
    digits = [symbol for symbol in text if symbol.isdigit()]
    cleaned_text = ''.join(digits)
    if not cleaned_text:
        return None
    return int(cleaned_text)
def clean_descr(text):
    for item in text:
        multi=str(item)
        clean_descr=re.sub('<[^<]+?>', '', multi)
        return clean_descr

