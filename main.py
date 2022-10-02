import json
import time
import re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from requests_html import HTMLSession

s = Service(r'D:\download\chromedriver')
driver = webdriver.Chrome(service=s)
driver.get('https://thevendry.com/pros/all?')
angka = 1
pagg = 1

while True:
    time.sleep(5)
    main = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/div/div[4]/div/div/div[3]')
    mainpage = main.find_elements(By.TAG_NAME, 'article')

    data = []

    for i in mainpage:
        href = i.find_element(By.TAG_NAME, 'a').get_attribute('href')
        try:
            img = i.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except Exception:
            img = 'No Image'

        driver.execute_script(f'window.open("{href}")')
        driver.switch_to.window(driver.window_handles[1])

        # scrap
        # bs4
        link = driver.current_url
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')

        try:
            web = soup.find('a', 'jsx-382714ad070dad2f web contact-item').get('href')
        except Exception:
            web = 'Not Available'

        # email scrap
        email_regex = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
        session = HTMLSession()
        try:
            r = session.get(web, timeout=30)
            try:
                r.html.render()
            except Exception:
                pass

            email = []
            for j in re.finditer(email_regex, r.html.raw_html.decode()):
                email.append(j.group())

            r.session.close()
            r.session.close()
            r.session.close()
            r.session.close()

        except Exception:
            email = ""

        # click phone
        try:
            driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/div/div[3]/article/div/div[2]/div/button').click()
            phone = driver.find_element(By.XPATH, '//div[@class="jsx-382714ad070dad2f contact-item phone"]').text
        except Exception:
            phone = 'No Phone Number'
        try:
            title = soup.find('h1', 'jsx-21f23791deaf9c8c jsx-a10fa766842a92a4').get_text()
        except Exception:
            title = '-'
        try:
            loc = soup.findAll('div', 'jsx-dc9c76884f10bede container')[1].find('div', 'jsx-dc9c76884f10bede value').get_text()
        except Exception:
            loc =  'Location Not Available'
        try:
            category = soup.findAll('div', 'jsx-dc9c76884f10bede container')[0].find('div', 'jsx-dc9c76884f10bede value').findAll('div')[1].get_text()
        except Exception:
            category = 'No Category'
        try:
            desc = soup.find('p', 'jsx-3c45933d44530363 headline').get_text().replace('\n', '')
        except Exception:
            desc = 'No Description'
        try:
            socmed = soup.find('a', 'jsx-382714ad070dad2f insta contact-item').get('href')
        except Exception:
            socmed = 'Not Available'

        datt = {
            'Vendors name': title,
            'Address': loc,
            'Phone number': phone,
            'Email': email,
            'Social account': socmed,
            'Website URL': web,
            'Image URL': img,
            'Vendors description': desc,
            'Category': category
        }
        data.append(datt)
        print(f'{angka}. title: {title}, Loc: {loc}, Category: {category}, Description: {desc}, Socmed: {socmed}, phone: {phone}, Web: {web}, Email: {email}, IMG URL: {img}')

        driver.close()
        driver.switch_to.window(driver.window_handles[0])
        angka += 1

    with open(f'tempatjson/page {pagg}.json', 'w+') as jsonfile:
        json.dump(data, jsonfile)
        print(f'file json page {pagg} was created')

    # click next page
    try:
        driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/div/div[5]/div/button[2]').click()
        print('next page')
        pagg += 1
    except Exception:
        print('all page was scrap')
        break

print('All Scrap Done!')

