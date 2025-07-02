import asyncio
import os
import random
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class AsyncPostReel:
    def __init__(self):
        # Initialize executor but NOT driver here
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.driver = None  # Will be initialized later

        # User account
        load_dotenv()
        self.username = os.getenv("USERNAME_INST")
        self.password = os.getenv("PASSWORD")

    async def init_driver(self):
        """Initialize driver asynchronously"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--lang=en-US")
        chrome_options.add_argument("--accept-lang=en")
        chrome_options.add_experimental_option(
            "prefs", {"intl.accept_languages": "en,en_US"}
        )
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")

        loop = asyncio.get_running_loop()

        # Create driver in executor thread
        self.driver = await loop.run_in_executor(
            self.executor, lambda: webdriver.Chrome(options=chrome_options)
        )
        self.driver.implicitly_wait(4)

    async def random_delay(self):
        """Non-blocking random delay"""
        await asyncio.sleep(random.random() + 2)

    async def check_session(self) -> bool:
        try:
            # Check if session was properly closed
            if hasattr(self.driver, "session_id") and self.driver.session_id is None:
                return False

            # Execute a safe command to verify responsiveness
            self.driver.current_window_handle
            if os.getenv('TEST') == 'True':
                print("DRIVER: is_active")
            return True
        except:
            if os.getenv('TEST') == 'True':
                print("DRIVER: is_down")
            return False

    async def login(self):
        """Login to Instagram with driver initialization check"""
        # Ensure driver is initialized
        if not self.driver:
            await self.init_driver()

        loop = asyncio.get_running_loop()

        # Open Instagram
        await loop.run_in_executor(
            self.executor,
            lambda: self.driver.get(
                "https://www.instagram.com/accounts/login/?next=%2F&amp%3Bsource=mobile_nav"
            ),
        )

        await self.random_delay()

        # Find elements
        username_field = await loop.run_in_executor(
            self.executor,
            lambda: WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.NAME, "username"))
            ),
        )

        password_field = await loop.run_in_executor(
            self.executor, lambda: self.driver.find_element(By.NAME, "password")
        )

        await self.random_delay()
        await loop.run_in_executor(
            self.executor, lambda: username_field.send_keys(self.username)
        )

        await self.random_delay()
        await loop.run_in_executor(
            self.executor, lambda: password_field.send_keys(self.password)
        )

        await self.random_delay()
        submit_btn = await loop.run_in_executor(
            self.executor,
            lambda: self.driver.find_element(
                by=By.CSS_SELECTOR, value='button[type="submit"]'
            ),
        )
        await loop.run_in_executor(self.executor, submit_btn.click)
        if os.getenv('TEST') == 'True':
            print("LOGIN: finished")

    async def upload_reel(self, video_path, first=True) -> tuple:
        """Upload reel with driver initialization check"""
        if not self.driver:
            await self.init_driver()

        loop = asyncio.get_running_loop()
        try:
            await self.random_delay()
            create_btn = await loop.run_in_executor(
                self.executor,
                lambda: WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, 'svg[aria-label="New post"]')
                    )
                ),
            )
            await loop.run_in_executor(self.executor, create_btn.click)

            # Uploading reel
            await self.random_delay()
            file_input = await loop.run_in_executor(
                self.executor,
                lambda: WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "input[type='file']")
                    )
                ),
            )

            await loop.run_in_executor(
                self.executor, lambda: file_input.send_keys(os.path.abspath(video_path))
            )
            await self.random_delay()
            if first:
                ok_btn = await loop.run_in_executor(
                    self.executor,
                    lambda: WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, "//*[text()='OK']"))
                    ),
                )
                await loop.run_in_executor(self.executor, ok_btn.click)

            await self.random_delay()
            next_btn = await loop.run_in_executor(
                self.executor,
                lambda: WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[text()='Next']"))
                ),
            )
            await loop.run_in_executor(self.executor, next_btn.click)
            await self.random_delay()
            next_btn = await loop.run_in_executor(
                self.executor,
                lambda: WebDriverWait(self.driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, "//*[text()='Next']"))
                ),
            )
            await loop.run_in_executor(self.executor, next_btn.click)
            await self.random_delay()
            try:
                share_btn = await loop.run_in_executor(
                    self.executor,
                    lambda: WebDriverWait(self.driver, 10).until(
                        EC.visibility_of_element_located(
                            (
                                By.CSS_SELECTOR,
                                'div[class="x9f619 xjbqb8w x78zum5 x15mokao x1ga7v0g x16uus16 xbiv7yw xyamay9 xv54qhq x1l90r2v xf7dkkf x1n2onr6 x1plvlek xryxfnj x1c4vz4f x2lah0s xdt5ytf xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]',
                            )
                        )
                    ),
                )
                await loop.run_in_executor(self.executor, share_btn.click)
            except Exception as e:
                if os.getenv('TEST') == 'True':
                    print(f"SHARE: failed: {e}")
                    return False, f"SHARE: failed: {e}"
                # share_btn = await loop.run_in_executor(
                #     self.executor,
                #     lambda: WebDriverWait(self.driver, 10).until(
                #         EC.visibility_of_element_located(
                #             (By.XPATH, "//*[text()='Share']")
                #         )
                #     ),
                # )
                #
                # await loop.run_in_executor(self.executor, share_btn.click)


            if os.getenv('TEST') == 'True':
                print("Waiting for sharing to complete...")

            await loop.run_in_executor(
                self.executor,
                lambda: WebDriverWait(self.driver, 120).until(
                    EC.visibility_of_element_located(
                        (By.XPATH, "//*[text()='Your reel has been shared.']")
                    )
                ),
            )

            await self.random_delay()
            await loop.run_in_executor(
                self.executor, lambda: self.driver.get("https://www.instagram.com")
            )
            if os.getenv('TEST') == 'True':
                print("Reel posted successfully!")

            # Deleting video
            os.remove(video_path)
            return True, 'OK'

        except TimeoutException as e:
            if os.getenv('TEST') == 'True':
                print(f"Element not found: {e}")
            await loop.run_in_executor(
                self.executor,
                lambda: self.driver.save_screenshot("error_screenshot.png"),
            )
            if os.getenv('TEST') == 'True':
                print("Saved error screenshot to error_screenshot.png")

        except Exception as e:
            if os.getenv('TEST') == 'True':
                print(f"POST FAILED: {e}")
            return False, f"POST FAILED: {e}"

    async def post_reel(self, video_path) -> tuple:
        """Main method to post reel with initialization checks"""
        if not self.driver or not (await self.check_session()):
            await self.init_driver()
        loop = asyncio.get_running_loop()
        try:
            # Check if already logged in
            await loop.run_in_executor(
                self.executor,
                lambda: self.driver.find_element(
                    by=By.CSS_SELECTOR, value='svg[aria-label="New post"]'
                ),
            )
            await self.random_delay()
            ret = await self.upload_reel(video_path, first=False)
            return ret

        except Exception:
            await self.login()
            await self.random_delay()
            ret = await self.upload_reel(video_path)
            return ret

    async def close(self):
        """Cleanup resources"""
        if self.driver:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(self.executor, self.driver.quit)
        self.executor.shutdown()
