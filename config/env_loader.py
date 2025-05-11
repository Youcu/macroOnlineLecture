from dotenv import load_dotenv
import os
import stdiomask

def load_credentials():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
    ENV_PATH = os.path.join(BASE_DIR, "src", "loginInfo.env")

    ID = None
    PW = None

    if os.path.exists(ENV_PATH):
        load_dotenv(ENV_PATH)
        ID = os.getenv("ID")
        PW = os.getenv("PW")

    if not ID:
        ID = input("ID를 입력하세요: ")
    if not PW:
        PW = stdiomask.getpass(prompt="비밀번호를 입력하세요: ", mask="*")

    return ID, PW