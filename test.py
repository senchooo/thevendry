import glob
import json
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import pandas as pd


s = Service(r'D:\download\chromedriver')
driver = webdriver.Chrome(service=s)
driver.get('https://thevendry.com/pros/all?')

main = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/div/div[4]/div/div/div[3]')
mainpage = main.find_elements(By.TAG_NAME, 'article')
mm = 1

while True:
    time.sleep(5)
    for i in mainpage:
        try:
            img = i.find_element(By.TAG_NAME, 'img').get_attribute('src')
        except Exception:
            img = 'No Image'

        data = {
            'Img': img
        }
        print(f'{img}')

    with open(f'page {mm}.json', 'w+') as jsonfile:
        json.dump(data, jsonfile)
        print(f'file json page {mm} was created')

    driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/div/div[5]/div/button[2]').click()

    if mm == 5:
        break
    mm += 1


filejson = sorted(glob.glob('*.json'))
datas = []
for i in filejson:
    with open(i) as jsonfile:
        dattt = json.load(jsonfile)
        datas.extend(dattt)

df = pd.DataFrame(datas)
df.to_csv('img data thevendry.csv', index=False)
df.to_excel('img data thevendry.xlsx', index=False)