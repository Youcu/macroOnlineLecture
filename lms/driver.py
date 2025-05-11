from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_driver(user_agent, mode):
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument(f"user-agent={user_agent}")
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_argument("--disable-blink-features=AutomationControlled") 
    options.add_argument("--mute-audio")

    if mode == "head_less":
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

    return webdriver.Chrome(options=options)