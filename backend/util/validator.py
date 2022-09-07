import re


def check_name(test):
    username = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?!]{3,15}$")
    return True if re.fullmatch(username, test) else False


def check_password(test):
    password = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?!]{8,15}$")
    return True if re.fullmatch(password, test) else False


def check_title(test):
    title = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣-.?!]{3,30}$")
    return True if re.fullmatch(title, test) else False


def check_comment(test):
    comment = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?!]{3,300}$")
    return True if re.fullmatch(comment, test) else False


def remove_tags(text):
    html = re.compile("<.*?>")
    return re.sub(html, "", text)


def check_date(test):
    pubDate = re.compile(r"[0-9.]{10}")
    if pubDate.search(test):
        return pubDate.search(test).__getitem__(0)
    elif pubDate.search(test) is None:
        return None