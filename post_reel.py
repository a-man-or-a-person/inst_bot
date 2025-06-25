from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


def post_reel_with_selenium(video_path, username, password, caption):
    driver = webdriver.Chrome()
    driver.get("https://www.instagram.com/")

    # Login
    time.sleep(2)
    driver.find_element(By.NAME, "username").send_keys(username)
    time.sleep(2.45)
    driver.find_element(By.NAME, "password").send_keys(password + Keys.ENTER)
    time.sleep(10)

    # Open creation menu
    time.sleep(5)
    # driver.find_element(By.XPATH, "//div[text()='Create']").click()
    driver.find_element(By.XPATH, "//div[text()='Создать']").click()
    time.sleep(3.56)

    # Upload video
    file_input = driver.find_element(By.XPATH, "//input[@type='file']")
    file_input.send_keys(video_path)
    time.sleep(5)

    # Set as reel
    driver.find_element(By.XPATH, "//div[contains(text(),'Reel')]").click()
    time.sleep(5)

    # Add caption
    caption_box = driver.find_element(By.XPATH, "//div[@aria-label='Write a caption...']")
    caption_box.send_keys(caption)
    time.sleep(5)

    # Post
    driver.find_element(By.XPATH, "//div[text()='Share']").click()
    time.sleep(10)
    driver.quit()


# Usage
post_reel_with_selenium(
    video_path="A:\Python Development\Instagramm_bot\bydastann\2025-05-07_14-00-02_UTC.mp4",
    username="invideo_king_wonders",
    password="benben123!!",
    caption="Hi"
)