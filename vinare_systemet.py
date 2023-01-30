from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import re

op = webdriver.ChromeOptions()
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")
op.add_argument('--blink-settings=imagesEnabled=false')
op.add_experimental_option('excludeSwitches', ['enable-logging'])

website = "https://www.systembolaget.se/sortiment/vin/mousserande-vin/?forpackning=Flaska"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op)
driver.get(website)

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

### SHOW MORE UNTIL NUMBER OF ELEMENTS MATCH SPECIFIED NUMBER OF PRODUCTS
while(len(driver.find_elements(By.CLASS_NAME, "css-1otywyl"))<tot_prod):
    try:
        driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div/div[2]/div[2]/div/div[5]/a').click()
    except:
        driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div/div[2]/div[2]/div/div[4]/a').click()
    time.sleep(1)
    print(len(driver.find_elements(By.CLASS_NAME, "css-1otywyl")))


### GET TEXT BOX ELEMENTS
time.sleep(2)
elements = driver.find_elements(By.CLASS_NAME, "css-1otywyl")
print("Retrieving " + str(len(elements)) + " elements.")

### CREATE DATA FRAME FOR STORING ELEMENTS
import pandas as pd

df = pd.DataFrame(columns=['ID', 'Name', 'Country', 'Volume', 'Alcohol', 'Price'])
df.index.name = 'idx'
df.to_csv(file_name)

i = 0
for el in elements:
    try:
        name = el.find_element(By.XPATH,"./div[1]/p[1]").text
    except:
        name = "NO NAME"
    
    try:
        id = el.find_element(By.CLASS_NAME,"css-10vqt1w").text
    except:
        id = "NO ID"

    try:
        price = el.find_element(By.XPATH,"./div[2]/p").text
    except:
        price = "NO PRICE"

    try:
        country = el.find_element(By.XPATH,"./div[2]/div/div[2]/p[1]").text
    except:
        country = "NO COUNTRY"

    try:
        volume = el.find_element(By.XPATH,"./div[2]/div/div[2]/p[2]").text
    except:
        volume = "NO VOLUME"

    try:
        alc = el.find_element(By.XPATH,"./div[2]/div/div[2]/p[3]").text
    except:
        alc = "NO ALCOHOL"
    
    # df = pd.concat([df, pd.DataFrame.from_records([{'ID':id, 'Name':name, 'Country':country, 'Volume':volume, 'Alcohol':alc, 'Price':price}])], ignore_index=True)

    df = pd.DataFrame.from_records([{'ID':id, 'Name':name, 'Country':country, 'Volume':volume, 'Alcohol':alc, 'Price':price}])
    df.to_csv(file_name, mode='a', header=False)

    i = i+1
    print(i)

driver.quit()
