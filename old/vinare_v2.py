from selenium import webdriver
from selenium.webdriver.common.by import By

import time
import re
import pandas as pd

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
# options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")
driver = webdriver.Firefox(options=options)

print("driver loaded")
website = "https://www.systembolaget.se/sortiment/vin/mousserande-vin/?forpackning=Flaska"
print(website)
driver.get(website)
print("website loaded")


file_name = re.search('/vin/(.+?)forpackning', website).group(1)
file_name = file_name.replace("/?","")
file_name = file_name.replace("/","_")
file_name = file_name + ".csv"
print(file_name)

### 20 YO OR OLDER + COOKIES
driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[2]/div/section/div/div/div[4]/div/div[2]').click()
driver.find_element(By.XPATH, '//*[@id="modalId"]/div[2]/div/button[1]').click()

time.sleep(2)
tot_prod = re.findall(r'\d+', driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/h2').text)
tot_prod = int(tot_prod[0])
print(tot_prod)
