import re


def name_check(test):
    username = re.compile(r"^[A-Za-z0-9ㅏ-ㅣㄱ-ㅎ가-핳]{3,15}$")
    return re.fullmatch(username, test)


def pass_check(test):
    password = re.compile(r"^[A-Za-z0-9]{8,15}$")
    return re.fullmatch(password, test)


def title_check(test):
    title = re.compile(r"^[A-Za-z0-9ㅏ-ㅣㄱ-ㅎ가-핳]{3,30}$")
    return re.fullmatch(title, test)


def remove_tags(text):
    html = re.compile("<.*?>")
    return re.sub(html, "", text)