from bs4 import BeautifulSoup


def convert_html_to_text(html_string):
    soup = BeautifulSoup(html_string, 'html.parser')
    elements = soup.find_all(class_='main-resume')
    element_texts = []
    for element in elements:
        element_text = ""
        for child in element.children:
            child_text = child.get_text()
            element_texts.append(child_text + "\n")
        element_texts.append(element_text + "\n")
    return element_texts


def get_basic_info_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find("p", class_="name mr-7")
    name = name.text.strip() if name else ""

    age = soup.find("span", class_="year mr-4")
    age = age.text.strip()[:-1] if age else ""

    education_elem = soup.find("span", text="最高學歷")
    education = education_elem.find_next("span").text.strip() if education_elem else ""

    job_title_elem = soup.find("span", text="希望職稱")
    job_title = job_title_elem.find_next("span").text.strip() if job_title_elem else ""

    experience_elem = soup.find("span", text="總年資")
    experience = experience_elem.find_next("span").text.strip() if experience_elem else ""

    latest_job_elem = soup.find("span", text="最近工作")
    latest_job = latest_job_elem.find_next("span").text.strip() if latest_job_elem else ""

    address_elem = soup.find("span", text="居住地")
    address = address_elem.find_next("span").text.strip() if address_elem else ""

    email_elem = soup.find("span", text="E-mail")
    email = email_elem.find_next("span").text.strip() if email_elem else ""

    phone_elem = soup.find("span", text="聯絡電話")
    phone = phone_elem.find_next("span").text.strip() if phone_elem else ""

    contact_method_elem = soup.find("span", text="聯絡方式")
    contact_method = contact_method_elem.find_next("span").text.strip() if contact_method_elem else ""

    update_date_elem = soup.find("span", text="更新日:")
    update_date = update_date_elem.find_next("span").text.strip() if update_date_elem else ""

    result = {
        "name": name,
        "age": age,
        "highestEducation": education,
        "desiredJobTitle": job_title,
        "totalExperience": experience,
        "latestJob": latest_job,
        "residence": address,
        "email": email,
        "phone": phone,
        "contactMethod": contact_method,
        "updateDate": update_date
    }
    return result
