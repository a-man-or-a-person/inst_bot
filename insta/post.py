import os
import time
from random import random

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class PostReel:
    def __init__(self):
        # settings for driver
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--lang=en-US")  # Set browser UI language
        chrome_options.add_argument(
            "--accept-lang=en"
        )  # Set HTTP Accept-Language header
        chrome_options.add_experimental_option(
            "prefs",
            {
                "intl.accept_languages": "en,en_US",  # Set internal Chrome language
            },
        )
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(4)

        # User_account
        load_dotenv()
        self.username = os.getenv("USERNAME_INST")
        self.password = os.getenv("PASSWORD")

    def random_time(self):
        return random() + 2

    def login(self):
        # Open Instagram
        self.driver.get(
            "https://www.instagram.com/accounts/login/?next=%2F&amp%3Bsource=mobile_nav"
        )
        time.sleep(self.random_time())
        username_field = WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        password_field = self.driver.find_element(By.NAME, "password")

        time.sleep(self.random_time())
        username_field.send_keys(self.username)

        time.sleep(self.random_time())
        password_field.send_keys(self.password)

        time.sleep(self.random_time())
        submit_btn = self.driver.find_element(
            by=By.CSS_SELECTOR, value='button[type="submit"]'
        )
        submit_btn.click()

    def upload_reel(self, video_path):
        try:
            # Wait for main page
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'a[tabindex="0"]'))
            )

            time.sleep(self.random_time())
            create_btn = self.driver.find_element(
                by=By.CSS_SELECTOR, value='svg[aria-label="New post"]'
            )
            create_btn.click()

            # Uploading reel
            time.sleep(self.random_time() + 2)
            file_input = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            file_input.send_keys(video_path)

            time.sleep(self.random_time())
            ok_btn = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='OK']"))
            )
            ok_btn.click()

            time.sleep(self.random_time() + 5)
            next_btn = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='Next']"))
            )
            next_btn.click()

            time.sleep(self.random_time())
            next_btn = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='Next']"))
            )
            next_btn.click()

            time.sleep(self.random_time())
            share_btn = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//*[text()='Share']"))
            )
            share_btn.click()
            print("waiting")
            WebDriverWait(self.driver, 120).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[text()='Your reel has been shared.']")
                )
            )
            time.sleep(self.random_time())
            exit_btn = self.driver.find_element(by=By.CSS_SELECTOR, value='div[class="x1qjc9v5 x9f619 x78zum5 xdt5ytf x1iyjqo2 xl56j7k"]')
            exit_btn.click()
    
            print("Reel posted successfully!")
        except TimeoutException as e:
            print(f"Element not found: {e}")
            # Take screenshot for debugging
            self.driver.save_screenshot("error_screenshot.png")
            print("Saved error screenshot to error_screenshot.png")

    def post_reel(self, video_path):
        self.login()
        time.sleep(4)
        self.upload_reel(video_path)
