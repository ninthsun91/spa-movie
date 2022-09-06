import re


def name_check(test):
    username = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?!]{3,15}$")
    return True if re.fullmatch(username, test) else False


def pass_check(test):
    password = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?!]{8,15}$")
    return True if re.fullmatch(password, test) else False


def title_check(test):
    title = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?!]{3,30}$")
    return True if re.fullmatch(title, test) else False


def comment_check(test):
    comment = re.compile(r"^[\s\wㄱ-ㅎㅏ-ㅣ가-힣.?!]{3,300}$")
    return True if re.fullmatch(comment, test) else False


def remove_tags(text):
    html = re.compile("<.*?>")
    return re.sub(html, "", text)