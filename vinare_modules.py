from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

import pandas as pd
from tqdm import tqdm
import time
import re
import logging
from datetime import datetime
import os

op = webdriver.ChromeOptions()
op.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36")
op.add_argument('--blink-settings=imagesEnabled=false')
op.add_argument('-headless')
op.add_experimental_option('excludeSwitches', ['enable-logging'])

logging.basicConfig(level=logging.INFO)
logging.getLogger('WDM').setLevel(logging.WARNING)

wine_types = {
    "rosé-1": "https://www.systembolaget.se/sortiment/vin/rosevin/flaska/",
    "mousserande-1": "https://www.systembolaget.se/sortiment/vin/mousserande-vin/flaska/?pris-till=199",
    "mousserande-2": "https://www.systembolaget.se/sortiment/vin/mousserande-vin/flaska/?pris-fran=200&pris-till=399",
    "mousserande-3": "https://www.systembolaget.se/sortiment/vin/mousserande-vin/flaska/?pris-fran=400&pris-till=599",
    "mousserande-4": "https://www.systembolaget.se/sortiment/vin/mousserande-vin/flaska/?pris-fran=600",
    "vitt-1": "https://www.systembolaget.se/sortiment/vin/vitt-vin/flaska/?pris-till=99",
    "vitt-2": "https://www.systembolaget.se/sortiment/vin/vitt-vin/flaska/?pris-fran=100&pris-till=139",
    "vitt-3": "https://www.systembolaget.se/sortiment/vin/vitt-vin/flaska/?pris-fran=140&pris-till=169",
    "vitt-4": "https://www.systembolaget.se/sortiment/vin/vitt-vin/flaska/?pris-fran=170&pris-till=199",
    "vitt-5": "https://www.systembolaget.se/sortiment/vin/vitt-vin/flaska/?pris-fran=200&pris-till=239",
    "vitt-6": "https://www.systembolaget.se/sortiment/vin/vitt-vin/flaska/?pris-fran=240&pris-till=299",
    "vitt-7": "https://www.systembolaget.se/sortiment/vin/vitt-vin/flaska/?pris-fran=300&pris-till=399",
    "vitt-8": "https://www.systembolaget.se/sortiment/vin/vitt-vin/flaska/?pris-fran=400",
    "rött-1": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-till=99",
    "rött-2": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=100&pris-till=139",
    "rött-3": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=170&pris-till=189",
    "rött-4": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=190&pris-till=209",
    "rött-5": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=210&pris-till=239",
    "rött-6": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=240&pris-till=269",
    "rött-7": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=270&pris-till=299",
    "rött-8": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=300&pris-till=369",
    "rött-9": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=370&pris-till=449",
    "rött-10": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=450&pris-till=599",
    "rött-11": "https://www.systembolaget.se/sortiment/vin/rott-vin/flaska/?pris-fran=1000"
}

snapdate = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0).date()
folder_name = 'wines_' + snapdate

if not os.path.exists(folder_name):
    os.mkdir(folder_name)
for wine_type, url in wine_types.items():
    # website = "https://www.systembolaget.se/sortiment/vin/rott-vin/fast-sortiment/"
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=op)
    driver.implicitly_wait(10)
    # driver.get(website)
    driver.get(url)

    logging.info('Website loaded')
    logging.info('Confirming age and cookies settings.')

    ### 20 YO OR OLDER + COOKIES
    driver.find_element(By.XPATH, '/html/body/div[1]/div/section/div/div/div[4]/div/div[2]').click()
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/button[1]').click()

    time.sleep(5)

    tot_prod = re.findall(r'\d+', driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div/div[2]/div[2]/div/div[1]/div[1]/h2').text)
    tot_prod = int(''.join(tot_prod))
    logging.info(f'{tot_prod} product tiles in the current category...')

    ### SHOW MORE UNTIL NUMBER OF ELEMENTS MATCH SPECIFIED NUMBER OF PRODUCTS
    with tqdm(total=tot_prod, desc = 'Loading more tiles...') as pbar:
        while(len(driver.find_elements(By.CLASS_NAME, "css-1otywyl"))<tot_prod):
            try:
                driver.find_element(By.CSS_SELECTOR, '.css-93uk39.e3whs8q0').click()
                # driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div/div[2]/div[2]/div/div[5]/a').click()
            except:
                pass
                # driver.find_element(By.XPATH, '//*[@id="__next"]/main/div[2]/div[2]/div/div[2]/div[2]/div/div[4]/a').click()
            time.sleep(0.2)

            loaded_elements = len(driver.find_elements(By.CLASS_NAME, "css-1otywyl"))
            pbar.n = loaded_elements
            pbar.update(0)  # Update without incrementing the total
            # logging.info(f'{len(driver.find_elements(By.CLASS_NAME, "css-1otywyl"))} tiles loaded...')

    logging.info('Scrolling page to reveal pricing...')


    wait = WebDriverWait(driver, 1)  # Adjust the timeout as needed
    tiles = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//*[contains(@id, 'tile:')]")))

    scroll_speed = 300 
    sleep_time = 0.005
    driver.execute_script("window.scrollTo(0, 0);")
    while True:
        current_height = driver.execute_script("return window.scrollY;")
        driver.execute_script(f"window.scrollBy(0, {scroll_speed});")
        time.sleep(sleep_time)
        new_height = driver.execute_script("return window.scrollY;")
        if new_height == current_height:
            break

    logging.info('Prices revealed, fetching data...')


    data = []
    # for tile in tqdm(tiles):
    for tile in tqdm(tiles, desc = 'Fetching data from all products...'):
        tile_wait = WebDriverWait(tile, 1)
        row = {}

        try:
            row['name'] = tile.find_element(By.CSS_SELECTOR, ".css-54mqg2.e3wog7r0").text
        except:
            row['name'] = ''

        # try:
        #     # Type and Year
        #     type_year_element = tile_wait.until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, ".css-18wuxp4.e3wog7r0"))
        #     )
        #     row['type_year'] = type_year_element.text
        # except TimeoutException:
        #     row['type_year'] = ''

        try:
            row['art_nr'] = tile.find_element(By.CSS_SELECTOR, ".css-kqd3bc.e3wog7r0").text
        except:
            row['art_nr'] = ''

        try:
            banner = tile.find_element(By.CSS_SELECTOR, ".css-5aqtg5.e3whs8q0").text.split('\n')
            row['country'] = banner[0]
            row['volume'] = banner[1]
            row['alc_vol'] = banner[2]
        except:
            row['country'] = ''
            row['volume'] = ''
            row['alc_vol'] = ''

        try:
            row['price'] = tile.find_element(By.CSS_SELECTOR, ".css-tny168.enp2lf70").text
        except:
            row['price'] = ''
        data.append(row)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    filename = folder_name+wine_type+'.csv'
    logging.info(f'Writing to {filename}')
    df.to_csv(filename, index=False)

    driver.quit()





    # try:
    #     row['type_year'] = tile.find_element(By.CSS_SELECTOR, ".css-18wuxp4.e3wog7r0").text
    # except:
    #     row['type_year'] = ''

