# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0004636E0271840CBEBB4D9EFAE261CC5F46C29570A2B6D276D84867C01CFDF04B0259C7C7C5B7EB4EEDCAFECEEF2A97879132C4AB132A59BD42485BB20581DCA1DE9832835FE7FC9337105F5CA5AC9B24D6C032FAF697C68B87C38080EF2569EF73843B6A384C6A91837449F4F33E4A6BDCF74CFD3FDBD11AA367830192F94A8710C8AFCC4CD81E26F785A43D1A7DB90E5299F2EBB221510E453A699BA0B1F5B93BA795A425F35BFDB6399B59187B22E1DE343400F4EECC548A49001673E8D93AE7E6DBB3DF51F176DB0AB75BEBF860724ACE804BC6CF4064937D11BB290EFBF4E95A8C7BB32A60A0E7F5343E636FA4E29C21425A59F01A1312EDCC66913439D3DB0A48088EAF3DE5DEC4BD7C607CCDBBAD83A41C86D50953CFEFDE5EDBCA1C29D21382D4C9A1761AF44EF1ABDF39FE83B3FF5B70FAA5A9F39278ACB08D32EBE217EBB2C2206BD4B28E306DA8E349F2A5E8583358B03A0FB86F5BE3D95967A156"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
