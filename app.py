"""
THIS IS A TEMPORARY FILE FOR DEVELOPMENT
DO NOT RUN THIS FILE OUT OF LOCALHOST
USE "flask run" INSTEAD

개발 환경을 위한 임시 파일입니다
로컬환경 밖에서 실행하지 마세요
"flask run"을 대신 사용하세요
"""
from backend import create_app


app = create_app()


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000, debug=True)