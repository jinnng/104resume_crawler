from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse, parse_qs
import os
import time
from datetime import datetime


def get_page_height(chrome_driver):
    return chrome_driver.execute_script("return document.body.scrollHeight")


def scroll_down(chrome_driver):
    body = chrome_driver.find_element(By.CSS_SELECTOR, 'body')
    for i in range(3):
        body.send_keys(Keys.END)
        time.sleep(3)


def reached_to_bottom(new_height, last_height):
    return new_height == last_height


def scroll_to_bottom(chrome_driver):
    last_height = get_page_height(chrome_driver)
    while True:
        scroll_down(chrome_driver)
        new_height = get_page_height(chrome_driver)
        if reached_to_bottom(new_height, last_height):
            break
        last_height = new_height


def extract_links(chrome_driver):
    elements = chrome_driver.find_elements(By.CSS_SELECTOR, ".userInfo-wrap a")
    links = [element.get_attribute("href") for element in elements]
    return links


def extract_idnos(links, already_processed_idnos):
    resume_idnos = []

    for link in links:
        parsed_url = urlparse(link)
        query_params = parse_qs(parsed_url.query)
        idno = query_params.get('idno', [None])[0]
        if idno and idno not in already_processed_idnos:
            resume_idnos.append(idno)

    return resume_idnos


def fetch_resume(chrome_driver, idno):
    url = f"https://vip.104.com.tw/ResumeTools/resumePreview?pageSource=search&searchEngineIdNos={idno}&snapshotIds=&jobNo=&ec=104"
    chrome_driver.get(url)
    WebDriverWait(chrome_driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.vip-resume-card.resume-block.resume-card"))
    )

    html = chrome_driver.page_source

    return html


def save_html_to_file(chrome_driver, output_path, idno):
    html = fetch_resume(chrome_driver, idno)
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"idno_{idno}_{timestamp}.html"

    resume_folder_path = os.path.join(output_path, 'resume')
    os.makedirs(resume_folder_path, exist_ok=True)
    file_path = os.path.join(resume_folder_path, filename)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)


def extract_data_from_website(chrome_driver, processed_idnos, batch_folder):
    scroll_to_bottom(chrome_driver)
    links = extract_links(chrome_driver)

    resume_idnos = extract_idnos(links, processed_idnos)

    # Only download the first 100 resumes
    for i, idno in enumerate(resume_idnos):
        if i < 100:
            save_html_to_file(chrome_driver, batch_folder, idno)
            processed_idnos.append(idno)
        else:
            break
