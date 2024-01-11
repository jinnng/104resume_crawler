from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


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


def logout_from_website(chrome_driver):
    if is_logged_in:
        chrome_driver.get('https://vip.104.com.tw/oidc/logout')
        time.sleep(3)
        chrome_driver.quit()
