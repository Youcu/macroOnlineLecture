##### Libraries #####

# Selenium Libraries 
from selenium import webdriver # to use selenium
from selenium.webdriver.common.by import By # to get resource
from selenium.webdriver.common.keys import Keys # to use key actions
from selenium.webdriver import ActionChains # Access item locations
from selenium.webdriver.chrome.options import Options # for Browser Option
# from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

# BeautifulSoup Libraries 
# import requests
from bs4 import BeautifulSoup

# Etc Libraries 
import time # to prevent problems from delay issue
# import os # to deal with file options
import re

##### Variables #####

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
headers = {
	"User-Agent" : user_agent
} # argument that requests class input

opt = Options() # Create Option Object
opt.add_argument("--start-maximized") # Maximize Browser's Window Size
opt.add_argument(f"user-agent={user_agent}")
opt.add_experimental_option("detach", True) # 자동꺼짐 방지

# Secondary Options (Not Primary)
opt.add_experimental_option("excludeSwitches", ["enable-automation"]) # remove automation message
opt.add_argument("--mute-audio") # 음소거 
opt.add_argument("--headless") # to use selenium without screen
opt.add_argument("--disable-gpu") # to use selenium without screen

base_url = "https://lms.mju.ac.kr/ilos/main/main_form.acl"
# url = input("Input Copy & Paste Urls : ") # input url value

##### Actions

# User Info
ID = input("Input ID : ")
PW = input("Input PW : ")
subject_count = int(input("Input Count of Subjects : "))

# Define Default Setting
# Define driver Function
def get_driver(opt, mode): 
    if mode == 'head_less':
        driver = webdriver.Chrome(options=opt)
    elif mode == 'browser':
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        option = Options() # Create Option Object
        option.add_argument("--start-maximized") # Maximize Browser's Window Size
        option.add_argument(f"user-agent={user_agent}")
        option.add_experimental_option("detach", True) # 자동꺼짐 방지
        option.add_experimental_option("prefs", prefs)

        # Secondary Options (Not Primary)
        option.add_experimental_option("excludeSwitches", ["enable-automation"]) # remove automation message
        option.add_argument("--mute-audio") # 음소거
        driver = webdriver.Chrome(options=option)
    return driver
driver = get_driver(opt, 'head_less')
driver.implicitly_wait(10)
driver.get(base_url) # set target

# Login
def login(driver, ID, PW):
    driver.find_element(By.CSS_SELECTOR, ".header_login.login-btn-color").click()
    driver.find_element(By.CSS_SELECTOR, "#sso_btn").click()
    driver.find_element(By.CSS_SELECTOR, "#id").send_keys(ID)
    driver.find_element(By.CSS_SELECTOR, "#passwrd").send_keys(PW)
    driver.find_element(By.CSS_SELECTOR, "#loginButton").click()
    driver.refresh()
    return driver.current_url # home link

# Get Home link to Back
home_link = login(driver, ID, PW)

# Get subject link list
def get_subject_link_list(driver):
    subjects = driver.find_elements(By.CSS_SELECTOR, ".sub_open")
    return [ subject.get_attribute('onclick') for i, subject in enumerate(subjects, 1) if i <= subject_count ]
subject_list = get_subject_link_list(driver)

# Define : [ weekly lectures link list, subject_name_lst, all_week_lst, incomplete_week_lst ]
def dict_lecture_subject_name_lst(driver, subject_list, home_link):
    dict_lecture_week_link = [[] for _ in range(len(subject_list))]  # 각 subject에 대해 빈 리스트 할당
    subject_name_lst=[]
    for i in range(len(subject_list)):
        # Enter the Online Lecture
        driver.execute_script(subject_list[i])
        subject_name = driver.find_element(By.CSS_SELECTOR, '.welcome_subject').text
        # print(subject_name)
        subject_name_lst.append(subject_name)
        driver.find_element(By.CSS_SELECTOR, '#menu_lecture_weeks').click()

        # Parsing Online Lecture page & Checking Status
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        all_week_lst = driver.find_elements(By.CSS_SELECTOR, '.wb-status')
        if not all_week_lst: 
            driver.get(home_link)
            continue
        incomplete_week_lst = [ idx for idx,status in enumerate(soup.select('.wb-status > img'),0) if 'gray' in status['src']] 
    
        if len(incomplete_week_lst) == 0:
            print('Already Completed Lectures')
            pass
        else:
            # print(incomplete_week_lst)
            for idx, item in enumerate(all_week_lst, 0):
                if idx in incomplete_week_lst:
                    item.click()
                    text = driver.find_elements(By.CSS_SELECTOR, '.wb-week')[idx].text
                    week_num = int(re.search(r'\d+', text).group())
                    print(driver.find_elements(By.CSS_SELECTOR, '.wb-week')[idx].text)
                    # time.sleep(5)
                    link_format = f"https://lms.mju.ac.kr/ilos/st/course/online_list_form.acl?WEEK_NO={week_num}"            
                    print(link_format)
                    dict_lecture_week_link[i].append(link_format)
                    driver.back()
        
        driver.get(home_link)
    return dict_lecture_week_link, subject_name_lst
dict_lecture_week_link, subject_name_lst = dict_lecture_subject_name_lst(driver, subject_list, home_link)

# print("\n\nLECTURE LIST")
# print(dict_lecture_week_link)

### Too long run time -> Selective Running way

# Mining Valid list 
# Select Valid Lecture Option
def select_valid_lecture(dict_lecture_week_link):
    valid_lecture_idx = []
    for i in range(len(dict_lecture_week_link)):
        if not dict_lecture_week_link[i]:
            continue
        valid_lecture_idx.append(i)

    # print(valid_lecture_idx)

    # Match Valid index to subject_name_lst, provide options
    print("<< Incomplete Online Lecture List >> \n")
    for i in valid_lecture_idx:
        print(f"   {i}. {subject_name_lst[i]}")
select_valid_lecture(dict_lecture_week_link)
driver.quit() # driver 를 종료해도 lst 들은 살아있다.

select_option = int(input("\n\n>> Select Lecture Number : "))

# Restart Driver
driver = get_driver(opt, 'head_less')
driver.implicitly_wait(10)
driver.get(base_url) # set target
home_link = login(driver, ID, PW)

# Taking Attendance a course that you select Automaically
def lect_time_to_sec(lect_time, mode):
    # mode 1. lect_time
    if mode=='end':
        lect_time = lect_time.split(" / ")[1]
    # mode 2. progress_time
    elif mode=='first':
        lect_time = lect_time.split(" / ")[0]

    # convert time to sec
    time_list = list(map(int, lect_time.split(":")))

    if len(time_list) == 3:
        h, m, s = time_list
        return h*3600 + m*60 + s
    elif len(time_list) == 2:
        m, s = time_list
        return m*60 + s
# def taking_attendance(driver, subject_list, select_option, ):
# driver, subject_list, select_option, dict_lecture_week_link

def taking_attendance(driver, select_option, subject_list, dict_lecture_week_link):
    driver.execute_script(subject_list[select_option]) # goto selected subject page
     
    for lecture in dict_lecture_week_link[select_option]:
        driver.get(lecture)  # goto online lecture page

        lect_items = driver.find_elements(By.CSS_SELECTOR, '.site-mouseover-color')
        lect_cnt = len(lect_items)  # Lecture Amount

        # Lecture Time Length List
        lect_time = [
            lect_time_to_sec(lect_time.text.strip(), 'end') 
            for lect_time in driver.find_elements(By.CSS_SELECTOR, "div[style='float: left;margin-left: 7px;margin-top:3px;']") 
        ]

        for i in range(len(lect_items)):
            # 매번 최신 상태로 `lect_items` 조회
            lect_items = driver.find_elements(By.CSS_SELECTOR, '.site-mouseover-color')
            lect_item = lect_items[i]
            try:
                lect_item.click()  # Enter Lecture
                time.sleep(5)
                ActionChains(driver).send_keys(Keys.SPACE).perform()
                time.sleep(lect_time[i] + 300)
                driver.find_element(By.CSS_SELECTOR, "#exit_off").click()  # Exit Lecture

                # Handling Alert
                try:
                    result = driver.switch_to.alert
                    result.accept()  # alert '확인' click
                except:
                    pass  # alert이 없을 경우

            except StaleElementReferenceException:
                print("StaleElementReferenceException 발생, 요소를 재조회합니다.")
                lect_items = driver.find_elements(By.CSS_SELECTOR, '.site-mouseover-color')  # 재조회하여 반복
                continue  # 재시도
taking_attendance(driver, select_option, subject_list, dict_lecture_week_link)
time.sleep(5)
print("\nComplete!\n")
driver.quit()

