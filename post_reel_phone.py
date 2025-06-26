from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def post_reel_with_selenium(video_path, username, password, caption):
    # Set mobile emulation
    # mobile_emulation = {"deviceName": "iPhone 12 Pro"}
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--lang=en-US")  # Set browser UI language
    chrome_options.add_argument("--accept-lang=en")  # Set HTTP Accept-Language header
    chrome_options.add_experimental_option('prefs', {
        'intl.accept_languages': 'en,en_US',  # Set internal Chrome language
    })
    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    try:
        # Open Instagram
        driver.get("https://www.instagram.com/accounts/login/?next=%2F&amp%3Bsource=mobile_nav")
        time.sleep(3)

        # Login
        username_field = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.NAME, "username")))
        password_field = driver.find_element(By.NAME, "password")
        time.sleep(3.53)
        username_field.send_keys(username)
        time.sleep(1.59)
        password_field.send_keys(password)
        time.sleep(1.2)
        # submit_btn = driver.find_element(by=By.CSS_SELECTOR, value='div[data-anchor-id="replay"]')
        # submit_btn.click()
        submit_btn = driver.find_element(by=By.CSS_SELECTOR, value='button[type="submit"]')
        submit_btn.click()

        # # Wait for login completion
        # WebDriverWait(driver, 15).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, 'a[tabindex="0"]'))
        # )
        time.sleep(6)

        # Navigate directly to create page
        # driver.get("https://www.instagram.com/create")
        time.sleep(4)
        # create_btn = driver.find_element(by=By.CSS_SELECTOR, value='a[href="#"]')
        create_btn = driver.find_element(by=By.CSS_SELECTOR, value='svg[aria-label="New post"]')
        create_btn.click()
        print('add')
        time.sleep(6.2)
        # post_btn = driver.find_element(by=By.CSS_SELECTOR, value='div[tabindex="0", role="button"]')
        # post_btn.click()

        # Upload video
        file_input = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(video_path)

        # Wait for video processing
        time.sleep(8)

        # Switch to Reel mode (using more reliable selector)
        reel_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[contains(@class, '_ac38') and contains(., 'Reel') or contains(., 'Ролик')]"))
        )
        reel_button.click()
        time.sleep(4.32)

        # Add caption
        caption_box = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//div[@aria-label='Write a caption...' or @aria-label='Напишите подпись...']"))
        )
        caption_box.send_keys(caption)
        time.sleep(2.4)

        # Post the reel
        share_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(., 'Share') or contains(., 'Поделиться')]"))
        )
        share_button.click()

        # Wait for completion
        WebDriverWait(driver, 30).until(
            EC.invisibility_of_element_located((By.XPATH, "//div[text()='Sharing...' or text()='Публикация...']"))
        )
        print("Reel posted successfully!")

    except TimeoutException as e:
        print(f"Element not found: {e}")
        # Take screenshot for debugging
        driver.save_screenshot("error_screenshot.png")
        print("Saved error screenshot to error_screenshot.png")

    finally:
        driver.quit()


# Usage
post_reel_with_selenium(
    video_path=r"C:\Users\User\Desktop\reels\2025-02-12_00-57-14_UTC.mp4",
    username="invideo_king_wonders",
    password="benben123!!",
    caption="Hi"
)

# <button class="x5yr21d  _aswp _aswq _aswu _asw_ _asx2" type="button">
