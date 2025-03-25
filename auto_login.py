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
    browser.add_cookie({"name": "MUSIC_U", "value": "004B16F7EB86141439CC2448BCA85661DCA77422A73D0D787928F1D7924931778A24F1C825F83157A5C685570817B968238B0C78E94FCBA74FA45AE444165DC560267F3B45904A3D7D67D5660CFBB6C79505BC7153E84F5132795EE320A83137EACBC73247DE33E4BC5AFE8F0946E67150E1F7307257698873A10416F5ECA94197BC2FCD677EB0FDC82ACECE0A2C2FBEA624702ABD9A18D0F6E788801D18F1E0C67CF98AF490CD7DFB69386699782EAC69888C5D7214E3A751C4EB94D80FB431FC3CCE42BF7CF7E2F6092F6DE8B7DB10C60935CFA4E439C401E9B03B3EBCD36B07ACDD50BC5281A71D0CD6BB2DF03451E61CAAD22715B1E2425C5D234D39821DBFD046B7E8533954D4C9941D3C800E9061B4241CBB7CFAC58402AB0F25A4DCBD66F198316BB8255B4144BDAB35D9F55BCCACC4BA784EF9BF43B53E03167B26A64EA2156C0C5A192AFE7465412F1DEF5223E7DE106761AFCECD43666C281BD3DB43"})
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
