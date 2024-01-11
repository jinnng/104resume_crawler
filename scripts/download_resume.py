import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from login import login_to_website
from fetch_resume import extract_data_from_website
from logout import logout_from_website

# get workspace from environment variable
WORKSPACE = os.getenv('WORKSPACE', './')
SEARCH_URL = os.getenv('SEARCH_URL', '')


def set_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument("user-data-dir=" + WORKSPACE + "/chrome-data")
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-setuid-sandbox")
    options.add_argument("--remote-debugging-port=9222")  # this
    options.add_argument("--disable-dev-shm-using")
    options.add_argument("--disable-extensions")
    options.add_argument("--disable-gpu")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    return options


def set_browser_size(driver):
    width = 1024
    height = 768
    driver.set_window_size(width, height)


def create_chrome_webdriver():
    service = Service(ChromeDriverManager().install())
    chrome_options = set_chrome_options()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    set_browser_size(driver)
    return driver


def download_resume(processed_idnos, batch_folder):
    chrome_driver = create_chrome_webdriver()
    login_to_website(chrome_driver)
    chrome_driver.get(SEARCH_URL)
    extract_data_from_website(chrome_driver, processed_idnos, batch_folder)
    logout_from_website(chrome_driver)
