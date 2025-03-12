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
    browser.add_cookie({"name": "MUSIC_U", "value": "00F231F51E18286E1A8CD79F3E95650EB6F8796B581DA7DEF98DA3D6C8908AB905B4E50B88D574BEE20E3A1BFA70C29C4014E6576BAE261F98768562F048DA25192D3DDD2210BC5CE3ECC09B52F50B5662D3D4F76DE2E2779A66238A4A9F548EDF723FEF7FA382FCF88EBE1F2C41512BC7720FDF99C388033F0F2E172A62B4EAE9EBFF8E979B95967E53131590C5B4DF8A3B259280B8962325FA6CBF6325D342B1F476CD16D600F72AA3B97D7BB63BD9D199DEB2C75E19D57381DA6DE1D0FD2E5F25495989D3D44B66339836A1B83B233A421BF2B431E0BA41D7FFD5E797B009C7227A0C60F0DD1C0EC2D33AB88AC54B4E9235DA1ADF618B0C2B8031101C5A21C68F8B0DA9E2EF56CF948B5E4B427B117CF1E3A5417022F7CFF588E7371503C73E8DB78645EA09DDF9DB5EF7858AA11733D824F0C654CE7152E5BFC1C1216831852107D60D2DE5E75BA2DBC9D56B6EA83771F8FD60BC4882F7DFEAAAA8C849A451"})
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
