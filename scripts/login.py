from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import configparser


def get_credentials():
    config = configparser.ConfigParser()
    config.read('config.ini')
    username = config.get('Credentials', 'username')
    password = config.get('Credentials', 'password')
    return username, password


def key_in_userinfo(chrome_driver, username, password):
    time.sleep(3)
    chrome_driver.find_element(By.CSS_SELECTOR, '[data-qa-id="loginUserName"]').send_keys(username)
    chrome_driver.find_element(By.CSS_SELECTOR, '[data-qa-id="loginPassword"]').send_keys(password)


def press_login_button(chrome_driver):
    login_button = chrome_driver.find_element(By.CSS_SELECTOR, 'button[data-qa-id="loginButton"]')
    if login_button:
        login_button.click()


def is_logged_in(chrome_driver):
    while True:
        try:
            # check if the home menu exists
            header_menu_element = chrome_driver.find_element(By.CSS_SELECTOR, 'div.header__menu')
            if header_menu_element:
                return True
        except NoSuchElementException:
            # if login unsuccessfully, wait and keep checking
            time.sleep(1)


def login_to_website(chrome_driver):
    chrome_driver.get('https://vip.104.com.tw/index/index')
    username, password = get_credentials()
    key_in_userinfo(chrome_driver, username, password)
    press_login_button(chrome_driver)
    if is_logged_in(chrome_driver):
        print("Login successfully")
