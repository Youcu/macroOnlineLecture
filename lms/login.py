# Path: lms/login.py
from selenium.webdriver.common.by import By

def login(driver, ID, PW):
    driver.find_element(By.CSS_SELECTOR, ".header_login.login-btn-color").click()
    driver.find_element(By.CSS_SELECTOR, "#sso_btn").click()
    driver.find_element(By.CSS_SELECTOR, "#id").send_keys(ID)
    driver.find_element(By.CSS_SELECTOR, "#passwrd").send_keys(PW)
    driver.find_element(By.CSS_SELECTOR, "#loginButton").click()
    driver.refresh()

    # 로그인 성공 여부 판단
    if "login" in driver.current_url.lower():
        print("❌ 로그인 실패! 현재 URL:", driver.current_url)
    else:
        print("✅ 로그인 성공! 현재 URL:", driver.current_url)
    return driver.current_url