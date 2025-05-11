# Path: lms/lecture_handler.py
from lms.lecture import taking_attendance
from lms.login import login
from lms.driver import get_driver
import time
from tqdm import tqdm

BASE_URL = "https://lms.mju.ac.kr/ilos/main/main_form.acl"
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"

def handle_attendance(ID, PW, subject_list, subject_name_lst, dict_lecture_week_link, valid_lecture_idx):
    mode = input("\n>> 전체 자동 출석(a) 또는 수동 선택(s) 중 하나를 입력하세요 [a/s]: ").strip().lower()

    if mode == 'a':
        for i in tqdm(valid_lecture_idx, desc="모든 강의 순회 중 .."):
            print(f"\n▶ 자동 출석 진행 중: {subject_name_lst[i]}")

            driver = get_driver(USER_AGENT, 'head_less')
            driver.implicitly_wait(10)
            driver.get(BASE_URL)
            login(driver, ID, PW)

            taking_attendance(driver, i, subject_list, dict_lecture_week_link)
            driver.quit()

            print(f"✅ {subject_name_lst[i]} 출석 완료\n")
            time.sleep(3)

        print("\n전체 강의 출석 완료\n")

    elif mode == 's':
        try:
            select_option = int(input(">> 수강할 강의 번호를 선택하세요: "))
            if select_option not in valid_lecture_idx:
                raise ValueError

            print(f"\n▶ 선택한 강의 출석 진행 중: {subject_name_lst[select_option]}")

            driver = get_driver(USER_AGENT, 'head_less')
            driver.implicitly_wait(10)
            driver.get(BASE_URL)
            login(driver, ID, PW)

            taking_attendance(driver, select_option, subject_list, dict_lecture_week_link)
            driver.quit()

            print(f"✅ {subject_name_lst[select_option]} 출석 완료\n")

        except ValueError:
            print("❌ 잘못된 번호입니다. 유효한 강의 번호를 선택하세요.")
    else:
        print("❌ 잘못된 입력입니다. 'a' 또는 's' 중 하나를 선택해주세요.")