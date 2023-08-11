### Project Steps

1. Create a web application by using Python and Flask.

```python
app = Flask(__name__)

if __name__ == '__main__':
    app.run()

```

2. Build the backend side by using Python and Selenium to download all 82 Json files from the website of YSK.

```python
import os
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver-manager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

class Fetcher:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        download_folder = os.path.join(os.getcwd(), 'csv')
        prefs = {'download.default_directory' : download_folder}
        chrome_options.add_experimental_option('prefs', prefs)
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def navigate_to_button(self, button_id):

        try:
                button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, button_id)))
                button.click()


        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            print("Button clicked successfully")

    def navigate_to_link(self, link_text):
        try:
            # Wait until the link is clickable
            link = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, link_text)))
            link.click()
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            print("Navigated to link successfully")

    def navigate_to_class(self, class_name):
        try:
            # Wait until the link is clickable
            class_click = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, class_name)))
            class_click.click()
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            print("Navigated to class successfully")

    def navigate_to_button_xpath(self, path):
        try:
            # Wait until the link is clickable
            button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, path)))
            button.click()
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            print("Navigated to class successfully")

    def click_button_by_css(self, button_css):
        try:
            # Wait until the button is clickable
            button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_css)))
            button.click()
        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            print(f"Button {button_css} clicked successfully")

    from selenium.webdriver.common.action_chains import ActionChains

    def click_buttons_by_city(self):
        try:

            for i in range(82, 163):  # 163 is exclusive, so it will loop until 162
                # Generate the CSS selector for the current city button
                button_css = f"text:nth-child({i})"
                self.driver.execute_script("window.scrollTo(0, 0);")

                # Wait until the button is clickable
                button = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, button_css)))
                button.click()
                time.sleep(3)
                download = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="kadinErkekOraniBar"]/div[2]/div/button[2]')))
                download.click()
                time.sleep(2)
                self.driver.back()
                time.sleep(3)
                self.click_button_by_css("#myModalClose > span:nth-child(1)")
                time.sleep(3)

                self.navigate_to_link("Cumhurbaşkanlığı Seçim Sonuçları")
                time.sleep(3)

        except Exception as e:
            print(f"An error occurred: {e}")
        else:
            print(f"Buttons {button} clicked successfully")

    def close(self):
        self.driver.quit()
```

3. Build the frontend side by using HTML, JavaScript and Plotly.js. You can select the plot types.

### Choropleth Map Box
![choropleth_mapbox](images/1.png)
### Histogram 
![Untitled](images/2.png)
### Pie Charts    
![Untitled](images/3.png)
![Untitled](images/4.png)
