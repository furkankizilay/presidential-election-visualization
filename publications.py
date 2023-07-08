import os
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class Publications:

 def fetch_publications(self):
        chrome_options = webdriver.ChromeOptions()
        browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        browser.get("http://boracanbula.com.tr/")
        browser.maximize_window()
        button = WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/main/div/div[2]/ul/li[4]/a')))
        button.click()
        time.sleep(2)
        publications_list = []

        counter = 1
        while True:
            try:
                publication = browser.find_element(by=By.CSS_SELECTOR, value=f'#articles > ul:nth-child({counter})')
                title = publication.find_element(by=By.CSS_SELECTOR, value=f'#articles > ul:nth-child({counter}) > li')
                publications_list.append(
                    {
                        'title': title.text
                    }
                )
                counter += 1  # increment counter
            except:
                # If no more elements can be found, break the loop
                break

        # Save publications_list to JSON file
        with open('data.json', 'w') as f:
            json.dump(publications_list, f)

        print("Data saved to data.json")

"""publications = Publications()

publications.fetch_publications()"""














