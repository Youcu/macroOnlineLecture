# Path: main.py
from config.env_loader import load_credentials
from lms.driver import get_driver
from lms.login import login
from lms.lecture import (
    get_subject_link_list,
    dict_lecture_subject_name_lst,
    taking_attendance,
    select_valid_lecture
)

import time

##### Variables #####
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
base_url = "https://lms.mju.ac.kr/ilos/main/main_form.acl"

##### Main Execution #####
if __name__ == "__main__":
    ID, PW = load_credentials()
    subject_count = int(input("전공 과목 수 입력 : "))

    # Setup driver for scanning incomplete lectures
    driver = get_driver(user_agent, 'head_less')
    driver.implicitly_wait(10)
    driver.get(base_url)

    home_link = login(driver, ID, PW)
    subject_list = get_subject_link_list(driver, subject_count)
    dict_lecture_week_link, subject_name_lst = dict_lecture_subject_name_lst(driver, subject_list, home_link)

    select_valid_lecture(dict_lecture_week_link, subject_name_lst)
    driver.quit()

    select_option = int(input("\n\n>> Select Lecture Number : "))

    # Setup driver for watching lectures
    driver = get_driver(user_agent, 'head_less')
    driver.implicitly_wait(10)
    driver.get(base_url)
    login(driver, ID, PW)

    taking_attendance(driver, select_option, subject_list, dict_lecture_week_link)
    time.sleep(5)
    print("\nComplete!\n")
    driver.quit()