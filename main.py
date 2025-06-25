from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
import os


def scrape_instagram_reel(reel_url, username, password, output_path="reel.mp4"):
    # Configure Tor Browser paths (UPDATE THESE TO YOUR SYSTEM'S PATHS)
    # tor_binary_path = "/path/to/tor-browser/Browser/firefox"  # Linux/Mac
    tor_binary_path = r"A:\Tor_browzer\Tor Browser\Browser\firefox.exe"  # Windows
    # tor_profile_path = "/path/to/tor-browser/Browser/TorBrowser/Data/Browser/profile.default"  # Linux/Mac
    tor_profile_path = r"A:\Tor_browzer\Tor Browser\Browser\TorBrowser\Data\Browser\Caches\profile.default"  # Windows

    # Configure Firefox options for Tor
    options = webdriver.FirefoxOptions()
    options.binary_location = tor_binary_path
    # options.set_preference("profile", tor_profile_path)
    options.set_preference("network.proxy.type", 1)
    options.set_preference("network.proxy.socks", "127.0.0.1")
    options.set_preference("network.proxy.socks_port", 9150)
    options.set_preference("network.proxy.socks_remote_dns", True)

    # Initialize WebDriver with Tor configuration
    driver = webdriver.Firefox(options=options)

    try:
        # Login to Instagram
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(5)  # Tor requires longer initial load times

        # Fill credentials
        username_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_field.send_keys(username)

        password_field = driver.find_element(By.NAME, "password")
        password_field.send_keys(password)

        # Submit login
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
        login_button.click()
        time.sleep(8)  # Extended sleep for Tor latency

        # Navigate to Reel
        driver.get(reel_url)
        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.TAG_NAME, "video"))
        )
        time.sleep(3)  # Additional buffer

        # Extract video URL
        video_element = driver.find_element(By.TAG_NAME, "video")
        video_url = video_element.get_attribute("src")

        if not video_url:
            # Fallback to meta tag extraction
            meta_tag = driver.find_element(
                By.XPATH,
                '//meta[@property="og:video" or @property="og:video:secure_url"]'
            )
            video_url = meta_tag.get_attribute("content")

        # Download video
        session = requests.Session()
        for cookie in driver.get_cookies():
            session.cookies.set(cookie['name'], cookie['value'])

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0"
        }

        response = session.get(video_url, headers=headers, stream=True)
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        print(f"Reel downloaded to {output_path}")

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        driver.quit()


# Usage
scrape_instagram_reel(
    # reel_url="https://www.instagram.com/reel/Cs8V8d2gQdE/",
    reel_url="https://www.instagram.com/reels/DJq5DRiM1QR/",
    username="invideo_king_wonders",
    password="benben123!",
    output_path="instagram_reel.mp4"
)
