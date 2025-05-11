# Path: lms/lecture.py
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
from bs4 import BeautifulSoup
from lms.utils import lect_time_to_sec
import time
import re
from tqdm import tqdm

def get_subject_link_list(driver, subject_count):
    subjects = driver.find_elements(By.CSS_SELECTOR, ".sub_open")
    return [subject.get_attribute('onclick') for i, subject in enumerate(subjects, 1) if i <= subject_count]

def dict_lecture_subject_name_lst(driver, subject_list, home_link):
    dict_lecture_week_link = [[] for _ in range(len(subject_list))]
    subject_name_lst = []
    for i in tqdm(range(len(subject_list)), desc="🟠 Parsing Subject Name List"):
        driver.execute_script(subject_list[i])
        subject_name = driver.find_element(By.CSS_SELECTOR, '.welcome_subject').text
        subject_name_lst.append(subject_name)
        driver.find_element(By.CSS_SELECTOR, '#menu_lecture_weeks').click()

        soup = BeautifulSoup(driver.page_source, "html.parser")
        all_week_lst = driver.find_elements(By.CSS_SELECTOR, '.wb-status')
        if not all_week_lst:
            driver.get(home_link)
            continue
        incomplete_week_lst = [idx for idx, status in enumerate(soup.select('.wb-status > img')) if 'gray' in status['src']]
        for idx in incomplete_week_lst:
            all_week_lst[idx].click()
            text = driver.find_elements(By.CSS_SELECTOR, '.wb-week')[idx].text
            week_num = int(re.search(r'\d+', text).group())
            link = f"https://lms.mju.ac.kr/ilos/st/course/online_list_form.acl?WEEK_NO={week_num}"
            dict_lecture_week_link[i].append(link)
            driver.back()

        driver.get(home_link)
    return dict_lecture_week_link, subject_name_lst

def taking_attendance(driver, select_option, subject_list, dict_lecture_week_link):
    driver.execute_script(subject_list[select_option])
    for lecture in dict_lecture_week_link[select_option]:
        driver.get(lecture)
        lect_items = driver.find_elements(By.CSS_SELECTOR, '.site-mouseover-color')
        lect_time = [
            lect_time_to_sec(t.text.strip(), 'end')
            for t in driver.find_elements(By.CSS_SELECTOR, "div[style='float: left;margin-left: 7px;margin-top:3px;']")
        ]

        # 추후 여기에 강의명까지 달아주자 
        for i in tqdm(range(len(lect_items)), desc="Attend a part of lectures"): 
            lect_items = driver.find_elements(By.CSS_SELECTOR, '.site-mouseover-color')
            try:
                lect_items[i].click()
                time.sleep(5)
                ActionChains(driver).send_keys(Keys.SPACE).perform()
                time.sleep(lect_time[i] + 300)
                driver.find_element(By.CSS_SELECTOR, "#exit_off").click()
                try:
                    driver.switch_to.alert.accept()
                except:
                    pass
            except StaleElementReferenceException:
                print("StaleElementReferenceException 발생, 요소를 재조회합니다.")
                continue

def select_valid_lecture(dict_lecture_week_link, subject_name_lst):
    valid_lecture_idx = [i for i, lst in enumerate(dict_lecture_week_link) if lst]
    print("\n\n<< Incomplete Online Lecture List >>\n")
    for i in valid_lecture_idx:
        print(f"   {i}. {subject_name_lst[i]}")

    print("\n")
    if not valid_lecture_idx:
        print("\n✅ 모든 강의가 수강 완료되었습니다.")
    return valid_lecture_idx