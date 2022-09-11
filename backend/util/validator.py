import re


def check_name(test):
    username = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?!]{3,15}$")
    return True if username.fullmatch(test) else False


def check_password(test):
    password = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?!]{8,15}$")
    return True if password.fullmatch(test) else False


def check_email(test):
    email = re.compile(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$")
    return True if email.fullmatch(test) else False


def check_contact(test):
    contact = re.compile(r"^[\d]{2,3}-[\d]{3,4}-[\d]{4}$")
    return True if contact.fullmatch(test) else False
    

def check_title(test):
    title = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣-.?! ]{3,30}$")
    return True if title.fullmatch(test) else False


def check_comment(test):
    comment = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?! ]{3,300}$")
    return True if comment.fullmatch(test) else False


def remove_tags(text):
    html = re.compile("<.*?>")
    return html.sub("", text)


def check_date(test):
    pubDate = re.compile(r"[0-9.]{10}")
    if pubDate.search(test):
        return pubDate.search(test).__getitem__(0)
    elif pubDate.search(test) is None:
        return None