from python3_capsolver.image_to_text import ImageToText
import base64
from selenium import webdriver
import selenium.common.exceptions
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import urllib.request
import json
import os

WORKING_PATH = 'C:/Users/armed/Desktop/Full Stack Dev Work/Scott G/12-29-23'


class CaptchaSolver:
    def __init__(self):

        # 1. Load webpage in Selenium/check that latest webdriver is installed. Additional settings for pulling network
        # logs

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.set_capability("goog:loggingPrefs", {"performance": "ALL", "browser": "ALL"})

        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=self.chrome_options)

        # 2. Navigate driver to page

        self.driver.get("https://www.whistlerblackcomb.com/plan-your-trip/lift-access/tickets")

        # Waiting for page to load

        time.sleep(3)

    def captcha_solve(self):

        # 3. Locate captcha image

        # Error handling for when the "Waiting Room"/Captcha page doesn't load

        try:
            source_image = self.driver.find_element(By.CLASS_NAME, "captcha-code").get_attribute('src')

            # 4. Download image and save as "captcha.jpg"

            urllib.request.urlretrieve(source_image, "captcha.jpg")

            # Waiting for image to download
            time.sleep(3)

            # 5. Solve captcha

            os.chdir(WORKING_PATH)

            with open("captcha.jpg", 'rb') as img_file:
                img_data = img_file.read()
            body = base64.b64encode(img_data).decode("utf-8")
            response = ImageToText(api_key="CAP-63233C481A54734246734522DCBB8652").captcha_handler(body=body)

            # Solution is not case-sensitive, no need to capitalize string

            captcha_solution = response.solution['text']
            print(f"Captcha solution is: {captcha_solution}")

            # 6. Selenium locates solution box and enters captcha solution

            input_field = self.driver.find_element(By.CLASS_NAME, "botdetect-input")
            input_field.click()
            input_field.send_keys(captcha_solution)
            time.sleep(2)

            # 7. Selenium locates "I'M NOT A ROBOT" button and clicks it

            submit_button = self.driver.find_element(By.CLASS_NAME, "botdetect-button")
            submit_button.click()

        # If Captcha page did not load, message printed to console and the process continues as normal

        except selenium.common.exceptions.NoSuchElementException:
            print("Captcha page didn't load. Proceeding as normal")

        # Waiting for page to load
        time.sleep(3)

    def cookie_grab(self):

        # 8. Selenium pulls network logs (which includes API cookie), then isolates API cookie

        log_entries = self.driver.get_log("performance")

        for entry in log_entries:

            try:
                obj_serialized = entry.get("message")
                obj = json.loads(obj_serialized)
                message = obj.get("message")
                method = message.get("method")
                params = message.get('params')
                headers = params.get('headers')
                cookie = headers.get('cookie')

                if method in ['Network.requestWillBeSentExtraInfo']:
                    if len(cookie) > 620:
                        api_cookie = cookie.rstrip()
                        print(api_cookie)

                        # 9. Dump new api cookie JSON into headers.json

                        headers_JSON = {
                            "cookie": api_cookie
                        }

                        os.chdir(WORKING_PATH)

                        with open('headers.json', 'w') as data_file:
                            json.dump(headers_JSON, data_file)

                        break

            except Exception as e:
                continue

        # 10. Selenium closes browser window

        self.driver.quit()
