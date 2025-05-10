# Path: lms/login.py
from selenium.webdriver.common.by import By

def login(driver, ID, PW):
    driver.find_element(By.CSS_SELECTOR, ".header_login.login-btn-color").click()
    driver.find_element(By.CSS_SELECTOR, "#sso_btn").click()
    driver.find_element(By.CSS_SELECTOR, "#id").send_keys(ID)
    driver.find_element(By.CSS_SELECTOR, "#passwrd").send_keys(PW)
    driver.find_element(By.CSS_SELECTOR, "#loginButton").click()
    driver.refresh()
    return driver.current_url