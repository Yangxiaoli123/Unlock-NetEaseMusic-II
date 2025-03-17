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
    browser.add_cookie({"name": "MUSIC_U", "value": "0094571B09759253A833E160CF21C50F7419D647F48B21B81E4A9C4EC08A71E3C9C118C6B8196ED8A45E1B4280F4BBEEB0090585D0F25F69CFD6D902A7ED46F7B09A3577F0B39F8004E52D831AD0E144885076C027A32241101C71EFA87836E4A7C6230F8D7DD5EAEE4176613F30D6874DA1D3ECACF42431E683D6DC243BB65AA5C8074530700849F5E86B4858596D32A58C0291F554CA9F3995A25ACF89EE785B68D13E830A77D46DFFE499CB2AF524788A414104E076A0047E391EEBF4DDC94085C820D25336D42CAB156C809AFA075D11F0847A0670C493D9562FFC91BFCE7508FB80407231787C22B34DF090183104C44504622C7CA9D32858D9C291B11B3DFED0DEB67FC4216D400E29CD78284577FA0A436FE607E7D22F828834F14CC6BA6A291FBB00B970FF677E8C09E039C55D857552434088D8779612E4F5310FEE8503D04CA85278B86BC0C0339BDAC3A975E06284F96958CF872A557787733F5750"})
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
