import re


pattern = re.compile(r"^[A-Za-z0-9]+$")

def is_alphs(test):
    return re.fullmatch(pattern, test)

def remove_tags(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)